# Engineering Guide (for humans and AI assistants)

**These rules apply to every task and every prompt, big or small.** If you're an AI assistant: read this before writing code, and follow the workflow in §1 every time.

---

## 1. The workflow: Ground → Ask → Plan → Build → Verify
Never jump straight to code.

### 1.1 Ground yourself in what already exists
Before writing anything:
- **Read the relevant code first.** Find the files, functions, types, components and DB tables that touch this feature.
- **Search for something that already does it** (or almost does it): utilities, hooks, components, API wrappers, DB functions, schemas. Extend it; don't duplicate it.
- **Check the conventions in use:** folder structure, naming, the error-handling style, the state management, how API calls and DB access are done. New code must look like the code around it.
- **Check the installed dependencies** before adding a new one. Prefer what's already there; prefer the platform (e.g. Supabase auth, storage and realtime) over custom code.

### 1.2 Ask yourself the questions before deciding
Answer these, in writing if the task is non-trivial. If an answer is unknown and it changes the design, **ask the team** instead of guessing.
- **What exactly is the outcome?** What does "done" look like for the user? What's out of scope?
- **What are the inputs and outputs?** Types, formats, sizes, and where they come from.
- **What can go wrong?** Network failure, timeouts, empty or invalid input, AI returning garbage, duplicate submissions, concurrent users, no permission.
- **Who can access it?** Auth required? Whose data is it? What must they *not* be able to see or change?
- **Where does it belong?** Which module or layer? Is there an existing place for it?
- **What's the simplest design that works?** Is there a library or existing function that already solves it?
- **How will I know it works?** Which test, which manual check, which demo path?
- **Does it affect anything else?** Shared types, DB schema, other features, the demo flow.

### 1.3 Plan before executing
Write a short plan before coding:
1. Files to create or change (and why each one).
2. Data/schema changes (tables, columns, RLS policies).
3. The main functions/components and how they connect.
4. Error cases and how each is handled.
5. How it will be tested.

Keep the plan small. If the plan touches many files or changes shared code, **share it with the team (or the user) before building.**

### 1.4 Build in small, working steps
- Implement the smallest slice that works end-to-end, run it, then extend it.
- Make one logical change at a time. Don't mix refactors with features.
- Commit working states often, with clear messages.

### 1.5 Verify before saying "done"
- Run it. Exercise the happy path **and** at least the main failure paths.
- Run the tests, the linter and the type-checker.
- Re-read your own diff: remove leftovers, debug logs, commented-out code and unused imports.
- Report honestly: what works, what doesn't, what was skipped, and what's mocked.

---

## 2. Design principles: pick what fits the feature
Use the simplest structure that fits the problem. Don't apply patterns for their own sake.

| Principle | Use it like this |
|---|---|
| **KISS** | The straightforward solution is the default. Add complexity only when a real requirement demands it. |
| **YAGNI** | Don't build for imagined future needs: no unused options, flags or "just in case" layers. |
| **DRY (with judgement)** | Extract shared code when the *same logic* appears for the *same reason*. Rule of thumb: once is fine, twice note it, three times extract it. Don't merge code that only *looks* similar. |
| **Separation of concerns** | Keep UI, business logic, data access and external services in separate layers. UI doesn't talk to the DB directly; business logic doesn't know about React. |
| **Single responsibility** | Each function, component or module does one thing and is named for it. If you need "and" to describe it, split it. |
| **Single source of truth** | Types, constants, config, DB schema, prompts and UI strings live in one place and are imported everywhere else. |
| **Pure core, thin edges** | Put logic (calculations, scoring, validation, transformations) in pure functions that are easy to test. Side effects (DB, network, AI calls) stay at the edges. |

**Match the pattern to the feature:**
| Feature type | Appropriate design |
|---|---|
| External APIs (LLM, maps, payments, SMS) | An **adapter/client module** per service: one place for keys, timeouts, retries, parsing and errors. The rest of the app calls *our* function, not the vendor SDK. Makes it swappable and mockable. |
| AI / LLM features | Prompts in their own files; **structured output (JSON) validated against a schema** (e.g. Zod/Pydantic); a deterministic fallback when the model fails; numbers come from code/DB, never invented by the model. |
| Database access | A data-access layer (queries in one module per entity). Use typed clients and generated types. Put **access rules in RLS**, not only in the frontend. |
| Multi-step workflows / statuses | An explicit **state machine** (an enum of states + allowed transitions) instead of scattered booleans. |
| Forms & user input | One schema used for both client and server validation. |
| UI | Small reusable components; a page = composition of components; **design tokens from the one theme file defined by the brand sheet ([04](04-brand-and-design.md)), with no hard-coded colours or fonts**; **RTL-aware layout and all text in a strings/i18n file** (Arabic + English). |
| Background / ML jobs | A clear input/output contract, idempotent (safe to re-run), and logs what it did. |
| Config | Environment variables + one typed config module. No magic values scattered in code. |

