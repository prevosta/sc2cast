# Development Workflow Guide# Development Workflow# Development Workflow Guide



## 🎯 How to Work With Me Effectively



### Before Each Sprint## 🎯 Core Principle: SIMPLICITY## 🎯 How to Work With Me Effectively



1. **Check CURRENT_SPRINT.md** - This is the ONLY file that matters

2. I will ONLY work on tasks listed in CURRENT_SPRINT.md

3. Each sprint produces 2-5 small, working files maximum**Everything must be minimal:**### Before Each Sprint



### During Sprint- Minimal code per task



**Your role:**- Minimal files (6 docs maximum)1. **Check CURRENT_SPRINT.md** - This is the ONLY file that matters

- Give me ONE task at a time: "Do task 1", "Do task 2"

- Test each deliverable before moving on- Minimal documentation (no redundancy)2. I will ONLY work on tasks listed in CURRENT_SPRINT.md

- Update checkboxes in CURRENT_SPRINT.md as we complete tasks

- One source of truth per concept3. Each sprint produces 2-5 small, working files maximum

**My role:**

- Create minimal, working code for that specific task

- No "over-engineering" or "future-proofing"

- No code that isn't needed for current sprint goal---### During Sprint



---



## 📋 File Structure (Final)## 📋 File Structure (Final)**Your role:**



### Code & Config- Give me ONE task at a time: "Do task 1", "Do task 2"

```

src/              # Source code only### Code & Config- Test each deliverable before moving on

tests/            # Tests only

config/           # Config files only```- Update checkboxes in CURRENT_SPRINT.md as we complete tasks

pyproject.toml    # Poetry dependencies

poetry.lock       # Locked dependenciessrc/              # Source code only

```

tests/            # Tests only**My role:**

### Documentation (6 Files Maximum)

```config/           # Config files only- Create minimal, working code for that specific task

README.md                    # Entry point + quick start

docs/TECHNICAL.md           # All technical info (architecture, setup, examples)Dockerfile- No "over-engineering" or "future-proofing"

docs/IMPLEMENTATION.md      # All planning (timeline, status, milestones)

docs/FAQ.md                 # Questions & answersdocker-compose.yml- No code that isn't needed for current sprint goal

docs/dev/CURRENT_SPRINT.md  # Active sprint tasks only

docs/dev/DEVLOG.md          # History log (concise)requirements.txt

```

```### Prompting Guidelines

**That's it. Never create more docs.**



---

### Documentation (6 Files Maximum)#### ✅ GOOD Prompts (Specific, One Task)

## 🚫 Documentation Rules

``````

### NEVER Create Separate Files For:

- ❌ "Architecture" vs "Overview" vs "Deep Dive" → ONE `TECHNICAL.md`README.md                    # Entry point + quick start"Create the Dockerfile"

- ❌ "Plan" vs "Status" vs "Timeline" → ONE `IMPLEMENTATION.md`

- ❌ "Quick Start" separate → Put in `README.md`docs/TECHNICAL.md           # All technical info (architecture, setup, examples)"Add the demo replay to the project"

- ❌ "Code Examples" separate → Put in `TECHNICAL.md`

- ❌ "Consistency Reports" → Just fix the actual filesdocs/IMPLEMENTATION.md      # All planning (timeline, status, milestones)"Fix the Docker build error"

- ❌ ANY "analysis" or "summary" files → Don't create them

docs/FAQ.md                 # Questions & answers"Complete task 3 in CURRENT_SPRINT.md"

### Rule: One Concept = One Section (Not One File)

docs/dev/CURRENT_SPRINT.md  # Active sprint tasks only"Test if nvidia-smi works in container"

---

docs/dev/DEVLOG.md          # History log (concise)```

## 🔄 Handling Changes

```

### When a Decision Changes:

1. **Search** all docs for mentions (grep)#### ❌ BAD Prompts (Too Broad)

2. **Update** all at once

3. **Log** in DEVLOG.md (one line)**That's it. Never create more docs.**```

4. Done.

"Implement the commentary system"  # Too big!

### Adding New Features:

1. Update `CURRENT_SPRINT.md` (current work)---"Set everything up"                # Too vague!

2. Write code in `src/`

