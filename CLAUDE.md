# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **single-file CLI-based Python application** that uses the Claude Agent SDK to synthesize technical course transcripts (SRT files) into comprehensive, expert-level markdown notes. The notes are written in the style of "Kevin Burleigh" - a battle-tested Java/Spring Boot architect with opinionated, practical insights.

**Architecture**: Single-file application with integrated CLI argument parsing, multi-worker support, SQLite-based task management, progress tracking, graceful shutdown handling, and automatic retry logic.

## Prerequisites & Environment Setup

### Required Installations
```bash
# 1. Install Claude Code CLI (required by SDK)
npm install -g @anthropic-ai/claude-code

# 2. Login to Claude Code (handles authentication)
claude-code login

# 3. Install Python SDK
pip install claude-agent-sdk

# 4. Install Python dependencies
pip install -r requirements.txt
```

### Authentication
Authentication is handled through the Claude Code CLI login. No API keys need to be configured in the application.

### Verify Installation
```bash
# Test Claude Code CLI
claude-code --version

# Verify login status
claude-code whoami

# Test SDK
python -c "import claude_agent_sdk; print('SDK ready')"

# Test application
python KevinTheAntagonizerClaudeCodeNotesMaker.py -h
```

## Architecture

### Directory Structure

```
KevinTheAntagonizerClaudeCodeNotesMaker/
├── KevinTheAntagonizerClaudeCodeNotesMaker.py  # Main application
├── config/                                      # Configuration files
│   ├── .anthropic_api_key                      # API key for --list-models
│   └── claude_models_cache.json                # Cached model data
├── __db/                                        # Database storage
│   └── synthesis_tasks.db                      # SQLite task database
├── __deprecated/                                # Old/deprecated code
├── requirements.txt                             # Python dependencies
├── CLAUDE.md                                    # This file
├── README.md                                    # Quick start guide
└── USAGE.md                                     # Detailed usage guide
```

### Single-File Design

The application is a **single, self-contained file** with all functionality integrated:

**KevinTheAntagonizerClaudeCodeNotesMaker.py** (~1200 lines)
- CLI argument parsing and validation
- Database management (SQLite in `__db/`)
- Configuration management (`config/`)
- File scanning and processing
- Quality control
- Synthesis engine using Claude Agent SDK
- Graceful shutdown handling (Ctrl+C support)
- Main application entry point

### Core Components

1. **CLI Argument Parsing** (lines 125-372)
   - Uses `argparse` for comprehensive CLI interface
   - `CLIArgs` dataclass for configuration
   - `create_parser()` - Argument parser setup
   - `validate_args()` - Input validation
   - `parse_arguments()` - Main entry point
   - `print_configuration()` - Config display

2. **Configuration** (lines 101-119)
   - Default system prompt (Kevin persona)
   - Quality control settings
   - Allowed/disallowed tools
   - Model selection

3. **DatabaseManager** (lines 378-558)
   - SQLite-based task tracking (`__db/synthesis_tasks.db`)
   - Schema: `tasks` and `processing_stats` tables
   - Operations: add_task, get_pending_tasks, update_status, get_statistics
   - Supports: batch operations, retry logic, progress tracking

4. **FileProcessor** (lines 564-602)
   - `clean_srt_content()` - Removes timestamps, line numbers
   - `save_notes()` - Saves output as `*_KevinTheAntagonizer_Notes.md`
   - Never overwrites existing files

5. **QualityController** (lines 608-673)
   - 7-point quality validation system
   - Checks: length, structure, code blocks, voice, automation markers, depth, emphasis
   - Pass threshold: 5/7 checks (70%)

6. **NoteSynthesisEngine** (lines 679-862)
   - Orchestrates synthesis using Claude Agent SDK
   - Uses `query()` function for prompt-response
   - Implements retry logic (max 3 attempts)
   - Model selection from CLI arguments
   - Custom system prompts supported

7. **File Inventory** (lines 868-903)
   - Scans folders for .srt files
   - Recursive or non-recursive modes
   - Skips existing notes (no overwrites)

8. **Main Application** (lines 909-1031)
   - Parses CLI arguments
   - Handles database operations
   - Processes files in batches
   - Shows progress and statistics

### Data Flow

