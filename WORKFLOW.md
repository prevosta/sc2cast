# Development Workflow Guide

## 🎯 How to Work With Me Effectively

### Before Each Sprint

1. **Check CURRENT_SPRINT.md** - This is the ONLY file that matters
2. I will ONLY work on tasks listed in CURRENT_SPRINT.md
3. Each sprint produces 2-5 small, working files maximum

### During Sprint

**Your role:**
- Give me ONE task at a time: "Do task 1", "Do task 2"
- Test each deliverable before moving on
- Update checkboxes in CURRENT_SPRINT.md as we complete tasks

**My role:**
- Create minimal, working code for that specific task
- No "over-engineering" or "future-proofing"
- No code that isn't needed for current sprint goal

### Prompting Guidelines

#### ✅ GOOD Prompts (Specific, One Task)
```
"Create the Dockerfile"
"Add the demo replay to the project"
"Fix the Docker build error"
"Complete task 3 in CURRENT_SPRINT.md"
"Test if nvidia-smi works in container"
```

#### ❌ BAD Prompts (Too Broad)
```
"Implement the commentary system"  # Too big!
"Set everything up"                # Too vague!
"Create all the infrastructure"    # Too much!
"Build the pipeline"               # Multiple sprints!
```

### File Organization (Keep It Simple)

```
sc2cast/
├── CURRENT_SPRINT.md           # ← THE ONLY FILE THAT MATTERS
├── README.md                    # Project overview
├── docs/                        # All design docs (reference only)
│   └── *.md
├── Dockerfile                   # Sprint 1.1
├── docker-compose.yml          # Sprint 1.1
└── src/                        # Code (starts in Sprint 1.2+)
    └── (empty for now)
```

## 🔄 Sprint Workflow

### Step 1: Start New Sprint
```
You: "Start Sprint 1.1"
Me: Updates CURRENT_SPRINT.md with tasks
```

### Step 2: Execute Tasks
```
You: "Do task 1"
Me: Creates Dockerfile (minimal, working)

You: "Test it - docker build works!"
You: "Do task 2"
Me: Adds SC2 installation to Dockerfile
```

### Step 3: Sprint Complete
```
You: "Mark Sprint 1.1 complete"
Me: Updates CURRENT_SPRINT.md to Sprint 1.2
```

## 📏 Quality Principles

1. **Minimal Viable Code** - Only what's needed for THIS task
2. **Working Increments** - Each task produces testable output
3. **No Speculation** - Don't code for future features
4. **Obvious Naming** - `parse_replay()` not `process_data()`
5. **Fail Fast** - Basic error handling only, let things crash

## 🎯 Example: Sprint 1.1 (Docker Setup)

### Task 1: Create Dockerfile
```dockerfile
# Minimal Dockerfile (50 lines max)
FROM nvidia/cuda:12.2.0-base-ubuntu22.04

# Install SC2
RUN wget https://... && unzip ...

# Install Python
RUN apt-get update && apt-get install -y python3.11

# Done. That's it. Nothing else.
```

### Task 2: Create docker-compose.yml
```yaml
# Minimal compose file (20 lines max)
version: '3.8'
services:
  sc2cast:
    build: .
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### Task 3: Test
```powershell
docker-compose build
docker-compose run sc2cast nvidia-smi
# Success! Sprint 1.1 complete.
```

## 🚧 When Things Go Wrong

**If I start creating too much code:**
- You: "STOP. Focus only on task X"
- I will: Delete extra code, focus on one task

**If you're not sure what to ask:**
- You: "What's the next task?"
- I will: Read CURRENT_SPRINT.md and tell you

**If sprint is taking too long:**
- You: "Simplify this task"
- I will: Cut scope, make it smaller

## 📊 Progress Tracking

Use CURRENT_SPRINT.md checkboxes:
```markdown
## Tasks
- [x] Task 1: Create Dockerfile ✅
- [x] Task 2: Add GPU support ✅
- [ ] Task 3: Test container
- [ ] Task 4: Add VS Code devcontainer
```

## 🎓 Philosophy

> "Make the smallest change that proves the concept works."

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