3. Update `TECHNICAL.md` if architecture changes"Create all the infrastructure"    # Too much!

4. Log in `DEVLOG.md` (one line)

## 🚫 Documentation Rules"Build the pipeline"               # Multiple sprints!

**Update everything immediately or don't update at all. Never let docs drift.**

```

---

### NEVER Create Separate Files For:

## 📏 Quality Standards

- ❌ "Architecture" vs "Overview" vs "Deep Dive" → ONE `TECHNICAL.md`### File Organization (Keep It Simple)

1. **Minimal Code** - Only what THIS task needs

2. **Working Increments** - Every task produces something testable- ❌ "Plan" vs "Status" vs "Timeline" → ONE `IMPLEMENTATION.md`

3. **No Speculation** - Don't code for future features

4. **Obvious Names** - Self-documenting code- ❌ "Quick Start" separate → Put in `README.md````

5. **One Source of Truth** - Each fact exists in ONE place only

- ❌ "Code Examples" separate → Put in `TECHNICAL.md`sc2cast/

---

- ❌ "Consistency Reports" → Just fix the actual files├── CURRENT_SPRINT.md           # ← THE ONLY FILE THAT MATTERS

## 🎯 Sprint Process

- ❌ ANY "analysis" or "summary" files → Don't create them├── README.md                    # Project overview

```

User: "Start Sprint 1.1"├── docs/                        # All design docs (reference only)

→ Update CURRENT_SPRINT.md (3-5 tasks)

### Rule: One Concept = One Section (Not One File)│   └── *.md

User: "Do task 1"

→ Write minimal code├── Dockerfile                   # Sprint 1.1

→ Test it

→ Mark task complete---├── docker-compose.yml          # Sprint 1.1



User: "Do task 2"└── src/                        # Code (starts in Sprint 1.2+)

→ Write minimal code

→ Test it## 🔄 Handling Changes    └── (empty for now)

→ Mark task complete

```

User: "Sprint done"

→ Update DEVLOG.md (2 lines)### When a Decision Changes:

→ Start next sprint

```1. **Search** all docs for mentions (grep)## 🔄 Sprint Workflow



**One task at a time. No exceptions.**2. **Update** all at once



---3. **Log** in DEVLOG.md (one line)### Step 1: Start New Sprint



## 📊 Tracking4. Done.```



**Current Work:** CURRENT_SPRINT.md (checkboxes)  You: "Start Sprint 1.1"

**History:** DEVLOG.md (2-3 lines per sprint)

### Adding New Features:Me: Updates CURRENT_SPRINT.md with tasks

No separate tracking files. No status reports.

1. Update `CURRENT_SPRINT.md` (current work)```

---

2. Write code in `src/`

## 🔄 Documentation Consistency

3. Update `TECHNICAL.md` if architecture changes### Step 2: Execute Tasks

**CRITICAL: Keep all docs aligned when decisions change!**

4. Log in `DEVLOG.md` (one line)```

### When Making ANY Design Decision or Change:

You: "Do task 1"

1. **Update CURRENT_SPRINT.md** if it affects current work

2. **Update DEVLOG.md** to record the change**Update everything immediately or don't update at all. Never let docs drift.**Me: Creates Dockerfile (minimal, working)

3. **Search for references** in design docs:

   - Use grep/search to find all mentions of the changed concept

   - Example: If switching from Docker → Windows native, search for "Docker" in all docs

---You: "Test it - docker build works!"

### Files That MUST Stay Consistent:

You: "Do task 2"

**Core Decisions (Update ALL when changed):**

- Technology choices → Update: README, TECHNICAL, IMPLEMENTATION, FAQ## 📏 Quality StandardsMe: Adds SC2 installation to Dockerfile

- Cost/budget → Update: README, IMPLEMENTATION

- Timeline/sprints → Update: IMPLEMENTATION, CURRENT_SPRINT```



### Preventing Inconsistency:1. **Minimal Code** - Only what THIS task needs

- ✅ When editing one doc, think: "What other docs mention this?"

- ✅ Use search tools to find all references2. **Working Increments** - Every task produces something testable### Step 3: Sprint Complete

- ✅ Update them ALL at once, not later```