```
CLI Arguments
    ↓
Configuration Validation
    ↓
Database Initialization
    ↓
File Scanning (scan_folders, recursive)
    ↓
DatabaseManager.add_tasks() → synthesis_tasks.db
    ↓
Batch Processing Loop
    ↓
    ├─→ Get pending tasks (batch_size)
    │   ↓
    │   FileProcessor.clean_srt() → Pure transcript
    │   ↓
    │   query(prompt, options) → Claude API (with selected model)
    │   ↓
    │   QualityController.check_synthesis()
    │   ↓
    │   FileProcessor.save_notes() → *_KevinTheAntagonizer_Notes.md
    │   ↓
    │   DatabaseManager.update_status() → completed/failed
    │
    └─→ Repeat until no pending tasks
    ↓
Final Statistics Report
```

## Command-Line Interface

### Basic Syntax

```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan <folder> [-scan <folder> ...] \
  [options]
```

### Required Arguments
- `-scan <folder>`: Folder(s) to scan for .srt files (repeatable)

### Optional Arguments

**Processing:**
- `-recursive`: Scan subfolders (default: false)
- `-workers <num>`: Parallel workers (default: 1) - *Note: Multi-worker support planned for future*
- `-batch-size <num>`: Files per batch (default: 10)

**Database:**
- `-db <path>`: Custom database path (default: synthesis_tasks.db)
- `-reset-db`: Clear database and start fresh
- `-list-failed`: Show failed tasks and exit
- `-retry-failed`: Retry all failed tasks
- `-stats`: Show database statistics and exit

**Advanced:**
- `-system-prompt <file>`: Custom system prompt file
- `-model <name>`: Model selection (opus, sonnet, haiku, sonnet-3.5, sonnet-4.5)
- `--dry-run`: Validate configuration without processing

### Automatic Features
- **Log File**: `runID.YYYYMMDD.HHMMSS.log` (always created)
- **Database Tracking**: All tasks tracked in SQLite

### Available Models

```python
AVAILABLE_MODELS = {
    "opus": "claude-3-opus-20240229",           # Most capable, expensive
    "sonnet": "claude-3-sonnet-20240229",       # Balanced
    "haiku": "claude-3-haiku-20240307",         # Fast, cheap
    "sonnet-3.5": "claude-3-5-sonnet-20241022", # Better than opus
    "sonnet-4.5": "claude-sonnet-4-5-20250929", # Latest, best (DEFAULT)
}
```

### Dynamic Model Discovery with Caching (Hybrid Approach)

The application uses a **hybrid authentication approach**:
- **`--list-models`**: Uses Anthropic API to fetch fresh model data (requires API key)
- **All other operations**: Uses Claude Code CLI authentication (subscription login)

This means you get live model updates without needing API credits for actual synthesis work.

#### How It Works

1. **For `--list-models` (API-based)**:
   - Uses Anthropic API to fetch the latest available models
   - Requires API key stored in `.anthropic_api_key` file
   - Prompts for API key on first run if not configured
   - Saves discovered models to cache for other operations

2. **For All Other Operations (CLI-based)**:
   - Uses cached models (fast lookup)
   - Falls back to static model list
   - **No API key needed** - uses Claude Code CLI authentication
   - All synthesis work uses your Claude Code subscription

3. **Persistent Cache**: Discovered models are saved to `claude_models_cache.json`
   - Located in the same directory as the script
   - Stores: models, timestamp, source, version
   - Updated when `--list-models` fetches fresh data
   - Used by model validation during normal operations

#### Files

All configuration files are stored in the `config/` directory:

- **`config/.anthropic_api_key`**: Stores API key for model listing only (not for synthesis)
- **`config/claude_models_cache.json`**: Cached model data

#### First-Time Setup

When you run `--list-models` for the first time:

```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py --list-models
```

You'll be prompted to enter your Anthropic API key:
```
================================================================================
AVAILABLE CLAUDE MODELS - Live Update
================================================================================
NOTE: This uses Anthropic API to fetch models.
      All other operations use Claude Code CLI auth.
================================================================================

[SETUP] No API key found for model listing.
[SETUP] Key file: /path/to/config/.anthropic_api_key

To enable live model updates, you need an Anthropic API key.
This is ONLY used for --list-models, not for synthesis.

Enter your Anthropic API key (or press Enter to use cached/static): sk-ant-...
```