---

## 3. Writing code: best practices
- **Readable over clever.** Clear names (`calculateFare`, not `calc2`), small functions, early returns instead of deep nesting.
- **Match the surrounding code:** naming, formatting, file layout, comment density, and the idioms in use.
- **Comments explain *why*, not *what*.** If code needs a comment to explain what it does, rename or simplify it first.
- **Types everywhere** (TypeScript strict / Python type hints). No `any` unless justified in a comment.
- **No dead code:** no commented-out blocks, unused exports or leftover debug logs. Git remembers history.
- **No magic numbers or strings:** name them as constants or config.
- **Format and lint automatically** (Prettier/ESLint, Ruff/Black). Don't argue about style; let the tool decide.

### Don't write unnecessary code
- **Before writing a function, search for an existing one** in the codebase, the standard library, or an already-installed dependency.
- **Don't rewrite what a mature library does well:** dates, validation, HTTP, auth, maps, CSV parsing, charts.
- **But don't add a dependency for a few lines of code.** Check that a library is maintained and widely used before adding it.
- **Build only what the current task needs.** No speculative abstractions, generic frameworks or "utils for later".
- **Delete code that's no longer used** as part of the same change that made it unused.

---

## 4. Handling failure: never swallow errors
**The rule: every error is either handled meaningfully or passed up, never silently ignored.**

❌ Never:
```ts
try { await save(data) } catch (e) {}          // silent: the bug disappears
try { ... } catch (e) { console.log(e) }       // "handled" but nobody acts; flow continues as if it worked
const result = data?.items ?? []               // hides that data failed to load
```

✅ Instead:
- **Catch only where you can do something useful:** retry, use a fallback, show a message, or add context and rethrow. Otherwise let it propagate.
- **Add context when rethrowing:** `throw new Error("Failed to create booking for route " + routeId, { cause: e })`.
- **Fail fast on invalid input or state.** Validate at the boundaries (API handlers, form submits, AI responses, env vars at startup) and stop with a clear error.
- **Distinguish error types:** the user's fault (show a clear message, in Arabic), temporary failures (retry with backoff), and bugs (log loudly with details).
- **The user always knows what happened:** loading, success and error states on every action. Never a frozen button or a blank screen.
- **External calls (LLM, APIs) get:** a timeout, limited retries with backoff for transient errors, response validation, and a fallback path.
- **Log useful details** (what failed, with which IDs and inputs, minus secrets/PII) to the console or server logs, so problems are debuggable.
- **Supabase/fetch calls return errors as values.** Always check `error` before using `data`.
- If you deliberately ignore an error, **write a comment explaining why** it's safe.

---

## 5. Testing
Test what matters most, proportionate to the time we have.

| What | How | Priority |
|---|---|---|
| Pure logic (calculations, validation, scoring, transformations, state transitions) | **Unit tests**: fast, many cases, including edge cases (empty, zero, max, invalid) | **Always** |
| AI output handling | Tests that the parser/validator accepts good output and **rejects malformed output** (fixtures of real and broken responses) | **Always** |
| API routes / DB functions | **Integration tests** against a local or test database, including permission checks (user A can't read user B's data) | High |
| The demo path | One **end-to-end smoke test** (or a scripted manual checklist) of the exact flow shown on stage | **Always, before the demo** |
| UI components | Test behaviour that has logic; skip testing pure layout | Medium |

Testing rules:
- **Write or update a test with every bug fix** that reproduces the bug first.
- Tests must be **deterministic**: mock time, randomness, network and AI calls (use recorded fixtures).
- **Run the tests before every commit/merge.** A broken test is fixed or deleted with a reason, never ignored.
- Never weaken an assertion just to make a test pass. Fix the code, or explain why the expectation was wrong.

---

