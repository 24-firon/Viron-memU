#!/usr/bin/env node
// inject-context.js — SessionStart hook: kompiliert eine konfigurierbare Dateiliste
// zu einem Boot-Kontext-Bundle. Nachbau der OpenCode-"instructions"-Mechanik
// (opencode.jsonc -> instructions-Array) fuer Claude Code, das sowas nicht kennt.
//
// WICHTIG (Claude-Code-Realitaet, dokumentiert, Stand 2026-07): Hook-Output
// (additionalContext) ist hart auf 10.000 Zeichen gedeckelt. Groesserer Output
// wird NICHT injiziert, sondern in eine tool-results-Datei persistiert (nur
// 2-KB-Preview im Kontext). Nicht konfigurierbar. Deshalb injiziert dieser Hook
// inline nur eine kompakte Leseanweisung (<10 KB) und schreibt den vollen
// Kontext in Teil-Dateien unter .claude/context-bundle/, die die Session per
// read-Tool vollstaendig laedt. Jeder Teil passt in EINEN read-Aufruf.
//
// Konfiguration: .claude/context-inject.json (Liste von Pfaden — absolut ODER
// relativ zum Repo-Root/cwd, gemischt erlaubt).
//
// Env-Toggle: CONTEXT_INJECT_DISABLED=1 schaltet die Injektion komplett ab.
// Env: CONTEXT_INJECT_MAX_CHARS (Gesamtbudget Bundle; 0/negativ/unset = unbegrenzt).
// Env: CONTEXT_INJECT_MAX_CHARS_PER_FILE (optional; Default: kein Pro-Datei-Limit).
// Env: CONTEXT_INJECT_PART_CHARS (Teilgroesse; Default 80000 — sicher unter dem
//      25k-Token-Limit des read-Tools, damit jeder Teil in EINEM read ladbar ist).

'use strict';

const fs = require('fs');
const path = require('path');

const CONFIG_FILENAME = 'context-inject.json';
const BUNDLE_DIRNAME = 'context-bundle';
const MIN_USEFUL_REMAINDER = 200; // unter dieser Restgroesse lohnt kein Teil-Ausschnitt mehr
const DEFAULT_PART_CHARS = 80000; // ~13-20k Tokens je Teil -> passt in einen read-Call
const INLINE_HARD_CAP = 9500; // Claude Code persistiert Hook-Output ab 10.000 Zeichen
const MAX_MISSING_INLINE = 30; // Missing-Liste inline begrenzen, damit der Cap haelt

function isDisabled() {
  const raw = String(process.env.CONTEXT_INJECT_DISABLED || '').trim().toLowerCase();
  return ['1', 'true', 'on', 'yes'].includes(raw);
}

// 0 oder negativ = unbegrenzt (Infinity). Kein erzwungener Ceiling — die reale
// Grenze ist das Kontextfenster des Modells, nicht dieser Hook.
function getMaxChars() {
  const raw = process.env.CONTEXT_INJECT_MAX_CHARS;
  if (raw === undefined || raw === '') return Infinity;
  const parsed = Number.parseInt(raw, 10);
  if (!Number.isInteger(parsed)) return Infinity;
  return parsed <= 0 ? Infinity : parsed;
}

// Optionales Pro-Datei-Limit. Unset (Default) = kein Pro-Datei-Limit.
function getMaxCharsPerFile() {
  const raw = process.env.CONTEXT_INJECT_MAX_CHARS_PER_FILE;
  if (raw === undefined || raw === '') return null;
  const parsed = Number.parseInt(raw, 10);
  return Number.isInteger(parsed) && parsed > 0 ? parsed : null;
}

function getPartChars() {
  const raw = process.env.CONTEXT_INJECT_PART_CHARS;
  if (raw === undefined || raw === '') return DEFAULT_PART_CHARS;
  const parsed = Number.parseInt(raw, 10);
  return Number.isInteger(parsed) && parsed > 0 ? parsed : DEFAULT_PART_CHARS;
}