After entering your key, it's saved and used for future model list updates.

#### Example Output (After Setup)

```
================================================================================
AVAILABLE CLAUDE MODELS - Live Update
================================================================================
NOTE: This uses Anthropic API to fetch models.
      All other operations use Claude Code CLI auth.
================================================================================

[INFO] Fetching latest models from Anthropic API...
[OK] API (fresh) - fetched 12 models
[INFO] Source: API (fresh)
[INFO] Cache file: /path/to/config/claude_models_cache.json
[INFO] Cache updated: 2025-12-08T10:30:00.000000

HAIKU Family:
  haiku           -> claude-3-haiku-20240307

OPUS Family:
  opus            -> claude-3-opus-20240229

SONNET Family:
  sonnet          -> claude-3-sonnet-20240229
  sonnet-3.5      -> claude-3-5-sonnet-20241022
  sonnet-4.5      -> claude-sonnet-4-5-20250929 (DEFAULT)

Total models: 5
Default: sonnet-4.5

Cache location: /path/to/config/claude_models_cache.json
API key file: /path/to/config/.anthropic_api_key

Usage: -model <alias>
================================================================================
```

#### Requirements

**For Model Listing (`--list-models`)**:
- Anthropic API key (prompted on first use, stored in `.anthropic_api_key`)
- One-time setup, then automatic

**For Synthesis (All Other Operations)**:
- Claude Code CLI: `npm install -g @anthropic-ai/claude-code`
- Claude Code login: `claude-code login`
- **No API key needed** - uses subscription authentication

#### Model Validation

When you select a model with `-model <alias>`, the application:

1. Checks cached models first (fast lookup, no API call)
2. Falls back to static model list if no cache
3. Validates your selection
4. Provides helpful error messages with suggestions

**Error Example:**
```bash
$ python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /courses -model invalid

[ERROR] Model 'invalid' not available
[INFO] Available models: opus, sonnet, haiku, sonnet-3.5, sonnet-4.5
[INFO] Run with --list-models for details
```

## Running the Application

### Basic Examples

```bash
# Single folder, sequential
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /courses/java

# Multiple folders, recursive
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/java \
  -scan /courses/spring \
  -recursive

# Custom model and batch size
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -model opus \
  -batch-size 5

# Dry run validation
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  --dry-run

# List available models
python KevinTheAntagonizerClaudeCodeNotesMaker.py --list-models

# Check statistics
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats

# Retry failed files
python KevinTheAntagonizerClaudeCodeNotesMaker.py -retry-failed

# Reset and start fresh
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -reset-db \
  -scan /courses
```

### Database Operations

The database is stored in `__db/synthesis_tasks.db`:

```bash
# Check progress
sqlite3 __db/synthesis_tasks.db "SELECT COUNT(*) FROM tasks WHERE status='completed'"

# View failed files
sqlite3 __db/synthesis_tasks.db "SELECT srt_path, error_message FROM tasks WHERE status='failed'"

# Get statistics
sqlite3 __db/synthesis_tasks.db "SELECT status, COUNT(*) FROM tasks GROUP BY status"

# Average quality score
sqlite3 __db/synthesis_tasks.db "SELECT AVG(quality_score) FROM tasks WHERE status='completed'"

# Reset failed files for retry
sqlite3 __db/synthesis_tasks.db "UPDATE tasks SET status='pending', attempts=0 WHERE status='failed'"
```

## Configuration

### CLI Arguments Configuration

All configuration is handled via CLI arguments:

- **Scan folders**: Via `-scan` argument(s)
- **Workers**: Via `-workers` argument (default: 1)
- **Batch size**: Via `-batch-size` argument (default: 10)
- **Model**: Via `-model` argument (default: sonnet-4.5)
- **Database**: Via `-db` argument (default: synthesis_tasks.db)
- **System prompt**: Via `-system-prompt` argument (optional)

### System Prompt Customization

Default system prompt emphasizes Kevin's persona. Override with `-system-prompt`:

