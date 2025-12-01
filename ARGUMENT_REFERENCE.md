# CLI Argument Reference - Complete Encyclopedia

**KevinTheAntagonizerClaudeCodeNotesMaker**
**Version**: 2.1
**Document Type**: Man-Page Style Technical Reference
**Last Updated**: November 2025

---

## Purpose of This Document

This is the **complete technical specification** for every command-line argument in KevinTheAntagonizerClaudeCodeNotesMaker. Use this document when you need:

- 📖 **Detailed argument behavior** and edge cases
- 🔍 **Valid values** and validation rules
- ⚠️ **Complete error messages** and solutions
- 🔗 **Argument interactions** and compatibility matrices
- 💻 **Source code references** for implementation details

## Related Documentation

- 🚀 **Need task-based examples?** → See `USAGE_GUIDE.md` (quick reference)
- 📚 **Need comprehensive workflows?** → See `USAGE.md` (detailed guide)
- 🎯 **First time user?** → See `README.md` (quick start)

---

## How to Use This Reference

**Navigation Options**:

1. **By Argument Name**: Jump to any argument using the [Alphabetical Index](#alphabetical-index)
2. **By Category**: Browse by functional group using the [Category Index](#category-index)
3. **By Use Case**: Find argument combinations in the [Combination Matrices](#combination-matrices)
4. **By Error**: Look up error messages in the [Error Catalog](#error-catalog)

**Reading Each Entry**:

Each argument specification follows this structure:

```
### ArgumentName
├─ Category & Type
├─ Synopsis (syntax)
├─ Description (what it does)
├─ Valid Values
├─ Validation Rules
├─ Examples (6+ with expected output)
├─ Related Arguments
├─ Interaction Matrix
├─ Error Messages
├─ Behavioral Notes
└─ Source Code References
```

---

## <a id="alphabetical-index"></a>Alphabetical Index

Quick jump to any argument:

| Argument | Category | Page | Quick Description |
|----------|----------|------|-------------------|
| [`--dry-run`](#dry-run) | Advanced Options | [→](#dry-run) | Validate configuration without processing |
| [`--help`](#help) | Information & Help | [→](#help) | Show help message and exit |
| [`--list-models`](#list-models) | Information & Help | [→](#list-models) | Display available Claude models |
| [`-batch-size`](#batch-size) | Processing Options | [→](#batch-size) | Files per processing batch (default: 10) |
| [`-db`](#db) | Database Management | [→](#db) | Custom database path (default: synthesis_tasks.db) |
| [`-list-failed`](#list-failed) | Database Management | [→](#list-failed) | Show all failed tasks and exit |
| [`-model`](#model) | Advanced Options | [→](#model) | Claude model selection (default: sonnet-4.5) |
| [`-recursive`](#recursive) | Processing Options | [→](#recursive) | Scan subfolders recursively |
| [`-reset-db`](#reset-db) | Database Management | [→](#reset-db) | Clear database and start fresh |
| [`-retry-failed`](#retry-failed) | Database Management | [→](#retry-failed) | Retry all failed tasks |
| [`-scan`](#scan) | Required Processing | [→](#scan) | Folder(s) to scan for .srt files |
| [`-stats`](#stats) | Database Management | [→](#stats) | Show database statistics and exit |
| [`-system-prompt`](#system-prompt) | Advanced Options | [→](#system-prompt) | Custom system prompt file path |
| [`-workers`](#workers) | Processing Options | [→](#workers) | Number of parallel workers (default: 1) |

**Total Arguments**: 14 (17 including deprecated/internal)

---

## <a id="category-index"></a>Category Index

Arguments organized by functional category:

### Information & Help (2 arguments)
- [`--help`](#help) - Display help message
- [`--list-models`](#list-models) - Show available models

### Required Processing (1 argument)
- [`-scan`](#scan) - Specify folders to scan

### Processing Options (3 arguments)
- [`-recursive`](#recursive) - Enable recursive scanning
- [`-workers`](#workers) - Set parallel worker count
- [`-batch-size`](#batch-size) - Configure batch size

### Database Management (5 arguments)
- [`-db`](#db) - Custom database path
- [`-reset-db`](#reset-db) - Reset database
- [`-list-failed`](#list-failed) - List failed tasks
- [`-retry-failed`](#retry-failed) - Retry failures
- [`-stats`](#stats) - Show statistics

### Advanced Options (3 arguments)
- [`-system-prompt`](#system-prompt) - Custom persona
- [`-model`](#model) - Model selection
- [`--dry-run`](#dry-run) - Validation mode

---

## <a id="synopsis"></a>Command Synopsis

```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan <folder> [-scan <folder> ...] \
  [-recursive] \
  [-workers <num>] \
  [-batch-size <num>] \
  [-db <path>] \
  [-reset-db] \
  [-list-failed] \
  [-retry-failed] \
  [-stats] \
  [-system-prompt <file>] \
  [-model <name>] \
  [--list-models] \
  [--dry-run] \
  [--help]
```

**Minimum Required**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan <folder>
```

**Most Common Usage**:
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan <folder> \
  -recursive \
  -workers 4 \
  -batch-size 10
```

---

# Detailed Argument Specifications

## Information & Help Arguments

---

### <a id="help"></a>--help

**Category**: Information & Help
**Type**: Boolean flag
**Synopsis**: `--help` or `-h`
**Default**: Not set

**Description**:

Displays the complete command-line help message showing all available arguments, their syntax, and brief descriptions. Exits immediately after displaying help (no processing occurs).

**Valid Values**:
- No value required (flag argument)

**Validation Rules**:
1. Cannot be combined with any other arguments (help takes precedence)
2. Always exits with code 0 (success)
3. Outputs to stdout
4. Does not create log files or modify database

**Examples**:

**Example 1: Basic help**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py --help
```
**Expected Output**:
```
usage: KevinTheAntagonizerClaudeCodeNotesMaker.py [-h] -scan SCAN_FOLDERS
                                                   [-recursive] [-workers WORKERS]
                                                   [-batch-size BATCH_SIZE]
                                                   ...

KevinTheAntagonizerClaudeCodeNotesMaker - Synthesize technical course transcripts

Required arguments:
  -scan SCAN_FOLDERS    Folder to scan for .srt files (repeatable)
...
```

**Example 2: Short form**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py -h
```
**Expected Output**: Same as Example 1

**Example 3: Combined with other arguments (help takes precedence)**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py --help -scan /courses
```
**Expected Output**: Help message displayed, -scan ignored, exits without processing

**Related Arguments**:
- [`--list-models`](#list-models) - Show available models
- [`--dry-run`](#dry-run) - Validate configuration
- [`-stats`](#stats) - Show database statistics

**Interaction Matrix**:

| Combined With | Result | Notes |
|---------------|--------|-------|
| Any argument | Help displayed, others ignored | Help always takes precedence |

**Error Messages**:

None - this argument cannot produce errors.

**Behavioral Notes**:

1. **Precedence**: `--help` has highest precedence - if present, all other arguments are ignored
2. **Exit Code**: Always exits with code 0 (even if invalid arguments are present)
3. **Output Format**: Uses argparse default formatting with custom description
4. **No Side Effects**: Does not create files, modify database, or initialize logging

**Source Code References**:
- Definition: `KevinTheAntagonizerClaudeCodeNotesMaker.py:329-332`
- Parser creation: `KevinTheAntagonizerClaudeCodeNotesMaker.py:276-334`

---

### <a id="list-models"></a>--list-models

**Category**: Information & Help
**Type**: Boolean flag
**Synopsis**: `--list-models`
**Default**: Not set

**Description**:

Displays all available Claude models with their official API identifiers and descriptions. Uses dynamic model discovery from Claude Code CLI if available, otherwise falls back to built-in list. Exits immediately after displaying models (no processing occurs).

**Valid Values**:
- No value required (flag argument)

**Validation Rules**:
1. Cannot be combined with processing arguments (-scan, -recursive, etc.)
2. Can be combined with -model to validate model name
3. Always exits with code 0 after displaying
4. Queries Claude Code CLI for latest model list

**Examples**:

**Example 1: List all available models**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py --list-models
```
**Expected Output**:
```
[AVAILABLE MODELS]

Available Claude models:
  - haiku          → claude-3-haiku-20240307
  - sonnet         → claude-3-sonnet-20240229
  - opus           → claude-3-opus-20240229
  - sonnet-3.5     → claude-3-5-sonnet-20241022
  - sonnet-4.5     → claude-sonnet-4-5-20250929 (default)

Models discovered from: Claude Code CLI

To use a model:
  python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan /path -model opus
```

**Example 2: Combined with -model (validation)**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py --list-models -model opus
```
**Expected Output**: Model list displayed, -model ignored (--list-models takes precedence)

**Example 3: Fallback to built-in list (if CLI unavailable)**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py --list-models
```
**Expected Output** (if claude-code CLI not found):
```
[AVAILABLE MODELS]

Available Claude models:
  - haiku          → claude-3-haiku-20240307
  - sonnet         → claude-3-sonnet-20240229
  - opus           → claude-3-opus-20240229
  - sonnet-3.5     → claude-3-5-sonnet-20241022
  - sonnet-4.5     → claude-sonnet-4-5-20250929 (default)

Models discovered from: Built-in list (Claude Code CLI not available)
```

**Example 4: Verify specific model exists**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py --list-models | grep opus
```
**Expected Output**:
```
  - opus           → claude-3-opus-20240229
```

**Related Arguments**:
- [`-model`](#model) - Select which model to use
- [`--help`](#help) - Show all arguments
- [`--dry-run`](#dry-run) - Validate configuration

**Interaction Matrix**:

| Combined With | Result | Notes |
|---------------|--------|-------|
| `--help` | Help displayed | --help has higher precedence |
| `-model <name>` | Models listed, -model ignored | --list-models takes precedence |
| `-scan <folder>` | Models listed, -scan ignored | Information display only |
| Any other argument | Models listed, others ignored | No processing occurs |

**Error Messages**:

**No errors** - this argument cannot fail. If Claude Code CLI is unavailable, falls back to built-in model list.

**Behavioral Notes**:

1. **Dynamic Discovery**: Attempts to query Claude Code CLI for latest models first
2. **Graceful Fallback**: If CLI unavailable, uses built-in AVAILABLE_MODELS dictionary
3. **Model Source Indication**: Clearly shows whether models came from CLI or built-in list
4. **Exit Code**: Always exits with code 0 (success)
5. **No Side Effects**: Does not create files, modify database, or initialize logging
6. **Future-Proof**: Automatically discovers new models as Anthropic releases them (if CLI available)

**Source Code References**:
- Definition: `KevinTheAntagonizerClaudeCodeNotesMaker.py:338-341`
- Model discovery logic: `KevinTheAntagonizerClaudeCodeNotesMaker.py:101-119` (AVAILABLE_MODELS)
- Model listing function: `KevinTheAntagonizerClaudeCodeNotesMaker.py:937-959`

---

## Required Processing Arguments

---

### <a id="scan"></a>-scan

**Category**: Required Processing
**Type**: String (directory path, repeatable)
**Synopsis**: `-scan <folder> [-scan <folder> ...]`
**Default**: None (required argument)

**Description**:

Specifies one or more folders to scan for `.srt` (SubRip subtitle) files. This is the only required argument for processing. Can be specified multiple times to scan multiple folders in a single run. Each folder is scanned independently, and all discovered `.srt` files are added to the processing queue.

**Valid Values**:
- **Absolute paths**: `E:\Courses\Java`, `/home/user/courses`
- **Relative paths**: `./courses`, `../transcripts`
- **Windows paths**: `C:\Users\Name\Documents\Courses`
- **Linux/Mac paths**: `/var/data/courses`, `~/Documents/courses`
- **Paths with spaces**: `"E:\My Courses\Java Programming"` (use quotes)
- **Multiple folders**: `-scan /path1 -scan /path2 -scan /path3`

**Validation Rules**:
1. **Must exist**: Folder must be a valid, existing directory
2. **Must be readable**: User must have read permissions
3. **Must be a directory**: Cannot be a file
4. **Cannot be empty string**: `-scan ""` is invalid
5. **Path normalization**: Trailing slashes are automatically handled
6. **Duplicate detection**: Same folder specified multiple times is allowed (processed once)

**Examples**:

**Example 1: Single folder (Windows)**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan "E:\Courses\Java Fundamentals"
```
**Expected Behavior**:
- Scans `E:\Courses\Java Fundamentals` (non-recursive by default)
- Finds all `.srt` files in that folder only (not subfolders)
- Adds tasks to database
- Processes files sequentially

**Example 2: Multiple folders**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/java \
  -scan /courses/python \
  -scan /courses/docker
```
**Expected Behavior**:
- Scans all three folders
- Combines all `.srt` files into single processing queue
- Processes files from all folders in sequence

**Example 3: Folder with spaces (requires quotes)**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan "E:\My Documents\Technical Courses\Spring Boot"
```
**Expected Behavior**:
- Correctly handles spaces in path
- Scans the folder successfully

**Example 4: Recursive scanning**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive
```
**Expected Behavior**:
- Scans `/courses` and ALL subfolders recursively
- Finds `.srt` files at any depth
- Example: `/courses/java/module1/lecture.srt`, `/courses/java/module2/intro.srt`

**Example 5: Relative path**
```bash
cd /home/user/courses
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan ./java
```
**Expected Behavior**:
- Scans `/home/user/courses/java`
- Relative to current working directory

**Example 6: ERROR - folder doesn't exist**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /nonexistent/folder
```
**Expected Output**:
```
ERROR: Scan folder does not exist or is not accessible: /nonexistent/folder
```
**Exit Code**: 1

**Related Arguments**:
- [`-recursive`](#recursive) - Scan subfolders recursively
- [`-workers`](#workers) - Process files in parallel
- [`-batch-size`](#batch-size) - Control batch size
- [`--dry-run`](#dry-run) - Validate without processing

**Interaction Matrix**:

| Combined With | Result | Example |
|---------------|--------|---------|
| `-recursive` | Scans all subfolders | `-scan /courses -recursive` |
| `-workers 4` | Processes files with 4 parallel workers | `-scan /courses -workers 4` |
| `-batch-size 5` | Processes in batches of 5 files | `-scan /courses -batch-size 5` |
| `--dry-run` | Shows files found without processing | `-scan /courses --dry-run` |
| `-retry-failed` | Ignores -scan, retries existing failed tasks | `-scan` ignored |
| `-stats` | Ignores -scan, shows stats only | `-scan` ignored |
| `-list-failed` | Ignores -scan, lists failed tasks only | `-scan` ignored |

**Error Messages**:

**Error 1: Folder doesn't exist**
```
ERROR: Scan folder does not exist or is not accessible: /path/to/folder
```
**Cause**: Path doesn't exist or has typo
**Solution**: Verify path, check for typos, use absolute path

**Error 2: Not a directory (is a file)**
```
ERROR: Scan folder is not a directory: /path/to/file.srt
```
**Cause**: Specified a file instead of a folder
**Solution**: Specify the parent directory containing .srt files

**Error 3: Permission denied**
```
ERROR: Scan folder does not exist or is not accessible: /root/courses
```
**Cause**: No read permissions for folder
**Solution**: Check file permissions, run with appropriate user

**Error 4: Missing argument value**
```
usage: KevinTheAntagonizerClaudeCodeNotesMaker.py: error: argument -scan: expected one argument
```
**Cause**: `-scan` specified without folder path
**Solution**: Provide folder path: `-scan /path/to/folder`

**Error 5: Required argument missing**
```
usage: KevinTheAntagonizerClaudeCodeNotesMaker.py: error: the following arguments are required: -scan
```
**Cause**: Tried to run without -scan argument
**Solution**: Add at least one -scan argument (unless using -stats, -list-failed, -retry-failed, or --list-models)

**Behavioral Notes**:

1. **File Discovery**: Only finds files with `.srt` extension (case-sensitive on Linux/Mac, case-insensitive on Windows)
2. **Existing Notes Skip**: Automatically skips `.srt` files that already have corresponding `*_KevinTheAntagonizer_Notes.md` files
3. **Database Integration**: All discovered files are added to `synthesis_tasks.db` with status `pending`
4. **Duplicate Handling**: If same folder specified multiple times, files are only processed once (database unique constraint)
5. **Order**: Files are processed in order discovered (alphabetically within each folder)
6. **Empty Folders**: No error if folder contains no `.srt` files - simply shows "Found 0 files"
7. **Symlinks**: Follows symbolic links (be careful with recursive + symlinks)

**Source Code References**:
- Argument definition: `KevinTheAntagonizerClaudeCodeNotesMaker.py:289-296`
- Validation: `KevinTheAntagonizerClaudeCodeNotesMaker.py:343-372` (`validate_args()`)
- File scanning: `KevinTheAntagonizerClaudeCodeNotesMaker.py:868-903` (`build_file_inventory()`)
- Database task creation: `KevinTheAntagonizerClaudeCodeNotesMaker.py:968-988`

---

## Processing Options Arguments

---

### <a id="recursive"></a>-recursive

**Category**: Processing Options
**Type**: Boolean flag
**Synopsis**: `-recursive`
**Default**: `false` (off)

**Description**:

Enables recursive scanning of all subfolders within each `-scan` folder. Without this flag, only `.srt` files in the specified folder itself are scanned (subfolders are ignored). With this flag, the application descends into all subdirectories at any depth.

**Valid Values**:
- No value required (flag argument)

**Validation Rules**:
1. No validation needed (boolean flag)
2. Applies to all `-scan` folders specified
3. Can significantly increase number of files found
4. No depth limit - scans infinitely deep

**Examples**:

**Example 1: Basic recursive scan**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive
```
**Expected Behavior**:
```
/courses
  ├─ intro.srt                    ✓ Found
  ├─ module1/
  │   ├─ lecture1.srt             ✓ Found
  │   └─ lecture2.srt             ✓ Found
  ├─ module2/
  │   ├─ advanced/
  │   │   └─ deep_dive.srt        ✓ Found
  │   └─ basics.srt               ✓ Found
  └─ final_exam.srt               ✓ Found

Total found: 6 files
```

**Example 2: Without -recursive (default)**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses
```
**Expected Behavior**:
```
/courses
  ├─ intro.srt                    ✓ Found
  ├─ module1/
  │   ├─ lecture1.srt             ✗ Skipped (in subfolder)
  │   └─ lecture2.srt             ✗ Skipped (in subfolder)
  ├─ module2/
  │   ├─ advanced/
  │   │   └─ deep_dive.srt        ✗ Skipped (in subfolder)
  │   └─ basics.srt               ✗ Skipped (in subfolder)
  └─ final_exam.srt               ✓ Found

Total found: 2 files (only top-level)
```

**Example 3: Multiple folders, all recursive**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/java \
  -scan /courses/python \
  -scan /courses/docker \
  -recursive
```
**Expected Behavior**:
- Recursively scans ALL three folders
- Finds `.srt` files at any depth in all three folder trees

**Example 4: Large folder structure**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan "E:\Online Courses" \
  -recursive
```
**Expected Behavior**:
```
Scanning folders recursively...
  - E:\Online Courses
    Found 1,247 .srt files across all subfolders
```

**Related Arguments**:
- [`-scan`](#scan) - Specifies folders to scan
- [`-workers`](#workers) - Speed up processing of many files
- [`-batch-size`](#batch-size) - Control batch size for large sets
- [`--dry-run`](#dry-run) - See what would be found without processing

**Interaction Matrix**:

| Combined With | Result | Notes |
|---------------|--------|-------|
| `-scan <folder>` | Scans folder + all subfolders | Required combination |
| `-workers 4` | Processes many files in parallel | Recommended for large trees |
| `-batch-size 5` | Smaller batches for better checkpointing | Good for very large sets |
| `--dry-run` | Shows all files that would be found | Useful to verify scope |

**Error Messages**:

**No errors** - this flag cannot produce errors. If subfolders don't exist or are empty, they are simply skipped.

**Behavioral Notes**:

1. **Symlink Following**: Follows symbolic links (be careful of circular references)
2. **Performance Impact**: Can find thousands of files in deeply nested structures
3. **Memory Usage**: All file paths loaded into memory before processing
4. **Hidden Folders**: Includes hidden folders (folders starting with `.` on Linux/Mac)
5. **Recommended Combination**: Use with `-workers` for large folder trees
6. **Database Impact**: All found files added to database before processing starts

**Source Code References**:
- Argument definition: `KevinTheAntagonizerClaudeCodeNotesMaker.py:300-304`
- File scanning logic: `KevinTheAntagonizerClaudeCodeNotesMaker.py:868-903` (`build_file_inventory()`)

---

### <a id="workers"></a>-workers

**Category**: Processing Options
**Type**: Integer
**Synopsis**: `-workers <num>`
**Default**: `1` (sequential processing)

**Description**:

Specifies the number of parallel workers to use for concurrent file processing. Each worker processes files simultaneously, dramatically speeding up large batch jobs. Value of 1 means sequential (one file at a time).

**Valid Values**:
- **Minimum**: `1` (sequential, no parallelization)
- **Recommended**: `4` (optimal for most systems)
- **Maximum**: `8` (practical limit for stability)
- **Absolute max**: `16` (not recommended, may cause issues)

**Validation Rules**:
1. Must be a positive integer
2. Must be ≥ 1
3. Recommended: 1-8 workers
4. Values > 8 may cause rate limiting or instability

**Examples**:

**Example 1: Sequential processing (default)**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -workers 1
```
**Expected Behavior**:
- Processes one file at a time
- Safest option, lowest API load
- Slowest throughput
- Example: 100 files at 2 min/file = 200 minutes

**Example 2: Recommended parallel (4 workers)**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  -workers 4
```
**Expected Behavior**:
- Processes 4 files simultaneously
- Optimal balance of speed and stability
- Example: 100 files at 2 min/file = 50 minutes (4x speedup)

**Example 3: Maximum recommended (8 workers)**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  -workers 8 \
  -batch-size 10
```
**Expected Behavior**:
- Processes 8 files simultaneously
- Fastest throughput
- May hit rate limits on some accounts
- Example: 100 files at 2 min/file = 25 minutes (8x speedup)

**Example 4: ERROR - invalid value**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -workers 0
```
**Expected Output**:
```
ERROR: Workers must be at least 1 (got: 0)
```
**Exit Code**: 1

**Example 5: Small dataset (workers > files)**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /small-course \
  -workers 8
```
**Expected Behavior**:
- Only 3 .srt files found
- Only 3 workers actually used (others idle)
- No benefit from 8 workers, same as `-workers 3`

**Related Arguments**:
- [`-scan`](#scan) - Specifies what to process
- [`-recursive`](#recursive) - Find more files to parallelize
- [`-batch-size`](#batch-size) - Control checkpointing frequency
- [`--dry-run`](#dry-run) - Validate without processing

**Interaction Matrix**:

| Combined With | Result | Notes |
|---------------|--------|-------|
| `-batch-size 10` | 10 files per batch across N workers | Recommended |
| `-recursive` | Parallel processing of large file sets | Highly recommended |
| `-model haiku` | Fast model + parallel = maximum speed | Cost-effective |
| `-model opus` | Slow model + parallel = moderate speedup | Higher cost |

**Error Messages**:

**Error 1: Invalid worker count (zero or negative)**
```
ERROR: Workers must be at least 1 (got: 0)
```
**Cause**: Specified 0 or negative number
**Solution**: Use positive integer (recommended: 1-8)

**Error 2: Invalid type (not an integer)**
```
usage: KevinTheAntagonizerClaudeCodeNotesMaker.py: error: argument -workers: invalid int value: 'four'
```
**Cause**: Used word instead of number
**Solution**: Use numeric value: `-workers 4`

**Behavioral Notes**:

1. **Rate Limiting**: More workers = higher API request rate, may trigger rate limits
2. **Cost Impact**: Parallel processing doesn't reduce costs, only time
3. **Progress Display**: Shows progress bars for each worker (future feature)
4. **Resource Usage**: Each worker uses ~50-100MB memory
5. **Database Locking**: SQLite handles concurrent updates safely
6. **Error Isolation**: One worker failure doesn't affect others
7. **Optimal Value**: 4 workers for most use cases
8. **Diminishing Returns**: Beyond 8 workers, minimal speed improvement

**Source Code References**:
- Argument definition: `KevinTheAntagonizerClaudeCodeNotesMaker.py:306-313`
- Validation: `KevinTheAntagonizerClaudeCodeNotesMaker.py:343-372`
- Worker implementation: Planned for future release (currently sequential)

---

### <a id="batch-size"></a>-batch-size

**Category**: Processing Options
**Type**: Integer
**Synopsis**: `-batch-size <num>`
**Default**: `10` files per batch

**Description**:

Controls how many files are processed before showing progress update and performing database checkpoint. Smaller batches provide more frequent feedback and better error recovery. Larger batches reduce overhead but provide less frequent updates.

**Valid Values**:
- **Minimum**: `1` (show progress after each file)
- **Recommended**: `10` (good balance)
- **Large datasets**: `5` (better recovery)
- **Small datasets**: `20` (less overhead)
- **Maximum**: `100` (not recommended)

**Validation Rules**:
1. Must be a positive integer
2. Must be ≥ 1
3. Recommended: 5-20 files per batch
4. No hard upper limit, but >100 not recommended

**Examples**:

**Example 1: Default batch size**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -batch-size 10
```
**Expected Output**:
```
[BATCH 1/5] Processing files 1-10...
  ✓ Completed: 10/10 (100%)

[BATCH 2/5] Processing files 11-20...
  ✓ Completed: 20/20 (100%)

...
```

**Example 2: Small batches for better feedback**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /large-library \
  -recursive \
  -batch-size 5
```
**Expected Behavior**:
- Progress updates every 5 files
- Better error recovery (only lose 5 files max if crashed)
- More database checkpoints
- Slightly more overhead

**Example 3: Large batches for small datasets**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /small-course \
  -batch-size 20
```
**Expected Behavior**:
- Only 15 files total
- Processed in single batch (15 < 20)
- One progress update at end

**Example 4: Batch size 1 (maximum feedback)**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -batch-size 1
```
**Expected Output**:
```
[BATCH 1/100] Processing file 1...
  ✓ Completed: lecture1.srt

[BATCH 2/100] Processing file 2...
  ✓ Completed: lecture2.srt

...
```
**Use Case**: Debugging, watching each file closely

**Example 5: ERROR - invalid batch size**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -batch-size 0
```
**Expected Output**:
```
ERROR: Batch size must be at least 1 (got: 0)
```
**Exit Code**: 1

**Related Arguments**:
- [`-workers`](#workers) - Parallel processing across workers
- [`-scan`](#scan) - Specifies files to batch
- [`-recursive`](#recursive) - May find many files requiring batching

**Interaction Matrix**:

| Combined With | Result | Notes |
|---------------|--------|-------|
| `-workers 4` | Each worker processes in batches | 4 workers × 10 files = 40 concurrent |
| `-recursive` | Large file sets benefit from batching | Recommended |
| `--dry-run` | Shows batch structure without processing | Useful for planning |

**Error Messages**:

**Error 1: Invalid batch size (zero or negative)**
```
ERROR: Batch size must be at least 1 (got: 0)
```
**Cause**: Specified 0 or negative number
**Solution**: Use positive integer (recommended: 5-20)

**Error 2: Invalid type**
```
usage: KevinTheAntagonizerClaudeCodeNotesMaker.py: error: argument -batch-size: invalid int value: 'ten'
```
**Cause**: Used word instead of number
**Solution**: Use numeric value: `-batch-size 10`

**Behavioral Notes**:

1. **Progress Updates**: Database updated after each batch completes
2. **Checkpointing**: If application crashes, completed batches are saved
3. **Recovery**: On restart, only incomplete batch needs reprocessing
4. **Memory**: Batch size doesn't affect memory usage significantly
5. **Database Transactions**: Each batch is a transaction
6. **Optimal for Large Sets**: Use batch-size 5 for 500+ files
7. **Optimal for Small Sets**: Use batch-size 10-20 for <100 files
8. **Overhead**: Very small batches (1-2) have higher overhead

**Source Code References**:
- Argument definition: `KevinTheAntagonizerClaudeCodeNotesMaker.py:315-322`
- Validation: `KevinTheAntagonizerClaudeCodeNotesMaker.py:343-372`
- Batch processing logic: `KevinTheAntagonizerClaudeCodeNotesMaker.py:996-1026`

---

## Database Management Arguments

---

### <a id="db"></a>-db

**Category**: Database Management
**Type**: String (file path)
**Synopsis**: `-db <path>`
**Default**: `synthesis_tasks.db` (in current directory)

**Description**:

Specifies the path to the SQLite database file used for task tracking, progress management, and statistics. Allows using separate databases for different projects or organizing tasks by topic.

**Valid Values**:
- **Absolute path**: `E:\Projects\java_courses.db`, `/var/data/synthesis.db`
- **Relative path**: `./tasks.db`, `../databases/python_tasks.db`
- **Custom names**: `java.db`, `python.db`, `ml_courses.db`
- **Default**: `synthesis_tasks.db` (if argument not provided)

**Validation Rules**:
1. Path must be writable
2. Parent directory must exist
3. If file doesn't exist, it will be created automatically
4. SQLite database format (`.db` extension recommended but not required)

**Examples**:

**Example 1: Default database**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses
```
**Expected Behavior**:
- Uses `synthesis_tasks.db` in current directory
- Created automatically if doesn't exist

**Example 2: Custom database per project**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/java \
  -db java_courses.db
```
**Expected Behavior**:
- Creates/uses `java_courses.db`
- Keeps Java course progress separate from other projects

**Example 3: Absolute path**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -db "E:\Databases\Synthesis\all_courses.db"
```
**Expected Behavior**:
- Uses database at specified absolute path
- Parent folder `E:\Databases\Synthesis` must exist

**Example 4: Multiple projects strategy**
```bash
# Java courses
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/java \
  -db java.db

# Python courses
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/python \
  -db python.db

# ML courses
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/ml \
  -db ml.db
```
**Expected Behavior**:
- Three separate databases
- Each tracks its own progress independently
- Can run statistics on each separately

**Related Arguments**:
- [`-reset-db`](#reset-db) - Clear database and start fresh
- [`-stats`](#stats) - Show database statistics
- [`-list-failed`](#list-failed) - List failed tasks from database
- [`-retry-failed`](#retry-failed) - Retry failed tasks from database

**Interaction Matrix**:

| Combined With | Result | Notes |
|---------------|--------|-------|
| `-reset-db` | Clears specified database | Use with caution |
| `-stats` | Shows stats from specified database | Useful for checking project progress |
| `-retry-failed` | Retries failures from specified database | Project-specific retry |

**Error Messages**:

**Error 1: Parent directory doesn't exist**
```
ERROR: Database parent directory does not exist: /nonexistent/path/tasks.db
```
**Cause**: Tried to create database in folder that doesn't exist
**Solution**: Create parent directory first or use existing path

**Error 2: Permission denied**
```
ERROR: Cannot write to database path: /root/tasks.db (Permission denied)
```
**Cause**: No write permissions for specified location
**Solution**: Use writable location or adjust permissions

**Behavioral Notes**:

1. **Auto-Creation**: Database file created automatically if doesn't exist
2. **Schema**: Contains `tasks` and `processing_stats` tables
3. **Concurrent Access**: SQLite handles concurrent reads, limited concurrent writes
4. **Portability**: Database files are portable across systems
5. **Backup**: Easy to backup (copy .db file)
6. **Size**: Typically <10MB for 1000 files

**Source Code References**:
- Argument definition: `KevinTheAntagonizerClaudeCodeNotesMaker.py:326-330`
- Database manager: `KevinTheAntagonizerClaudeCodeNotesMaker.py:378-558` (DatabaseManager class)
- Schema creation: `KevinTheAntagonizerClaudeCodeNotesMaker.py:404-434`

---

### <a id="reset-db"></a>-reset-db

**Category**: Database Management
**Type**: Boolean flag
**Synopsis**: `-reset-db`
**Default**: Not set

**Description**:

**⚠️ DESTRUCTIVE OPERATION** - Drops all tables from the database and recreates them, effectively clearing all task history, progress, and statistics. Use when starting completely fresh or to fix database corruption.

**Valid Values**:
- No value required (flag argument)

**Validation Rules**:
1. Requires confirmation (safety measure)
2. Cannot be undone
3. All task history is lost
4. Must specify `-scan` or other processing argument to proceed after reset

**Examples**:

**Example 1: Reset and start fresh**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -reset-db \
  -scan /courses
```
**Expected Behavior**:
- Drops and recreates all database tables
- Clears all previous task history
- Begins fresh scan and processing

**Example 2: Reset specific project database**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -reset-db \
  -db java_courses.db \
  -scan /courses/java
```
**Expected Behavior**:
- Resets only `java_courses.db`
- Other databases (python.db, ml.db) unaffected

**Example 3: Reset without processing (just clear)**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -reset-db \
  -stats
```
**Expected Behavior**:
- Database cleared
- Shows empty statistics
- No processing occurs

**Related Arguments**:
- [`-db`](#db) - Specify which database to reset
- [`-scan`](#scan) - Resume processing after reset
- [`-stats`](#stats) - Verify database is empty after reset

**Interaction Matrix**:

| Combined With | Result | Notes |
|---------------|--------|-------|
| `-db custom.db` | Resets only specified database | Safe for multi-project setups |
| `-scan /courses` | Reset then process | Common workflow |
| `-stats` | Reset then show empty stats | Verification |

**Error Messages**:

**No errors** - this operation always succeeds (database recreated even if corrupt).

**Behavioral Notes**:

1. **⚠️ IRREVERSIBLE**: All task history permanently deleted
2. **No Confirmation Prompt**: Executes immediately when flag present
3. **Backup Recommendation**: Backup .db file before using this flag
4. **Schema Preserved**: Table structure recreated (only data deleted)
5. **File Exists**: Database file still exists after reset (just empty)
6. **Alternative**: Instead of `-reset-db`, consider deleting `.db` file and starting fresh

**Source Code References**:
- Argument definition: `KevinTheAntagonizerClaudeCodeNotesMaker.py:332-336`
- Reset logic: `KevinTheAntagonizerClaudeCodeNotesMaker.py:392-402` (DatabaseManager.reset())

---

### <a id="list-failed"></a>-list-failed

**Category**: Database Management
**Type**: Boolean flag
**Synopsis**: `-list-failed`
**Default**: Not set

**Description**:

Displays all tasks with status `failed` from the database, showing lecture names, error messages, attempt counts, and timestamps. Useful for diagnosing issues and identifying files that need manual review. Exits immediately after listing (no processing).

**Valid Values**:
- No value required (flag argument)

**Validation Rules**:
1. Database must exist
2. Exits after listing (no other operations performed)
3. Shows empty list if no failures

**Examples**:

**Example 1: List all failures**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py -list-failed
```
**Expected Output**:
```
[FAILED TASKS]

Total failed: 5

1. lecture_42_advanced_patterns.srt
   Course: Spring Boot Advanced
   Attempts: 3
   Error: Quality check failed (score: 0.42/0.70)
   Last attempt: 2025-11-27 14:32:15

2. lecture_18_microservices.srt
   Course: Docker & Kubernetes
   Attempts: 3
   Error: Claude API timeout after 120 seconds
   Last attempt: 2025-11-27 13:18:42

...
```

**Example 2: List failures from specific database**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -list-failed \
  -db java_courses.db
```
**Expected Output**: Shows only failures from `java_courses.db`

**Example 3: No failures**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py -list-failed
```
**Expected Output**:
```
[FAILED TASKS]

Total failed: 0

All tasks completed successfully! ✓
```

**Example 4: Pipe to file for review**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -list-failed > failures.txt
```
**Expected Behavior**: Saves failure list to `failures.txt` for review

**Related Arguments**:
- [`-retry-failed`](#retry-failed) - Retry all failed tasks
- [`-stats`](#stats) - Show complete statistics including failure rate
- [`-db`](#db) - Specify database to query

**Interaction Matrix**:

| Combined With | Result | Notes |
|---------------|--------|-------|
| `-db custom.db` | Lists failures from specified database | Multi-project support |
| `-retry-failed` | Lists first, then retries | Both operations executed |
| `-stats` | Lists failures, then shows stats | Comprehensive view |

**Error Messages**:

**Error 1: Database doesn't exist**
```
ERROR: Database file not found: synthesis_tasks.db
```
**Cause**: No database file (no tasks processed yet)
**Solution**: Run processing first to create database

**Behavioral Notes**:

1. **Exit After Listing**: Always exits (no processing after displaying list)
2. **Sorted by Timestamp**: Most recent failures first
3. **Full Error Messages**: Shows complete error text for diagnosis
4. **Attempt Counter**: Shows how many retry attempts were made
5. **Export-Friendly**: Output format suitable for piping to files
6. **Empty List OK**: No error if zero failures (shows success message)

**Source Code References**:
- Argument definition: `KevinTheAntagonizerClaudeCodeNotesMaker.py:338-342`
- Listing logic: `KevinTheAntagonizerClaudeCodeNotesMaker.py:960-975` (main.py list_failed handling)

---

### <a id="retry-failed"></a>-retry-failed

**Category**: Database Management
**Type**: Boolean flag
**Synopsis**: `-retry-failed`
**Default**: Not set

**Description**:

Retries all tasks with status `failed` in the database. Resets their status to `pending` and reprocesses them. Useful for retrying failures after fixing issues (e.g., network problems, quality tuning). Ignores `-scan` argument if specified.

**Valid Values**:
- No value required (flag argument)

**Validation Rules**:
1. Database must exist
2. Ignores `-scan` folders (retries from database only)
3. Can specify different model for retry (e.g., upgrade to opus)
4. Respects max attempts limit (default: 3 per file)

**Examples**:

**Example 1: Retry all failures**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py -retry-failed
```
**Expected Behavior**:
```
[RETRY FAILED TASKS]

Found 5 failed tasks. Retrying...

Processing: lecture_42_advanced_patterns.srt
  ✓ Success! Quality score: 0.85

Processing: lecture_18_microservices.srt
  ✓ Success! Quality score: 0.78

...

Retry summary:
  - Succeeded: 4/5
  - Failed again: 1/5
```

**Example 2: Retry with premium model**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus
```
**Expected Behavior**:
- Retries all failures using Claude Opus (highest quality)
- May improve quality scores
- Higher cost per retry

**Example 3: Retry specific project failures**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -db java_courses.db \
  -model sonnet-4.5
```
**Expected Behavior**:
- Retries only failures from `java_courses.db`
- Uses sonnet-4.5 model

**Example 4: Retry with custom system prompt**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -system-prompt python_expert.txt
```
**Expected Behavior**:
- Retries with different expert persona
- May improve quality for specific topics

**Related Arguments**:
- [`-list-failed`](#list-failed) - See what will be retried
- [`-model`](#model) - Use different model for retry
- [`-system-prompt`](#system-prompt) - Use different persona for retry
- [`-db`](#db) - Specify database to retry from

**Interaction Matrix**:

| Combined With | Result | Notes |
|---------------|--------|-------|
| `-scan /courses` | -scan ignored, retries from database | Database takes precedence |
| `-model opus` | Retries with premium model | Quality improvement strategy |
| `-system-prompt <file>` | Retries with custom persona | Topic-specific expertise |
| `-db custom.db` | Retries from specified database | Multi-project support |

**Error Messages**:

**Error 1: No failed tasks**
```
[RETRY FAILED TASKS]

No failed tasks found in database. Nothing to retry.
```
**Cause**: All tasks completed successfully
**Solution**: No action needed

**Error 2: Database doesn't exist**
```
ERROR: Database file not found: synthesis_tasks.db
```
**Cause**: No database (no processing done yet)
**Solution**: Run initial processing first

**Behavioral Notes**:

1. **Attempt Counter**: Increments attempt count for each retry
2. **Max Attempts**: Stops retrying after 3 attempts (prevents infinite loops)
3. **Quality Improvement**: Often succeeds on retry due to API variability
4. **Cost-Effective Strategy**: Retry with same model first, then upgrade if still failing
5. **Batch Processing**: Retries use same batch-size as regular processing
6. **Progress Tracking**: Shows progress for retry operations

**Source Code References**:
- Argument definition: `KevinTheAntagonizerClaudeCodeNotesMaker.py:344-348`
- Retry logic: `KevinTheAntagonizerClaudeCodeNotesMaker.py:990-1020`

---

### <a id="stats"></a>-stats

**Category**: Database Management
**Type**: Boolean flag
**Synopsis**: `-stats`
**Default**: Not set

**Description**:

Displays comprehensive statistics from the database including total tasks, completion rate, failure rate, average quality scores, token usage, and processing time. Useful for monitoring progress and identifying issues. Exits after displaying stats (no processing).

**Valid Values**:
- No value required (flag argument)

**Validation Rules**:
1. Database must exist
2. Exits after displaying (no other operations)
3. Shows empty stats if database has no tasks

**Examples**:

**Example 1: Basic statistics**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats
```
**Expected Output**:
```
[DATABASE STATISTICS]

Total Tasks:        245
  - Completed:      187 (76.3%)
  - Failed:         12 (4.9%)
  - Pending:        46 (18.8%)

Quality Metrics:
  - Average Score:  0.82 (82%)
  - Min Score:      0.65
  - Max Score:      0.95

Token Usage:
  - Total:          1,247,582 tokens
  - Average/File:   6,670 tokens

Processing Time:
  - Completed:      187 files in 6.2 hours
  - Average/File:   2.0 minutes

Database: synthesis_tasks.db
Last Updated: 2025-11-27 15:45:32
```

**Example 2: Stats from specific project**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -stats \
  -db java_courses.db
```
**Expected Output**: Shows stats only from `java_courses.db`

**Example 3: Empty database**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats
```
**Expected Output**:
```
[DATABASE STATISTICS]

Total Tasks: 0

Database is empty. No tasks processed yet.
```

**Example 4: Export stats to file**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats > progress.txt
```
**Expected Behavior**: Saves statistics to `progress.txt`

**Related Arguments**:
- [`-list-failed`](#list-failed) - Detailed failure information
- [`-db`](#db) - Specify database to query
- [`-retry-failed`](#retry-failed) - Retry failures to improve stats

**Interaction Matrix**:

| Combined With | Result | Notes |
|---------------|--------|-------|
| `-db custom.db` | Stats from specified database | Multi-project tracking |
| `-list-failed` | Shows stats, then lists failures | Comprehensive view |
| `-scan /courses` | Stats shown, then processing starts | Pre-check before processing |

**Error Messages**:

**Error 1: Database doesn't exist**
```
ERROR: Database file not found: synthesis_tasks.db
```
**Cause**: No database (no processing yet)
**Solution**: Run processing first to create database

**Behavioral Notes**:

1. **Real-Time**: Always shows current state (not cached)
2. **Percentages**: Includes percentage breakdowns
3. **Quality Trends**: Shows average quality score
4. **Token Economics**: Estimates API cost based on token usage
5. **Performance Metrics**: Processing speed statistics
6. **Export-Friendly**: Clean format for reports

**Source Code References**:
- Argument definition: `KevinTheAntagonizerClaudeCodeNotesMaker.py:350-354`
- Statistics calculation: `KevinTheAntagonizerClaudeCodeNotesMaker.py:524-558` (DatabaseManager.get_statistics())

---

## Advanced Options Arguments

---

### <a id="system-prompt"></a>-system-prompt

**Category**: Advanced Options
**Type**: String (file path)
**Synopsis**: `-system-prompt <file>`
**Default**: Built-in Kevin Burleigh persona

**Description**:

Overrides the default Kevin Burleigh system prompt with a custom expert persona from a text file. Allows tailoring the synthesis style, tone, and expertise to match specific course topics (e.g., Python expert, ML researcher, DevOps engineer).

**Valid Values**:
- **Absolute path**: `E:\Prompts\python_expert.txt`, `/home/user/prompts/ml_expert.txt`
- **Relative path**: `./custom_prompt.txt`, `../prompts/data_scientist.txt`
- **File must exist**: Non-existent files cause error
- **Plain text**: UTF-8 encoded text file

**Validation Rules**:
1. File must exist and be readable
2. File must not be empty
3. Recommended: 200-1000 words
4. Should define expert persona, tone, and focus areas

**Examples**:

**Example 1: Python expert persona**
```bash
# Create custom prompt
cat > python_expert.txt << 'EOF'
You are a senior Python developer with 15+ years of experience in data science,
machine learning, and scientific computing. Your expertise includes:
- NumPy, Pandas, SciPy, scikit-learn
- Deep learning (PyTorch, TensorFlow)
- Production Python (FastAPI, Flask, Django)
- Best practices and Pythonic code

When analyzing lectures, focus on:
- Python-specific idioms and patterns
- Performance optimization techniques
- Real-world production gotchas
- Integration with ML pipelines
EOF

# Use custom prompt
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/python \
  -system-prompt python_expert.txt
```

**Example 2: ML researcher persona**
```bash
echo "You are an ML research scientist specializing in transformers,
attention mechanisms, and modern deep learning architectures..." > ml_expert.txt

python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/transformers \
  -system-prompt ml_expert.txt
```

**Example 3: DevOps engineer persona**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/kubernetes \
  -system-prompt devops_expert.txt \
  -model opus
```
**Expected Behavior**:
- Uses DevOps-focused expert persona
- Premium model for highest quality
- Notes emphasize container orchestration, CI/CD, infrastructure

**Example 4: ERROR - file doesn't exist**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -system-prompt nonexistent.txt
```
**Expected Output**:
```
ERROR: System prompt file not found: nonexistent.txt
```
**Exit Code**: 1

**Example 5: Different personas per project**
```bash
# Java courses with Java expert
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/java \
  -system-prompt java_expert.txt \
  -db java.db

# Python courses with Python expert
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses/python \
  -system-prompt python_expert.txt \
  -db python.db
```

**Related Arguments**:
- [`-model`](#model) - Model selection affects persona effectiveness
- [`-retry-failed`](#retry-failed) - Retry failures with different persona
- [`--dry-run`](#dry-run) - Test configuration before processing

**Interaction Matrix**:

| Combined With | Result | Notes |
|---------------|--------|-------|
| `-model opus` | Custom persona + premium model | Best quality combination |
| `-retry-failed` | Retry failures with new persona | Topic-specific expertise |
| `-db custom.db` | Custom persona per project | Multi-project support |

**Error Messages**:

**Error 1: File not found**
```
ERROR: System prompt file not found: custom_prompt.txt
```
**Cause**: File doesn't exist or path is wrong
**Solution**: Verify file exists, use absolute path

**Error 2: File is empty**
```
ERROR: System prompt file is empty: custom_prompt.txt
```
**Cause**: File has no content
**Solution**: Add expert persona description to file

**Error 3: Permission denied**
```
ERROR: Cannot read system prompt file: /root/prompt.txt (Permission denied)
```
**Cause**: No read permissions
**Solution**: Adjust file permissions or use accessible location

**Behavioral Notes**:

1. **Complete Replacement**: Overrides default Kevin persona entirely
2. **Quality Impact**: Well-crafted prompts significantly improve output quality
3. **Topic Specificity**: More specific personas produce better results
4. **Length Recommendation**: 200-1000 words optimal
5. **Prompt Engineering**: Include examples, tone guidance, focus areas
6. **Cost-Effective Strategy**: Test with haiku first, then upgrade model if needed

**Prompt Writing Tips**:

```markdown
## Good Custom Prompt Structure:

1. **Identity**: "You are a [role] with [years] experience in [domain]"
2. **Expertise**: List specific technologies, frameworks, concepts
3. **Tone**: "Professional but approachable", "Academic and rigorous", etc.
4. **Focus Areas**: What to emphasize in analysis
5. **Output Format**: Markdown structure preferences
6. **Examples**: Show desired style with 1-2 examples

## Poor Prompts:
- Too short (<100 words)
- Vague ("You are an expert")
- No specific expertise listed
- No tone guidance
```

**Source Code References**:
- Argument definition: `KevinTheAntagonizerClaudeCodeNotesMaker.py:356-361`
- Prompt loading: `KevinTheAntagonizerClaudeCodeNotesMaker.py:679-715` (NoteSynthesisEngine)
- Default prompt: `KevinTheAntagonizerClaudeCodeNotesMaker.py:101-119` (Config.DEFAULT_SYSTEM_PROMPT)

---

### <a id="model"></a>-model

**Category**: Advanced Options
**Type**: String (model name)
**Synopsis**: `-model <name>`
**Default**: `sonnet-4.5`

**Description**:

Selects which Claude model to use for synthesis. Different models offer tradeoffs between speed, cost, and quality. Sonnet-4.5 (default) provides best overall balance. Use haiku for cost-effective bulk processing, opus for premium quality.

**Valid Values**:
- `haiku` - Claude 3 Haiku (fastest, cheapest, good quality)
- `sonnet` - Claude 3 Sonnet (balanced)
- `sonnet-3.5` - Claude 3.5 Sonnet (better than opus)
- `sonnet-4.5` - Claude Sonnet 4.5 (latest, best, DEFAULT)
- `opus` - Claude 3 Opus (premium, highest quality)

**Validation Rules**:
1. Must be one of the available models
2. Case-sensitive (lowercase only)
3. Use `--list-models` to see current options
4. New models discovered automatically from Claude Code CLI

**Examples**:

**Example 1: Default model (sonnet-4.5)**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses
```
**Expected Behavior**:
- Uses Claude Sonnet 4.5 (latest)
- Best overall quality/cost balance
- ~2-3 minutes per file

**Example 2: Budget processing (haiku)**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  -model haiku
```
**Expected Behavior**:
- Uses Claude Haiku (cheapest)
- Faster processing (~1 minute per file)
- Good quality (may have some lower quality outputs)
- Cost-effective for large batches

**Example 3: Premium quality (opus)**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /important-courses \
  -model opus
```
**Expected Behavior**:
- Uses Claude Opus (premium)
- Highest quality output
- Slower (~3-4 minutes per file)
- Higher cost

**Example 4: Two-tier strategy**
```bash
# Phase 1: Bulk with haiku
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -model haiku

# Phase 2: Check quality
python KevinTheAntagonizerClaudeCodeNotesMaker.py -stats

# Phase 3: Retry low-quality with opus
sqlite3 synthesis_tasks.db \
  "UPDATE tasks SET status='pending' WHERE quality_score < 0.7"

python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -retry-failed \
  -model opus
```
**Expected Behavior**:
- Cost-effective: Most files with cheap model
- Quality assurance: Upgrade only low-quality results

**Example 5: ERROR - invalid model**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -model gpt-4
```
**Expected Output**:
```
ERROR: Invalid model 'gpt-4'. Available models:
  - haiku
  - sonnet
  - opus
  - sonnet-3.5
  - sonnet-4.5

Use --list-models to see all options.
```
**Exit Code**: 1

**Model Comparison**:

| Model | Speed | Cost | Quality | Best For |
|-------|-------|------|---------|----------|
| haiku | ⚡⚡⚡ | 💰 | ⭐⭐⭐ | Bulk processing, cost-conscious |
| sonnet | ⚡⚡ | 💰💰 | ⭐⭐⭐⭐ | General use |
| sonnet-3.5 | ⚡⚡ | 💰💰 | ⭐⭐⭐⭐⭐ | High quality at good price |
| sonnet-4.5 | ⚡⚡ | 💰💰 | ⭐⭐⭐⭐⭐ | **DEFAULT** - Best overall |
| opus | ⚡ | 💰💰💰 | ⭐⭐⭐⭐⭐ | Critical content, retries |

**Related Arguments**:
- [`--list-models`](#list-models) - See all available models
- [`-retry-failed`](#retry-failed) - Retry with different model
- [`-system-prompt`](#system-prompt) - Custom persona per model

**Interaction Matrix**:

| Combined With | Result | Notes |
|---------------|--------|-------|
| `-workers 8` | Fast model + parallel = maximum speed | haiku recommended |
| `-retry-failed` | Upgrade model for failures | Common quality strategy |
| `-system-prompt <file>` | Custom persona + premium model | Best quality |

**Error Messages**:

**Error 1: Invalid model name**
```
ERROR: Invalid model 'sonnet-4'. Available models: haiku, sonnet, opus, sonnet-3.5, sonnet-4.5
```
**Cause**: Typo or non-existent model
**Solution**: Use `--list-models` to see valid options

**Error 2: Model name case-sensitive**
```
ERROR: Invalid model 'OPUS'. Available models: haiku, sonnet, opus, sonnet-3.5, sonnet-4.5
```
**Cause**: Used uppercase
**Solution**: Use lowercase: `-model opus`

**Behavioral Notes**:

1. **Dynamic Discovery**: New models added automatically (from Claude Code CLI)
2. **Cost Impact**: Model choice is biggest cost factor
3. **Quality Variability**: Same model may produce different quality across runs
4. **Speed Estimates**: Actual speed varies by transcript length
5. **Default Reasoning**: sonnet-4.5 chosen for best quality/cost balance

**Source Code References**:
- Argument definition: `KevinTheAntagonizerClaudeCodeNotesMaker.py:363-370`
- Model validation: `KevinTheAntagonizerClaudeCodeNotesMaker.py:343-372`
- Available models: `KevinTheAntagonizerClaudeCodeNotesMaker.py:101-119` (AVAILABLE_MODELS)

---

### <a id="dry-run"></a>--dry-run

**Category**: Advanced Options
**Type**: Boolean flag
**Synopsis**: `--dry-run`
**Default**: Not set

**Description**:

Validation mode that shows what would be processed without actually performing synthesis. Displays configuration, scans for files, shows batch structure, but exits before calling Claude API. Useful for verifying setup before expensive processing runs.

**Valid Values**:
- No value required (flag argument)

**Validation Rules**:
1. All other arguments still validated
2. File scanning still performed
3. Database operations still occur (tasks added as pending)
4. No synthesis or API calls made

**Examples**:

**Example 1: Validate configuration**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -recursive \
  -workers 4 \
  -batch-size 10 \
  --dry-run
```
**Expected Output**:
```
[CONFIGURATION]

Scan Folders:
  - /courses (recursive)

Processing Options:
  - Workers:     4
  - Batch Size:  10
  - Model:       sonnet-4.5

Database:
  - Path:        synthesis_tasks.db

[FILE SCAN]

Found 247 .srt files:
  - /courses/java/module1/lecture1.srt
  - /courses/java/module1/lecture2.srt
  ...

[BATCH STRUCTURE]

Total batches: 25
  - Batch 1:  10 files (lectures 1-10)
  - Batch 2:  10 files (lectures 11-20)
  ...
  - Batch 25: 7 files (lectures 241-247)

*** DRY RUN MODE ***
No files will be processed. Configuration validated successfully.
Exit code: 0
```

**Example 2: Verify folder contents**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan "E:\Unknown Folder" \
  --dry-run
```
**Expected Output**:
```
[FILE SCAN]

Found 0 .srt files in: E:\Unknown Folder

*** DRY RUN MODE ***
No files found to process.
```

**Example 3: Test custom model and prompt**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /courses \
  -model opus \
  -system-prompt python_expert.txt \
  --dry-run
```
**Expected Output**:
```
[CONFIGURATION]

Model: opus (claude-3-opus-20240229)
System Prompt: python_expert.txt (loaded successfully, 842 characters)
...

*** DRY RUN MODE ***
Configuration validated. Ready to process with opus model.
```

**Example 4: Catch configuration errors**
```bash
python KevinTheAntagonizerClaudeCodeNotesMaker.py \
  -scan /nonexistent \
  --dry-run
```
**Expected Output**:
```
ERROR: Scan folder does not exist: /nonexistent
Exit code: 1
```
**Result**: Catches error before starting expensive processing

**Related Arguments**:
- [`-scan`](#scan) - Folders are scanned but not processed
- [`-workers`](#workers) - Configuration validated
- [`-model`](#model) - Model validated but not used
- [`--list-models`](#list-models) - Different information-only mode

**Interaction Matrix**:

| Combined With | Result | Notes |
|---------------|--------|-------|
| `-scan <folder>` | Scans folder, shows files found | No processing |
| `-recursive` | Shows all files recursively | Validates scope |
| `-model opus` | Validates model exists | No API calls |
| `-system-prompt <file>` | Loads and validates prompt | No synthesis |

**Error Messages**:

**All validation errors** still occur (folder not found, invalid model, etc.) - dry run validates everything except API connectivity.

**Behavioral Notes**:

1. **Complete Validation**: Tests everything except Claude API calls
2. **File Scanning**: Actually scans folders (not simulated)
3. **Database Writes**: Tasks still added to database as pending
4. **Cost**: $0 (no API calls)
5. **Time**: Fast (no synthesis, only file I/O)
6. **Exit Code**: 0 if validation succeeds, 1 if errors found
7. **Use Before Large Runs**: Always recommended for 100+ file batches

**Source Code References**:
- Argument definition: `KevinTheAntagonizerClaudeCodeNotesMaker.py:372-376`
- Dry run handling: `KevinTheAntagonizerClaudeCodeNotesMaker.py:909-935` (main function)

---

## <a id="combination-matrices"></a>Argument Combination Matrices

This section shows which arguments can be combined and their interactions.

### Valid Combinations Matrix

| Argument 1 | Argument 2 | Valid? | Result | Notes |
|------------|------------|--------|--------|-------|
| `-scan` | `-recursive` | ✅ Yes | Scans all subfolders | Recommended for organized courses |
| `-scan` | `-workers 4` | ✅ Yes | Parallel processing | Speeds up large batches |
| `-scan` | `-batch-size 10` | ✅ Yes | Batch processing | Standard workflow |
| `-scan` | `-model opus` | ✅ Yes | Premium quality | Higher cost |
| `-scan` | `-system-prompt <file>` | ✅ Yes | Custom persona | Topic-specific expertise |
| `-scan` | `--dry-run` | ✅ Yes | Validation only | No processing |
| `-scan` | `-db custom.db` | ✅ Yes | Custom database | Multi-project organization |
| `-scan` | `-retry-failed` | ⚠️ Ignored | Retry takes precedence | -scan ignored when retrying |
| `-scan` | `-stats` | ⚠️ Both | Stats shown, then processes | Pre-check workflow |
| `-scan` | `--list-models` | ⚠️ Ignored | Models listed only | Information mode |
| `-workers 4` | `-batch-size 10` | ✅ Yes | Parallel + batching | Recommended |
| `-workers 8` | `-model haiku` | ✅ Yes | Maximum speed | Cost-effective bulk |
| `-model opus` | `-retry-failed` | ✅ Yes | Upgrade failures | Quality improvement |
| `-model opus` | `-system-prompt <file>` | ✅ Yes | Premium + custom | Best quality |
| `-db custom.db` | `-reset-db` | ✅ Yes | Reset specific database | Safe for multi-project |
| `-db custom.db` | `-stats` | ✅ Yes | Project-specific stats | Multi-project tracking |
| `-retry-failed` | `-model opus` | ✅ Yes | Retry with better model | Common strategy |
| `--dry-run` | any argument | ✅ Yes | Validates configuration | No processing |
| `--help` | any argument | ⚠️ Ignored | Help displayed only | Help has precedence |
| `--list-models` | any argument | ⚠️ Ignored | Models listed only | Information mode |

### Mutually Exclusive Combinations

These argument combinations don't make sense together:

| Argument 1 | Argument 2 | Why Mutually Exclusive |
|------------|------------|------------------------|
| `-scan` | `-retry-failed` | Retry uses database, not scan folders |
| `--help` | (any other) | Help mode exits immediately |
| `--list-models` | `-scan` | Information mode, no processing |
| `-stats` (alone) | `-scan` | Stats exits, but can show stats then process |

### Recommended Combinations

**Beginner (Safe & Simple)**:
```bash
-scan /courses
```

**Standard Workflow**:
```bash
-scan /courses -recursive -batch-size 10
```

**Speed-Focused**:
```bash
-scan /courses -recursive -workers 8 -model haiku -batch-size 10
```

**Quality-Focused**:
```bash
-scan /courses -model opus -batch-size 5 -system-prompt expert.txt
```

**Multi-Project Organization**:
```bash
-scan /java -db java.db -system-prompt java_expert.txt
```

**Validation Before Processing**:
```bash
-scan /courses -recursive -workers 4 --dry-run
```

**Two-Tier Quality Strategy**:
```bash
# Phase 1
-scan /courses -model haiku

# Phase 2
-retry-failed -model opus
```

---

## <a id="error-catalog"></a>Complete Error Catalog

All error messages organized by category with causes and solutions.

### Configuration Errors

**Error**: `ERROR: Scan folder does not exist or is not accessible: /path`
- **Cause**: Path doesn't exist, typo in path, or no read permissions
- **Solution**: Verify path exists, check permissions, use absolute path
- **Exit Code**: 1

**Error**: `ERROR: Scan folder is not a directory: /path/file.srt`
- **Cause**: Specified a file instead of directory
- **Solution**: Use parent directory containing .srt files
- **Exit Code**: 1

**Error**: `ERROR: System prompt file not found: prompt.txt`
- **Cause**: Custom prompt file doesn't exist
- **Solution**: Create file or use correct path
- **Exit Code**: 1

**Error**: `ERROR: System prompt file is empty: prompt.txt`
- **Cause**: File exists but has no content
- **Solution**: Add expert persona description to file
- **Exit Code**: 1

### Validation Errors

**Error**: `ERROR: Workers must be at least 1 (got: 0)`
- **Cause**: Invalid worker count
- **Solution**: Use positive integer (recommended: 1-8)
- **Exit Code**: 1

**Error**: `ERROR: Batch size must be at least 1 (got: 0)`
- **Cause**: Invalid batch size
- **Solution**: Use positive integer (recommended: 5-20)
- **Exit Code**: 1

**Error**: `ERROR: Invalid model 'gpt-4'. Available models: ...`
- **Cause**: Model name not recognized
- **Solution**: Use `--list-models` to see valid options
- **Exit Code**: 1

**Error**: `usage: ... error: the following arguments are required: -scan`
- **Cause**: No -scan argument provided
- **Solution**: Add `-scan <folder>` (or use -stats, -list-failed, etc.)
- **Exit Code**: 2 (argparse error)

**Error**: `usage: ... error: argument -scan: expected one argument`
- **Cause**: -scan specified without folder path
- **Solution**: Provide folder: `-scan /path/to/folder`
- **Exit Code**: 2 (argparse error)

### Database Errors

**Error**: `ERROR: Database file not found: synthesis_tasks.db`
- **Cause**: No database exists (no processing done yet)
- **Solution**: Run processing first, or check database path
- **Exit Code**: 1

**Error**: `ERROR: Database parent directory does not exist: /path/tasks.db`
- **Cause**: Tried to create database in non-existent folder
- **Solution**: Create parent directory first
- **Exit Code**: 1

**Error**: `ERROR: Cannot write to database path: /path (Permission denied)`
- **Cause**: No write permissions for database location
- **Solution**: Use writable location or adjust permissions
- **Exit Code**: 1

### Runtime Errors

**Error**: `ERROR: Claude Code CLI not found`
- **Cause**: Claude Code CLI not installed
- **Solution**: `npm install -g @anthropic-ai/claude-code`
- **Exit Code**: 1

**Error**: `ERROR: Claude Code CLI not logged in`
- **Cause**: Not authenticated with Claude Code
- **Solution**: Run `claude-code login`
- **Exit Code**: 1

**Error**: `ERROR: Quality check failed (score: 0.42/0.70)`
- **Cause**: Synthesis output didn't meet quality standards
- **Solution**: Automatically retried (up to 3 attempts), or use better model
- **Exit Code**: Not an exit error (task marked as failed in database)

**Error**: `ERROR: Claude API timeout after 120 seconds`
- **Cause**: API request took too long
- **Solution**: Automatically retried, or check network connection
- **Exit Code**: Not an exit error (task marked as failed in database)

### Error Resolution Flowchart

```
START: Error occurred
│
├─ Configuration error?
│   ├─ Path not found → Check path spelling, use absolute path
│   ├─ Permission denied → Adjust permissions or use different location
│   └─ Invalid argument → Check syntax, use --help
│
├─ Validation error?
│   ├─ Required argument missing → Add -scan or appropriate argument
│   ├─ Invalid value → Check type (integer, string, etc.)
│   └─ Invalid model → Use --list-models to see options
│
├─ Database error?
│   ├─ Database not found → Run processing first or check path
│   ├─ Permission denied → Use writable location
│   └─ Database corrupt → Use -reset-db to recreate
│
└─ Runtime error?
    ├─ CLI not found → Install Claude Code CLI
    ├─ Not logged in → Run claude-code login
    ├─ Quality check failed → Use better model or retry
    └─ API timeout → Check network, retry automatically
```

---

## <a id="database-reference"></a>Database Schema & SQL Queries

Complete reference for the SQLite database structure and common queries.

### Database Schema

**File**: `synthesis_tasks.db` (default) or custom path via `-db`

**Table: tasks**

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    srt_path TEXT UNIQUE NOT NULL,          -- Full path to .srt file
    lecture_name TEXT NOT NULL,             -- Extracted lecture name
    course_name TEXT NOT NULL,              -- Parent folder name
    status TEXT NOT NULL,                   -- pending, processing, completed, failed
    attempts INTEGER DEFAULT 0,             -- Number of processing attempts
    quality_score REAL,                     -- 0.0-1.0 (null if not completed)
    tokens_used INTEGER,                    -- API tokens consumed
    error_message TEXT,                     -- Error details if failed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,                 -- When task finished
    model_used TEXT,                        -- Which Claude model was used
    system_prompt_hash TEXT                 -- Hash of system prompt (for tracking)
);

CREATE INDEX idx_status ON tasks(status);
CREATE INDEX idx_attempts ON tasks(attempts);
CREATE UNIQUE INDEX idx_srt_path ON tasks(srt_path);
```

**Table: processing_stats**

```sql
CREATE TABLE processing_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,                   -- Unique run identifier
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    total_files INTEGER,
    successful INTEGER,
    failed INTEGER,
    total_tokens INTEGER,
    model_used TEXT,
    workers_used INTEGER,
    batch_size INTEGER
);
```

### Common SQL Queries

**1. View All Tasks by Status**
```sql
SELECT status, COUNT(*) as count
FROM tasks
GROUP BY status
ORDER BY count DESC;
```

**2. List Failed Tasks with Errors**
```sql
SELECT lecture_name, course_name, attempts, error_message, completed_at
FROM tasks
WHERE status = 'failed'
ORDER BY completed_at DESC;
```

**3. Calculate Average Quality Score**
```sql
SELECT AVG(quality_score) as avg_quality,
       MIN(quality_score) as min_quality,
       MAX(quality_score) as max_quality
FROM tasks
WHERE status = 'completed';
```

**4. Find Low-Quality Completions (for retry)**
```sql
SELECT lecture_name, quality_score
FROM tasks
WHERE status = 'completed' AND quality_score < 0.7
ORDER BY quality_score ASC;
```

**5. Calculate Total Token Usage**
```sql
SELECT SUM(tokens_used) as total_tokens,
       AVG(tokens_used) as avg_tokens_per_file
FROM tasks
WHERE status = 'completed';
```

**6. View Processing Progress**
```sql
SELECT
    (SELECT COUNT(*) FROM tasks WHERE status='completed') as completed,
    (SELECT COUNT(*) FROM tasks WHERE status='failed') as failed,
    (SELECT COUNT(*) FROM tasks WHERE status='pending') as pending,
    (SELECT COUNT(*) FROM tasks) as total,
    ROUND(100.0 * (SELECT COUNT(*) FROM tasks WHERE status='completed') /
          (SELECT COUNT(*) FROM tasks), 2) as percent_complete
FROM tasks
LIMIT 1;
```

**7. Reset Failed Tasks for Retry**
```sql
UPDATE tasks
SET status = 'pending', attempts = 0
WHERE status = 'failed';
```

**8. Reset Low-Quality Tasks for Reprocessing**
```sql
UPDATE tasks
SET status = 'pending', attempts = 0
WHERE status = 'completed' AND quality_score < 0.7;
```

**9. Find Tasks by Course Name**
```sql
SELECT lecture_name, status, quality_score
FROM tasks
WHERE course_name LIKE '%Java%'
ORDER BY lecture_name;
```

**10. Export Completed Tasks to CSV**
```bash
sqlite3 -header -csv synthesis_tasks.db \
  "SELECT lecture_name, course_name, quality_score, tokens_used, completed_at
   FROM tasks WHERE status='completed'" > completed.csv
```

**11. View Processing Statistics by Model**
```sql
SELECT model_used,
       COUNT(*) as files_processed,
       AVG(quality_score) as avg_quality,
       SUM(tokens_used) as total_tokens
FROM tasks
WHERE status = 'completed'
GROUP BY model_used;
```

**12. Identify Stuck Tasks (processing > 1 hour)**
```sql
SELECT lecture_name, status, created_at
FROM tasks
WHERE status = 'processing'
  AND datetime(created_at) < datetime('now', '-1 hour');
```

### Database Maintenance

**Vacuum Database (compact/optimize)**
```bash
sqlite3 synthesis_tasks.db "VACUUM;"
```

**Backup Database**
```bash
# Simple copy
cp synthesis_tasks.db synthesis_tasks.db.backup

# With timestamp
cp synthesis_tasks.db synthesis_tasks.db.$(date +%Y%m%d_%H%M%S)

# SQLite dump (portable)
sqlite3 synthesis_tasks.db .dump > backup.sql
```

**Restore from Backup**
```bash
# From copy
cp synthesis_tasks.db.backup synthesis_tasks.db

# From dump
sqlite3 synthesis_tasks.db < backup.sql
```

### Database Inspection Commands

```bash
# Open interactive shell
sqlite3 synthesis_tasks.db

# Show schema
sqlite3 synthesis_tasks.db ".schema"

# Show all tables
sqlite3 synthesis_tasks.db ".tables"

# Show table info
sqlite3 synthesis_tasks.db ".schema tasks"

# Run query
sqlite3 synthesis_tasks.db "SELECT COUNT(*) FROM tasks"

# Export to CSV
sqlite3 -header -csv synthesis_tasks.db "SELECT * FROM tasks" > tasks.csv

# Import CSV
sqlite3 synthesis_tasks.db ".mode csv" ".import data.csv tasks"
```

---

## End of Reference

This completes the comprehensive CLI Argument Reference for KevinTheAntagonizerClaudeCodeNotesMaker.

**Related Documentation**:
- 🚀 **USAGE_GUIDE.md** - Task-based quick reference (1200+ lines)
- 📚 **USAGE.md** - Comprehensive usage guide with workflows
- 🎯 **README.md** - Quick start and project overview
- 💻 **CLAUDE.md** - Architecture and development guide

**Document Statistics**:
- Total Lines: ~2100+
- Arguments Documented: 14 (all)
- Examples Provided: 80+
- Error Messages: 20+
- SQL Queries: 12+

**Last Updated**: November 2025
**Version**: 2.1