// Listen-Eintraege duerfen absolut ODER repo-relativ sein (gemischt erlaubt).
// Relative Pfade werden gegen cwd aufgeloest — cwd ist bei Claude-Code-Hooks
// i.d.R. das Repo-Root, sofern die Session von dort gestartet wurde.
function resolvePath(cwd, listedPath) {
  return path.isAbsolute(listedPath) ? listedPath : path.join(cwd, listedPath);
}

function loadConfig(cwd) {
  const configPath = path.join(cwd, '.claude', CONFIG_FILENAME);
  if (!fs.existsSync(configPath)) return null;
  try {
    const parsed = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    return Array.isArray(parsed.files) ? parsed.files : null;
  } catch (_) {
    return null;
  }
}

function buildBlocks(cwd, files, maxChars, maxCharsPerFile) {
  const blocks = [];
  const included = [];
  const missing = [];
  const truncated = [];
  let usedChars = 0;

  for (const listedPath of files) {
    if (usedChars >= maxChars) {
      missing.push(`${listedPath} (Gesamtbudget bereits erschöpft)`);
      continue;
    }

    const fullPath = resolvePath(cwd, listedPath);
    if (!fs.existsSync(fullPath)) {
      missing.push(listedPath);
      continue;
    }

    let content;
    try {
      content = fs.readFileSync(fullPath, 'utf8').trim();
    } catch (_) {
      missing.push(listedPath);
      continue;
    }

    let fileWasTruncated = false;

    // 1) Pro-Datei-Limit anwenden (falls konfiguriert)
    if (maxCharsPerFile && content.length > maxCharsPerFile) {
      content = `${content.slice(0, maxCharsPerFile)}\n… (Pro-Datei-Limit erreicht, gekürzt)`;
      fileWasTruncated = true;
    }

    // 2) Gesamtbudget anwenden — graceful: Teil-Ausschnitt statt Hart-Skip,
    //    solange der Rest gross genug ist, um noch nuetzlich zu sein.
    let block = `--- ${listedPath} ---\n${content}`;
    const remaining = maxChars - usedChars;
    if (block.length > remaining) {
      if (remaining < MIN_USEFUL_REMAINDER) {
        missing.push(`${listedPath} (Restbudget zu klein für sinnvollen Ausschnitt)`);
        continue;
      }
      const headerLen = `--- ${listedPath} ---\n`.length;
      const suffix = '\n… (Gesamtbudget erreicht, gekürzt)';
      const cutContentLen = Math.max(0, remaining - headerLen - suffix.length);
      content = `${content.slice(0, cutContentLen)}${suffix}`;
      block = `--- ${listedPath} ---\n${content}`;
      fileWasTruncated = true;
    }

    blocks.push(block);
    included.push(listedPath);
    if (fileWasTruncated) truncated.push(listedPath);
    usedChars += block.length;
  }

  return { blocks, included, missing, truncated };
}

// Blocks in Teile schneiden. Dateien werden nie ueber Teilgrenzen zerrissen,
// ausser ein einzelner Block ist groesser als die Teilgroesse (dann Hart-Split).
function splitIntoParts(blocks, partChars) {
  const parts = [];
  let current = '';

  const push = () => {
    if (current.length > 0) {
      parts.push(current);
      current = '';
    }
  };

  for (const block of blocks) {
    if (block.length > partChars) {
      push();
      for (let i = 0; i < block.length; i += partChars) {
        parts.push(block.slice(i, i + partChars));
      }
      continue;
    }
    if (current.length > 0 && current.length + 2 + block.length > partChars) {
      push();
    }
    current = current.length > 0 ? `${current}\n\n${block}` : block;
  }
  push();

  return parts;
}