- ✅ Record changes in DEVLOG.mdYou: "Mark Sprint 1.1 complete"

Me: Updates CURRENT_SPRINT.md to Sprint 1.2

**Never let docs drift out of sync!** 🎯    Updates DEVLOG.md with Sprint 1.1 summary

    **CRITICAL: Updates IMPLEMENTATION.md current status**

---```



## 🚫 File Creation Discipline**🚨 CRITICAL RULE: When completing a sprint:**

1. Update `CURRENT_SPRINT.md` with new sprint

**CRITICAL: Minimize new files!**2. Update `DEVLOG.md` with completed sprint entry

3. **Update `IMPLEMENTATION.md` → "Current Status" section**

### Before Creating ANY New File, Ask:4. Commit all three files together

1. ❓ Can this go in an existing file?

2. ❓ Does this NEED to exist permanently?**Never skip step 3!** IMPLEMENTATION.md must always reflect current progress.

3. ❓ Will the user reference this file regularly?

---

### ✅ GOOD Reasons to Create a File:

- Core code files (required for functionality)## 📏 Quality Principles

- Essential config files (pyproject.toml, poetry.lock)

- Primary docs (README, DEVLOG, WORKFLOW, CURRENT_SPRINT)3. **No Speculation** - Don't code for future features```



### ❌ BAD Reasons to Create a File:4. **Obvious Names** - Self-documenting codeYou: "Mark Sprint 1.1 complete"

- "Consistency reports" ← Update the actual files instead!

- "Status summaries" ← Use DEVLOG.md5. **One Source of Truth** - Each fact exists in ONE place onlyMe: Updates CURRENT_SPRINT.md to Sprint 1.2

- "Analysis documents" ← Mention in conversation, don't save

- "Temporary notes" ← Never create these```

- "Planning files" ← Use CURRENT_SPRINT.md

---

### Rule of Thumb:

**If it's not code, config, or a core workflow doc → DON'T CREATE IT**## 📏 Quality Principles



When in doubt: Update existing files or just tell the user verbally.## 🎯 Sprint Process



---1. **Minimal Viable Code** - Only what's needed for THIS task



## 🎯 Example: Sprint 1.1 (Windows Environment Setup)```2. **Working Increments** - Each task produces testable output



### Task 1: Install Python & PoetryUser: "Start Sprint 1.2"3. **No Speculation** - Don't code for future features

```powershell

# Install Poetry→ Update CURRENT_SPRINT.md (3-5 tasks)4. **Obvious Naming** - `parse_replay()` not `process_data()`

pip install poetry

5. **Fail Fast** - Basic error handling only, let things crash

# Verify installation

poetry --versionUser: "Do task 1"

```

→ Write minimal code## 🚫 File Creation Discipline

### Task 2: Initialize Project

```powershell→ Test it

# Create pyproject.toml

poetry init→ Mark task complete**CRITICAL: Minimize new files!**



# Add dependencies

poetry add sc2reader python-sc2

poetry add --group dev pytest blackUser: "Do task 2"### Before Creating ANY New File, Ask:

```

→ Write minimal code1. ❓ Can this go in an existing file?

### Task 3: Verify SC2 Installation

```python→ Test it2. ❓ Does this NEED to exist permanently?

# Simple script to check SC2 path

import os→ Mark task complete3. ❓ Will the user reference this file regularly?

from pathlib import Path



sc2_path = Path("C:/Program Files (x86)/StarCraft II")

if sc2_path.exists():User: "Sprint done"### ✅ GOOD Reasons to Create a File:

    print(f"✅ SC2 found at: {sc2_path}")

else:→ Update DEVLOG.md (2 lines)- Core code files (required for functionality)

    print("❌ SC2 not found!")

```→ Start next sprint- Essential config files (Dockerfile, docker-compose.yml)



### Task 4: Test Poetry Environment```- Primary docs (README, DEVLOG, WORKFLOW, CURRENT_SPRINT)

```powershell

poetry install

poetry run python --version

# Success! Sprint 1.1 complete.**One task at a time. No exceptions.**### ❌ BAD Reasons to Create a File:

```

- "Consistency reports" ← Update the actual files instead!

---

---- "Status summaries" ← Use DEVLOG.md

## 🚧 When Things Go Wrong

