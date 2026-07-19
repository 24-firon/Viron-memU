# Graph Report - memU  (2026-07-06)

## Corpus Check
- 189 files · ~99.673 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1540 nodes · 3471 edges · 85 communities detected
- Extraction: 75% EXTRACTED · 25% INFERRED · 0% AMBIGUOUS · INFERRED: 869 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: uses: 869 · method: 515 · ON_BRANCH: 400 · calls: 361 · rationale_for: 352 · MODIFIES: 336 · contains: 297 · PARENT_OF: 232 · inherits: 91 · imports_from: 17 · imports: 1


## Input Scope
- Requested: auto
- Resolved: committed (source: cli)
- Included files: 189 · Candidates: 1509
- Excluded: 75 untracked · 24961 ignored · 0 sensitive · 2 missing committed
- Recommendation: Use --scope all or graphify.yaml inputs.corpus for a knowledge-base folder.

## Graph Freshness
- Built from Git commit: `a1ae8c7`
- Compare this hash to `git rev-parse HEAD` before trusting freshness-sensitive graph output.
## God Nodes (most connected - your core abstractions)
1. `MemoryService` - 83 edges
2. `MemorizeMixin` - 78 edges
3. `Database` - 77 edges
4. `Context` - 69 edges
5. `WorkflowStep` - 68 edges
6. `DatabaseState` - 65 edges
7. `RetrieveMixin` - 60 edges
8. `SQLiteRepoBase` - 51 edges
9. `CRUDMixin` - 49 edges
10. `RetrieveConfig` - 35 edges

## Surprising Connections (you probably didn't know these)
- `Test LazyLLMClient with basic operations.` --uses--> `LazyLLMClient`  [INFERRED]
  tests/test_lazyllm.py → src/memu/llm/lazyllm_client.py
- `Demo script for MemU LangGraph Integration.` --uses--> `MemoryService`  [INFERRED]
  examples/langgraph_demo.py → src/memu/app/service.py
- `Initialize the MemoryService and the LangGraph adapter.` --uses--> `MemoryService`  [INFERRED]
  examples/langgraph_demo.py → src/memu/app/service.py
- `Simulate a conversation where memory is saved.` --uses--> `MemoryService`  [INFERRED]
  examples/langgraph_demo.py → src/memu/app/service.py
