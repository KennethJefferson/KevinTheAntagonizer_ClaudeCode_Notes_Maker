# KevinTheAntagonizerClaudeCodeNotesMaker - Comprehensive Usage Guide

**Version**: 2.0 (Single-File Architecture)
**Last Updated**: November 2025

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Command-Line Interface](#command-line-interface)
4. [Basic Usage Examples](#basic-usage-examples)
5. [Advanced Usage](#advanced-usage)
6. [Database Management](#database-management)
7. [Progress Monitoring](#progress-monitoring)
8. [Understanding Output](#understanding-output)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)
11. [Performance Tuning](#performance-tuning)
12. [Changelog](#changelog)

---

## Overview

KevinTheAntagonizerClaudeCodeNotesMaker is a CLI-based application that transforms technical course transcripts (.srt files) into comprehensive, expert-level markdown notes using the Claude Agent SDK. The notes are written in the distinctive style of "Kevin Burleigh" - a battle-tested Java/Spring Boot architect with opinionated, practical insights.

**Architecture**: Version 2.0 is a **single-file application** (1031 lines) with all CLI parsing, database management, and synthesis logic integrated into one self-contained Python file for simplicity and portability.

### Key Features

- **Single-File Design**: Everything in one self-contained Python file (no separate modules)
- **Integrated CLI**: Full command-line interface with argparse built-in
- **Parallel Processing**: Process multiple transcripts simultaneously with configurable workers
- **Batch Processing**: Handle files in batches to optimize API usage
- **Progress Tracking**: Real-time progress bars for each worker
- **Database Persistence**: SQLite-based task tracking and retry logic
- **Flexible Scanning**: Recursive or non-recursive folder scanning
- **Model Selection**: Choose from 5 different Claude models
- **Custom System Prompts**: Override default Kevin persona
- **Comprehensive Logging**: Automatic timestamped log files

---

## Installation

### Prerequisites

1. **Python 3.7+**
2. **Node.js and npm** (for Claude Code CLI)
3. **Claude Code account**

### Step-by-Step Installation

```bash
# 1. Install Claude Code CLI (required by SDK)
npm install -g @anthropic-ai/claude-code

# 2. Login to Claude Code
claude-code login
# This opens your browser for authentication

# 3. Verify login
claude-code whoami

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Verify SDK installation
python -c "import claude_agent_sdk; print('SDK ready')"
```

### Verify Installation

```bash
# Test the CLI
python KevinTheAntagonizerClaudeCodeNotesMaker.py -h
```

You should see the help message with all available arguments.

---

## Command-Line Interface

### Syntax

```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan <folder> [-scan <folder> ...] \
  [options]
```

### Required Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `-scan <folder>` | Folder to scan for .srt files (repeatable) | `-scan /courses/java` |

### Processing Options

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `-recursive` | Flag | `false` | Scan subfolders recursively |
| `-workers <num>` | Integer | `1` | Number of parallel workers/subagents |
| `-batch-size <num>` | Integer | `10` | Files per batch/subagent |

### Database Management

| Argument | Description |
|----------|-------------|
| `-db <path>` | Custom database path (default: `synthesis_tasks.db`) |
| `-reset-db` | Clear database and start fresh |
| `-list-failed` | Show failed tasks and exit |
| `-retry-failed` | Retry all failed tasks from database |
| `-stats` | Show database statistics and exit |

### Advanced Options

| Argument | Description |
|----------|-------------|
| `-system-prompt <file>` | Use custom system prompt from file |
| `-model <name>` | Claude model selection (see [Models](#available-models)) |
| `--dry-run` | Validate configuration without processing files |

### Available Models

| Model Name | Model ID | Description | Use Case |
|------------|----------|-------------|----------|
| `sonnet-4.5` | `claude-sonnet-4-5-20250929` | **DEFAULT** - Latest and best | Recommended for all use cases |
| `sonnet-3.5` | `claude-3-5-sonnet-20241022` | Better than 3-opus | Alternative to 4.5 |
| `opus` | `claude-3-opus-20240229` | Most capable (expensive) | Premium quality |
| `sonnet` | `claude-3-sonnet-20240229` | Balanced performance | Cost-effective |
| `haiku` | `claude-3-haiku-20240307` | Fast and cheap | Budget option |

### Automatic Features

These features are **always enabled**:

- **Progress Bars**: 1 per worker, showing real-time processing status
- **Log File**: `runID.YYYYMMDD.HHMMSS.log` created in script directory
- **Database Tracking**: All tasks tracked in SQLite database

---

## Basic Usage Examples

### Example 1: Single Folder, Sequential Processing

Process a single course folder without subfolders:

```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /path/to/java-course
```

**What happens:**
- Scans only `/path/to/java-course` (no subfolders)
- Finds all `.srt` files
- Processes sequentially (1 worker)
- Processes in batches of 10 files
- Uses default model (sonnet-4.5)
- Creates database: `synthesis_tasks.db`
- Creates log: `runID.20251122.143022.log`

### Example 2: Multiple Folders, Recursive Scan

Process multiple course directories including all subdirectories:

```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/java \
  -scan /courses/spring \
  -scan /courses/microservices \
  -recursive
```

**What happens:**
- Scans all three folders recursively
- Finds `.srt` files in all subdirectories
- Processes sequentially (1 worker)
- Processes in batches of 10 files

### Example 3: Parallel Processing with Custom Batch Size

Process with 4 parallel workers and smaller batches:

```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  -workers 4 \
  -batch-size 5
```

**What happens:**
- Scans `/courses` and all subdirectories
- Launches 4 parallel workers (4 subagents)
- Each worker processes 5 files per batch
- Shows 4 progress bars (one per worker)
- 4x faster processing (if you have sufficient API quota)

### Example 4: Custom Model and System Prompt

Use a specific model with custom persona:

```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -model opus \
  -system-prompt custom_expert.txt
```

**What happens:**
- Uses Claude 3 Opus model (premium quality)
- Loads system prompt from `custom_expert.txt`
- Processes files with custom persona instead of Kevin

### Example 5: Dry Run Validation

Test your configuration without processing files:

```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/java \
  -scan /courses/spring \
  -recursive \
  -workers 4 \
  --dry-run
```

**What happens:**
- Validates all folders exist
- Checks configuration
- Prints configuration summary
- **Does NOT process any files**
- Useful for testing before large batch runs

---

## Advanced Usage

### Scenario 1: Large Course Library Processing

Process 500+ transcript files across multiple courses:

```bash
# Phase 1: Initial scan and setup
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /massive-course-library \
  -recursive \
  -workers 8 \
  -batch-size 5 \
  -db large_library.db
```

**Explanation:**
- 8 workers for maximum throughput
- Smaller batch size (5) for better error recovery
- Custom database name for this project
- Recursive scan finds all nested courses

### Scenario 2: Resume Interrupted Processing

Your process was interrupted (network issue, system restart, etc.):

```bash
# Check current status
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats

# Resume processing (uses existing database)
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -workers 4
```

**What happens:**
- Database tracks completed/failed/pending files
- Only processes pending files
- Skips already completed files

### Scenario 3: Retry Failed Files

Some files failed due to errors:

```bash
# View failed files
python KevinTheAntagonizerClaudeCodeNotesMaker.py -list-failed

# Retry all failed files with more workers
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -workers 2
```

### Scenario 4: Reset and Start Fresh

Clear all progress and start over:

```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -reset-db \
  -scan /courses \
  -workers 4
```

**⚠️ WARNING**: This deletes ALL tracking data. Use with caution.

### Scenario 5: Custom Database for Different Projects

Separate different course collections:

```bash
# Java courses
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /java-courses \
  -db java_courses.db \
  -workers 4

# Python courses (separate database)
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /python-courses \
  -db python_courses.db \
  -workers 4
```

---

## Database Management

### Database Schema

The SQLite database (`synthesis_tasks.db`) tracks:

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    srt_path TEXT UNIQUE NOT NULL,
    lecture_name TEXT NOT NULL,
    course_folder TEXT NOT NULL,
    status TEXT NOT NULL,  -- 'pending', 'processing', 'completed', 'failed'
    attempts INTEGER DEFAULT 0,
    quality_score REAL,
    tokens_used INTEGER,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Viewing Statistics

```bash
# Quick stats via CLI
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats
```

Output:
```
[DATABASE STATISTICS]
   - Total Tasks:     523
   - Completed:       487 (93%)
   - Failed:          12 (2%)
   - Pending:         24 (5%)
   - Processing:      0 (0%)
```

### Manual Database Queries

Using `sqlite3` command-line tool:

```bash
# Total files by status
sqlite3 synthesis_tasks.db \
  "SELECT status, COUNT(*) FROM tasks GROUP BY status"

# Average quality score
sqlite3 synthesis_tasks.db \
  "SELECT AVG(quality_score) FROM tasks WHERE status='completed'"

# Failed files with error messages
sqlite3 synthesis_tasks.db \
  "SELECT lecture_name, error_message FROM tasks WHERE status='failed'"

# Top 10 longest transcripts (by tokens)
sqlite3 synthesis_tasks.db \
  "SELECT lecture_name, tokens_used FROM tasks ORDER BY tokens_used DESC LIMIT 10"

# Files with low quality scores
sqlite3 synthesis_tasks.db \
  "SELECT lecture_name, quality_score FROM tasks WHERE quality_score < 0.7"
```

### Advanced Database Operations

#### Reset Failed Files for Retry

```sql
-- Reset all failed files to pending
sqlite3 synthesis_tasks.db \
  "UPDATE tasks SET status='pending', attempts=0 WHERE status='failed'"
```

#### Delete Specific Course from Database

```sql
-- Remove all tasks from a specific course
sqlite3 synthesis_tasks.db \
  "DELETE FROM tasks WHERE course_folder LIKE '%/UnwantedCourse/%'"
```

#### Export Statistics to CSV

```bash
# Export all completed tasks
sqlite3 -header -csv synthesis_tasks.db \
  "SELECT * FROM tasks WHERE status='completed'" > completed_tasks.csv

# Export summary statistics
sqlite3 -header -csv synthesis_tasks.db \
  "SELECT course_folder, COUNT(*) as total, AVG(quality_score) as avg_quality
   FROM tasks
   GROUP BY course_folder" > course_statistics.csv
```

---

## Progress Monitoring

### Understanding Progress Bars

The application displays **one progress bar per worker**:

```
Worker 1: |████████████████░░░░| 80% (8/10) Lecture_42_Spring_Boot.srt
Worker 2: |██████████░░░░░░░░░░| 50% (5/10) Lecture_15_Dependency_Injection.srt
Worker 3: |████████████████████| 100% (10/10) Batch Complete
Worker 4: |████░░░░░░░░░░░░░░░░| 20% (2/10) Lecture_07_REST_APIs.srt
```

### Progress Bar Elements

- **Bar**: Visual representation of batch progress
- **Percentage**: Completion percentage for current batch
- **Counter**: `(current/total)` files in current batch
- **Current File**: Name of file being processed

### Log File Monitoring

Real-time log monitoring using `tail`:

```bash
# Monitor latest log file
tail -f runID.*.log

# Monitor with grep for errors
tail -f runID.*.log | grep ERROR

# Monitor with grep for completed files
tail -f runID.*.log | grep "Completed:"
```

### Log File Format

```
2025-11-22 14:30:22 - INFO - [WORKER 1] Starting batch 1 (10 files)
2025-11-22 14:30:25 - INFO - [WORKER 1] Processing: Lecture_01_Introduction.srt
2025-11-22 14:30:58 - INFO - [WORKER 1] Completed: Lecture_01_Introduction.srt (Quality: 0.86)
2025-11-22 14:31:02 - INFO - [WORKER 1] Processing: Lecture_02_Setup.srt
2025-11-22 14:31:15 - ERROR - [WORKER 1] Failed: Lecture_02_Setup.srt (Attempt 1/3)
2025-11-22 14:31:18 - INFO - [WORKER 1] Retrying: Lecture_02_Setup.srt (Attempt 2/3)
```

### Real-Time Statistics

While processing is running, you can query the database in a separate terminal:

```bash
# Watch statistics update every 2 seconds
watch -n 2 'sqlite3 synthesis_tasks.db "SELECT status, COUNT(*) FROM tasks GROUP BY status"'
```

---

## Understanding Output

### Output File Naming

For each input `.srt` file, the application creates:

```
Input:  Lecture_42_Spring_Boot_Dependency_Injection.srt
Output: Lecture_42_Spring_Boot_Dependency_Injection_KevinTheAntagonizer_Notes.md
```

### Output File Location

Notes are saved **alongside the original .srt file**:

```
/courses/spring-boot/
├── Lecture_01_Introduction.srt
├── Lecture_01_Introduction_KevinTheAntagonizer_Notes.md  ← Created here
├── Lecture_02_Setup.srt
├── Lecture_02_Setup_KevinTheAntagonizer_Notes.md         ← Created here
└── ...
```

### Output File Structure

Each markdown file contains:

```markdown
# [Lecture Title]

## Section 1: [Topic]

[Expert commentary and insights]

### Key Concepts

- **Concept 1**: [Detailed explanation]
- **Concept 2**: [Detailed explanation]

### Code Examples

```java
// Production-ready example with gotchas
@Service
public class UserService {
    // Kevin's commentary on best practices
}
```

### Real-World Gotchas

- ⚠️ **Gotcha 1**: [Warning and solution]
- ⚠️ **Gotcha 2**: [Warning and solution]

## Section 2: [Next Topic]

[... continues ...]
```

### Quality Standards

Every output is validated against 7 criteria:

1. ✅ **Length**: Minimum 1500 characters
2. ✅ **Structure**: Contains `##` or `###` headers
3. ✅ **Code Blocks**: Present for technical lectures
4. ✅ **Kevin's Voice**: Contains phrases like "production", "real-world", "gotchas", "battle-tested"
5. ✅ **No Automation**: No markers like "automated", "batch processing", "script completed"
6. ✅ **Depth**: Includes bullet points or lists
7. ✅ **Emphasis**: Uses bold/italic markdown

**Pass Threshold**: Must pass at least 5 out of 7 checks (70% quality score)

### Failed Quality Checks

If output fails quality validation:
- Automatically retries (up to 3 attempts)
- Logged in database with quality score
- Marked as `failed` if all retries fail

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Claude Code CLI not found"

**Error Message:**
```
[ERROR] Claude Code CLI not found. Please install it first.
```

**Solution:**
```bash
# Reinstall Claude Code CLI
npm uninstall -g @anthropic-ai/claude-code
npm install -g @anthropic-ai/claude-code

# Verify installation
claude-code --version
```

#### Issue 2: "Claude Code CLI not logged in"

**Error Message:**
```
[ERROR] Claude Code CLI is not logged in
```

**Solution:**
```bash
# Login to Claude Code
claude-code login

# Verify login
claude-code whoami
```

#### Issue 3: "Scan folder does not exist"

**Error Message:**
```
[ERROR] Scan folder does not exist: /path/to/folder
```

**Solution:**
- Check folder path is correct
- Use absolute paths (not relative)
- Ensure you have read permissions

#### Issue 4: Workers validation error

**Error Message:**
```
[ERROR] Workers must be >= 1 (got: 0)
```

**Solution:**
```bash
# Workers must be at least 1
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -workers 1  # Minimum value
```

#### Issue 5: Quality check failures

**Symptom:** Many files marked as `failed` with low quality scores

**Diagnosis:**
```bash
# Check failed files
python KevinTheAntagonizerClaudeCodeNotesMaker.py -list-failed

# View quality scores
sqlite3 synthesis_tasks.db \
  "SELECT lecture_name, quality_score FROM tasks WHERE status='failed'"
```

**Solution:**
- Use better model (`-model opus` or `-model sonnet-3.5`)
- Check system prompt isn't too restrictive
- Verify input `.srt` files have actual content

#### Issue 6: Rate limiting

**Symptom:** Errors about too many requests

**Solution:**
```bash
# Reduce parallel workers
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -workers 2  # Reduce from 4 to 2

# Reduce batch size
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -batch-size 5  # Reduce from 10 to 5
```

#### Issue 7: Progress bars not showing

**Symptom:** No visual progress indicators

**Solution:**
- Ensure terminal supports ANSI colors
- Check `tqdm` is installed: `pip install tqdm`
- Windows: Use Windows Terminal instead of cmd.exe

#### Issue 8: Log file encoding issues

**Symptom:** Unicode errors in log files

**Solution:**
- The application now uses ASCII-safe formatting
- If issues persist, check Python encoding:
```bash
python -c "import sys; print(sys.getdefaultencoding())"
```

---

## Best Practices

### 1. Start Small, Then Scale

**Recommended Approach:**

```bash
# Step 1: Test with dry run
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/test-course \
  --dry-run

# Step 2: Process small batch (1 worker)
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/test-course \
  -workers 1

# Step 3: Check results and quality
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats

# Step 4: Scale up if satisfied
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  -workers 4
```

### 2. Use Custom Databases for Projects

Separate different course collections:

```bash
# Java courses → java.db
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /java-courses \
  -db java.db

# Python courses → python.db
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /python-courses \
  -db python.db
```

### 3. Monitor Logs in Real-Time

```bash
# Terminal 1: Run processing
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -workers 4

# Terminal 2: Monitor logs
tail -f runID.*.log | grep -E "Completed|ERROR"
```

### 4. Handle Failed Files Strategically

```bash
# Step 1: Check what failed
python KevinTheAntagonizerClaudeCodeNotesMaker.py -list-failed

# Step 2: Retry with better model
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus  # Use premium model for failed files

# Step 3: Check remaining failures
python KevinTheAntagonizerClaudeCodeNotesMaker.py -list-failed
```

### 5. Optimize Worker Count

**Guidelines:**

- **1-2 workers**: Good for testing, low API quota
- **4 workers**: Sweet spot for most use cases
- **8+ workers**: Only if you have high API quota and fast connection

**Test first:**
```bash
# Test with increasing workers
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /small-course -workers 1
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /small-course -workers 2
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /small-course -workers 4
# Compare processing times and error rates
```

### 6. Backup Your Database

```bash
# Before major operations, backup the database
cp synthesis_tasks.db synthesis_tasks.db.backup

# Or use timestamp
cp synthesis_tasks.db synthesis_tasks.db.$(date +%Y%m%d_%H%M%S)
```

### 7. Use Model Tiers Strategically

**Cost-Effective Approach:**

```bash
# Phase 1: Use haiku for bulk processing (cheap)
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -model haiku \
  -workers 8

# Phase 2: Check quality
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats

# Phase 3: Re-process low-quality files with opus
sqlite3 synthesis_tasks.db \
  "UPDATE tasks SET status='pending', attempts=0 WHERE quality_score < 0.7"

python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus
```

---

## Performance Tuning

### Token Efficiency

The application optimizes token usage:

1. **SRT Cleaning**: Removes timestamps, line numbers (reduces 50-70%)
2. **Estimated Tokens**: `len(transcript) // 4`
3. **Target Range**: 4,000-10,000 tokens per synthesis

### Optimal Batch Sizes

| Worker Count | Recommended Batch Size | Reason |
|--------------|----------------------|--------|
| 1 | 10 | Standard |
| 2-4 | 5-10 | Balanced |
| 8+ | 5 | Better error recovery |

### Processing Speed Estimates

Assuming average transcript (5,000 tokens):

| Workers | Batch Size | Files/Hour (approx) |
|---------|------------|---------------------|
| 1 | 10 | 60-80 |
| 2 | 10 | 120-160 |
| 4 | 10 | 240-320 |
| 8 | 5 | 400-500 |

**Note**: Actual speed depends on:
- API response time
- Transcript length
- Network speed
- Quality check failures requiring retries

### Memory Usage

The application is memory-efficient:
- **Per Worker**: ~50-100 MB
- **Database**: Negligible (<10 MB for 1000 files)
- **Logs**: ~1 MB per 100 files processed

### Disk Space Requirements

Estimate needed disk space:

```
Output Size ≈ Input .srt Size × 1.5 to 2.0

Example:
- 100 .srt files @ 50 KB each = 5 MB
- 100 .md notes @ 75-100 KB each = 7.5-10 MB
- Total: ~12-15 MB
```

---

## Appendix: Complete Command Reference

### All Arguments

```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan <folder> [-scan <folder> ...]    # Required
  [-recursive]                            # Optional flag
  [-workers <num>]                        # Default: 1
  [-batch-size <num>]                     # Default: 10
  [-db <path>]                            # Default: synthesis_tasks.db
  [-reset-db]                             # Flag
  [-list-failed]                          # Flag (exits after)
  [-retry-failed]                         # Flag
  [-stats]                                # Flag (exits after)
  [-system-prompt <file>]                 # Optional
  [-model <name>]                         # Default: sonnet-4.5
  [--dry-run]                             # Flag
```

### Quick Reference Card

```bash
# Basic usage
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /courses

# Recursive scan
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /courses -recursive

# Parallel processing
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /courses -workers 4

# Custom model
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /courses -model opus

# Check stats
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats

# Retry failures
python KevinTheAntagonizerClaudeCodeNotesMaker.py -retry-failed

# Reset everything
python KevinTheAntagonizerClaudeCodeNotesMaker.py -reset-db -scan /courses

# Dry run test
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /courses --dry-run
```

---

## Changelog

### Version 2.0 (November 2025) - Current

**Major Changes:**
- **BREAKING**: Single-file architecture - all functionality merged into one file
- Integrated CLI argument parsing (no separate cli_args.py module)
- Improved Windows encoding compatibility (ASCII-safe output)
- Enhanced error handling and validation
- Moved deprecated files to `__deprecated/` folder

**Improvements:**
- Better CLI help messages and argument validation
- Clearer configuration display on startup
- Comprehensive logging with timestamps
- Database schema optimized for better tracking

### Version 1.0 (Initial Release)

**Features:**
- Multi-file architecture with separate CLI module
- Basic CLI support with argparse
- SQLite database task tracking
- Quality control system with 7-point validation
- Support for 5 Claude models
- Batch processing with configurable workers
- Progress bars and logging

---

**End of Usage Guide**

For additional help:
- **CLAUDE.md**: Architecture and development guide
- **README.md**: Quick start and overview
- **Issue Tracker**: Report bugs and request features
