# <PROJECT_NAME>

<!-- One sentence: what it is and for whom. -->

## 1. Project Overview

<!-- 3-5 sentences:
     - What does this project do?
     - What problem does it solve?
     - Who are the users (humans, services, both)?
     Keep it factual. No marketing copy. -->

## 2. Architecture

<!-- A diagram (mermaid or ASCII) plus 5-10 sentences explaining the
     main flow of data and control. Mention the major boundaries
     (modules, services, processes) and how they communicate. -->

```mermaid
graph LR
  A[<Replace with a real diagram>] --> B[<Or remove this fenced block>]
```

## 3. Key Directories

<!-- Only the directories that matter. Don't dump the full tree.
     Format: a short table. -->

| Path | Purpose |
|---|---|
| `<path/to/dir>` | <one-line purpose> |
| `<path/to/dir>` | <one-line purpose> |

## 4. Conventions

<!-- Style, naming, testing approach. Link to .editorconfig, eslint
     config, ruff config, etc. instead of duplicating their content. -->

- **Code style:** <e.g. "Black + Ruff" or "Prettier + ESLint">.
- **Naming:** <e.g. "snake_case for files, PascalCase for classes">.
- **Tests:** <e.g. "pytest, one test file per source file, AAA layout">.

## 5. Commands

<!-- Only the commands a developer runs daily. -->

| Command | Purpose |
|---|---|
| `<build cmd>` | Build the project. |
| `<test cmd>` | Run the test suite. |
| `<lint cmd>` | Run the linter. |
| `<run cmd>` | Run the application locally. |

## 6. Common Workflows

<!-- "How do I X" recipes. Two or three is enough; more goes in
     .claude/memory/playbooks/. -->

### How to add a feature

<!-- Replace with the actual workflow for this repo. -->

### How to fix a typical bug

<!-- Replace with the actual workflow for this repo. -->

## 7. Anti-Patterns

<!-- What NOT to do in this repo + why. The why is the important part —
     a rule without a reason invites being ignored. -->

- **Don't <X>** — because <reason>.
- **Don't <Y>** — because <reason>.