- "Analysis documents" ← Mention in conversation, don't save

**If I start creating too much code:**

- You: "STOP. Focus only on task X"## 📊 Tracking- "Temporary notes" ← Never create these

- I will: Delete extra code, focus on one task

- "Planning files" ← Use CURRENT_SPRINT.md

**If you're not sure what to ask:**

- You: "What's the next task?"**Current Work:** CURRENT_SPRINT.md (checkboxes)

- I will: Read CURRENT_SPRINT.md and tell you

**History:** DEVLOG.md (2-3 lines per sprint)### Rule of Thumb:

**If sprint is taking too long:**

- You: "Simplify this task"**If it's not code, config, or a core workflow doc → DON'T CREATE IT**

- I will: Cut scope, make it smaller

No separate tracking files. No status reports.

---

When in doubt: Update existing files or just tell the user verbally.

## 📊 Progress Tracking

---

Use CURRENT_SPRINT.md checkboxes:

```markdown## 🔄 Documentation Consistency

## Tasks

- [x] Task 1: Install Poetry ✅**Keep it simple. Keep it clean. Keep moving.** 🚀

- [x] Task 2: Initialize project ✅

- [ ] Task 3: Verify SC2 path**CRITICAL: Keep all docs aligned when decisions change!**

- [ ] Task 4: Test environment

```### When Making ANY Design Decision or Change:



---1. **Update CURRENT_SPRINT.md** if it affects current work

2. **Update DEVLOG.md** to record the change

## 🎓 Philosophy3. **Search for references** in design docs:

   - Use grep/search to find all mentions of the changed concept

> "Make the smallest change that proves the concept works."   - Example: If switching from GPT-4 → Llama, search for "GPT-4" in all docs



- Sprint 1.1: Python environment ready ✅### Files That MUST Stay Consistent:

- Sprint 1.2: Replay file parsed ✅

- Sprint 1.3: Events extracted ✅**Core Decisions (Update ALL when changed):**

- Sprint 1.4: Video generated ✅- Technology choices → Update: PROJECT_OVERVIEW, TECHNICAL_DEEP_DIVE, ARCHITECTURE, CODE_EXAMPLES, FAQ

- Cost/budget → Update: README, PANEL_PRESENTATION, PROJECT_STATUS, ZERO_BUDGET_APPROACH

Each sprint adds ONE capability. No more.- Timeline/sprints → Update: IMPLEMENTATION_PLAN, PROJECT_STATUS, CURRENT_SPRINT



---**Example Workflow for a Decision Change:**

```

## 🚀 Ready to Start?User: "Let's use GPT-4 instead of Llama"



When you're ready:You: 

1. Review CURRENT_SPRINT.md1. ❓ Search all docs for "Llama" and "GPT-4"

2. Say: "Do task 1" or "Install Poetry"2. ✏️ Update 5-6 files with new decision

3. Test the output3. 📝 Record in DEVLOG.md: "Changed LLM from Llama to GPT-4"

4. Move to next task4. 💰 Update cost estimates (now $150/mo instead of $0)

5. ✅ Verify consistency across all docs

**Let's build this one small step at a time!** 🎯```



---### Preventing Inconsistency:

- ✅ When editing one doc, think: "What other docs mention this?"

## Prompting Guidelines- ✅ Use search tools to find all references

- ✅ Update them ALL at once, not later

### ✅ GOOD Prompts (Specific, One Task)- ✅ Record changes in DEVLOG.md

```

"Install Poetry"**Never let docs drift out of sync!** 🎯

"Add the demo replay to the project"

"Test if SC2 path is correct"## 🎯 Example: Sprint 1.1 (Docker Setup)

"Complete task 3 in CURRENT_SPRINT.md"

"Parse the replay metadata"### Task 1: Create Dockerfile

``````dockerfile

# Minimal Dockerfile (50 lines max)

### ❌ BAD Prompts (Too Broad)FROM nvidia/cuda:12.2.0-base-ubuntu22.04

```

"Implement the commentary system"  # Too big!# Install SC2

"Set everything up"                # Too vague!RUN wget https://... && unzip ...

"Create all the infrastructure"    # Too much!

"Build the pipeline"               # Multiple sprints!# Install Python