## 6. Security basics (non-negotiable)
- **Secrets:** API keys and service keys live in environment variables only. **Never commit them**; keep `.env` in `.gitignore`, and commit a `.env.example` with placeholder values. If a key leaks, rotate it immediately.
- **Server vs client:** the Supabase **service-role key and LLM API keys never go to the browser.** Call LLMs and privileged operations from server code / edge functions only.
- **Row Level Security ON for every Supabase table**, with explicit policies. The frontend's checks are UX, not security.
- **Authorise on the server:** check that the user is allowed to do *this action on this record*, every time.
- **Validate and sanitise all input** on the server (schema validation, length limits, allowed values). Use parameterised queries or the query builder; never build SQL from strings.
- **Treat AI output as untrusted input:** validate it against a schema, never execute it, never render it as raw HTML, and never let it decide permissions. Watch for prompt injection from user-provided text.
- **File uploads:** check type and size, store them in private buckets, and serve them via signed URLs.
- **Privacy:** collect the minimum personal data, get consent, aggregate or anonymise where possible, don't log PII or secrets, and delete raw data you don't need.
- **Cost and abuse limits:** rate-limit expensive endpoints (LLM calls), set spending caps on API keys, and cap input sizes.
- **Dependencies:** use well-known packages, pin versions with a lockfile, and avoid copy-pasting unknown code.
- **Errors shown to users** must not leak stack traces, keys or internal details.

---

## 7. Modular, reusable structure
Organise by feature, with shared code in one obvious place. Example layout (adapt it to the framework in use):
```
src/
  features/<feature>/      # everything for one feature: components, hooks, logic, tests
  components/ui/           # shared UI building blocks (Button, Card, Map, ...)
  lib/                     # shared logic: validation schemas, utils, formatting
  services/                # adapters for external services: llm.ts, maps.ts, payments.ts
  db/                      # data-access functions, generated types, migrations
  config/                  # typed env/config, constants
  i18n/                    # UI strings (ar, en)
  prompts/                 # LLM prompts + their output schemas
tests/                     # or co-located *.test.ts next to the code
```
- **One way to do each thing:** one LLM client, one DB access pattern, one error format, one fetch wrapper, one date format. Reuse it everywhere.
- **Clear module boundaries:** each module exposes a small public API; others import only that.
- **Components take props, don't fetch their own unrelated data**, and don't hard-code text (use i18n).
- **Before creating a new helper/component, check `lib/`, `components/ui/` and `services/`.** If something similar exists, extend it (carefully, without breaking current users).

---

## 8. Efficiency
- **Correct first, then fast, and only where it matters.** Measure before optimising.
- **Avoid obvious waste:** N+1 queries (fetch in batches/joins), re-fetching unchanged data, unbounded queries (always paginate or limit), and re-rendering big lists without keys/memoisation.
- **LLM calls are slow and cost money:** cache identical requests, batch where possible, stream long responses, use the smallest model that does the job well, keep prompts tight, and set max tokens.
- **Do heavy work once:** precompute, index the DB columns you filter on, and load large static data once.
- **Keep the demo snappy:** show progress/streaming for anything over ~1 second, and pre-warm services before the pitch.

---

## 9. Git hygiene
- Work on a branch per feature; `main` stays demo-ready.
- **Small, focused commits** with messages that say *what* and *why*.
- Pull and merge often to avoid big conflicts; resolve conflicts carefully and re-run the app.
- Never commit secrets, `.env`, large datasets or generated build output.

---

## 10. Definition of done (check before every "it's finished")
- [ ] I grounded myself in the existing code and reused what was there
- [ ] I planned first and answered the key questions (§1.2)
- [ ] It works end-to-end, including the main failure cases
- [ ] No error is swallowed; users see clear states (loading / success / error), in Arabic where relevant
- [ ] Tests added or updated and passing; lint and type-check clean
- [ ] Security basics hold: no secrets in code, RLS/permissions, input validation, AI output validated
- [ ] No unnecessary code: no duplicates, dead code, debug logs or unused dependencies
- [ ] Follows the existing structure and conventions; shared code lives in the shared place
- [ ] UI uses only the brand's theme tokens, fonts, names and terms ([04](04-brand-and-design.md))
- [ ] README updated if setup or usage changed; mocked parts are labelled
- [ ] I reported honestly what's done, what's not, and what's mocked

---

## 11. Reusable instruction block for AI assistants
Paste this at the start of any coding prompt (or keep it in `CLAUDE.md`):

> Before writing code: (1) read the relevant existing code and search for anything that already does this; (2) list your questions and assumptions, and ask me if an answer changes the design; (3) give me a short plan: files to change, data changes, error cases, tests. Then implement in small steps that match the existing conventions. Reuse existing utilities/components; don't add unnecessary code or dependencies. Never swallow errors: handle them meaningfully or propagate them with context. Validate inputs and AI outputs; keep secrets server-side; respect RLS/permissions. Add or update tests for the logic you change and run them. Finish with a summary of what changed, how you verified it, and anything mocked, skipped or still broken.