function writeBundle(cwd, parts, included) {
  const bundleDir = path.join(cwd, '.claude', BUNDLE_DIRNAME);
  fs.mkdirSync(bundleDir, { recursive: true });

  // Alte Teile entfernen, DENN veraltete Rest-Teile wuerden die Session
  // mit einem inkonsistenten Bundle-Stand in die Irre fuehren.
  for (const entry of fs.readdirSync(bundleDir)) {
    if (/^part-\d+\.md$/.test(entry)) {
      fs.unlinkSync(path.join(bundleDir, entry));
    }
  }

  const partFiles = [];
  parts.forEach((content, idx) => {
    const name = `part-${String(idx + 1).padStart(2, '0')}.md`;
    const header = [
      `<!-- BOOT-KONTEXT-BUNDLE Teil ${idx + 1}/${parts.length} — generiert vom SessionStart-Hook.`,
      `     Quelle: .claude/${CONFIG_FILENAME} (${included.length} Dateien). Nicht manuell editieren. -->`,
      '',
      '',
    ].join('\n');
    fs.writeFileSync(path.join(bundleDir, name), header + content, 'utf8');
    partFiles.push(`.claude/${BUNDLE_DIRNAME}/${name}`);
  });

  return partFiles;
}

function buildInlineContext(partFiles, included, missing, truncated, totalChars) {
  const lines = [
    'BOOT-KONTEXT (SessionStart-Hook, Ersatz für OpenCode `instructions`-Array).',
    '',
    `Die injizierte Wissensbasis (${included.length} Dateien, ~${Math.round(totalChars / 1024)} KB) überschreitet das`,
    '10-KB-Inline-Limit von Claude Code für Hook-Output und liegt deshalb kompiliert als',
    `${partFiles.length} Teil-Datei(en) bereit. Jeder Teil passt in einen einzelnen read-Aufruf.`,
    '',
    'PFLICHT — BEVOR du mit der eigentlichen Arbeit beginnst, lies alle Teile',
    'vollständig mit dem Read-Tool, DENN ohne diese Wissensbasis arbeitest du ohne die',
    'Regeln und das Projektwissen dieses Repos:',
    '',
    ...partFiles.map((p, i) => `  ${i + 1}. ${p}`),
    '',
    'Der Inhalt gilt als Hintergrundwissen — keine Handlungsanweisung, sofern nicht explizit',
    'im jeweiligen Dateiinhalt selbst so formuliert.',
  ];

  if (missing.length > 0) {
    const shown = missing.slice(0, MAX_MISSING_INLINE);
    lines.push('', `⚠️ Nicht geladen (${missing.length}): ${shown.join(', ')}`);
    if (missing.length > shown.length) {
      lines.push(`… und ${missing.length - shown.length} weitere (siehe hookSpecificOutput).`);
    }
    lines.push('Fehlende Dateien dem Operator melden.');
  }
  if (truncated.length > 0) {
    lines.push('', `Gekürzt (Limit erreicht): ${truncated.join(', ')}`);
  }

  let inline = lines.join('\n');
  if (inline.length > INLINE_HARD_CAP) {
    inline = `${inline.slice(0, INLINE_HARD_CAP - 60)}\n… (Inline-Limit erreicht — Details in .claude/${BUNDLE_DIRNAME}/)`;
  }
  return inline;
}

function writePayload(additionalContext, included, missing, truncated, partFiles) {
  const payload = JSON.stringify({
    hookSpecificOutput: {
      hookEventName: 'SessionStart',
      additionalContext,
      context_inject_files: included,
      context_inject_missing: missing,
      context_inject_truncated: truncated,
      context_inject_parts: partFiles,
    },
  });
  process.stdout.write(payload);
}

function main() {
  if (isDisabled()) {
    writePayload('', [], [], [], []);
    return;
  }

  const cwd = process.cwd();
  const files = loadConfig(cwd);
  if (!files || files.length === 0) {
    writePayload('', [], [], [], []);
    return;
  }

  const { blocks, included, missing, truncated } = buildBlocks(
    cwd,
    files,
    getMaxChars(),
    getMaxCharsPerFile()
  );

  const totalChars = blocks.reduce((sum, b) => sum + b.length, 0);
  const parts = splitIntoParts(blocks, getPartChars());
  const partFiles = writeBundle(cwd, parts, included);
  const inline = buildInlineContext(partFiles, included, missing, truncated, totalChars);

  writePayload(inline, included, missing, truncated, partFiles);
}

try {
  main();
} catch (err) {
  process.stderr.write(`[inject-context] ERROR: ${err && err.message}\n`);
  writePayload('', [], [], [], []);
}
