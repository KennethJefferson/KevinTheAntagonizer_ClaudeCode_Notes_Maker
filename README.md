# KevinTheAntagonizerClaudeCodeNotesMaker

A powerful single-file CLI Python application that transforms technical course transcripts (.srt files) into comprehensive, expert-level learning notes using the Claude Agent SDK.

**Notes Style**: Written in the distinctive voice of "Kevin Burleigh" - a battle-tested Java/Spring Boot architect with opinionated, practical insights and real-world gotchas.

**Version**: 2.3 (Hybrid Auth with Model Caching)

---

## Key Features

- **Single-File Design**: Everything in one self-contained Python file (~1200 lines)
- **Integrated CLI**: Full command-line interface with argparse (no separate modules)
- **Flexible Scanning**: Scan single or multiple folders, with or without recursion
- **Database Persistence**: SQLite-based task tracking, retry logic, and statistics
- **Quality Control**: 7-point validation system ensures high-quality synthesis
- **Model Selection**: Choose from 5 Claude models (haiku, sonnet, opus, sonnet-3.5, sonnet-4.5)
- **Multi-Worker Support**: True parallel processing with configurable worker count
- **Graceful Shutdown**: Ctrl+C completes current batch; double Ctrl+C force exits
- **Custom Personas**: Override default Kevin voice with custom system prompts
- **Automatic Retry**: Failed files automatically retry up to 3 times
- **Resume Support**: Continue where you left off if interrupted
- **No Overwrites**: Skips files that already have notes
- **Comprehensive Logging**: Timestamped log files with detailed progress tracking

---

## Quick Start

### 1. Installation

```bash
# Install Claude Code CLI (required by SDK)
npm install -g @anthropic-ai/claude-code

# Login to Claude Code
claude-code login

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
claude-code whoami
python -c "import claude_agent_sdk; print('SDK ready')"
```

### 2. Basic Usage

```bash
# Process a single course folder
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /path/to/course

# Process multiple folders recursively
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/java \
  -scan /courses/spring \
  -recursive
```

### 3. Monitor Progress

The application provides:
- Real-time console output with progress
- Automatic log file: `runID.YYYYMMDD.HHMMSS.log`
- Database tracking: `__db/synthesis_tasks.db`
- Configuration storage: `config/`

---

## Command-Line Interface

### Synopsis

```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan <folder> [-scan <folder> ...] \
  [options]
```

### Required Arguments

| Argument | Description |
|----------|-------------|
| `-scan <folder>` | Folder to scan for .srt files (repeatable) |

### Processing Options

| Argument | Default | Description |
|----------|---------|-------------|
| `-recursive` | `false` | Scan subfolders recursively |
| `-workers <num>` | `1` | Number of parallel workers |
| `-batch-size <num>` | `10` | Files per batch per worker |

**Note**: With multiple workers, total batch = `workers × batch_size` (e.g., 25 workers × 10 = 250 tasks)

### Database Management

| Argument | Description |
|----------|-------------|
| `-db <path>` | Custom database path (default: `__db/synthesis_tasks.db`) |
| `-reset-db` | Clear database and start fresh |
| `-list-failed` | Show failed tasks and exit |
| `-retry-failed` | Retry all failed tasks |
| `-stats` | Show database statistics and exit |

### Advanced Options

