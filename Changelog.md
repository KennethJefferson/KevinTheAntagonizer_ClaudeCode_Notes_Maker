# Changelog

All notable changes to KevinTheAntagonizerClaudeCodeNotesMaker are documented here.

---

## Version 2.5 (December 2025) - Current

### Changed
- **Concurrency limit raised from 3 to 100** for full parallelism
  - All workers can now hit the API simultaneously
  - Jitter (0.1-0.5s) still provides slight staggering between calls
  - Full speed restored for multi-worker processing

### Tunable Concurrency
Edit line 36 in `KevinTheAntagonizerClaudeCodeNotesMaker.py`:

```python
# ==============================================================================
# Concurrency Control for Claude API Calls
# ==============================================================================
# Set high to allow full parallelism - user accepts crash risk for speed
# If EBUSY errors occur, reduce this value (e.g., 3-10) for stability
CLAUDE_CONCURRENCY_LIMIT = 100  # Effectively unlimited - all workers can run
```

**Recommended values:**
| Value | Use Case |
|-------|----------|
| `100` | Maximum speed - all workers run simultaneously |
| `10-15` | Balanced - good speed with some stability |
| `3` | Maximum stability - prevents most EBUSY errors |

**If EBUSY crashes return:**
- Edit line 36: change `100` to `10` or `15` for a middle ground
- Or restart and hope for better timing luck

---

## Version 2.4 (December 2025)

### Fixed
- **Windows command line limit** for large transcripts
  - Windows has 8191 character command line limit
  - Large transcripts (40KB+) exceed limit when passed via CLI
  - Solution: Use streaming mode for prompts > 7500 chars
  - Sends prompt via stdin instead of command line

- **EBUSY file locking** for parallel workers
  - Multiple workers competing for `~/.claude.json` caused errors
  - Solution: Semaphore with jitter to stagger file access timing
  - Retry logic with exponential backoff for EBUSY errors

- **Windows "[Errno 22] Invalid argument"** in multi-worker mode
  - tqdm progress bar cursor positioning failed on Windows console
  - Solution: Safe wrapper functions for all progress bar operations
  - `safe_pbar_update()`, `safe_pbar_set_description()`, `safe_pbar_close()`
  - Gracefully handles OSError with errno 22 without crashing

### Improved
- Better error logging for SDK exceptions
  - Logs full exception type and message
  - Includes traceback for debugging

---

## Version 2.3 (December 2025)

### New Features
- **Hybrid authentication approach**
  - `--list-models`: Uses Anthropic API for fresh model data
  - All other operations: Uses Claude Code CLI auth (subscription login)
  - No API credits used for synthesis work

- **Persistent model caching** with `claude_models_cache.json`
  - Models fetched via API are cached locally
  - Cache used for fast model validation during normal operations
  - Includes timestamp, source, and version info

- **API key storage** in `.anthropic_api_key` file
  - Prompted on first `--list-models` run
  - Stored securely in script directory
  - Only used for model listing, not synthesis

### Improved
- `--list-models` now shows setup prompts and cache info
  - Guides user through API key setup
  - Displays source (API, cache, or static)
  - Shows both cache and API key file locations

---

## Version 2.2 (November 2025)

### New Features
- **Graceful shutdown support** (Ctrl+C handling)
  - First Ctrl+C: Complete current batch before exiting
  - Second Ctrl+C: Force immediate exit
  - Progress bar cleanup via atexit handler
  - Works on Windows (SIGINT, SIGBREAK) and Unix

### Improved
- Multi-worker mode now fully functional
- True parallel asyncio workers with shared task queue

---

## Version 2.1 (November 2025)

### New Features
- **Dynamic model discovery** from Claude Code CLI
- **`--list-models` command** to see available models
- Automatic model updates (no code changes needed for new releases)
- Enhanced model validation with helpful error messages
- Model source indication in configuration display

---

## Version 2.0 (November 2025)

### Breaking Changes
- **Single-file architecture** - merged `cli_args.py` into main application file
- Moved deprecated files to `__deprecated/` folder

### Improved
- Improved CLI argument parsing
- Better error handling and logging
- Windows encoding compatibility

---

## Version 1.0 (Initial Release)

### Features
- Multi-file architecture with separate CLI module
- Basic CLI support with argparse
- SQLite database task tracking
- Quality control system with 7-point validation
- Support for 5 Claude models
- Batch processing with configurable workers
- Progress bars and logging