```bash
# Create custom_prompt.txt with your persona
echo "You are a Python expert..." > custom_prompt.txt

# Use custom prompt
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -system-prompt custom_prompt.txt
```

### Agent Options

Each synthesis uses Claude Agent SDK with:

```python
options = ClaudeAgentOptions(
    system_prompt=system_prompt,  # Kevin persona or custom
    model=cli_args.model,          # Model from CLI
    allowed_tools=["Read", "Write", "Bash"],
    disallowed_tools=["CreateAgent", "RunPython"],
    permission_mode='default',
    max_turns=1,
    cwd=Path.cwd()
)
```

## Quality Standards

### Automated Checks (7 criteria)

Each synthesis is validated:

1. **Length**: ≥1500 characters
2. **Structure**: Contains `##` or `###` headers
3. **Code blocks**: Present for technical lectures
4. **Voice**: Contains Kevin-isms ("production", "real-world", "gotchas", "battle-tested")
5. **No automation markers**: Rejects "automated", "batch processing", "script completed"
6. **Depth**: Has bullet points or lists
7. **Emphasis**: Uses bold/italic markdown

**Pass threshold**: 5/7 checks (0.7 score)

### Retry Logic

- **Max attempts**: 3 per file
- **On failure**: Updated in database with error message
- **Manual retry**: Use `-retry-failed` flag

## Error Handling

### Common Issues

**"Claude Code CLI not found"**
```bash
npm install -g @anthropic-ai/claude-code
claude-code --version
```

**"Claude Code CLI not logged in"**
```bash
claude-code login
claude-code whoami
```

**"Scan folder does not exist"**
- Check folder path is correct
- Use absolute paths
- Verify read permissions

**Quality check failures**
- Automatically retries up to 3 times
- Check failed files: `python KevinTheAntagonizerClaudeCodeNotesMaker.py -list-failed`
- Retry with better model: `python KevinTheAntagonizerClaudeCodeNotesMaker.py -retry-failed -model opus`

**Rate limiting**
- Reduce batch size: `-batch-size 5`
- Add delays (already implemented: 1s between files, 2s between batches)

### Exception Handling

```python
from claude_agent_sdk import CLINotFoundError, ProcessError, CLIJSONDecodeError

try:
    async for message in query(prompt=prompt, options=options):
        # Process response
except CLINotFoundError:
    logger.error("Claude Code CLI not found")
except ProcessError as e:
    logger.error(f"Process error: {e.exit_code}")
except CLIJSONDecodeError:
    logger.error("JSON decode error in response")
```

## Development Workflow

### File Structure

```
KevinTheAntagonizerClaudeCodeNotesMaker/
├── KevinTheAntagonizerClaudeCodeNotesMaker.py  # Main application (SINGLE FILE)
├── config/                        # Configuration directory
│   ├── .anthropic_api_key         # API key for --list-models only
│   └── claude_models_cache.json   # Cached model list
├── __db/                          # Database directory
│   └── synthesis_tasks.db         # SQLite task tracking
├── requirements.txt               # Dependencies
├── CLAUDE.md                      # This file
├── README.md                      # Quick start
├── USAGE.md                       # Comprehensive guide
└── __deprecated/
    └── cli_args.py                # Deprecated (merged into main file)
```

### Testing Workflow

```bash
# 1. Test CLI parsing
python KevinTheAntagonizerClaudeCodeNotesMaker.py -h

# 2. Test with dry run
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /test-course \
  --dry-run

# 3. Test with small dataset
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /test-course

# 4. Check results
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats

# 5. Scale up
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /all-courses \
  -recursive \
  -batch-size 10
```

### Modifying the Application

**To add new CLI argument:**
1. Edit `create_parser()` function
2. Add argument to parser group
3. Add validation to `validate_args()`
4. Add to `CLIArgs` class
5. Update `print_configuration()`

**To customize synthesis:**
1. Edit `Config.DEFAULT_SYSTEM_PROMPT` or use `-system-prompt`
2. Modify synthesis prompt in `NoteSynthesisEngine.synthesize_with_sdk()`
3. Adjust quality checks in `QualityController.check_synthesis()`

**To add new model:**
1. Add to `AVAILABLE_MODELS` dictionary
2. Test with `-model <name>`

## File Naming Conventions