| Argument | Description |
|----------|-------------|
| `-system-prompt <file>` | Use custom system prompt from file |
| `-model <name>` | Model selection (see [Models](#available-models)) |
| `--dry-run` | Validate configuration without processing |

### Available Models

Use `--list-models` to see current options:

```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py --list-models
```

Models are fetched from Anthropic API (requires API key for `--list-models`) and cached locally in `config/claude_models_cache.json`.

| Model | Description | Use Case |
|-------|-------------|----------|
| `sonnet-4.5` | **DEFAULT** - Latest Claude 4.5 | Recommended |
| `sonnet-3.5` | Claude 3.5 Sonnet | Alternative |
| `opus` | Claude 3 Opus (premium) | Highest quality |
| `sonnet` | Claude 3 Sonnet | Balanced |
| `haiku` | Claude 3 Haiku | Budget option |

**Hybrid Auth**:
- `--list-models` uses Anthropic API (requires API key, prompted on first use)
- All synthesis uses Claude Code CLI auth (subscription login, no API key needed)

---

## Usage Examples

### Example 1: Single Folder, Sequential

```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /courses/java-basics
```

**What happens:**
- Scans `/courses/java-basics` (no subfolders)
- Finds all `.srt` files
- Processes sequentially
- Creates notes alongside .srt files
- Uses default model (sonnet-4.5)

### Example 2: Multiple Folders, Recursive

```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/java \
  -scan /courses/spring \
  -scan /courses/microservices \
  -recursive \
  -batch-size 5
```

**What happens:**
- Scans 3 folders recursively
- Processes 5 files per batch
- Shows progress for each batch

### Example 3: Custom Model and System Prompt

```bash
# Create custom expert persona
echo "You are a Python expert with Django expertise..." > python_expert.txt

# Process with custom persona
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /python-courses \
  -model opus \
  -system-prompt python_expert.txt
```

### Example 4: Check Statistics

```bash
# View current progress
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats
```

**Output:**
```
[DATABASE STATISTICS]
   - Total Tasks:     523
   - Completed:       487 (93.1%)
   - Failed:          12 (2.3%)
   - Pending:         24 (4.6%)
   - Average Quality: 82.50%
```

### Example 5: Retry Failed Files

```bash
# List failed files
python KevinTheAntagonizerClaudeCodeNotesMaker.py -list-failed

# Retry with premium model
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus
```

### Example 6: Dry Run Validation

```bash
# Test configuration without processing
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  --dry-run
```

**Output:**
```
[SCAN FOLDERS]
   - /courses

[PROCESSING OPTIONS]
   - Recursive:   True
   - Workers:     1
   - Batch Size:  10
   - Model:       sonnet-4.5

*** DRY RUN MODE - No files will be processed ***
```

### Example 7: Multi-Worker Processing

```bash
# Process with 25 parallel workers, 10 files per batch each
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  -workers 25 \
  -batch-size 10
```

**What happens:**
- Loads up to 250 tasks (25 × 10) per batch
- Each worker processes files concurrently
- Individual progress bars for each worker
- Main progress bar shows overall completion

---

## Graceful Shutdown

The application supports graceful shutdown when you press Ctrl+C:

### First Ctrl+C: Complete Current Batch

```
Processing batch 1...
[████████████████████] 100/250

<Ctrl+C pressed>

======================================================================
[SHUTDOWN] Ctrl+C detected - completing current batch...
[SHUTDOWN] Press Ctrl+C again to force immediate exit
======================================================================

Worker01: Shutting down...
Worker02: Shutting down...
[████████████████████] 250/250

[SHUTDOWN] Batch processing complete, exiting gracefully
```

- All tasks currently loaded will complete
- Workers finish their current files before exiting
- Database remains consistent

### Second Ctrl+C: Force Exit

```
<Ctrl+C pressed again>

======================================================================
[SHUTDOWN] Force exit requested - terminating immediately
======================================================================
```

- Immediate termination
- Progress bars cleaned up via atexit handler
- In-progress tasks remain "pending" in database for retry

---

## How It Works

### Architecture

```
1. CLI Parsing      → Validate arguments
2. Database Setup   → Initialize SQLite tracking
3. File Scanning    → Find all .srt files
4. Batch Processing → Process in configurable batches
5. Synthesis        → Claude SDK generates notes
6. Quality Check    → Validate output quality
7. Save Notes       → Write markdown files
8. Update Database  → Track completion/failure
9. Statistics       → Report final results
```

### Data Flow

```
Input: lecture.srt
    ↓
File Scanner → Database (pending task)
    ↓
Batch Assignment → Process batch of N files
    ↓
SRT Cleaning → Remove timestamps/line numbers
    ↓
Claude API → Generate expert-level notes
    ↓
Quality Check → Validate 7 criteria
    ↓
Save → lecture_KevinTheAntagonizer_Notes.md
    ↓
Database Update → Mark as completed
```

### Single-File Architecture

**Benefits:**
- **Simplicity**: Everything in one place (1031 lines)
- **Portability**: Easy to copy and deploy
- **Maintenance**: Single point of update
- **No Import Issues**: No module path problems
- **Self-Contained**: All functionality integrated

---

## Output

### File Naming

```
Input:  Lecture_42_Spring_Boot_Dependency_Injection.srt
Output: Lecture_42_Spring_Boot_Dependency_Injection_KevinTheAntagonizer_Notes.md
```

### File Location

Notes are saved **alongside** the original .srt file:

```
/courses/spring-boot/
├── Lecture_01_Introduction.srt
├── Lecture_01_Introduction_KevinTheAntagonizer_Notes.md  ← Created here
├── Lecture_02_Setup.srt
├── Lecture_02_Setup_KevinTheAntagonizer_Notes.md
└── ...
```

### Output Structure

Each markdown file contains:

```markdown
# [Lecture Title]

## Section 1: Core Concepts

[Expert commentary with Kevin's opinionated insights]

### Key Points

- **Concept 1**: Detailed explanation with production gotchas
- **Concept 2**: Real-world examples and anti-patterns

### Code Examples

```java
// Production-ready code with Kevin's warnings
@Service
public class UserService {
    // Constructor injection - the ONLY way in production
    private final UserRepository userRepo;

    public UserService(UserRepository userRepo) {
        this.userRepo = userRepo;
    }
}
```

### Real-World Gotchas

- **Gotcha 1**: Field injection breaks testability
- **Gotcha 2**: Circular dependencies mean bad design

## Section 2: Advanced Topics

[... continues ...]
```

### Quality Standards

Every output is validated against 7 criteria:

1. ✅ **Length**: ≥1500 characters
2. ✅ **Structure**: Contains `##` or `###` headers
3. ✅ **Code Blocks**: Present for technical lectures
4. ✅ **Kevin's Voice**: Uses "production", "real-world", "gotchas", "battle-tested"
5. ✅ **No Automation**: No markers like "automated", "batch processing"
6. ✅ **Depth**: Includes bullet points and lists
7. ✅ **Emphasis**: Uses bold/italic markdown

**Pass Threshold**: Must pass at least 5 out of 7 checks (70%)

---

## Database Management

### Database Schema

SQLite database tracks all tasks:

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    srt_path TEXT UNIQUE NOT NULL,
    lecture_name TEXT NOT NULL,
    course_name TEXT NOT NULL,
    status TEXT NOT NULL,           -- pending, processing, completed, failed
    attempts INTEGER DEFAULT 0,
    quality_score REAL,
    tokens_used INTEGER,
    error_message TEXT,
    created_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

### Manual Database Queries

The database is stored in `__db/synthesis_tasks.db`:

```bash
# View statistics by status
sqlite3 __db/synthesis_tasks.db \
  "SELECT status, COUNT(*) FROM tasks GROUP BY status"

# Average quality score
sqlite3 __db/synthesis_tasks.db \
  "SELECT AVG(quality_score) FROM tasks WHERE status='completed'"

# Failed files with errors
sqlite3 __db/synthesis_tasks.db \
  "SELECT lecture_name, error_message FROM tasks WHERE status='failed'"

# Export to CSV
sqlite3 -header -csv __db/synthesis_tasks.db \
  "SELECT * FROM tasks WHERE status='completed'" > completed.csv
```

---

## Progress Monitoring

### Log Files

Automatic timestamped logs: `runID.YYYYMMDD.HHMMSS.log`

```bash
# Monitor log in real-time
tail -f runID.*.log

# Filter for errors
tail -f runID.*.log | grep ERROR

# Filter for completions
tail -f runID.*.log | grep "Completed:"
```

### Real-Time Statistics

```bash
# Terminal 1: Run processing
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses

# Terminal 2: Monitor logs
tail -f runID.*.log

# Terminal 3: Watch database stats
watch -n 2 'sqlite3 __db/synthesis_tasks.db "SELECT status, COUNT(*) FROM tasks GROUP BY status"'
```

---

## Troubleshooting

### Issue: "Claude Code CLI not found"

**Solution:**
```bash
npm install -g @anthropic-ai/claude-code
claude-code --version
```

### Issue: "Claude Code CLI not logged in"

**Solution:**
```bash
claude-code login
claude-code whoami
```

### Issue: Quality check failures

**Diagnosis:**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py -list-failed
```

**Solution:**
```bash
# Retry with premium model
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus
```

### Issue: Rate limiting

**Solution:**
```bash
# Reduce batch size
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -batch-size 5
```

---

## Best Practices

### 1. Start Small, Then Scale

```bash
# Test with dry run
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /test-course \
  --dry-run

# Process small batch
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /test-course

# Check quality
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats

# Scale up
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /all-courses \
  -recursive
```

### 2. Use Custom Databases for Projects

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

### 3. Cost Optimization Strategy

```bash
# Phase 1: Bulk with haiku (cheap)
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -model haiku

# Phase 2: Check quality
sqlite3 __db/synthesis_tasks.db \
  "SELECT COUNT(*) FROM tasks WHERE quality_score < 0.7"

# Phase 3: Re-process low-quality with opus
sqlite3 __db/synthesis_tasks.db \
  "UPDATE tasks SET status='pending' WHERE quality_score < 0.7"

python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus
```

### 4. Backup Important Databases

```bash
# Before major operations
cp __db/synthesis_tasks.db __db/synthesis_tasks.db.backup

# Or with timestamp
cp __db/synthesis_tasks.db __db/synthesis_tasks.db.$(date +%Y%m%d_%H%M%S)
```

---

## Performance

### Processing Speed Estimates

Assuming average 5,000-token transcripts:

| Batch Size | Files/Hour (approx) | Best For |
|------------|---------------------|----------|
| 5 | 50-70 | Better error recovery |
| 10 | 60-80 | Recommended default |
| 20 | 70-90 | Large stable datasets |

*Actual speed depends on: API response time, transcript length, network speed, quality check failures*

### Resource Usage

- **Memory**: ~50-100 MB per process
- **Database** (`__db/`): <10 MB for 1000 files
- **Config** (`config/`): <1 KB
- **Logs**: ~1 MB per 100 files processed
- **Output**: 1.5-2x size of input .srt files

### Optimization Tips

- **Batch Size 10**: Good default for most use cases
- **Batch Size 5**: Better error recovery for large datasets
- **Model Selection**: Use haiku for bulk, opus for quality

---

## Documentation

- **README.md** (this file): Quick start and overview
- **USAGE.md**: Comprehensive usage guide with examples
- **CLAUDE.md**: Architecture and development guide
- **Inline Comments**: Extensive documentation in code

---

## Prerequisites

### System Requirements

- **Python**: 3.7 or higher
- **Node.js**: For Claude Code CLI
- **Claude Code Account**: For authentication

### Dependencies

```bash
pip install -r requirements.txt
```

Main dependencies:
- `claude-agent-sdk`: Claude AI integration
- Standard library: `sqlite3`, `argparse`, `pathlib`, `logging`, `asyncio`

---

## Project Structure

```
KevinTheAntagonizerClaudeCodeNotesMaker/
├── KevinTheAntagonizerClaudeCodeNotesMaker.py  # Main application (~1200 lines)
├── config/                        # Configuration directory
│   ├── .anthropic_api_key         # API key for --list-models only
│   └── claude_models_cache.json   # Cached model list
├── __db/                          # Database directory
│   └── synthesis_tasks.db         # SQLite task tracking
├── requirements.txt               # Dependencies
├── CLAUDE.md                      # Architecture guide
├── README.md                      # This file
├── USAGE.md                       # Comprehensive usage
└── __deprecated/
    └── cli_args.py                # Deprecated (merged into main file)
```

**Note**: Version 2.3 uses hybrid auth - API for model listing, Claude Code CLI for synthesis.

---

## Support

For issues with:
- **Claude Agent SDK**: https://github.com/anthropics/claude-agent-sdk-python
- **Claude Code CLI**: https://github.com/anthropics/claude-code
- **API Questions**: https://docs.anthropic.com/

---

## License

This project uses the Claude Agent SDK which is subject to Anthropic's terms of service.

---

## Quick Reference

```bash
# Help
python KevinTheAntagonizerClaudeCodeNotesMaker.py -h

# List available models
python KevinTheAntagonizerClaudeCodeNotesMaker.py --list-models

# Basic usage
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /courses

# Recursive
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /courses -recursive

# Custom model
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /courses -model opus

# Check stats
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats

# Retry failed
python KevinTheAntagonizerClaudeCodeNotesMaker.py -retry-failed

# Dry run
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /courses --dry-run
```

---

## Changelog

### Version 2.3 (December 2025) - Current
- **NEW**: Hybrid authentication approach
  - `--list-models`: Uses Anthropic API for fresh model data
  - All synthesis: Uses Claude Code CLI auth (subscription login)
  - No API credits used for synthesis work
- **NEW**: Organized directory structure
  - `config/`: Configuration files (.anthropic_api_key, claude_models_cache.json)
  - `__db/`: Database storage (synthesis_tasks.db)
- **NEW**: Persistent model caching
  - Models fetched via API cached in `config/claude_models_cache.json`
  - Fast model validation without API calls
- **NEW**: API key storage in `config/.anthropic_api_key`
  - Prompted on first `--list-models` run
  - Only used for model listing, not synthesis

### Version 2.2 (November 2025)
- **NEW**: Graceful shutdown support (Ctrl+C handling)
  - First Ctrl+C: Complete current batch before exiting
  - Second Ctrl+C: Force immediate exit
  - Progress bar cleanup via atexit handler
  - Works on Windows (SIGINT, SIGBREAK) and Unix
- Multi-worker mode now fully functional
- True parallel asyncio workers with shared task queue

### Version 2.1 (November 2025)
- **NEW**: Dynamic model discovery from Claude Code CLI
- **NEW**: `--list-models` command to see available models
- Automatic model updates (no code changes needed for new releases)
- Enhanced model validation with helpful error messages
- Model source indication in configuration display

### Version 2.0 (November 2025)
- **BREAKING**: Single-file architecture
- Merged `cli_args.py` into main application
- Improved CLI argument parsing
- Better error handling and logging
- Windows encoding compatibility
- Moved deprecated files to `__deprecated/`

### Version 1.0 (Initial Release)
- Multi-file architecture
- Basic CLI support
- Database task tracking
- Quality control system

---

**Made with Claude Agent SDK** | **Questions?** See USAGE.md for comprehensive documentation