```RUN apt-get update && apt-get install -y python3.11



---# Done. That's it. Nothing else.

```

## File Organization (Keep It Simple)

### Task 2: Create docker-compose.yml

``````yaml

sc2cast/# Minimal compose file (20 lines max)

├── CURRENT_SPRINT.md           # ← THE ONLY FILE THAT MATTERSversion: '3.8'

├── README.md                    # Project overviewservices:

├── pyproject.toml               # Poetry config  sc2cast:

├── poetry.lock                  # Locked dependencies    build: .

├── docs/                        # All design docs (reference only)    deploy:

│   └── *.md      resources:

└── src/                         # Code (starts in Sprint 1.2+)        reservations:

    └── (empty for now)          devices:

```            - driver: nvidia

              count: 1

---              capabilities: [gpu]

```

## 🔄 Sprint Workflow

### Task 3: Test

### Step 1: Start New Sprint```powershell

```docker-compose build

You: "Start Sprint 1.1"docker-compose run sc2cast nvidia-smi

Me: Updates CURRENT_SPRINT.md with tasks# Success! Sprint 1.1 complete.

``````



### Step 2: Execute Tasks## 🚧 When Things Go Wrong

```

You: "Do task 1"**If I start creating too much code:**

Me: Installs Poetry (minimal, working)- You: "STOP. Focus only on task X"

- I will: Delete extra code, focus on one task

You: "Test it - poetry --version works!"

You: "Do task 2"**If you're not sure what to ask:**

Me: Initializes pyproject.toml- You: "What's the next task?"

```- I will: Read CURRENT_SPRINT.md and tell you



### Step 3: Sprint Complete**If sprint is taking too long:**

```- You: "Simplify this task"

You: "Mark Sprint 1.1 complete"- I will: Cut scope, make it smaller

Me: Updates CURRENT_SPRINT.md to Sprint 1.2

    Updates DEVLOG.md with Sprint 1.1 summary## 📊 Progress Tracking

    **CRITICAL: Updates IMPLEMENTATION.md current status**

```Use CURRENT_SPRINT.md checkboxes:

```markdown

**🚨 CRITICAL RULE: When completing a sprint:**## Tasks

1. Update `CURRENT_SPRINT.md` with new sprint- [x] Task 1: Create Dockerfile ✅

2. Update `DEVLOG.md` with completed sprint entry- [x] Task 2: Add GPU support ✅

3. **Update `IMPLEMENTATION.md` → "Current Status" section**- [ ] Task 3: Test container

4. Commit all three files together- [ ] Task 4: Add VS Code devcontainer

```

**Never skip step 3!** IMPLEMENTATION.md must always reflect current progress.

## 🎓 Philosophy

---

> "Make the smallest change that proves the concept works."

**Keep it simple. Keep it clean. Keep moving.** 🚀

- Sprint 1.1: Container runs ✅
- Sprint 1.2: Replay file parsed ✅
- Sprint 1.3: First frame captured ✅
- Sprint 1.4: Video file created ✅

Each sprint adds ONE capability. No more.

---

## 🚀 Ready to Start?

When you're ready:
1. Review CURRENT_SPRINT.md
2. Say: "Do task 1" or "Create the Dockerfile"
3. Test the output
4. Move to next task

**Let's build this one small step at a time!** 🎯

---

## 📜 Sprint History Log

### Sprint 1.1: Docker Environment Setup
**Status:** In Progress - Task 3  
**Started:** November 5, 2025

#### Completed Tasks:
- ✅ **Task 1**: `Dockerfile` exists (33 lines)
- ✅ **Task 2**: `docker-compose.yml` exists (29 lines)

#### Current Task:
- 🔄 **Task 3**: Test Container Build
  - Status: Building now (5-10 minutes estimated)
  - Running: `docker compose build`
  - Progress: Installing system packages

#### Next Tasks:
- ⏸️ **Task 4**: Test GPU Access
- ⏸️ **Task 5**: Test Python

#### Files Created:
```
Dockerfile              (SC2 + CUDA + Python environment)
docker-compose.yml      (GPU support, volume mounts)
```

#### Notes:
- Build in progress, downloading packages (~4GB SC2 client next)