- **Input**: `[lecture_name].srt`
- **Output**: `[lecture_name]_KevinTheAntagonizer_Notes.md`
- **Database**: `__db/synthesis_tasks.db` (or custom via `-db`)
- **Config**: `config/.anthropic_api_key`, `config/claude_models_cache.json`
- **Log**: `runID.YYYYMMDD.HHMMSS.log`

## Performance Optimization

### Token Efficiency
- SRT cleaning removes 50-70% of content (timestamps, numbers)
- Estimated tokens: `len(transcript) // 4`
- Target: <10k tokens per synthesis

### Batch Processing
- **Default**: 10 files per batch
- **Large datasets**: 5 files per batch (better error recovery)
- **Small datasets**: 10-20 files per batch

### Database Performance
- Primary key on `tasks.id`
- Unique constraint on `tasks.srt_path`
- Indexed queries on `status` and `attempts`
- Vacuum database periodically for large datasets

### Resource Usage
- **Memory**: ~50-100 MB per process
- **Database** (`__db/`): <10 MB for 1000 files
- **Config** (`config/`): <1 KB
- **Logs**: ~1 MB per 100 files

## Progress Monitoring

### Real-Time Monitoring

```bash
# Terminal 1: Run application
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses

# Terminal 2: Monitor logs
tail -f runID.*.log

# Terminal 3: Watch database stats
watch -n 2 'sqlite3 synthesis_tasks.db "SELECT status, COUNT(*) FROM tasks GROUP BY status"'
```

### Log Output

Application creates detailed logs with:
- Run ID and timestamp
- Configuration summary
- File processing status
- Quality scores
- Error messages
- Final statistics

## Design Principles

### Single-File Architecture

**Benefits:**
- **Simplicity**: Everything in one place
- **Portability**: Easy to copy and deploy
- **Maintenance**: Single point of update
- **No Import Issues**: No module path problems

### Sequential Processing (Single Worker)

Tasks are processed sequentially with:
- 1 second delay between files (rate limiting)
- 2 second delay between batches
- Quality checks after each file
- Automatic retry on failure (up to 3 attempts)

### Multi-Worker Support

Parallel processing with multiple workers:
- True parallel asyncio workers with shared task queue
- Each worker processes `batch_size` files concurrently
- Total batch: `workers × batch_size` tasks (e.g., 25 workers × 10 = 250 tasks)
- Individual progress bars per worker plus main progress bar
- 0.5 second delay between files per worker

### Graceful Shutdown

The application supports graceful shutdown via Ctrl+C:

**First Ctrl+C**: Complete current batch
- Shows: `[SHUTDOWN] Ctrl+C detected - completing current batch...`
- All tasks currently loaded (up to `workers × batch_size`) will complete
- Workers finish their current files before exiting
- Database remains consistent (tasks either completed or pending)

**Second Ctrl+C**: Force immediate exit
- Shows: `[SHUTDOWN] Force exit requested - terminating immediately`
- Raises KeyboardInterrupt for immediate termination
- atexit handler cleans up progress bars

**Implementation Details**:
- Uses `asyncio.Event` for cross-coroutine signaling
- Signal handlers for SIGINT (Ctrl+C) and SIGBREAK (Windows Ctrl+Break)
- Progress bars tracked for cleanup via atexit handler
- Works on both Windows and Unix platforms

**Example Output**:
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

## Advanced Features

### Custom System Prompts

Create custom expert personas:

```bash
# Create custom prompt
cat > data_science_expert.txt << 'EOF'
You are a senior data scientist with 15 years of experience...
Focus on practical ML implementations, data pipelines, and production gotchas.
EOF

# Use custom prompt
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /ml-courses \
  -system-prompt data_science_expert.txt
```

### Multi-Project Management

Separate databases for different projects:

```bash
# Java courses
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /java-courses \
  -db java.db

# Python courses
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /python-courses \
  -db python.db

# ML courses
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /ml-courses \
  -db ml.db \
  -system-prompt ml_expert.txt
```

### Cost Optimization

Use model tiers strategically:

```bash
# Phase 1: Bulk with haiku (cheap)
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -model haiku

# Phase 2: Check quality
sqlite3 synthesis_tasks.db \
  "SELECT COUNT(*) FROM tasks WHERE quality_score < 0.7"

# Phase 3: Re-process low-quality with opus
sqlite3 synthesis_tasks.db \
  "UPDATE tasks SET status='pending', attempts=0 WHERE quality_score < 0.7"

python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus
```

## Documentation

- **README.md**: Quick start and project overview
- **USAGE.md**: Comprehensive usage guide with examples
- **CLAUDE.md**: This file - architecture and development
- **Code Comments**: Extensive inline documentation

## Contributing Guidelines

### Code Style
- Python 3.7+ syntax
- Type hints where applicable
- Docstrings for all functions
- Follow PEP 8

### Testing New Features
1. Test CLI parsing with `--dry-run`
2. Test with single file
3. Test with batch processing
4. Check database integrity
5. Verify log files

### Modification Checklist
- [ ] CLI arguments documented
- [ ] USAGE.md updated if needed
- [ ] CLAUDE.md updated if architecture changed
- [ ] Tested with `--dry-run`
- [ ] Tested with real data
- [ ] Database schema migrations handled
- [ ] Backward compatibility maintained

## Support

For issues with:
- **Claude Agent SDK**: https://github.com/anthropics/claude-agent-sdk-python
- **Claude Code CLI**: https://github.com/anthropics/claude-code
- **API Questions**: https://docs.anthropic.com/

---

**Note**: This application requires Claude Code CLI authentication. Usage is tracked through your Claude Code account.

## Changelog

### Version 2.5 (December 2025) - Current
- **CHANGED**: Concurrency limit raised from 3 to 100 for full parallelism
  - All workers can now hit the API simultaneously (was limited to 3)
  - Jitter (0.1-0.5s) still provides slight staggering between calls
  - Full speed restored for multi-worker processing
  - **Tunable**: Edit `CLAUDE_CONCURRENCY_LIMIT` in code (line 36) if EBUSY errors occur
  - Recommended values: 100 (max speed), 10-15 (balanced), 3 (max stability)

### Version 2.4 (December 2025)
- **FIXED**: Windows command line limit for large transcripts
  - Windows has 8191 character command line limit
  - Large transcripts (40KB+) exceed limit when passed via CLI
  - Solution: Use streaming mode for prompts > 7500 chars
  - Sends prompt via stdin instead of command line
- **FIXED**: EBUSY file locking for parallel workers
  - Multiple workers competing for `~/.claude.json` caused errors
  - Solution: Semaphore with jitter to stagger file access timing
  - Retry logic with exponential backoff for EBUSY errors
- **FIXED**: Windows "[Errno 22] Invalid argument" in multi-worker mode
  - tqdm progress bar cursor positioning failed on Windows console
  - Solution: Safe wrapper functions for all progress bar operations
  - `safe_pbar_update()`, `safe_pbar_set_description()`, `safe_pbar_close()`
  - Gracefully handles OSError with errno 22 without crashing
- **IMPROVED**: Better error logging for SDK exceptions
  - Logs full exception type and message
  - Includes traceback for debugging

### Version 2.3 (December 2025)
- **NEW**: Hybrid authentication approach
  - `--list-models`: Uses Anthropic API for fresh model data
  - All other operations: Uses Claude Code CLI auth (subscription login)
  - No API credits used for synthesis work
- **NEW**: Persistent model caching with `claude_models_cache.json`
  - Models fetched via API are cached locally
  - Cache used for fast model validation during normal operations
  - Includes timestamp, source, and version info
- **NEW**: API key storage in `.anthropic_api_key` file
  - Prompted on first `--list-models` run
  - Stored securely in script directory
  - Only used for model listing, not synthesis
- **IMPROVED**: `--list-models` now shows setup prompts and cache info
  - Guides user through API key setup
  - Displays source (API, cache, or static)
  - Shows both cache and API key file locations

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

### Version 2.0 (November 2025)
- **BREAKING**: Merged `cli_args.py` into main application file
- Single-file architecture for simplicity
- Improved CLI argument parsing
- Better error handling and logging
- Windows encoding compatibility
- Moved deprecated files to `__deprecated/`

### Version 1.0 (Initial Release)
- Multi-file architecture
- Basic CLI support
- Database task tracking
- Quality control system