- `Simulate retrieving memory.` --uses--> `MemoryService`  [INFERRED]
  examples/langgraph_demo.py → src/memu/app/service.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (38): DoubaoLLMBackend, Build payload for Doubao chat completions (OpenAI-compatible)., Build payload for Doubao Vision API (OpenAI-compatible)., GoogleLLMBackend, GrokBackend, Backend for Grok (xAI) LLM API., OpenAILLMBackend, Build payload for OpenAI Vision API. (+30 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (44): 08d0fb0 feat: add multi-provider fallback infrastructure (Google -> Nvidia NIM -> vLLM), 3da3cc5 docs: add comprehensive REPORT.md for multi-provider infrastructure, 7b09d17 feat: Introduce a production-ready memU setup including a configuration factory, Docker Compose infrastructure, automated setup script, and comprehensive tests for database, memorization, and retrieval., 84c703b chore: unignore data/ in .gitignore, a1ae8c7 feat: switch to LiteLLM proxy as primary LLM provider (Free Zen), ccb0239 feat: integrate Google AI embedding backend (gemini-embedding-001, 3072-dim), f1dbaec feat: introduce initial setup and orchestration documentation for self-hosted memU, including environment configuration, agent rules, and a comprehensive user guide., Fallback LLM Client - Multi-Provider Failover Wrapper ========================== (+36 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (1): MemorizeMixin

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (8): EmbeddingBackend, LLMBackend, Defines how to talk to a specific HTTP LLM provider., 4a2e86c feat: initialize the memorize and retrieve workflows with the new 3-layer architecture (#81), eb69ddf Feat/expanded config (#135), fb96e54 feat: add non-RAG retrieve solution (#84), Utility modules for memU., Video processing utilities for frame extraction.

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (32): _build_embedding_request_view(), _build_embedding_response_view(), _build_text_request_view(), _build_text_response_view(), _coerce_filter(), _convert_to_dict(), _ensure_set(), _extract_finish_reason() (+24 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (42): production-setup, 03a27a6 making changes to README.ko.md, 0cddabe making changes to README.ko.md, 0fa721a fix: correct binary name after making a release (#91), 161117f Merge pull request #58 from arnav-terex/main, 1e3baf9 docs: fix several words in README (#89), 2235b09 docs: revise README for clarity and roadmap inclusion (#86), 23ce7d1 docs: fix api doc link (#146) (+34 more)

### Community 6 - "Community 6"
Cohesion: 0.11
Nodes (12): Category summary prompt with inline references to memory items.  This prompt i, 23f37ee fix!: v1.0.0 (#147), 3cd3dc6 feat: patch & crud workflows (#127), 5213571 feat: Add inline memory item references in category summaries (#202) (#205), 7d5e0cb fix: postgres model definitions & database initialization (#124), 7da36da feat: clear memory (#239), 825df56 feat: add conversation created at (#120), a175811 feat: add workflow implementation and postgres store (#122) (+4 more)

### Community 7 - "Community 7"
Cohesion: 0.07
Nodes (1): CRUDMixin

### Community 8 - "Community 8"
Cohesion: 0.09
Nodes (8): Format LLM-ranked category content for judger, Format LLM-ranked item content for judger, Decide if the query requires memory retrieval (or MORE retrieval) and rewrite it, Format query context for prompts, including role information, Extract RETRIEVE or NO_RETRIEVE decision from LLM response, Extract rewritten query from LLM response, Embedding-based retrieval with query rewriting and judging at each tier, RetrieveMixin

### Community 9 - "Community 9"
Cohesion: 0.11
Nodes (36): main, 01efae6 add: max-token env, 02846e8 Update README.md, 101eb85 fix: __version__, 11267c4 test: fix sqlite example path (#234), 15d5f03 fix: javascript api & reference, 22f0453 fix(memu-js): add wantSummary to retrieveDefaultCategories options, 2460bbd fix: correct coverage source to track memu package instead of tests (#220) (+28 more)

### Community 10 - "Community 10"
Cohesion: 0.19
Nodes (21): Initialize LLM client based on configuration.          If `config.fallback_pro, Lazily initialize and cache LLM clients per profile to avoid eager network setup, Default LLM client (lazy)., Current workflow runner backend., Register an interceptor to be called before each workflow step.          The i, Register an interceptor to be called after each workflow step.          The in, Register an interceptor to be called when a workflow step raises an exception., Execute a workflow through the configured runner backend. (+13 more)

### Community 11 - "Community 11"
Cohesion: 0.09
Nodes (17): DoubaoEmbeddingBackend, DoubaoMultimodalEmbeddingInput, Backend for Doubao embedding API (including multimodal embedding)., Build payload for standard text embeddings., Parse embedding response., Build payload for multimodal embedding API.          Args:             inputs, Parse multimodal embedding response., Backend for Doubao LLM API. (+9 more)

### Community 12 - "Community 12"
Cohesion: 0.09
Nodes (18): CategoryItemRepo, Repository contract for item/category relations., SQLite category-item relation repository implementation., Remove a link between an item and a category.          Args:             item, Get all category relations for a given item.          Args:             item_, Load all existing relations from database into cache., SQLite implementation of category-item relation repository., Initialize category-item repository.          Args:             state: Shared (+10 more)

### Community 13 - "Community 13"
Cohesion: 0.08
Nodes (15): MemoryItemRepo, Repository contract for memory items., SQLite memory item repository implementation., List items by their ref_id in the extra column.          Args:             re, Clear items matching the where clause.          Args:             where: Opti, Create a new memory item.          Args:             resource_id: Associated, SQLite implementation of memory item repository., Update an existing memory item.          Args:             item_id: ID of ite (+7 more)

### Community 14 - "Community 14"
Cohesion: 0.29
Nodes (28): Persist ref_id to items that are referenced in category summaries.          Th, Build the prompt for updating a category summary.          Args:, Update category summaries based on new memory items.          Returns:, Parse multimodal preprocessing response (video, image, document, audio)., Parse conversation preprocess response and extract segments.         Returns: (, Find the start index, end index, and closing tag for XML root element., Parse a single memory XML element into a dict., Parse XML memory extraction output into a list of memory items.          Expec (+20 more)

### Community 15 - "Community 15"
Cohesion: 0.08
Nodes (4): MemoryService, CRUDMixin, MemorizeMixin, RetrieveMixin

### Community 16 - "Community 16"
Cohesion: 0.07
Nodes (27): DateTime, TZDateTime, build_sqlite_table_model(), _merge_models(), _normalize_table_args(), SQLite-specific models for MemU database storage., Serialize embedding to JSON string., SQLite memory category model. (+19 more)

### Community 17 - "Community 17"
Cohesion: 0.09
Nodes (25): initialize_infrastructure(), main(), process_conversation(), process_retrieval(), Demo script for MemU LangGraph Integration., Initialize the MemoryService and the LangGraph adapter., Simulate a conversation where memory is saved., Simulate retrieving memory. (+17 more)

### Community 18 - "Community 18"
Cohesion: 0.10
Nodes (19): complete_prompt_blocks(), DefaultUserModel, LazyLLMSource, MetadataStoreConfig, PatchConfig, PromptBlock, RetrieveCategoryConfig, RetrieveItemConfig (+11 more)

### Community 19 - "Community 19"
Cohesion: 0.11
Nodes (13): FallbackLLMClient, Return per-provider success/fallback/error counts., Execute a method across providers, falling back on retryable errors.          It, Summarize text using the primary provider, falling back on errors., Generate embeddings using the primary provider's embedding backend.          NOT, Call a vision model using the primary provider, falling back on errors., Transcribe audio using the primary provider, falling back on errors., Return the chat model of the primary provider. (+5 more)

### Community 20 - "Community 20"
Cohesion: 0.11
Nodes (24): CategoryItem, build_inmemory_models(), InMemoryCategoryItem, InMemoryMemoryCategory, InMemoryMemoryItem, InMemoryResource, Concrete in-memory resource model., Concrete in-memory memory item model. (+16 more)

### Community 21 - "Community 21"
Cohesion: 0.11
Nodes (12): LLM-based retrieval that uses language model to search and rank results, Format categories for LLM consumption, Format memory items for LLM consumption, optionally filtered by category, Use LLM to rank categories based on query relevance, Use LLM to rank memory items from relevant categories, Parse LLM category ranking response, Parse LLM item ranking response, Format LLM-ranked resource content for judger (+4 more)

### Community 22 - "Community 22"
Cohesion: 0.10
Nodes (14): Register an interceptor to be called when a step raises an exception., Remove an interceptor by ID. Returns True if found and removed., Remove the interceptor from the registry. Returns True if removed., Registry for workflow step interceptors.      Interceptors are called before a, If True, interceptor exceptions will propagate instead of being logged., Register an interceptor to be called before each step.          The intercepto, Register an interceptor to be called after each step.          The interceptor, WorkflowInterceptorRegistry (+6 more)

### Community 23 - "Community 23"
Cohesion: 0.12
Nodes (12): MemoryCategoryRepo, Repository contract for memory categories., SQLite memory category repository implementation., Get existing category by name or create a new one.          Args:, Update an existing category.          Args:             category_id: ID of ca, SQLite implementation of memory category repository., Load all existing categories from database into cache., Initialize memory category repository.          Args:             state: Shar (+4 more)

### Community 24 - "Community 24"
Cohesion: 0.11
Nodes (14): 4b899d7 feat(database): add SQLite storage backend (#201), build_database(), Initialize a database backend for the configured provider.      Supported prov, Storage backends for MemU., Base repository class for SQLite backend., get_sqlite_metadata(), get_sqlite_sqlalchemy_models(), SQLAlchemy schema definitions for SQLite backend. (+6 more)

### Community 25 - "Community 25"
Cohesion: 0.13
Nodes (12): Protocol, SQLite repository implementations for MemU., Repository contract for resource records., SQLite resource repository implementation., Create a new resource record.          Args:             url: Resource URL., Load all existing resources from database into cache., SQLite implementation of resource repository., Initialize resource repository.          Args:             state: Shared data (+4 more)

### Community 26 - "Community 26"
Cohesion: 0.11
Nodes (19): 067262a chore: upgrade GitHub Actions for Node 24 compatibility (#279), 0d3cff6 chore(main): release 1.3.0 (#245), 0e490f7 fix: remove unused type: ignore comment and add lazyllm mypy override (#275), 1075d7c docs: Update README.md (#300), 16b65e5 fix(video): cleanup temp files on extraction failure (#295), 16c36b2 Update bot name and description in README (#286), 2f30798 docs: readme memubot (#289), 2f84231 docs: Add link to memU bot (#276) (+11 more)

### Community 27 - "Community 27"
Cohesion: 0.13
Nodes (11): 200f47a docs: multilingual readme (#271), 603ae12 fix: proactive examples (#273), 710f14d fix: memory type & proactive example (#272), b531d39 docs: update README (#270), d3d1de1 feat: add proactive example (#268), dump_conversation_resource(), memorize(), get_memory() (+3 more)

### Community 28 - "Community 28"
Cohesion: 0.15
Nodes (11): DatabaseState, Check if object matches where clause (for in-memory filtering)., Base class for SQLite repository implementations., Initialize base repository.          Args:             state: Shared database, Extract scope fields from an object., Normalize embedding from various formats to list[float]., Serialize embedding to JSON string for SQLite storage., Merge object into session and commit. (+3 more)

### Community 29 - "Community 29"
Cohesion: 0.13
Nodes (1): PatchMixin

### Community 30 - "Community 30"
Cohesion: 0.11
Nodes (17): 14d0333 docs: fix issue template dropdown (#167), 29c414a docs: add custom LLM and embedding configuration guide (#160), 3fa9be2 Encourage users to give GitHub stars (#176), 51c9ea4 fix: ensure both Linux x86_64 and ARM64 wheels are built (#162), 5a0032f fix: custom memory type default prompt (#169), 5d91237 docs: issue template fix (#165), 996913c chore(main): release 1.1.1 (#159), a02c042 chore(main): release 1.1.0 (#155) (+9 more)

### Community 31 - "Community 31"
Cohesion: 0.16
Nodes (15): Validate and clean the `where` scope filters against the configured user model., Extract item IDs from category summary references., Database, Backend-agnostic database contract., build_item_reference_map(), extract_references(), fetch_referenced_items(), format_references_as_citations() (+7 more)

### Community 32 - "Community 32"
Cohesion: 0.14
Nodes (13): 704c302 feat: add valcano model support (#110), 7c37fb1 feat: add user model and user context store (#113), 85586f5 fix: resource caption miss problem (#111), generate_skill_md(), main(), Example 2: Workflow & Agent Logs -> Skill Extraction  This example demonstrate, Extract skills from agent logs using incremental memory updates.      This exa, Use LLM to generate a concise task execution guide (skill.md).      This creat (+5 more)

### Community 33 - "Community 33"
Cohesion: 0.12
Nodes (17): 1e732f0 add: usecase in test data (#96), 2162c39 Feat/usecase example (#108), 21aad6a docs: fix example file path (#105), 228306c docs: fix readme test case (#107), 47b5b39 feat: add usecase examples (#94), 5b6ce54 docs: highlight OpenAI key (#106), 6370c6e feat: retrieve args change conversation_history to queries (#98), 6b71fa6 chore(release): fix maturin build and pypi deploy (#99) (+9 more)

### Community 34 - "Community 34"
Cohesion: 0.14
Nodes (14): Get a point-in-time snapshot of registered interceptors., Run all before-step interceptors., Context information for a workflow step execution., Run all after-step interceptors in reverse order., Run all on-error interceptors in reverse order., Safely invoke an interceptor, handling exceptions based on strict mode., run_after_interceptors(), run_before_interceptors() (+6 more)

### Community 35 - "Community 35"
Cohesion: 0.17
Nodes (13): 20f0342 chore: update port numbers for PostgreSQL, vLLM, and Open WebUI components in `MISSION_CORE.md`., ae6f03a docs: anchor correct hybrid rag strategy and onboarding prompts, b6a2497 docs: standardize governance (global/local rules) and fix mission core logic, bb5b4ef chore: restore global governance and clean up mission core, ca03d4f chore: full sync for migration (proactive loop + logs), check_filesystem(), check_schedule(), log() (+5 more)

### Community 36 - "Community 36"
Cohesion: 0.13
Nodes (9): Tests for extract_references function., Should extract a single reference ID., Should extract multiple reference IDs in order., Should handle comma-separated IDs in single reference., Should not return duplicate IDs., Should return empty list for empty text., Should return empty list when no references present., Should handle IDs with hyphens and underscores. (+1 more)

### Community 37 - "Community 37"
Cohesion: 0.14
Nodes (4): Handle engine lifecycle and session creation for Postgres store., SessionManager, PostgresRepoBase, List items by their ref_id in the extra column.          Args:             re

### Community 38 - "Community 38"
Cohesion: 0.24
Nodes (2): PipelineManager, PipelineRevision

### Community 39 - "Community 39"
Cohesion: 0.16
Nodes (14): 059b17d update: chat api supported parameters, 087b2a7 javascript sdk, 19ba53d Update README.md, 21b0c1a Update README.md, 3eab0ba add: openagents, 6ed3ff7 update README, 7983278 generator version, 7f1e8c7 Merge pull request #46 from kwaa/refactor/memu-js-internal (+6 more)

### Community 40 - "Community 40"
Cohesion: 0.22
Nodes (13): check_and_memorize(), get_next_input(), get_user_input(), main(), process_response(), Run the main conversation loop., Create a background task to memorize conversation messages.      Returns True, Get the next input for the conversation.      Returns:         tuple of (inpu (+5 more)

### Community 41 - "Community 41"
Cohesion: 0.22
Nodes (1): PostgresMemoryItemRepo

### Community 42 - "Community 42"
Cohesion: 0.21
Nodes (7): Extract multiple evenly-spaced frames from a video.          Args:, Check if ffmpeg is available in the system., Ensure the given path is safe to pass to a CLI command., Resolve and validate an existing filesystem path., Resolve output paths (which may not yet exist) for CLI safety., Run an ffmpeg/ffprobe command after validating the executable., Extract the middle frame from a video file.          Args:             video_

### Community 43 - "Community 43"
Cohesion: 0.17
Nodes (3): MemoryItemRepo, InMemoryMemoryItemRepository, List items by their ref_id in the extra column.          Args:             re

### Community 44 - "Community 44"
Cohesion: 0.24
Nodes (11): _print_categories(), _print_items(), Test OpenRouter integration with MemU's full workflow.  Tests: 1. Conversatio, Print category summaries., Print memory item summaries., Test conversation memorization., Test retrieval with specified method., Test OpenRouter integration with full MemU workflow. (+3 more)

### Community 45 - "Community 45"
Cohesion: 0.17
Nodes (7): Tests for strip_references function., Should remove single reference., Should remove all references., Should remove comma-separated references., Should handle empty text., Should return text unchanged if no references., TestStripReferences

### Community 46 - "Community 46"
Cohesion: 0.20
Nodes (10): 144fd32 fix: default embed size (#192), 3d9f7f5 Update README.md (#191) - add trending badge, 576670c Add GitHub Star section to README (#194), 5a56ce0 chore(main): release 1.1.2 (#166), 849f881 fix: readme partners link & github issue link (#198), 919d2ca docs: add docs folder (#181), abe0f1b feat: improve issue template (#199), b474c54 feat: optimize topk pick function (#196) (+2 more)

### Community 47 - "Community 47"
Cohesion: 0.27
Nodes (10): BaseRecord, build_scoped_models(), CategoryItem, MemoryCategory, MemoryItem, merge_scope_model(), Backend-agnostic record interface., Create a scoped model inheriting both the user scope model and the core model. (+2 more)

### Community 48 - "Community 48"
Cohesion: 0.18
Nodes (6): Test that valid JSON inputs are correctly formatted into the expected line-based, Test edge cases handling for empty or whitespace-only inputs, and empty JSON lis, Test handling of malformed JSON strings.          Note: The implementation swa, Test handling of valid JSON that does not match expected conversation schema., Test suite for format_conversation_for_preprocess function in src/memu/utils/con, TestFormatConversationForPreprocess

### Community 49 - "Community 49"
Cohesion: 0.24
Nodes (10): 19e934e refactor(memu-js)!: use fetch instead of axios, 1fc574b update: qrcode, 22473e3 update: documentation for v0.1.10, 4c57f45 Merge pull request #36 from kwaa/refactor/memu-js, 5ca172a chore: update examples, 5de91b3 refactor(memu-js): support multiple signal, 60fb7ac update: v0.2.1 (chat) sdk, 750b262 update: v0.1.11 sdk with message time support (+2 more)

### Community 50 - "Community 50"
Cohesion: 0.20
Nodes (5): Transcribe audio content to text using the configured STT (Speech-to-Text) backe, Asynchronously call a LazyLLM client with given arguments and keyword arguments., Generate a summary or response for the input text using the configured LLM backe, Process an image with a text prompt using the configured VLM (Vision-Language Mo, Generate vector embeddings for a list of text strings.          Args:

### Community 51 - "Community 51"
Cohesion: 0.20
Nodes (5): OpenAISDKClient, Create text embeddings via the official SDK., Transcribe audio file using OpenAI Audio API.          Args:             audi, OpenAI LLM client that relies on the official Python SDK., Call OpenAI Vision API with an image.          Args:             prompt: Text

### Community 52 - "Community 52"
Cohesion: 0.20
Nodes (6): Handle engine lifecycle and session creation for SQLite store., Initialize SQLite session manager.          Args:             dsn: SQLite con, Create a new database session., Close the database engine and release resources., Return the underlying SQLAlchemy engine., SQLiteSessionManager

### Community 53 - "Community 53"
Cohesion: 0.20
Nodes (6): Tests for format_references_as_citations function., Should convert single reference to numbered citation., Should number citations in order of appearance., Should handle empty text., Should return text unchanged if no references., TestFormatReferencesAsCitations

### Community 54 - "Community 54"
Cohesion: 0.20
Nodes (6): Tests for build_item_reference_map function., Should format single item reference., Should format multiple item references., Should truncate summaries longer than 100 chars., Should return empty string for empty list., TestBuildItemReferenceMap

### Community 55 - "Community 55"
Cohesion: 0.31
Nodes (1): LLMInterceptorRegistry

### Community 56 - "Community 56"
Cohesion: 0.33
Nodes (2): MemoryCategoryRepo, PostgresMemoryCategoryRepo

### Community 57 - "Community 57"
Cohesion: 0.31
Nodes (3): PostgresRepoBase, PostgresResourceRepo, ResourceRepo

### Community 58 - "Community 58"
Cohesion: 0.25
Nodes (2): CategoryItemRepo, InMemoryCategoryItemRepository

### Community 59 - "Community 59"
Cohesion: 0.25
Nodes (8): 0c90fcf feat: add Linux ARM64 (aarch64) build target (#156), 11fda41 docs: remove legacy docs (#154), 442bd8b chore(main): release 1.0.0 (#145), 6661eef Improve link formatting for New Year Challenge (#150), 76716a4 fix: get embedding client (#152), 8ed7f15 chore(main): release 1.0.1 (#149), a871ccb Fix link to memU-server in README.md (#151), f8bc748 fix: Readme incomplete (#148)

### Community 60 - "Community 60"
Cohesion: 0.25
Nodes (3): Database, InMemoryStore, PostgresStore

### Community 61 - "Community 61"
Cohesion: 0.39
Nodes (7): generate_markdown_output(), generate_skill_guide(), main(), Unified Example: LazyLLM Integration Demo =====================================, run_conversation_memory_demo(), run_multimodal_demo(), run_skill_extraction_demo()

### Community 62 - "Community 62"
Cohesion: 0.25
Nodes (2): MemoryCategoryRepoProtocol, InMemoryMemoryCategoryRepository

### Community 63 - "Community 63"
Cohesion: 0.39
Nodes (1): PostgresCategoryItemRepo

### Community 64 - "Community 64"
Cohesion: 0.25
Nodes (5): Tests for memory item reference functionality (Issue #202).  Tests cover: 1., Integration tests for reference functionality., Extracting then stripping should give clean text., Citation formatting should preserve text content., TestReferenceIntegration

### Community 65 - "Community 65"
Cohesion: 0.43
Nodes (7): _extract_created_at(), _extract_messages(), _extract_text_content(), format_conversation_for_preprocess(), _format_messages(), Normalize a conversation into a line-based format suitable for LLM preprocessing, _try_parse_json()

### Community 66 - "Community 66"
Cohesion: 0.29
Nodes (3): Format resources for LLM consumption, optionally filtered by related items, Use LLM to rank resources related to the context, Parse LLM resource ranking response

### Community 67 - "Community 67"
Cohesion: 0.43
Nodes (7): 472e349 translated README.md to japanese, 76c3fc4 docs: add German translation for README, 7b0d666 Added Spanish translation for README (#57), b924dcd Merge pull request #63 from AMIT20-P/translate_jap, cd48cd1 Merge pull request #61 from programmer-aarya7/i18n/readme-es, f6d6ab1 Merge pull request #59 from Shubham-Jain52/docs/readme-de, fd51651 Delete Questionnaire section from README

### Community 68 - "Community 68"
Cohesion: 0.29
Nodes (2): InMemoryResourceRepository, ResourceRepoProtocol

### Community 69 - "Community 69"
Cohesion: 0.40
Nodes (5): 060067a feat: add configurable batch_size for embedding API calls (#114), 2d908e1 docs: Add memU-experiment link to README (#119), 56b7c50 chore(main): release 0.7.0 (#104), 65ef7c6 fix: example 3 output (#117), da27875 docs: clearer introduction and new agent examples (#115)

### Community 70 - "Community 70"
Cohesion: 0.33
Nodes (5): 16ae534 docs: update readme (#266), 50b5502 feat(integrations): Add LangGraph Adapter for MemU (Track A) (#258), 77938e9 feat: add happened at and extra fields to memory item (#262), 8fbdf3c feat: add Sealos support agent use case (Track G) (#255), bba620b test(utils): add unit tests for conversation formatter (#229) (#256)

### Community 71 - "Community 71"
Cohesion: 0.40
Nodes (5): generate_memory_md(), main(), Example 1: Multiple Conversations -> Memory Category File  This example demons, Generate concise markdown files for each memory category., Process multiple conversation files and generate memory categories.      This

### Community 72 - "Community 72"
Cohesion: 0.53
Nodes (5): get_metadata(), get_sqlalchemy_models(), Build (and cache) SQLModel ORM models for Postgres storage., require_sqlalchemy(), SQLAModels

### Community 73 - "Community 73"
Cohesion: 0.40
Nodes (3): OpenAIEmbeddingSDKClient, OpenAI embedding client that relies on the official Python SDK., Create text embeddings.          Args:             inputs: List of text strin

### Community 74 - "Community 74"
Cohesion: 0.40
Nodes (4): get_memory(), _get_todos(), Retrieve memory from the memory API based on the provided query., Retrieve todos from the memory API.

### Community 75 - "Community 75"
Cohesion: 0.50
Nodes (4): main(), _print_results(), Test SQLite database backend for MemU., Test with SQLite storage.

### Community 76 - "Community 76"
Cohesion: 0.50
Nodes (3): main(), Getting Started with MemU: A Robust Example.  This script demonstrates the cor, Run the MemU lifecycle demonstration.

### Community 77 - "Community 77"
Cohesion: 0.67
Nodes (3): print_slow(), Typing effect for realism, run_rigorous_demo()

### Community 78 - "Community 78"
Cohesion: 0.67
Nodes (2): _cosine(), query_cosine()

### Community 80 - "Community 80"
Cohesion: 0.67
Nodes (3): make_alembic_config(), Run database migrations based on the ddl_mode setting.      Args:         dsn, run_migrations()

### Community 81 - "Community 81"
Cohesion: 0.50
Nodes (3): build_sqlite_database(), SQLite database backend for MemU., Build a SQLite database store instance.      Args:         config: Database c

### Community 82 - "Community 82"
Cohesion: 0.67
Nodes (1): Extract a clean filename from URL, handling query parameters.          Args:

### Community 83 - "Community 83"
Cohesion: 0.67
Nodes (2): matches_where(), Basic field/`__in` matcher for in-memory repos.

### Community 84 - "Community 84"
Cohesion: 0.67
Nodes (2): Test LazyLLMClient with basic operations., test_lazyllm_client()

### Community 85 - "Community 85"
Cohesion: 1.00
Nodes (1): run_steps()

## Knowledge Gaps
- **193 isolated node(s):** `Example 1: Multiple Conversations -> Memory Category File  This example demons`, `Generate concise markdown files for each memory category.`, `Process multiple conversation files and generate memory categories.      This`, `Example 2: Workflow & Agent Logs -> Skill Extraction  This example demonstrate`, `Use LLM to generate a concise task execution guide (skill.md).      This creat` (+188 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 2`** (1 nodes): `MemorizeMixin`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 7`** (1 nodes): `CRUDMixin`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `PatchMixin`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (2 nodes): `PipelineManager`, `PipelineRevision`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (1 nodes): `PostgresMemoryItemRepo`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 55`** (1 nodes): `LLMInterceptorRegistry`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 56`** (2 nodes): `MemoryCategoryRepo`, `PostgresMemoryCategoryRepo`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 58`** (2 nodes): `CategoryItemRepo`, `InMemoryCategoryItemRepository`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 62`** (2 nodes): `MemoryCategoryRepoProtocol`, `InMemoryMemoryCategoryRepository`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 63`** (1 nodes): `PostgresCategoryItemRepo`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 68`** (2 nodes): `InMemoryResourceRepository`, `ResourceRepoProtocol`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 78`** (2 nodes): `_cosine()`, `query_cosine()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 82`** (1 nodes): `Extract a clean filename from URL, handling query parameters.          Args:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 83`** (2 nodes): `matches_where()`, `Basic field/`__in` matcher for in-memory repos.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 84`** (2 nodes): `Test LazyLLMClient with basic operations.`, `test_lazyllm_client()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 85`** (1 nodes): `run_steps()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MemoryService` connect `Community 15` to `Community 6`, `Community 7`, `Community 2`, `Community 8`, `Community 10`, `Community 14`, `Community 21`, `Community 31`, `Community 19`, `Community 55`, `Community 22`, `Community 38`, `Community 17`, `Community 18`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Why does `Database` connect `Community 31` to `Community 7`, `Community 2`, `Community 14`, `Community 29`, `Community 21`, `Community 66`, `Community 8`, `Community 15`, `Community 10`, `Community 24`, `Community 6`, `Community 25`, `Community 60`, `Community 12`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Why does `MemorizeMixin` connect `Community 2` to `Community 6`, `Community 14`, `Community 31`, `Community 15`, `Community 10`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Are the 48 inferred relationships involving `MemoryService` (e.g. with `CRUDMixin` and `MemorizeMixin`) actually correct?**
  _`MemoryService` has 48 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `MemorizeMixin` (e.g. with `Context` and `CategoryConfig`) actually correct?**
  _`MemorizeMixin` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 73 inferred relationships involving `Database` (e.g. with `CRUDMixin` and `Validate and clean the `where` scope filters against the configured user model.`) actually correct?**
  _`Database` has 73 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Example 1: Multiple Conversations -> Memory Category File  This example demons`, `Generate concise markdown files for each memory category.`, `Process multiple conversation files and generate memory categories.      This` to the rest of the system?**
  _193 weakly-connected nodes found - possible documentation gaps or missing edges._