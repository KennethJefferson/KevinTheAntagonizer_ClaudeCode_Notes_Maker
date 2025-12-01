# Usage Guide - Task-First Quick Reference

**Version**: 2.1 | **Last Updated**: November 2025

---

## How to Use This Guide

This guide is organized by **what you want to accomplish**, not by technical arguments. Find your goal, get the complete command, understand why it works.

**Choose your path**:
- 🚀 **First time?** → [30-Second Quickstart](#quickstart)
- 🎯 **Know your task?** → [Task Index](#task-index)
- 📖 **Need argument details?** → See [ARGUMENT_REFERENCE.md](ARGUMENT_REFERENCE.md)
- 🔧 **Technical deep-dive?** → See [USAGE.md](USAGE.md)

---

## Table of Contents

### Quick Start
- [30-Second Quickstart](#quickstart)
- [Prerequisites Check](#prerequisites)

### Task Index

**Basic Operations**
- [Task 01: Process Single Folder](#task-01)
- [Task 02: Process Multiple Folders](#task-02)
- [Task 03: Include All Subfolders (Recursive)](#task-03)
- [Task 04: Resume Interrupted Work](#task-04)

**Quality & Models**
- [Task 05: List Available Models](#task-05)
- [Task 06: Use Premium Model (Opus)](#task-06)
- [Task 07: Cost-Effective Processing (Haiku)](#task-07)
- [Task 08: Two-Tier Quality Strategy](#task-08)

**Database Operations**
- [Task 09: Check Progress Statistics](#task-09)
- [Task 10: List Failed Files](#task-10)
- [Task 11: Retry All Failures](#task-11)
- [Task 12: Reset and Start Fresh](#task-12)

**Advanced Processing**
- [Task 13: Speed Up with Parallel Workers](#task-13)
- [Task 14: Optimize Batch Size](#task-14)
- [Task 15: Custom Expert Persona](#task-15)
- [Task 16: Separate Databases per Project](#task-16)

**Troubleshooting**
- [Task 17: Validation Before Processing (Dry Run)](#task-17)
- [Task 18: Monitor Progress in Real-Time](#task-18)
- [Task 19: Handle Large Libraries (500+ files)](#task-19)
- [Task 20: Common Errors and Solutions](#task-20)

### Decision Support
- [Decision Tree: How Many Workers?](#decision-workers)
- [Decision Tree: Which Model?](#decision-model)
- [Decision Tree: Batch Size Optimization](#decision-batch)

### Quick Reference
- [Command Templates](#templates)
- [Common Combinations](#combinations)

---

## <a id="prerequisites"></a>Prerequisites Check

Before you begin, verify your setup:

```bash
# 1. Check Claude Code CLI is installed and logged in
claude-code whoami

# Should show your account email
# If not, install and login:
npm install -g @anthropic-ai/claude-code
claude-code login

# 2. Check Python dependencies
python -c "import claude_agent_sdk; print('SDK ready')"

# If fails, install:
pip install -r requirements.txt

# 3. Verify application access
python KevinTheAntagonizerClaudeCodeNotesMaker.py -h

# Should show help message
```

✓ **All working?** → Proceed to [Quickstart](#quickstart)
✗ **Issues?** → See [Task 20: Common Errors](#task-20)

---

## <a id="quickstart"></a>30-Second Quickstart

**Goal**: Process your first course folder

**The Command**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan "E:\WORKSPACE.DEV.PYTHON\AIML.Agents\KevinTheAntagonizerClaudeCodeNotesMaker\__Black Men - Amigoscode - Professional Full Stack Developer"
```

**What Happens**:
1. Scans folder for `.srt` files (root level only, non-recursive)
2. Adds all found files to `synthesis_tasks.db` database
3. Processes files sequentially (1 worker, 1 file at a time)
4. Creates `*_KevinTheAntagonizer_Notes.md` files alongside each `.srt` file
5. Uses default `sonnet-4.5` model
6. Creates log file: `runID.YYYYMMDD.HHMMSS.log`

**Files Created**:
- Notes: Same folder as `.srt` files
- Database: `synthesis_tasks.db` (current directory)
- Log: `runID.20251126.143052.log` (current directory)

**What You'll See**:
```
[SCAN FOLDERS]
   - E:\WORKSPACE.DEV.PYTHON\...Professional Full Stack Developer
[FILES FOUND]
   - Total: 15 files
   - New: 15
   - Existing notes: 0 (skipped)
[PROCESSING]
   ████████░░░░░░░░░░ 53% (8/15)
   Completed: Lecture_08_Spring_Data_JPA.srt (quality: 0.86)
```

**Next Steps**:
- Want subfolders too? → [Task 03: Include Subfolders](#task-03)
- Multiple folders? → [Task 02: Multiple Folders](#task-02)
- Speed up? → [Task 13: Parallel Workers](#task-13)
- Check progress? → [Task 09: Statistics](#task-09)

---

## <a id="task-index"></a>Task Recipes

### <a id="task-01"></a>Task 01: Process Single Folder

**When to Use**: You have one course folder to process

**Complete Command**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /path/to/course
```

**Arguments Explained**:
- `-scan /path/to/course` - Folder containing `.srt` files (**REQUIRED**)

**What Happens**:
1. Scans folder for `.srt` files (non-recursive, root level only)
2. Adds all found files to database
3. Processes sequentially (1 worker)
4. Creates notes: `*_KevinTheAntagonizer_Notes.md`
5. Skips files that already have notes (no overwrites)

**Expected Output**:
```
[SCAN FOLDERS]
   - /path/to/course
[FILES FOUND]
   - Total: 42 files
   - New: 42
   - Existing notes: 0 (skipped)
[PROCESSING]
   ████████░░░░░░░░░░ 40% (17/42)
   Completed: Lecture_17_Introduction.srt (quality: 0.86)
   Tokens: 5,234 | Time: 15s
```

**Files Created**:
- Notes: Same folder as `.srt` files (e.g., `Lecture_01_Intro_KevinTheAntagonizer_Notes.md`)
- Database: `synthesis_tasks.db` (current directory)
- Log: `runID.20251126.143052.log` (current directory)

**Common Issues**:
- ❌ "Folder does not exist" → Check path spelling, use absolute path
- ❌ "Permission denied" → Check folder read permissions
- ❌ "No .srt files found" → Verify folder contains `.srt` files, try `-recursive`

**Related Tasks**:
- Include subfolders: [Task 03](#task-03)
- Speed up processing: [Task 13](#task-13)
- Check progress: [Task 09](#task-09)

**Performance Estimates**:
- **Files**: 42 files
- **Cost**: 42 × 5k tokens avg × $3/1M tokens ≈ $0.60
- **Time**: ~40 minutes (1 worker, sequential)

---

### <a id="task-02"></a>Task 02: Process Multiple Folders

**When to Use**: You have courses in different folders

**Complete Command**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/java \
  -scan /courses/spring \
  -scan /courses/python
```

**Arguments Explained**:
- `-scan` can be **repeated** multiple times
- Each `-scan` adds another folder to process
- All files tracked in single database

**What Happens**:
1. Scans all three folder roots
2. Combines all found files into single processing queue
3. Processes all files in one run
4. All tracked in same `synthesis_tasks.db`

**Expected Output**:
```
[SCAN FOLDERS]
   - /courses/java
   - /courses/spring
   - /courses/python
[FILES FOUND]
   - Total: 89 files (java: 32, spring: 28, python: 29)
   - New: 89
   - Existing notes: 0 (skipped)
[PROCESSING]
   ██████░░░░░░░░░░░░ 33% (29/89)
```

**Use Cases**:
- Multiple related courses
- Organized folder structure
- Want single database tracking all courses

**Related Tasks**:
- Include subdirectories: [Task 03](#task-03)
- Separate databases per project: [Task 16](#task-16)

**Performance Estimates**:
- **Files**: 89 files
- **Cost**: 89 × 5k tokens avg × $3/1M tokens ≈ $1.35
- **Time**: ~90 minutes (1 worker)

---

### <a id="task-03"></a>Task 03: Include All Subfolders (Recursive)

**When to Use**: Course files are organized in subdirectories

**Complete Command**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive
```

**Arguments Explained**:
- `-scan /courses` - Top-level folder
- `-recursive` - Include ALL subdirectories at any depth

**What Happens**:
1. Scans `/courses` **and ALL subdirectories** (recursive)
2. Finds files at any depth in folder tree
3. Discovers: `/courses/java/advanced/Lecture_10.srt`
4. Without `-recursive`: Only finds `/courses/Lecture_01.srt` (root level)

**Example Folder Structure**:
```
/courses/
├── java/
│   ├── Lecture_01.srt  ✓ Found
│   └── advanced/
│       └── Lecture_10.srt  ✓ Found with -recursive
├── spring/
│   ├── basics/
│   │   └── Lecture_01.srt  ✓ Found
│   └── boot/
│       └── Lecture_05.srt  ✓ Found
└── Intro.srt  ✓ Found
```

**Without `-recursive`**:
- Only finds: `Intro.srt` (root level)
- Ignores: All subdirectory files

**With `-recursive`**:
- Finds: All 5 files at any depth

**Performance Notes**:
- Scanning 1000+ files recursively may take 30-60 seconds
- Files processed in alphabetical order
- Database tracks folder structure

**Related Tasks**:
- Multiple top-level folders: [Task 02](#task-02)
- Large libraries: [Task 19](#task-19)

---

### <a id="task-04"></a>Task 04: Resume Interrupted Work

**When to Use**: Processing was interrupted (Ctrl+C, crash, timeout)

**Complete Command**:
```bash
# Simply re-run the same command:
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive
```

**Why This Works**:
- Database tracks all files: `pending`, `processing`, `completed`, `failed`
- Already-completed files are automatically skipped
- Only pending/failed files are processed
- Progress is preserved across runs

**Alternative - Explicit Retry**:
```bash
# Retry only failed files (no -scan needed):
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed
```

**What Happens**:
```
[DATABASE CHECK]
   - Total tasks: 100
   - Completed: 67
   - Failed: 3
   - Pending: 30
[RESUMING]
   - Processing: 30 pending + 3 failed = 33 files
   - Skipping: 67 completed files
```

**Interruption Scenarios**:
1. **Ctrl+C** (KeyboardInterrupt) - Safe, progress saved, exit code 130
2. **Crash** - Last completed file saved, resume from next
3. **Rate Limiting** - Failed files marked, retry later
4. **Quality Failures** - Auto-retry up to 3 times

**Check Progress Before Resuming**:
```bash
# See what's pending
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats
```

**Related Tasks**:
- Check statistics: [Task 09](#task-09)
- Retry with better model: [Task 11](#task-11)

---

### <a id="task-05"></a>Task 05: List Available Models

**When to Use**: Want to see all Claude models you can use

**Complete Command**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py --list-models
```

**No `-scan` required** - This is an information-only command

**Expected Output**:
```
================================================================================
AVAILABLE CLAUDE MODELS
================================================================================

HAIKU Family:
  haiku           -> claude-3-haiku-20240307

OPUS Family:
  opus            -> claude-3-opus-20240229

SONNET Family:
  sonnet          -> claude-3-sonnet-20240229
  sonnet-3.5      -> claude-3-5-sonnet-20241022
  sonnet-4.5      -> claude-sonnet-4-5-20250929 (DEFAULT)

Default: sonnet-4.5

Usage: -model <alias>
================================================================================
```

**Model Details**:

| Alias | Full ID | Best For | Relative Cost |
|-------|---------|----------|---------------|
| `haiku` | claude-3-haiku-20240307 | Speed, bulk processing | $ |
| `sonnet` | claude-3-sonnet-20240229 | Balanced | $$ |
| `sonnet-3.5` | claude-3-5-sonnet-20241022 | Better than opus | $$$ |
| `sonnet-4.5` | claude-sonnet-4-5-20250929 | Latest, **DEFAULT** | $$$ |
| `opus` | claude-3-opus-20240229 | Premium quality | $$$$ |

**Dynamic Discovery**:
- Models fetched from Claude Code CLI
- New models appear automatically (no code updates)
- Falls back to static list if CLI unavailable

**Related Tasks**:
- Use premium model: [Task 06](#task-06)
- Cost-effective processing: [Task 07](#task-07)
- Two-tier strategy: [Task 08](#task-08)

**See Also**: [Decision Tree: Which Model?](#decision-model)

---

### <a id="task-06"></a>Task 06: Use Premium Model (Opus)

**When to Use**: Need highest quality for critical/complex content

**Complete Command**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/advanced-architecture \
  -model opus \
  -batch-size 5
```

**Arguments Explained**:
- `-model opus` - Use Claude 3 Opus (most capable model)
- `-batch-size 5` - Smaller batches for better quality focus

**What Happens**:
- Uses Claude 3 Opus instead of default sonnet-4.5
- Higher quality output
- Higher cost (~5x more than haiku)
- Slower processing

**When to Choose Opus**:
- ✅ Complex technical content (advanced architecture, mathematics)
- ✅ Critical documentation (production systems, security)
- ✅ Quality over cost priority
- ✅ Failed files from lower-tier models
- ❌ Bulk processing (use haiku then upgrade)
- ❌ Simple introductory content

**Cost Comparison** (100 files, 5k tokens avg):
- haiku: ~$0.25
- sonnet-4.5: ~$1.50
- opus: ~$7.50

**Performance Estimates**:
- **Files**: 100 files
- **Cost**: ~$7.50
- **Time**: ~100 minutes (sequential), ~25 minutes (4 workers)

**Related Tasks**:
- Cost-effective bulk: [Task 07](#task-07)
- Two-tier strategy: [Task 08](#task-08)
- List all models: [Task 05](#task-05)

---

### <a id="task-07"></a>Task 07: Cost-Effective Processing (Haiku)

**When to Use**: Large library, budget-conscious, willing to upgrade low-quality later

**Complete Command**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  -model haiku \
  -workers 8
```

**Arguments Explained**:
- `-model haiku` - Cheapest Claude model (~$0.25/1M tokens)
- `-workers 8` - Fast parallel processing
- `-recursive` - Include all subdirectories

**What Happens**:
- Uses Claude 3 Haiku (fastest, cheapest model)
- Processes quickly with 8 parallel workers
- Lower cost (~5x cheaper than opus)
- Quality may be lower for complex content

**Strategy - Two-Phase Approach**:

**Phase 1: Bulk with Haiku**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -model haiku \
  -workers 8
```

**Phase 2: Check Quality**
```bash
# View statistics
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats

# Find low-quality files (<0.7 score)
sqlite3 synthesis_tasks.db \
  "SELECT lecture_name, quality_score
   FROM tasks
   WHERE status='completed' AND quality_score < 0.7
   ORDER BY quality_score ASC"
```

**Phase 3: Upgrade Low-Quality**
```bash
# Reset low-quality to pending
sqlite3 synthesis_tasks.db \
  "UPDATE tasks
   SET status='pending', attempts=0
   WHERE quality_score < 0.7"

# Reprocess with opus
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus
```

**Cost Analysis** (500 files):
- All haiku: $1.25
- All opus: $37.50
- **Two-tier (haiku→opus for 10%)**: ~$5 (87% savings)

**Related Tasks**:
- Two-tier strategy: [Task 08](#task-08)
- Premium model: [Task 06](#task-06)
- Check statistics: [Task 09](#task-09)

---

### <a id="task-08"></a>Task 08: Two-Tier Quality Strategy

**When to Use**: Maximize cost efficiency while maintaining quality

**Complete Workflow**:

**Tier 1: Bulk Processing (Haiku)**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  -model haiku \
  -workers 8 \
  -db courses.db
```

Cost: ~$1.25 for 500 files

**Tier 2: Quality Checkpoint**
```bash
# View overall statistics
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats -db courses.db

# Find low-quality files
sqlite3 courses.db \
  "SELECT lecture_name, quality_score, error_message
   FROM tasks
   WHERE status='completed' AND quality_score < 0.75
   ORDER BY quality_score ASC"

# Count low-quality
sqlite3 courses.db \
  "SELECT COUNT(*)
   FROM tasks
   WHERE quality_score < 0.75"
```

**Tier 3: Selective Upgrade (Opus)**
```bash
# Reset low-quality to pending
sqlite3 courses.db \
  "UPDATE tasks
   SET status='pending', attempts=0
   WHERE quality_score < 0.75"

# Reprocess with premium model
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus \
  -workers 2 \
  -db courses.db
```

Cost: ~$3.75 for 50 files (10%)

**Total Cost Savings**:
- All haiku: $1.25 (lowest quality)
- All opus: $37.50 (highest cost)
- **Two-tier**: $5.00 (87% savings, high quality)

**Quality Threshold Guidance**:
- **0.7**: Pass threshold (5/7 checks)
- **0.75**: Recommended upgrade threshold
- **0.85+**: High quality, no upgrade needed

**When to Use Two-Tier**:
- ✅ 100+ files
- ✅ Budget constraints
- ✅ Mix of simple and complex content
- ✅ Time to run multiple passes

**Related Tasks**:
- Cost-effective: [Task 07](#task-07)
- Premium model: [Task 06](#task-06)
- Check statistics: [Task 09](#task-09)

---

### <a id="task-09"></a>Task 09: Check Progress Statistics

**When to Use**: Monitor processing progress, check quality scores

**Complete Command**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats
```

**No `-scan` required** - This is an information-only command

**Expected Output**:
```
================================================================================
DATABASE STATISTICS
================================================================================

[TASK SUMMARY]
   - Total Tasks:     523
   - Completed:       487 (93.1%)
   - Failed:          12 (2.3%)
   - Pending:         24 (4.6%)

[QUALITY METRICS]
   - Average Quality: 82.50%
   - Pass Rate:       98.8% (481/487)
   - High Quality:    75.2% (quality ≥ 0.80)

[PROCESSING STATUS]
   - Currently Running: No
   - Last Run:          2025-11-26 14:30:52
   - Total Runtime:     4h 23m

[TOKENS USED]
   - Total:           2,615,000 tokens
   - Average/File:    5,234 tokens
   - Estimated Cost:  $7.85 (sonnet-4.5)

[ERRORS]
   - Rate Limiting:   3
   - Quality Failures: 9
   - Other:           0

================================================================================
```

**What This Tells You**:
- **Progress**: 93.1% complete (487/523)
- **Quality**: Average 82.5%, most files high quality
- **Problems**: 12 failed files (2.3%)
- **Next Step**: Review failed files or retry with better model

**Related Commands**:
```bash
# View failed files with details
python KevinTheAntagonizerClaudeCodeNotesMaker.py -list-failed

# Retry failed files
python KevinTheAntagonizerClaudeCodeNotesMaker.py -retry-failed

# Custom database
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats -db custom.db
```

**Related Tasks**:
- List failures: [Task 10](#task-10)
- Retry failures: [Task 11](#task-11)
- Two-tier strategy: [Task 08](#task-08)

---

### <a id="task-10"></a>Task 10: List Failed Files

**When to Use**: See which files failed and why

**Complete Command**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py -list-failed
```

**No `-scan` required** - This is an information-only command

**Expected Output**:
```
================================================================================
FAILED TASKS
================================================================================

[FAILED FILES] (12 total)

1. Lecture_42_Advanced_Concurrency.srt
   Path: /courses/java/advanced/Lecture_42_Advanced_Concurrency.srt
   Attempts: 3/3
   Error: Quality check failed (score: 0.43) - Too short
   Last Attempt: 2025-11-26 14:25:10

2. Lecture_15_Microservices_Patterns.srt
   Path: /courses/spring/Lecture_15_Microservices_Patterns.srt
   Attempts: 3/3
   Error: Quality check failed (score: 0.57) - Missing structure
   Last Attempt: 2025-11-26 14:20:05

3. Lecture_08_Async_Programming.srt
   Path: /courses/python/Lecture_08_Async_Programming.srt
   Attempts: 2/3
   Error: Rate limit exceeded - will retry
   Last Attempt: 2025-11-26 14:15:30

[SUMMARY]
- Quality failures: 9 (upgrade model recommended)
- Rate limiting: 3 (reduce workers or wait)
- Other errors: 0

[NEXT STEPS]
- Retry with better model: -retry-failed -model opus
- Reduce workers: -retry-failed -workers 2
- Manual investigation: Check log files

================================================================================
```

**Error Categories**:

| Error Type | Cause | Solution |
|------------|-------|----------|
| Quality check failed | Output too short/poor structure | Retry with `-model opus` |
| Rate limit exceeded | Too many requests | Reduce `-workers`, wait 10 min |
| File too large | SRT file >50,000 chars | Split file or increase limit |
| CLINotFoundError | Claude Code not logged in | Run `claude-code login` |

**Related Tasks**:
- Retry failures: [Task 11](#task-11)
- Check statistics: [Task 09](#task-09)
- Common errors: [Task 20](#task-20)

---

### <a id="task-11"></a>Task 11: Retry All Failures

**When to Use**: Files failed during processing, want to retry

**Complete Command**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed
```

**No `-scan` required** - Processes failed files from database

**What Happens**:
1. Gets all failed tasks from database
2. Resets attempt counter for retry
3. Processes failed files only
4. Uses same model unless you specify `-model`

**Retry with Better Model**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus \
  -workers 2
```

**Arguments Explained**:
- `-retry-failed` - Process only failed files from database
- `-model opus` - Use premium model for better quality
- `-workers 2` - Parallel processing (reduce if rate limiting)

**Expected Output**:
```
[RETRY FAILED TASKS]
   - Failed tasks found: 12
   - Retrying with model: opus
   - Workers: 2

[PROCESSING]
   ████████████░░░░░░ 66% (8/12)
   Completed: Lecture_42_Advanced_Concurrency.srt (quality: 0.86)
   Previous attempts: 3, Current: SUCCESS
```

**Retry Strategy**:

**Low-Quality Failures** → Upgrade model:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus
```

**Rate Limiting** → Reduce workers:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -workers 1
```

**Mixed Errors** → Check logs first:
```bash
# View failures
python KevinTheAntagonizerClaudeCodeNotesMaker.py -list-failed

# Check log
tail -f runID.*.log | grep ERROR

# Retry with adjustments
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus \
  -workers 2 \
  -batch-size 5
```

**Related Tasks**:
- List failed files: [Task 10](#task-10)
- Check statistics: [Task 09](#task-09)
- Premium model: [Task 06](#task-06)

---

### <a id="task-12"></a>Task 12: Reset and Start Fresh

**When to Use**: Want to clear all tracking and reprocess everything

**Complete Command**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -reset-db \
  -scan /courses
```

**Arguments Explained**:
- `-reset-db` - **DELETES** all data from database
- `-scan /courses` - Required (what to process after reset)

**⚠️ WARNING**: This is **DESTRUCTIVE**
- Deletes `synthesis_tasks.db` completely
- Loses all progress tracking
- Loses quality scores and statistics
- Cannot be undone

**What Happens**:
1. Database file deleted: `synthesis_tasks.db`
2. New empty database created
3. Scans folders fresh
4. Processes all files (ignores existing notes if `-reset-db`)

**When to Use**:
- ✅ Testing different configurations
- ✅ Fresh start after major changes
- ✅ Database corrupted
- ❌ Just want to retry failures (use `-retry-failed` instead)
- ❌ Resume interrupted work (just re-run command)

**Backup Strategy**:
```bash
# Backup database before reset
cp synthesis_tasks.db synthesis_tasks.db.backup

# Reset and process
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -reset-db \
  -scan /courses
```

**Alternative - Manual Database Reset**:
```bash
# Delete database manually
rm synthesis_tasks.db

# Run normally (creates new database)
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses
```

**Related Tasks**:
- Resume work: [Task 04](#task-04)
- Retry failures: [Task 11](#task-11)
- Statistics: [Task 09](#task-09)

---

### <a id="task-13"></a>Task 13: Speed Up with Parallel Workers

**When to Use**: Large library, want faster processing

**Complete Command**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  -workers 4 \
  -batch-size 10
```

**Arguments Explained**:
- `-workers 4` - Process 4 files simultaneously
- `-batch-size 10` - Each worker handles 10 files per batch

**What Happens**:
- 4 parallel workers process files concurrently
- Total capacity: 4 workers × 10 files = 40 files in parallel
- Shows 5 progress bars (1 main + 4 workers)
- 4x faster throughput (if API quota allows)

**Speed Comparison** (100 files):

| Workers | Time | Best For |
|---------|------|----------|
| 1 | ~100 min | First run, verify quality |
| 2 | ~50 min | Small batches |
| 4 | ~25 min | **Recommended default** |
| 8 | ~15 min | Large libraries, fast network |

**Recommended Worker Counts**:
- **1 worker**: First time (verify quality)
- **2 workers**: Small batches (<50 files)
- **4 workers**: Normal use ⭐ **RECOMMENDED**
- **8 workers**: Large libraries (500+ files)

**When to Reduce Workers**:
- ❌ Seeing rate limit errors → Reduce to 1-2
- ❌ Many quality failures → Use 1 worker with better model
- ❌ Slow internet → Reduce to 2
- ❌ First time processing → Use 1 to verify quality

**Performance Optimization**:
```bash
# Balanced: 4 workers, moderate batches
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -workers 4 \
  -batch-size 10

# Speed: 8 workers, small batches (better error recovery)
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -workers 8 \
  -batch-size 5

# Conservative: 2 workers, larger batches
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -workers 2 \
  -batch-size 20
```

**Related Tasks**:
- Batch size optimization: [Task 14](#task-14)
- Large libraries: [Task 19](#task-19)

**See Also**: [Decision Tree: How Many Workers?](#decision-workers)

---

### <a id="task-14"></a>Task 14: Optimize Batch Size

**When to Use**: Fine-tune processing batches for your scenario

**Complete Command**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -workers 4 \
  -batch-size 5
```

**Arguments Explained**:
- `-batch-size 5` - Process 5 files per batch per worker

**What is Batch Size?**
- Files grouped into batches for processing
- After each batch: checkpoint, progress report
- Smaller batches = better error recovery
- Larger batches = fewer interruptions

**Recommended Batch Sizes**:

| Scenario | Workers | Batch Size | Rationale |
|----------|---------|------------|-----------|
| Default | 1 | 10 | Standard setting |
| Parallel | 4 | 10 | Balanced |
| High parallel | 8 | 5 | Better error recovery |
| Quality issues | Any | 5 | More focus per batch |
| Large dataset | 4-8 | 5 | Better checkpointing |

**Batch Size Trade-offs**:

**Small Batches (5)**:
- ✅ Better error recovery
- ✅ More frequent checkpoints
- ✅ Better for unstable connections
- ❌ More overhead

**Large Batches (20)**:
- ✅ Less overhead
- ✅ Faster for stable datasets
- ❌ Lose more progress on interruption
- ❌ Harder to debug failures

**Examples**:

**Conservative (best error recovery)**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -workers 4 \
  -batch-size 5
```

**Aggressive (fastest for stable)**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -workers 8 \
  -batch-size 20
```

**Related Tasks**:
- Parallel workers: [Task 13](#task-13)
- Large libraries: [Task 19](#task-19)

**See Also**: [Decision Tree: Batch Size](#decision-batch)

---

### <a id="task-15"></a>Task 15: Custom Expert Persona

**When to Use**: Want different expert voice than Kevin Burleigh

**Step 1: Create System Prompt File**:
```bash
cat > data_scientist_expert.txt << 'EOF'
You are Dr. Sarah Chen, a senior data scientist with 15 years of ML experience.

You synthesize technical lecture transcripts with focus on:
- Statistical rigor and mathematical foundations
- Practical ML pipelines and production systems
- Data quality, bias detection, and model validation
- Real-world deployment challenges and solutions

Your style:
- Precise and methodical
- Emphasize reproducibility and best practices
- Include Python/R code examples
- Highlight common pitfalls in ML projects
- Reference relevant research papers when applicable

Structure your notes with:
- Clear section headers (## and ###)
- Code examples with explanations
- Key takeaways and action items
- Cautions about data quality and bias
EOF
```

**Step 2: Process with Custom Prompt**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/machine-learning \
  -system-prompt data_scientist_expert.txt \
  -recursive
```

**Arguments Explained**:
- `-system-prompt data_scientist_expert.txt` - Overrides Kevin persona
- Uses content from file as system prompt

**What Happens**:
- Synthesis uses Dr. Chen persona instead of Kevin
- Notes reflect data science perspective
- Voice and emphasis changes completely
- Quality checks remain the same

**Example Personas**:

**Python Expert**:
```bash
cat > python_expert.txt << 'EOF'
You are a Python expert with Django and async expertise.
Focus on Pythonic code, type hints, async/await patterns.
Emphasize testing, documentation, and production-ready code.
EOF
```

**Frontend Developer**:
```bash
cat > frontend_expert.txt << 'EOF'
You are a senior frontend developer specializing in React.
Focus on component design, state management, performance.
Emphasize modern JavaScript, TypeScript, and best practices.
EOF
```

**DevOps Engineer**:
```bash
cat > devops_expert.txt << 'EOF'
You are a DevOps engineer with Kubernetes expertise.
Focus on infrastructure as code, CI/CD, monitoring.
Emphasize scalability, reliability, and automation.
EOF
```

**Use Cases**:
- ✅ Domain-specific courses (ML, frontend, DevOps)
- ✅ Multiple courses with different domains
- ✅ Need different technical perspective
- ✅ Team prefers specific voice

**Related Tasks**:
- Separate databases: [Task 16](#task-16)
- Model selection: [Task 05](#task-05)

---

### <a id="task-16"></a>Task 16: Separate Databases per Project

**When to Use**: Multiple projects, want independent tracking

**Complete Workflow**:

**Java Project**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/java \
  -db java_synthesis.db \
  -recursive
```

**Python Project**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/python \
  -db python_synthesis.db \
  -system-prompt python_expert.txt \
  -recursive
```

**ML Project**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/machine-learning \
  -db ml_synthesis.db \
  -system-prompt data_scientist.txt \
  -model opus \
  -recursive
```

**Arguments Explained**:
- `-db <project>.db` - Custom database file per project
- Each project has independent tracking

**Benefits**:
- ✅ Independent progress per project
- ✅ Different models per project
- ✅ Different personas per project
- ✅ Isolated statistics
- ✅ Easy cleanup (delete database)

**Check Project Statistics**:
```bash
# Java project stats
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -stats \
  -db java_synthesis.db

# Python project stats
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -stats \
  -db python_synthesis.db

# ML project stats
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -stats \
  -db ml_synthesis.db
```

**Retry Project Failures**:
```bash
# Retry Java failures
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -db java_synthesis.db

# Retry ML failures with better model
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus \
  -db ml_synthesis.db
```

**Project Organization**:
```
/project/
├── java_synthesis.db
├── python_synthesis.db
├── ml_synthesis.db
├── java_expert.txt
├── python_expert.txt
└── ml_expert.txt
```

**Related Tasks**:
- Custom personas: [Task 15](#task-15)
- Statistics: [Task 09](#task-09)
- Reset database: [Task 12](#task-12)

---

### <a id="task-17"></a>Task 17: Validation Before Processing (Dry Run)

**When to Use**: Test configuration before committing to long processing run

**Complete Command**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -scan /lectures \
  -recursive \
  -workers 8 \
  -batch-size 20 \
  -model sonnet-3.5 \
  --dry-run
```

**Arguments Explained**:
- `--dry-run` - **NO FILES PROCESSED**, validation only
- All other arguments validated

**What Happens**:
1. Validates all folders exist
2. Checks model availability
3. Validates numeric arguments (workers, batch-size)
4. Shows configuration summary
5. **Exits without processing** (exit code 0)

**Expected Output**:
```
================================================================================
DRY RUN MODE - Configuration Validation
================================================================================

[SCAN FOLDERS]
   ✓ /courses (exists, readable)
   ✓ /lectures (exists, readable)

[PROCESSING OPTIONS]
   - Recursive:   True
   - Workers:     8
   - Batch Size:  20
   - Model:       sonnet-3.5 (claude-3-5-sonnet-20241022)

[DATABASE]
   - Path:        synthesis_tasks.db (will be created)
   - Reset:       False

[VALIDATION]
   ✓ All folders exist and readable
   ✓ Model available
   ✓ Arguments valid
   ✓ Claude Code CLI logged in

*** DRY RUN MODE - No files will be processed ***

To run for real, remove --dry-run flag

Exit Code: 0
================================================================================
```

**Validation Errors Example**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /nonexistent \
  --dry-run
```

Output:
```
[ERROR] Scan folder does not exist: /nonexistent

Exit Code: 1
```

**Use Cases**:
- ✅ Testing complex configurations
- ✅ Verify folders before overnight run
- ✅ Check model availability
- ✅ Validate permissions

**Related Tasks**:
- Parallel workers: [Task 13](#task-13)
- Model selection: [Task 05](#task-05)

---

### <a id="task-18"></a>Task 18: Monitor Progress in Real-Time

**When to Use**: Long-running processing, want live monitoring

**Setup - Multiple Terminals**:

**Terminal 1: Run Processing**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  -workers 4
```

**Terminal 2: Monitor Logs**
```bash
# Watch log file in real-time
tail -f runID.*.log

# Filter for completions only
tail -f runID.*.log | grep "Completed:"

# Filter for errors
tail -f runID.*.log | grep "ERROR"

# Show quality scores
tail -f runID.*.log | grep "quality:"
```

**Terminal 3: Watch Database Stats**
```bash
# Update every 2 seconds
watch -n 2 'python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats'

# Or with SQL directly
watch -n 2 'sqlite3 synthesis_tasks.db "SELECT status, COUNT(*) FROM tasks GROUP BY status"'
```

**Terminal 4: Monitor System Resources**
```bash
# CPU and memory usage
htop

# Network usage
iftop

# Disk I/O
iotop
```

**Single Terminal - Combined View**:
```bash
# Process in background
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -workers 4 &

# Monitor log
tail -f runID.*.log | grep -E "Completed|ERROR|quality"
```

**PowerShell (Windows)**:
```powershell
# Terminal 1: Run processing
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan E:\courses -workers 4

# Terminal 2: Monitor log
Get-Content runID.*.log -Wait -Tail 20

# Terminal 3: Watch stats every 5 seconds
while ($true) { cls; python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats; Start-Sleep 5 }
```

**Monitoring Metrics**:

**Progress Rate**:
```bash
# Count completed per minute
watch -n 60 'sqlite3 synthesis_tasks.db "SELECT COUNT(*) FROM tasks WHERE status='\''completed'\''"'
```

**Quality Distribution**:
```bash
# View quality score distribution
sqlite3 synthesis_tasks.db \
  "SELECT
    CASE
      WHEN quality_score >= 0.9 THEN 'Excellent (0.9+)'
      WHEN quality_score >= 0.8 THEN 'Good (0.8-0.9)'
      WHEN quality_score >= 0.7 THEN 'Acceptable (0.7-0.8)'
      ELSE 'Low (<0.7)'
    END as quality_tier,
    COUNT(*) as count
   FROM tasks
   WHERE status='completed'
   GROUP BY quality_tier"
```

**Related Tasks**:
- Check statistics: [Task 09](#task-09)
- Large libraries: [Task 19](#task-19)

---

### <a id="task-19"></a>Task 19: Handle Large Libraries (500+ files)

**When to Use**: Processing hundreds or thousands of files

**Recommended Strategy** (4 phases):

**Phase 1: Start Conservative**
```bash
# Test with first section
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /library/section-1 \
  -workers 4 \
  -db library.db
```

Wait for 10-20 files to complete, check quality and speed

**Phase 2: Monitor and Validate**
```bash
# Check stats frequently
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats -db library.db

# Watch in real-time (Terminal 2)
watch -n 30 'python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats -db library.db'

# Check for rate limiting
tail -f runID.*.log | grep -i "rate\|limit"
```

**Phase 3: Scale Up If Stable**
```bash
# Increase workers if no issues
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /library/section-2 \
  -scan /library/section-3 \
  -workers 8 \
  -batch-size 5 \
  -db library.db
```

**Phase 4: Handle Failures**
```bash
# After main processing, retry failures with better model
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus \
  -workers 2 \
  -db library.db
```

**Large Library Best Practices**:

**1. Use Smaller Batches**
```bash
-workers 8 -batch-size 5  # Better than -workers 8 -batch-size 20
```
- Better error recovery
- Less progress lost on interruption
- Easier debugging

**2. Monitor Rate Limits**
```bash
# Watch for rate limit warnings
tail -f runID.*.log | grep -i rate
```
If seen → Reduce workers immediately

**3. Progressive Scaling**
```
Start: 1 worker (verify)
 ↓ (if stable)
Scale: 4 workers (recommended)
 ↓ (if still stable)
Max: 8 workers (large libraries)
```

**4. Use Custom Database**
```bash
-db large_library.db
```
- Isolate from other projects
- Easier to manage
- Can delete if needed to restart

**5. Two-Tier Strategy for Cost**
```bash
# Phase 1: Bulk with haiku (cheap)
python ... -model haiku -workers 8

# Phase 2: Upgrade low-quality with opus
python ... -retry-failed -model opus
```

**Expected Timeline** (500 files, 5k tokens avg):

| Configuration | Time | Cost (est) |
|---------------|------|------------|
| 1 worker, sonnet-4.5 | 6-8 hours | $7.50 |
| 4 workers, sonnet-4.5 | 1.5-2 hours | $7.50 |
| 8 workers, sonnet-4.5 | 45-60 min | $7.50 |
| 8 workers, haiku | 30-40 min | $1.25 |
| Two-tier (haiku→opus 10%) | 45-60 min | $5.00 |

**Overnight Processing**:
```bash
# Start before bed
nohup python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /library \
  -recursive \
  -workers 4 \
  -db library.db \
  > overnight.log 2>&1 &

# Check in morning
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats -db library.db
```

**Related Tasks**:
- Parallel workers: [Task 13](#task-13)
- Monitor progress: [Task 18](#task-18)
- Two-tier strategy: [Task 08](#task-08)

---

### <a id="task-20"></a>Task 20: Common Errors and Solutions

**Error 1: Claude Code CLI Not Found**

**Error Message**:
```
CLINotFoundError: Claude Code CLI not found or not logged in
```

**Solution**:
```bash
# Install CLI
npm install -g @anthropic-ai/claude-code

# Login
claude-code login

# Verify
claude-code whoami
```

---

**Error 2: Scan Folder Doesn't Exist**

**Error Message**:
```
[ERROR] Scan folder does not exist: /typo/path
```

**Solutions**:
1. Check spelling:
```bash
# Use tab completion
python ... -scan /cours[TAB]
```

2. Use absolute paths:
```bash
# Instead of: -scan ../courses
# Use: -scan /full/path/to/courses
```

3. Verify folder:
```bash
ls -la /path/to/folder
```

---

**Error 3: Rate Limiting**

**Error Message**:
```
Error: Rate limit exceeded - too many requests
```

**Solutions**:
1. Reduce workers:
```bash
# From: -workers 8
# To: -workers 2
```

2. Wait 10 minutes, then resume:
```bash
# Just re-run same command
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses
```

3. Use smaller batches:
```bash
-workers 2 -batch-size 5
```

---

**Error 4: Quality Check Failures**

**Error Message**:
```
Quality check failed (score: 0.43) - Too short
```

**Solutions**:
1. Retry with better model:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus
```

2. Check if transcript is valid:
```bash
# View .srt file
head -50 path/to/file.srt

# Check file size
ls -lh path/to/file.srt
```

3. Reduce batch size for more focus:
```bash
-retry-failed -model opus -batch-size 5
```

---

**Error 5: Model Not Available**

**Error Message**:
```
[ERROR] Model 'gpt-4' not available
```

**Solution**:
```bash
# List valid models
python KevinTheAntagonizerClaudeCodeNotesMaker.py --list-models

# Use valid alias
python ... -model sonnet-4.5
```

---

**Error 6: Permission Denied**

**Error Message**:
```
[ERROR] Cannot read directory: /courses
```

**Solutions**:
1. Check folder permissions:
```bash
ls -la /courses
```

2. Run with proper permissions:
```bash
# Linux/Mac
sudo python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /courses

# Windows (run as Administrator)
```

3. Change folder permissions:
```bash
chmod -R 755 /courses
```

---

**Error 7: File Too Large**

**Error Message**:
```
Too large (52,000 chars) - exceeds MAX_FILE_SIZE
```

**Solutions**:
1. Split large file manually
2. Increase limit in code:
```python
# Edit Config.MAX_FILE_SIZE in source
```

3. Skip problematic file, process others

---

**Error 8: Database Locked**

**Error Message**:
```
sqlite3.OperationalError: database is locked
```

**Solutions**:
1. Check for other running instances:
```bash
ps aux | grep KevinTheAntagonizer
kill <pid>
```

2. Wait and retry:
```bash
# Wait 30 seconds
sleep 30
python ... -scan /courses
```

3. Use different database:
```bash
-db new_synthesis.db
```

---

**Error 9: Out of Memory**

**Symptoms**:
- Process killed
- System slowdown
- Swap usage high

**Solutions**:
1. Reduce workers:
```bash
-workers 2  # Instead of 8
```

2. Process in smaller batches:
```bash
# Instead of all at once:
python ... -scan /courses/section-1
# Then:
python ... -scan /courses/section-2
```

3. Close other applications

---

**Error 10: Network Timeout**

**Error Message**:
```
ProcessError: Connection timeout
```

**Solutions**:
1. Check internet connection
2. Reduce workers:
```bash
-workers 1  # More reliable on slow connection
```

3. Retry (progress saved):
```bash
# Just re-run
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /courses
```

---

**Getting Help**:

1. **Check logs**:
```bash
tail -100 runID.*.log
```

2. **View database**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats
python KevinTheAntagonizerClaudeCodeNotesMaker.py -list-failed
```

3. **Dry run to validate**:
```bash
python ... -scan /courses --dry-run
```

4. **Start small**:
```bash
# Test with 1 file first
python ... -scan /test-folder
```

---

## <a id="decision-workers"></a>Decision Tree: How Many Workers Should I Use?

```
START: How many .srt files total?
├─ < 20 files → 1 worker (not worth parallelizing)
├─ 20-100 files → Continue below
├─ 100-500 files → Continue below
└─ 500+ files → Continue below

Internet speed?
├─ Slow (<10 Mbps) → workers = 1-2
├─ Medium (10-50 Mbps) → workers = 2-4
└─ Fast (>50 Mbps) → Continue below

Have you processed before with this setup?
├─ First time → workers = 1 (verify quality first!)
└─ Know it works → Continue below

Seeing rate limit errors?
├─ YES → workers = 1-2 IMMEDIATELY (reduce load)
└─ NO → Continue below

RECOMMENDATION:
┌─────────────────────────────────────────┐
│ First run:        1 worker              │
│ Small batch:      2 workers             │
│ Normal use:       4 workers ⭐ DEFAULT  │
│ Large library:    8 workers             │
│ Rate limited:     1-2 workers           │
└─────────────────────────────────────────┘

VALIDATION STEPS:
1. Start with 1 worker (verify quality)
2. Check stats after 10-20 files
3. If quality good → Scale to 4 workers
4. Monitor for rate limits
5. Adjust as needed
```

**Worker Count by Use Case**:

| Use Case | Workers | Rationale |
|----------|---------|-----------|
| **First time** | **1** | Verify quality, understand process |
| Testing config | 2 | Safe exploration |
| **Normal use** | **4** | **⭐ RECOMMENDED** - Best balance |
| Large libraries (500+) | 8 | Max throughput |
| Rate limited | 1-2 | Avoid API quota issues |
| Slow internet | 1-2 | Better reliability |
| Quality failures | 1 | More focus per file |

**Signs You Need to Reduce Workers**:
- ❌ "Rate limit exceeded" errors
- ❌ High quality failure rate (>10%)
- ❌ Network timeouts
- ❌ System slowdown/high CPU
- ❌ Many incomplete files

**Signs You Can Increase Workers**:
- ✅ No rate limit warnings
- ✅ High quality scores (>0.80 avg)
- ✅ Fast internet connection
- ✅ Low system resource usage
- ✅ Stable processing

**Test Incrementally**:
```bash
# Start conservative
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses -workers 2

# Monitor for rate limits
tail -f runID.*.log | grep -i "rate\|limit"

# If clean after 20+ files, increase
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses -workers 4

# Continue increasing until you find sweet spot
```

---

## <a id="decision-model"></a>Decision Tree: Which Model Should I Choose?

```
What's your priority?
├─ 💰 COST → haiku (cheapest, ~$0.25/100 files)
├─ ⚡ SPEED → haiku + workers 8
├─ 🏆 QUALITY → opus (best, ~$7.50/100 files)
└─ 🎯 BALANCED → sonnet-4.5 ⭐ DEFAULT (~$1.50/100 files)

Budget constraints?
├─ Tight ($) → Two-tier: haiku bulk, upgrade low-quality to opus
├─ Moderate ($$) → sonnet-4.5 for everything
└─ No limit ($$$) → opus for everything

Content complexity?
├─ Simple (intros, overviews) → haiku or sonnet
├─ Moderate (typical lectures) → sonnet-4.5
└─ Complex (advanced architecture, math, theory) → opus

RECOMMENDATION BY SCENARIO:
┌──────────────────────────────────────────────────┐
│ First processing:    sonnet-4.5 (default)       │
│ Budget mode:         haiku (bulk processing)     │
│ Premium quality:     opus (critical content)     │
│ Cost-optimized:      Two-tier (haiku → opus)    │
│ Failed retries:      Upgrade model (opus)       │
└──────────────────────────────────────────────────┘
```

**Model Comparison Matrix**:

| Model | Speed | Quality | Cost/100 files | Best For |
|-------|-------|---------|----------------|----------|
| **haiku** | ⚡⚡⚡⚡⚡ | ⭐⭐ | ~$0.25 | Bulk processing, simple content |
| **sonnet** | ⚡⚡⚡⚡ | ⭐⭐⭐ | ~$0.75 | Balanced option |
| **sonnet-3.5** | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | ~$1.50 | Alternative to opus |
| **sonnet-4.5** | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | ~$1.50 | **⭐ DEFAULT - Best balance** |
| **opus** | ⚡⚡ | ⭐⭐⭐⭐⭐ | ~$7.50 | Premium quality, complex content |

*(Estimates based on 5k tokens avg per file)*

**Cost Optimization Strategy - Two-Tier**:

```bash
# Phase 1: Bulk with haiku (cheap)
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses -model haiku -workers 8

# Phase 2: Check quality
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats

# Find low-quality (<0.75)
sqlite3 synthesis_tasks.db \
  "SELECT COUNT(*) FROM tasks WHERE quality_score < 0.75"

# Phase 3: Upgrade low-quality with opus
sqlite3 synthesis_tasks.db \
  "UPDATE tasks SET status='pending' WHERE quality_score < 0.75"

python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed -model opus
```

**Cost Analysis** (500 files):
- All haiku: $1.25 (lowest quality)
- All sonnet-4.5: $7.50 (good quality)
- All opus: $37.50 (highest quality)
- **Two-tier (haiku → opus 10%)**: $5.00 ⭐ **(87% savings vs all-opus)**

**When to Upgrade Model**:
- Quality score < 0.7 (failed threshold)
- Complex technical content
- Failed with lower model
- Critical documentation
- Customer-facing content

---

## <a id="decision-batch"></a>Decision Tree: Batch Size Optimization

```
How many workers?
├─ 1 worker → batch-size = 10 (default is fine)
├─ 2-4 workers → batch-size = 10 (balanced)
├─ 4-8 workers → batch-size = 5 (smaller batches, better recovery)
└─ 8+ workers → batch-size = 5 (critical for error recovery)

Seeing quality failures?
├─ YES → Reduce to batch-size = 5 (more focus per batch)
└─ NO → Keep default 10

Large dataset (500+ files)?
├─ YES → batch-size = 5 (better checkpointing)
└─ NO → batch-size = 10 (standard)

Unstable connection?
├─ YES → batch-size = 5 (less progress lost)
└─ NO → batch-size = 10

RECOMMENDATION:
┌────────────────────────────────────────┐
│ Default:           batch-size = 10     │
│ High workers (8+): batch-size = 5      │
│ Quality issues:    batch-size = 5      │
│ Stable + fast:     batch-size = 20     │
└────────────────────────────────────────┘
```

**Batch Size Trade-offs**:

| Batch Size | Error Recovery | Overhead | Best For |
|------------|----------------|----------|----------|
| **5** | ✅ Excellent | ❌ Higher | High workers, unstable, quality issues |
| **10** | ✅ Good | ✅ Balanced | **⭐ RECOMMENDED - Default** |
| **20** | ❌ Poor | ✅ Lower | Stable datasets, low workers |

**Batch Size Effects**:

**Small Batches (5)**:
- ✅ Lose less progress on interruption
- ✅ More frequent checkpoints
- ✅ Easier to debug failures
- ✅ Better for unstable connections
- ❌ More overhead (batch setup/teardown)
- ❌ More log messages

**Large Batches (20)**:
- ✅ Less overhead
- ✅ Faster for stable, simple datasets
- ✅ Fewer log interruptions
- ❌ Lose more progress on crash
- ❌ Harder to identify problem files
- ❌ Less frequent checkpoints

**Recommended Combinations**:

| Workers | Batch Size | Use Case |
|---------|------------|----------|
| 1 | 10 | Standard sequential |
| 2 | 10 | Small parallel |
| 4 | 10 | **⭐ RECOMMENDED** |
| 4 | 5 | Quality-focused |
| 8 | 5 | Large library, parallel |
| 8 | 20 | Very stable, fast |

---

## <a id="templates"></a>Quick Command Templates

### Copy-Paste Ready Examples

**Basic Processing**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /path/to/course
```

**User's Real-World Example**:
```bash
cd "E:\WORKSPACE.DEV.PYTHON\AIML.Agents\KevinTheAntagonizerClaudeCodeNotesMaker" && \
.\.venv\scripts\activate.ps1 && \
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan "E:\WORKSPACE.DEV.PYTHON\AIML.Agents\KevinTheAntagonizerClaudeCodeNotesMaker\__Black Men - Amigoscode - Professional Full Stack Developer" \
  -recursive \
  -workers 5 \
  -batch-size 10 \
  -retry-failed
```
*What this does*: Activates venv, processes folder recursively with 5 workers, batches of 10, AND retries any previous failures

---

**Multi-Folder Recursive**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/java \
  -scan /courses/spring \
  -scan /courses/python \
  -recursive
```

**Recommended Production Setup**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  -workers 4 \
  -batch-size 10
```

**Information Commands (No Processing)**:
```bash
# Check statistics
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats

# List models
python KevinTheAntagonizerClaudeCodeNotesMaker.py --list-models

# Show failures
python KevinTheAntagonizerClaudeCodeNotesMaker.py -list-failed
```

**Retry with Upgrade**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus \
  -workers 2
```

**Two-Tier Cost Optimization**:
```bash
# Phase 1: Bulk with haiku (cheap)
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  -model haiku \
  -workers 8

# Phase 2: Check stats
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats

# Phase 3: Find and upgrade low-quality
sqlite3 synthesis_tasks.db \
  "UPDATE tasks SET status='pending' WHERE quality_score < 0.7"

python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus
```

**Premium Quality from Start**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/advanced \
  -model opus \
  -batch-size 5 \
  -recursive
```

**Dry Run Validation**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  -workers 4 \
  --dry-run
```

**Custom Expert Persona**:
```bash
# Create persona file
cat > ml_expert.txt << 'EOF'
You are a machine learning expert.
Focus on statistical methods, model validation, and production ML.
EOF

# Process with custom persona
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/ml \
  -system-prompt ml_expert.txt \
  -recursive
```

**Separate Projects**:
```bash
# Java project
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/java \
  -db java.db \
  -recursive

# Python project
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/python \
  -db python.db \
  -system-prompt python_expert.txt \
  -recursive
```

**Large Library (500+ files)**:
```bash
# Conservative start
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /large-library \
  -recursive \
  -workers 4 \
  -batch-size 5 \
  -db large.db

# Monitor progress
watch -n 30 'python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats -db large.db'

# Scale up if stable
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /large-library \
  -workers 8 \
  -batch-size 5 \
  -db large.db
```

**Overnight Processing**:
```bash
# Linux/Mac
nohup python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  -workers 4 \
  > overnight.log 2>&1 &

# Check morning
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats
```

---

## <a id="combinations"></a>Common Argument Combinations

### By Purpose

**Speed-Focused** (finish fast):
```bash
-model haiku -workers 8 -batch-size 10
```

**Quality-Focused** (best output):
```bash
-model opus -batch-size 5 -workers 2
```

**Cost-Focused** (cheapest):
```bash
-model haiku -workers 8
# Then upgrade low-quality with opus
```

**Balanced** (recommended):
```bash
-model sonnet-4.5 -workers 4 -batch-size 10
```

**Error-Recovery** (unstable setup):
```bash
-workers 2 -batch-size 5
```

**First-Time** (verify setup):
```bash
-workers 1 --dry-run
# Then without --dry-run
```

---

### Valid Combinations Matrix

| Primary | Can Combine With | Notes |
|---------|------------------|-------|
| `-scan` | `-recursive`, `-workers`, `-batch-size`, `-model`, `-db`, `-system-prompt`, `--dry-run` | Most versatile |
| `-retry-failed` | `-workers`, `-batch-size`, `-model`, `-db` | NO `-scan` needed |
| `-stats` | `-db` | Information only, NO processing |
| `-list-failed` | `-db` | Information only, NO processing |
| `--list-models` | None | Information only, standalone |
| `-reset-db` | `-scan` | **DESTRUCTIVE** - requires `-scan` |
| `--dry-run` | All processing args | Validation only, NO processing |

---

**End of USAGE_GUIDE.md**

For detailed argument specifications, error catalogs, and database reference, see:
- **[ARGUMENT_REFERENCE.md](ARGUMENT_REFERENCE.md)** - Complete argument encyclopedia
- **[USAGE.md](USAGE.md)** - Comprehensive technical reference
- **[README.md](README.md)** - Project overview and installation

---

**Questions? Issues?**
- Check logs: `tail -100 runID.*.log`
- Validate setup: `python KevinTheAntagonizerClaudeCodeNotesMaker.py --dry-run -scan /test`
- Test incrementally: Start with 1 folder, 1 worker, verify quality, then scale

