# WORKFLOW GUIDE — Continuing this project in Claude Code / Cowork / Codex / Antigravity

> How to **hand off and continue** the work across AI tools using the vibe-coding course methods
> (Harness Engineering, Agentic Engineering, SDD, AI-Native). Read with `HANDOFF.md` (context) and
> the repo-root `CLAUDE.md` / `AGENTS.md` (rules).

---

## 1. The handoff model in one picture
```
            docs/  = the single source of truth (the "second brain")
            ├── CLAUDE.md / AGENTS.md   ← constitution (rules every tool obeys)
            ├── SPEC.md                 ← what the analysis must do (update before coding)
            ├── DATA_SOURCES.md         ← data + license + status
            └── handoff/ (HANDOFF, PROJECT_JOURNEY, WORKFLOW_GUIDE)
                         │
   ┌─────────────────────┼───────────────────────┐
   ▼                     ▼                        ▼
Claude Code        Claude Cowork              Codex / Antigravity
(reads CLAUDE.md)  (reads CLAUDE.md)          (reads AGENTS.md)
```
**Principle (Harness Engineering):** tools are interchangeable *because the context lives in the
repo, not in any one chat.* To switch tools, you don't re-explain — you point the new tool at the
repo and these docs. Keep the docs current; that is the real work of a handoff.

## 2. Tool roles (use the right one per task)
| Tool | Best for | How it reads context |
|---|---|---|
| **Claude Code** (terminal/IDE agent) | writing/refactoring code, running the pipeline, tests, git | auto-reads `CLAUDE.md`; run `/init` if needed |
| **Claude Cowork** (desktop knowledge-work agent) | docs, the report, slides, data spelunking, planning | reads repo files; paste `HANDOFF.md` to start |
| **Codex** (OpenAI agent) | parallel coding tasks, alt-model cross-check, when Claude credits are low | auto-reads `AGENTS.md` |
| **Antigravity** (Google agentic IDE) | agentic multi-file coding / alt environment | paste `AGENTS.md` + `HANDOFF.md` at start |

> When **Claude credits run low** or the course exercise calls for Codex/Antigravity: open the repo
> there, ensure `AGENTS.md` is present, and paste `HANDOFF.md` as the first message. That single
> file + `AGENTS.md` is enough to continue.

## 3. Onboarding a tool (copy-paste starting prompts)

**Claude Code** (in the repo dir):
```
Read CLAUDE.md and docs/handoff/HANDOFF.md. Confirm the rules (esp. "no chatbot", 고어 char-level,
never commit corpus). Then run tests/test_smoke.py and python -m src.pipeline --data data/sample,
and report the persona types. Wait for my go-ahead before changing analysis logic.
```

**Claude Cowork:**
```
This is the K-Story Persona Lab project. Read docs/handoff/HANDOFF.md and docs/SPEC.md. Help me
[draft the report / build slides / curate analysis units]. Follow CLAUDE.md rules. Do not add any
chatbot or dialogue-generation; this is a stylometry data analysis.
```

**Codex / Antigravity:**
```
Read AGENTS.md (rules) and docs/handoff/HANDOFF.md (context). Set up the env (pip install -r
requirements.txt), make tests/test_smoke.py pass, then do <one scoped task>. Update docs/SPEC.md
before changing analysis logic. Never commit data/raw.
```

## 4. Course methods, applied to handoff
- **SDD (Spec-Driven Development):** never change analysis logic before updating `docs/SPEC.md`.
  The spec is the contract a handed-off tool implements. New decisions → `docs/ADR/`.
- **Agentic Engineering (plan → execute → validate):** ask the tool to *plan* first (list steps,
  files it will touch), then execute, then **validate** (degenerate clusters? unstable k? data
  leakage?). For bigger work, use sub-agents / parallel tasks (e.g. one builds features, one writes
  the report) — but they all read the same `docs/`.
- **Harness Engineering:** `CLAUDE.md`/`AGENTS.md` + `docs/` are the harness. Optionally add hooks
  (e.g. run `test_smoke.py` before commit) and project skills. The harness is what makes the project
  portable across tools and sessions.
- **AI-Native working:** keep raw artifacts in the repo and let AI transform them (data → features →
  report). Commit often; each commit is a checkpoint a new tool can resume from.

## 5. Task → tool delegation matrix
| Task | Tool | Hand-off artifact to point at |
|---|---|---|
| Run/extend the pipeline on real corpus | Claude Code / Codex | `CLAUDE.md`, `SPEC.md`, `src/` |
| Add stylometric features | Claude Code / Codex | `SPEC.md` §3, `METRICS` list, `stylometry.py` |
| Validate clustering (stability/leakage) | Claude Code (alt-model cross-check via Codex) | `SPEC.md` §5 |
| Curate analysis units (which figures/works) | Claude Cowork | `SPEC.md` §2, `DATA_SOURCES.md` |
| Write the 분석 보고서 | Claude Cowork | `reports/typology.md`, `HANDOFF.md` |
| Build 발표 슬라이드 | Claude Cowork (pptx) | report + results figures |
| Draft blog posts (dev log) | Claude Cowork / Code | `티스토리_블로그_콘텐츠_기획서.md` |
| Submission packaging (zip per spec) | Claude Code | `K-페르소나DNA_9일_실행계획서_v1.md` D9 |

## 6. How to hand off ONE task cleanly (checklist)
1. Make sure `docs/SPEC.md` describes the desired end-state (update it if not).
2. Write the task as: *goal · files in scope · acceptance check · "do not" list.*
3. Point the tool at the repo + the relevant doc (use the prompts in §3).
4. Require **plan → execute → validate**; have it run `test_smoke.py` (or the real pipeline) as the
   acceptance check.
5. After the tool finishes, update `docs/` (SPEC/ADR/HANDOFF status) so the *next* hand-off is clean.

## 7. Keeping context in sync across tools (avoid drift)
- Treat `docs/` as canonical; if a tool's answer conflicts with a doc, the doc wins (or update the
  doc deliberately).
- Update `HANDOFF.md` §7 "Repo state" and §9 "Open items" after each work session.
- One change at a time + commit; a fresh tool resumes from the latest commit + `HANDOFF.md`.
- Don't paste long chat history into a new tool — paste `HANDOFF.md` (and `PROJECT_JOURNEY.md` if it
  needs the *why*). That's what these files are for.
