#!/usr/bin/env python3
"""
Kevin's Note Synthesis Application - Claude Agent SDK Implementation with CLI
===============================================================================
This uses the Claude Agent SDK from https://github.com/anthropics/claude-agent-sdk-python
Authentication is handled through Claude Code CLI, not API keys.

Prerequisites:
1. Install Claude Code CLI: npm install -g @anthropic-ai/claude-code
2. Login to Claude Code: claude-code login
3. Install Python SDK: pip install claude-agent-sdk
4. Run: python KevinTheAntagonizerClaudeCodeNotesMaker.py -scan <folder>
"""

import json
import sqlite3
import asyncio
import argparse
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import logging
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# REAL Claude Agent SDK imports
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    AssistantMessage,
    TextBlock,
    ClaudeSDKError,
    CLINotFoundError,
    ProcessError,
    CLIJSONDecodeError
)

# ==============================================================================
# CLI Configuration & Constants
# ==============================================================================

# Available Claude models
AVAILABLE_MODELS = {
    # Claude 3 Family
    "opus": "claude-3-opus-20240229",
    "sonnet": "claude-3-sonnet-20240229",
    "haiku": "claude-3-haiku-20240307",

    # Claude 3.5
    "sonnet-3.5": "claude-3-5-sonnet-20241022",

    # Claude 4.5 (Latest - Default)
    "sonnet-4.5": "claude-sonnet-4-5-20250929",
}

DEFAULT_MODEL = "sonnet-4.5"
DEFAULT_WORKERS = 1
DEFAULT_BATCH_SIZE = 10
DEFAULT_DB_NAME = "synthesis_tasks.db"

# ==============================================================================
# CLI Argument Container
# ==============================================================================

class CLIArgs:
    """Container for parsed CLI arguments"""

    def __init__(self):
        self.scan_folders: List[Path] = []
        self.recursive: bool = False
        self.workers: int = DEFAULT_WORKERS
        self.batch_size: int = DEFAULT_BATCH_SIZE
        self.db_path: Path = Path(DEFAULT_DB_NAME)
        self.reset_db: bool = False
        self.list_failed: bool = False
        self.retry_failed: bool = False
        self.stats: bool = False
        self.system_prompt_file: Optional[Path] = None
        self.model: str = AVAILABLE_MODELS[DEFAULT_MODEL]
        self.model_name: str = DEFAULT_MODEL
        self.dry_run: bool = False
        self.log_file: Path = self._generate_log_filename()
        self.run_id: str = self._generate_run_id()

    @staticmethod
    def _generate_run_id() -> str:
        """Generate unique run ID"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def _generate_log_filename() -> Path:
        """Generate log filename: runID.YYYYMMDD.HHMMSS.log"""
        timestamp = datetime.now().strftime("%Y%m%d.%H%M%S")
        return Path(__file__).parent / f"runID.{timestamp}.log"

# ==============================================================================
# Configuration
# ==============================================================================

class Config:
    """Application configuration"""

    # Default system prompt (can be overridden via CLI)
    DEFAULT_SYSTEM_PROMPT = """You are Kevin Burleigh, a battle-tested Java/Spring Boot architect with 20+ years of experience.
You synthesize technical transcripts into comprehensive learning notes.
You are opinionated, practical, and thorough.
You extract maximum value from every transcript."""

    # Quality control settings
    MIN_QUALITY_LENGTH = 1500
    MIN_QUALITY_SCORE = 0.7
    MAX_FILE_SIZE = 50000  # Characters

    # Tools the agent can use
    ALLOWED_TOOLS = ["Read", "Write", "Bash"]  # Basic file operations only

    # Disable tools that could lead to automation
    DISALLOWED_TOOLS = ["CreateAgent", "RunPython"]  # No spawning agents or Python scripts

# ==============================================================================
# CLI Argument Parsing
# ==============================================================================

def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser"""

    parser = argparse.ArgumentParser(
        prog="KevinTheAntagonizerClaudeCodeNotesMaker",
        description="Synthesize .srt transcripts into expert-level notes using Claude Agent SDK",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic: Single folder, sequential processing
  %(prog)s -scan /courses/java

  # Multi-folder recursive with parallel workers
  %(prog)s -scan /courses/java -scan /courses/spring -recursive -workers 4

  # Custom model and batch size
  %(prog)s -scan /courses -model opus -batch-size 5 -workers 2

  # Database management
  %(prog)s -stats
  %(prog)s -list-failed
  %(prog)s -retry-failed -workers 3
  %(prog)s -reset-db -scan /courses

  # Dry run to validate
  %(prog)s -scan /courses -recursive --dry-run

Available Models:
  opus        - Claude 3 Opus (most capable, expensive)
  sonnet      - Claude 3 Sonnet (balanced)
  haiku       - Claude 3 Haiku (fast, cheap)
  sonnet-3.5  - Claude 3.5 Sonnet (better than opus)
  sonnet-4.5  - Claude 4.5 Sonnet (latest, default)
        """
    )

    # Required arguments
    required = parser.add_argument_group('required arguments')
    required.add_argument(
        '-scan',
        dest='scan_folders',
        action='append',
        metavar='<folder>',
        help='Folder to scan for .srt files (repeatable)'
    )

    # Processing options
    processing = parser.add_argument_group('processing options')
    processing.add_argument(
        '-recursive',
        action='store_true',
        help='Scan subfolders recursively (default: only scan root folders)'
    )
    processing.add_argument(
        '-workers',
        type=int,
        default=DEFAULT_WORKERS,
        metavar='<num>',
        help=f'Number of parallel workers/subagents (default: {DEFAULT_WORKERS})'
    )
    processing.add_argument(
        '-batch-size',
        type=int,
        default=DEFAULT_BATCH_SIZE,
        metavar='<num>',
        help=f'Files per batch/subagent (default: {DEFAULT_BATCH_SIZE})'
    )

    # Database management
    database = parser.add_argument_group('database management')
    database.add_argument(
        '-db',
        type=str,
        default=DEFAULT_DB_NAME,
        metavar='<path>',
        help=f'Custom database path (default: {DEFAULT_DB_NAME})'
    )
    database.add_argument(
        '-reset-db',
        action='store_true',
        help='Clear database and start fresh'
    )
    database.add_argument(
        '-list-failed',
        action='store_true',
        help='Show failed tasks and exit'
    )
    database.add_argument(
        '-retry-failed',
        action='store_true',
        help='Retry all failed tasks from database'
    )
    database.add_argument(
        '-stats',
        action='store_true',
        help='Show database statistics and exit'
    )

    # Advanced options
    advanced = parser.add_argument_group('advanced options')
    advanced.add_argument(
        '-system-prompt',
        type=str,
        metavar='<file>',
        help='Use custom system prompt from file'
    )
    advanced.add_argument(
        '-model',
        type=str,
        choices=list(AVAILABLE_MODELS.keys()),
        default=DEFAULT_MODEL,
        metavar='<name>',
        help=f'Claude model selection (default: {DEFAULT_MODEL})'
    )
    advanced.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate configuration without processing files'
    )

    return parser

def validate_args(args: argparse.Namespace) -> CLIArgs:
    """
    Validate and transform argparse namespace into CLIArgs object

    Performs validation:
    - Scan folders exist and are directories
    - Workers/batch-size are positive integers
    - System prompt file exists if specified
    - Database path is valid
    """

    cli_args = CLIArgs()

    # Check if scan_folders is provided for operations that need it
    if args.scan_folders:
        # Validate scan folders
        for folder_str in args.scan_folders:
            folder = Path(folder_str).resolve()
            if not folder.exists():
                print(f"[ERROR] Scan folder does not exist: {folder}")
                sys.exit(1)
            if not folder.is_dir():
                print(f"[ERROR] Scan path is not a directory: {folder}")
                sys.exit(1)
            cli_args.scan_folders.append(folder)
    elif not any([args.stats, args.list_failed, args.retry_failed]):
        # Scan folders are required unless doing database management operations
        print("[ERROR] -scan argument is required (unless using -stats, -list-failed, or -retry-failed)")
        sys.exit(1)

    # Validate workers
    if args.workers < 1:
        print(f"[ERROR] Workers must be >= 1 (got: {args.workers})")
        sys.exit(1)
    cli_args.workers = args.workers

    # Validate batch size
    if args.batch_size < 1:
        print(f"[ERROR] Batch size must be >= 1 (got: {args.batch_size})")
        sys.exit(1)
    cli_args.batch_size = args.batch_size

    # Validate system prompt file
    if args.system_prompt:
        prompt_file = Path(args.system_prompt).resolve()
        if not prompt_file.exists():
            print(f"[ERROR] System prompt file not found: {prompt_file}")
            sys.exit(1)
        if not prompt_file.is_file():
            print(f"[ERROR] System prompt path is not a file: {prompt_file}")
            sys.exit(1)
        cli_args.system_prompt_file = prompt_file

    # Set model
    cli_args.model_name = args.model
    cli_args.model = AVAILABLE_MODELS[args.model]

    # Set database path
    cli_args.db_path = Path(args.db).resolve()

    # Set flags
    cli_args.recursive = args.recursive
    cli_args.reset_db = args.reset_db
    cli_args.list_failed = args.list_failed
    cli_args.retry_failed = args.retry_failed
    cli_args.stats = args.stats
    cli_args.dry_run = args.dry_run

    return cli_args

def parse_arguments() -> CLIArgs:
    """
    Main entry point for CLI argument parsing

    Returns:
        CLIArgs: Validated CLI arguments
    """
    parser = create_parser()
    args = parser.parse_args()

    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return validate_args(args)

def print_configuration(cli_args: CLIArgs):
    """Print configuration summary for user validation"""

    print("\n" + "="*70)
    print("KevinTheAntagonizerClaudeCodeNotesMaker - Configuration")
    print("="*70)

    if cli_args.scan_folders:
        print("\n[SCAN FOLDERS]")
        for folder in cli_args.scan_folders:
            print(f"   - {folder}")

    print(f"\n[PROCESSING OPTIONS]")
    print(f"   - Recursive:   {cli_args.recursive}")
    print(f"   - Workers:     {cli_args.workers}")
    print(f"   - Batch Size:  {cli_args.batch_size}")
    print(f"   - Model:       {cli_args.model_name} ({cli_args.model})")

    print(f"\n[DATABASE]")
    print(f"   - Path:        {cli_args.db_path}")
    if cli_args.reset_db:
        print(f"   - Action:      *** RESET DATABASE (all data will be cleared) ***")

    print(f"\n[LOGGING]")
    print(f"   - Run ID:      {cli_args.run_id}")
    print(f"   - Log File:    {cli_args.log_file}")

    if cli_args.system_prompt_file:
        print(f"\n[CUSTOM SYSTEM PROMPT]")
        print(f"   - File:        {cli_args.system_prompt_file}")

    if cli_args.retry_failed:
        print(f"\n[RETRY MODE]")
        print(f"   - Will retry all failed tasks from database")

    if cli_args.dry_run:
        print(f"\n*** DRY RUN MODE - No files will be processed ***")

    print("\n" + "="*70 + "\n")

# ==============================================================================
# Database Manager
# ==============================================================================

class DatabaseManager:
    """Manages SQLite database for task tracking"""

    def __init__(self, db_path: Path, reset: bool = False):
        self.db_path = str(db_path)
        if reset and db_path.exists():
            os.remove(self.db_path)
            print(f"[INFO] Database reset: {self.db_path}")
        self.init_database()

    def init_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                srt_path TEXT UNIQUE NOT NULL,
                course_name TEXT NOT NULL,
                lecture_name TEXT NOT NULL,
                file_size_kb INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                attempts INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT,
                error_message TEXT,
                quality_score REAL,
                tokens_used INTEGER
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS processing_stats (
                batch_id INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                files_processed INTEGER,
                files_failed INTEGER,
                avg_quality REAL
            )
        """)

        conn.commit()
        conn.close()

    def add_task(self, srt_path: str, course_name: str, lecture_name: str, file_size_kb: int) -> bool:
        """Add a new task to the database"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT OR IGNORE INTO tasks
                (srt_path, course_name, lecture_name, file_size_kb)
                VALUES (?, ?, ?, ?)
            """, (srt_path, course_name, lecture_name, file_size_kb))

            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            logging.error(f"Failed to add task: {e}")
            return False
        finally:
            conn.close()

    def get_pending_tasks(self, limit: int, retry_failed: bool = False) -> List[Dict]:
        """Get pending tasks from database"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        if retry_failed:
            # Get failed tasks for retry
            cur.execute("""
                SELECT id, srt_path, course_name, lecture_name, file_size_kb
                FROM tasks
                WHERE status = 'failed' AND attempts < 3
                ORDER BY file_size_kb ASC
                LIMIT ?
            """, (limit,))
        else:
            # Get normal pending tasks
            cur.execute("""
                SELECT id, srt_path, course_name, lecture_name, file_size_kb
                FROM tasks
                WHERE status = 'pending' AND attempts < 3
                ORDER BY file_size_kb ASC
                LIMIT ?
            """, (limit,))

        tasks = []
        for row in cur.fetchall():
            tasks.append({
                'id': row[0],
                'srt_path': row[1],
                'course_name': row[2],
                'lecture_name': row[3],
                'file_size_kb': row[4]
            })

        conn.close()
        return tasks

    def update_task_status(self, task_id: int, status: str, **kwargs):
        """Update task status in database"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        updates = [f"status = '{status}'"]
        updates.append(f"attempts = attempts + 1")

        if status == 'completed':
            updates.append(f"completed_at = '{datetime.now().isoformat()}'")

        for key, value in kwargs.items():
            if key == 'error_message':
                updates.append(f"error_message = '{value}'")
            elif key == 'quality_score':
                updates.append(f"quality_score = {value}")
            elif key == 'tokens_used':
                updates.append(f"tokens_used = {value}")

        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        cur.execute(query, (task_id,))

        conn.commit()
        conn.close()

    def get_statistics(self) -> Dict:
        """Get processing statistics"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = 'failed' AND attempts >= 3 THEN 1 ELSE 0 END) as failed,
                AVG(CASE WHEN quality_score IS NOT NULL THEN quality_score ELSE 0 END) as avg_quality
            FROM tasks
        """)

        row = cur.fetchone()
        conn.close()

        return {
            'total': row[0] or 0,
            'completed': row[1] or 0,
            'pending': row[2] or 0,
            'failed': row[3] or 0,
            'avg_quality': row[4] or 0
        }

    def list_failed_tasks(self):
        """List all failed tasks with details"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("""
            SELECT lecture_name, srt_path, attempts, error_message
            FROM tasks
            WHERE status = 'failed'
            ORDER BY lecture_name
        """)

        rows = cur.fetchall()
        conn.close()

        if not rows:
            print("[INFO] No failed tasks found")
            return

        print("\n[FAILED TASKS]")
        print("-" * 70)
        for row in rows:
            print(f"Lecture: {row[0]}")
            print(f"Path: {row[1]}")
            print(f"Attempts: {row[2]}")
            print(f"Error: {row[3]}")
            print("-" * 70)

# ==============================================================================
# File Processing
# ==============================================================================

class FileProcessor:
    """Handles file operations and content cleaning"""

    @staticmethod
    def clean_srt_content(srt_path: str) -> Optional[str]:
        """Clean SRT file content by removing timestamps"""
        try:
            with open(srt_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            lines = []
            for line in content.split('\n'):
                line = line.strip()
                # Skip line numbers and timestamps
                if line and not line.isdigit() and '-->' not in line:
                    lines.append(line)

            return ' '.join(lines)

        except Exception as e:
            logging.error(f"Failed to read {srt_path}: {e}")
            return None

    @staticmethod
    def save_notes(content: str, srt_path: str) -> Optional[str]:
        """Save synthesized notes to markdown file"""
        srt_path = Path(srt_path)
        output_path = srt_path.parent / f"{srt_path.stem}_KevinTheAntagonizer_Notes.md"

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logging.info(f"Saved notes to {output_path.name}")
            return str(output_path)

        except Exception as e:
            logging.error(f"Failed to save notes: {e}")
            return None

# ==============================================================================
# Quality Control
# ==============================================================================

class QualityController:
    """Ensures synthesis quality meets standards"""

    @staticmethod
    def check_synthesis(content: str, lecture_name: str) -> Tuple[float, List[str]]:
        """
        Check synthesis quality
        Returns: (quality_score, list_of_issues)
        """
        issues = []
        checks_passed = 0
        total_checks = 7

        # Length check
        if len(content) >= Config.MIN_QUALITY_LENGTH:
            checks_passed += 1
        else:
            issues.append(f"Too short ({len(content)} chars, min {Config.MIN_QUALITY_LENGTH})")

        # Structure check - headers
        if '##' in content or '###' in content:
            checks_passed += 1
        else:
            issues.append("Missing section headers")

        # Code blocks (for technical content)
        if any(tech in lecture_name.lower() for tech in ['code', 'spring', 'java', 'programming']):
            if '```' in content:
                checks_passed += 1
            else:
                issues.append("Technical content missing code blocks")
        else:
            checks_passed += 1  # Not applicable

        # Kevin's voice/personality
        kevin_phrases = ['production', 'real-world', 'actually', 'here\'s the thing',
                        'gotcha', 'reality', 'battle-tested', 'in the trenches']
        if any(phrase in content.lower() for phrase in kevin_phrases):
            checks_passed += 1
        else:
            issues.append("Missing Kevin's personality/voice")

        # CRITICAL: Automation detection - MODIFIED for severity levels (Nov 2024)
        # Previous version auto-failed on any automation word, causing 48% failure rate
        # Now uses tiered approach: critical (auto-fail) vs minor (warning only)

        # Tiered approach: Critical vs Minor issues
        critical_markers = [
            'i have processed',
            'i generated these',
            'this script',
            'as an ai',
            'i cannot access',
            'files have been processed',
            'batch processing completed',
            'script completed'
        ]

        minor_markers = [
            'automated',  # Could be "automated testing"
            'processed',  # Could be "processed data"
            'generated'   # Could be "generated code"
        ]

        content_lower = content.lower()

        if any(marker in content_lower for marker in critical_markers):
            issues.append("CRITICAL: Meta-commentary detected!")
            checks_passed = 0  # Still auto-fail for obvious breaks
        elif any(marker in content_lower for marker in minor_markers):
            issues.append("Minor: Potential automation language")
            # Don't add point, but don't auto-fail
        else:
            checks_passed += 1  # Clean content

        # Depth - bullet points or lists
        if any(marker in content for marker in ['- ', '* ', '1. ', '• ']):
            checks_passed += 1
        else:
            issues.append("Missing detailed lists/points")

        # Emphasis markers
        if '**' in content or '*' in content or '__' in content:
            checks_passed += 1
        else:
            issues.append("Missing emphasis/bold text")

        quality_score = checks_passed / total_checks

        return quality_score, issues

# ==============================================================================
# Note Synthesis Engine using Claude Agent SDK
# ==============================================================================

class NoteSynthesisEngine:
    """Main synthesis engine using Claude Agent SDK"""

    def __init__(self, cli_args: CLIArgs):
        self.cli_args = cli_args
        self.db = DatabaseManager(cli_args.db_path, cli_args.reset_db)
        self.file_processor = FileProcessor()
        self.quality_controller = QualityController()

        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(cli_args.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Load system prompt
        if cli_args.system_prompt_file:
            with open(cli_args.system_prompt_file, 'r') as f:
                self.system_prompt = f.read()
        else:
            self.system_prompt = Config.DEFAULT_SYSTEM_PROMPT

    async def synthesize_with_sdk(self, transcript: str, lecture_name: str, course_name: str) -> Optional[str]:
        """
        Use Claude Agent SDK to synthesize transcript
        Returns synthesized content or None if failed
        """

        # Construct the prompt - CRITICAL: Don't mention files or automation!
        prompt = f"""You are Kevin Burleigh, a battle-tested Java/Spring Boot architect.

CRITICAL CONSTRAINTS:
- You are processing ONE SINGLE TRANSCRIPT
- You CANNOT access the file system
- You CANNOT write automation scripts
- You MUST synthesize manually

LECTURE: {lecture_name}
COURSE: {course_name}

TRANSCRIPT TEXT:
{transcript}

REQUIREMENTS:
1. Extract EVERY concept, pattern, technique, anti-pattern, best practice
2. Add your expert commentary, warnings, and real-world insights
3. Use clear markdown with ##, ###, code blocks, tables
4. Include practical examples and gotchas
5. Minimum {Config.MIN_QUALITY_LENGTH} words of thorough analysis
6. Be opinionated, detailed, and practical

OUTPUT: Provide ONLY the markdown content. No preambles, no confirmations, just the comprehensive notes."""

        try:
            # Configure agent options with model from CLI
            options = ClaudeAgentOptions(
                system_prompt=self.system_prompt,
                model=self.cli_args.model,  # Use model from CLI
                allowed_tools=Config.ALLOWED_TOOLS,
                disallowed_tools=Config.DISALLOWED_TOOLS,
                permission_mode='default',  # Use default permission handling with allowed/disallowed tools
                max_turns=1,  # Single turn for synthesis
                cwd=Path.cwd()  # Use current directory
            )

            # Use the SDK to query Claude
            full_response = ""
            async for message in query(prompt=prompt, options=options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            full_response += block.text

            return full_response if full_response else None

        except CLINotFoundError:
            self.logger.error("Claude Code CLI not found or not logged in.")
            self.logger.error("Install: npm install -g @anthropic-ai/claude-code")
            self.logger.error("Then login: claude-code login")
            return None
        except ProcessError as e:
            self.logger.error(f"Process failed with exit code {e.exit_code}")
            return None
        except CLIJSONDecodeError as e:
            self.logger.error(f"Failed to parse response: {e}")
            return None
        except Exception as e:
            self.logger.error(f"SDK synthesis failed: {e}")
            return None

    async def process_single_task(self, task: Dict, worker_id: int = 0, worker_pbar: tqdm = None) -> bool:
        """
        Process a single synthesis task
        Returns True if successful
        """
        task_id = task['id']
        srt_path = task['srt_path']
        lecture_name = task['lecture_name']
        course_name = task['course_name']

        # Update worker progress bar description
        if worker_pbar:
            worker_pbar.set_description(f"Worker{worker_id:02d}: {lecture_name[:30]}")

        self.logger.info(f"Worker{worker_id:02d} processing [{task_id}]: {lecture_name}")

        # Clean the transcript
        transcript = self.file_processor.clean_srt_content(srt_path)

        if not transcript:
            self.db.update_task_status(task_id, 'failed',
                                      error_message="Failed to read SRT file")
            return False

        # Check size
        if len(transcript) > Config.MAX_FILE_SIZE:
            self.logger.warning(f"File too large: {lecture_name} ({len(transcript)} chars)")
            self.db.update_task_status(task_id, 'failed',
                                      error_message=f"Too large ({len(transcript)} chars)")
            return False

        # Synthesize using SDK
        synthesized = await self.synthesize_with_sdk(transcript, lecture_name, course_name)

        if not synthesized:
            self.db.update_task_status(task_id, 'failed',
                                      error_message="Synthesis failed")
            return False

        # Quality check
        quality_score, issues = self.quality_controller.check_synthesis(synthesized, lecture_name)

        if quality_score < Config.MIN_QUALITY_SCORE:
            self.logger.warning(f"Quality check failed for {lecture_name}: {issues}")
            self.db.update_task_status(task_id, 'failed',
                                      error_message=f"Quality issues: {', '.join(issues)}",
                                      quality_score=quality_score)
            return False

        # Save notes
        output_path = self.file_processor.save_notes(synthesized, srt_path)

        if not output_path:
            self.db.update_task_status(task_id, 'failed',
                                      error_message="Failed to save notes")
            return False

        # Mark as complete
        self.db.update_task_status(task_id, 'completed',
                                  quality_score=quality_score,
                                  tokens_used=len(transcript) // 4)  # Rough estimate

        # Update worker progress bar if provided
        if worker_pbar:
            worker_pbar.update(1)

        self.logger.info(f"Worker{worker_id:02d} completed: {lecture_name} (quality: {quality_score:.2f})")
        return True

    async def worker_process_tasks(self, worker_id: int, task_queue: asyncio.Queue,
                                   worker_pbar: tqdm, main_pbar: tqdm) -> int:
        """
        Worker process that handles tasks from a queue
        """
        success_count = 0
        tasks_processed = 0

        while True:
            try:
                # Get task from queue (with timeout to check for completion)
                task = await asyncio.wait_for(task_queue.get(), timeout=1.0)

                tasks_processed += 1
                # Update worker bar to show current task
                worker_pbar.set_description(f"Worker{worker_id:02d}: Task {tasks_processed}/{self.cli_args.batch_size}")

                # Process the task
                result = await self.process_single_task(task, worker_id, worker_pbar)

                if result:
                    success_count += 1
                    main_pbar.update(1)  # Update main progress bar

                # Mark task as done
                task_queue.task_done()

                # Small delay between files to avoid overwhelming API
                await asyncio.sleep(0.5)

            except asyncio.TimeoutError:
                # No more tasks available
                if task_queue.empty():
                    break
            except Exception as e:
                self.logger.error(f"Worker{worker_id:02d} error: {e}")

        worker_pbar.set_description(f"Worker{worker_id:02d}: Complete ({success_count} files)")
        return success_count

    async def process_all_tasks(self) -> int:
        """
        Process all pending tasks using true parallel workers
        Returns total number of successful tasks
        """
        # Get all pending tasks for workers
        all_tasks = []
        batch_size_total = self.cli_args.batch_size * self.cli_args.workers

        while True:
            batch = self.db.get_pending_tasks(batch_size_total, self.cli_args.retry_failed)
            if not batch:
                break
            all_tasks.extend(batch)
            # Process in chunks to avoid memory issues
            if len(all_tasks) >= batch_size_total:
                break

        if not all_tasks:
            self.logger.info("No pending tasks")
            return 0

        total_tasks = len(all_tasks)
        self.logger.info(f"Processing {total_tasks} files with {self.cli_args.workers} workers...")

        # Create task queue
        task_queue = asyncio.Queue()
        for task in all_tasks:
            await task_queue.put(task)

        # Create progress bars for each worker plus main progress
        # Position 0 is for main progress, 1+ for workers
        worker_pbars = []

        # Main progress bar at top
        main_pbar = tqdm(total=total_tasks, desc="Overall Progress",
                        position=0, leave=True,
                        bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]',
                        ncols=100)

        # Create worker progress bars
        for i in range(self.cli_args.workers):
            worker_pbar = tqdm(total=self.cli_args.batch_size,
                             desc=f"Worker{i+1:02d}: Starting",
                             position=i+1, leave=False,
                             bar_format='{desc: <30} {bar}| {n_fmt}/{total_fmt}',
                             ncols=100)
            worker_pbars.append(worker_pbar)

        # Create worker tasks
        worker_tasks = []
        for i in range(self.cli_args.workers):
            worker_task = asyncio.create_task(
                self.worker_process_tasks(i+1, task_queue, worker_pbars[i], main_pbar)
            )
            worker_tasks.append(worker_task)

        # Wait for all workers to complete
        results = await asyncio.gather(*worker_tasks)

        # Close all progress bars properly
        for pbar in worker_pbars:
            pbar.close()
        main_pbar.close()

        # Clear the progress bar area
        print("\n" * (self.cli_args.workers + 2))

        total_success = sum(results)
        self.logger.info(f"All workers complete: {total_success}/{total_tasks} successful")

        return total_success

    async def process_batch(self) -> int:
        """
        Process a batch of tasks
        Returns number of successful tasks
        """
        # If using multiple workers, use the new true parallel architecture
        if self.cli_args.workers > 1:
            return await self.process_all_tasks()

        # Otherwise, use simple sequential processing for single worker
        tasks = self.db.get_pending_tasks(
            self.cli_args.batch_size,
            self.cli_args.retry_failed
        )

        if not tasks:
            self.logger.info("No pending tasks")
            return 0

        self.logger.info(f"Processing batch of {len(tasks)} files...")

        success_count = 0
        # Create a simple progress bar for single worker
        with tqdm(total=len(tasks), desc="Processing", leave=True,
                  bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}') as pbar:
            for task in tasks:
                if await self.process_single_task(task, worker_id=1):
                    success_count += 1
                pbar.update(1)

                # Brief pause between API calls to avoid rate limiting
                await asyncio.sleep(1)

        self.logger.info(f"Batch complete: {success_count}/{len(tasks)} successful")
        return success_count

# ==============================================================================
# File Inventory
# ==============================================================================

def inventory_files(cli_args: CLIArgs, db: DatabaseManager) -> int:
    """Inventory all files that need processing"""

    logger = logging.getLogger(__name__)
    logger.info(f"Scanning {len(cli_args.scan_folders)} folder(s)")

    added_count = 0
    skipped_count = 0

    for scan_folder in cli_args.scan_folders:
        # Find all SRT files based on recursive flag
        if cli_args.recursive:
            srt_files = list(scan_folder.rglob("*.srt"))
        else:
            srt_files = list(scan_folder.glob("*.srt"))

        logger.info(f"Found {len(srt_files)} .srt files in {scan_folder}")

        # Process files with progress logging
        for idx, srt_file in enumerate(srt_files):
            # Log progress every 50 files
            if idx % 50 == 0:
                logger.info(f"Processing file {idx+1}/{len(srt_files)}: {srt_file.name}")

            # Check if notes already exist
            notes_path = srt_file.parent / f"{srt_file.stem}_KevinTheAntagonizer_Notes.md"

            if notes_path.exists():
                skipped_count += 1
                continue

            # Add to database
            course_name = srt_file.parent.name
            lecture_name = srt_file.stem
            file_size_kb = srt_file.stat().st_size // 1024

            if db.add_task(str(srt_file), course_name, lecture_name, file_size_kb):
                added_count += 1

    logger.info(f"Inventory complete: {added_count} new files, {skipped_count} already processed")
    return added_count

# ==============================================================================
# Main Application
# ==============================================================================

async def main():
    """Main application entry point"""

    # Parse command-line arguments
    cli_args = parse_arguments()

    print("""
    +==============================================================+
    |   Kevin's Note Synthesis App - Claude Agent SDK Edition     |
    +==============================================================+
    """)

    # Set up logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(cli_args.log_file),
            logging.StreamHandler()
        ]
    )

    logger.info(f"Starting run {cli_args.run_id}")

    # Initialize database
    db = DatabaseManager(cli_args.db_path, cli_args.reset_db)

    # Handle database management commands
    if cli_args.stats:
        stats = db.get_statistics()
        print("\n[DATABASE STATISTICS]")
        print(f"   - Total Tasks:     {stats['total']}")
        print(f"   - Completed:       {stats['completed']} ({stats['completed']/stats['total']*100 if stats['total'] > 0 else 0:.1f}%)")
        print(f"   - Failed:          {stats['failed']} ({stats['failed']/stats['total']*100 if stats['total'] > 0 else 0:.1f}%)")
        print(f"   - Pending:         {stats['pending']} ({stats['pending']/stats['total']*100 if stats['total'] > 0 else 0:.1f}%)")
        print(f"   - Average Quality: {stats['avg_quality']:.2%}")
        print()
        return

    if cli_args.list_failed:
        db.list_failed_tasks()
        return

    # Print configuration
    print_configuration(cli_args)

    # Exit if dry run
    if cli_args.dry_run:
        print("[INFO] Dry run complete - no files were processed")
        return

    # Inventory files if needed
    if not cli_args.retry_failed and cli_args.scan_folders:
        # Check if we need to run inventory
        stats = db.get_statistics()
        pending_count = stats.get('pending', 0)

        # Run inventory if database was reset or no pending files
        if cli_args.reset_db or pending_count == 0:
            print("\n[1/3] Inventorying files...")
            count = inventory_files(cli_args, db)

            if count > 0:
                print(f"Added {count} new files to process queue")

            # Update pending count
            stats = db.get_statistics()
            pending_count = stats.get('pending', 0)
        else:
            print(f"\n[1/3] Found {pending_count} pending files in database - skipping inventory")

        if pending_count == 0:
            print("No files to process!")
            return

    # Process files
    print(f"\n[2/3] Processing files...")
    if cli_args.workers > 1:
        print(f"[INFO] Using {cli_args.workers} TRUE PARALLEL WORKERS")
        print(f"[INFO] Each worker will process batches of {cli_args.batch_size} files")
    else:
        print(f"[INFO] Single worker processing batches of {cli_args.batch_size} files")

    engine = NoteSynthesisEngine(cli_args)

    # Get initial statistics
    initial_stats = engine.db.get_statistics()
    total_files = initial_stats.get('pending', 0) + initial_stats.get('failed', 0)

    if total_files == 0:
        print("No files to process!")
        return

    print(f"[INFO] Total files to process: {total_files}")

    batch_num = 0
    total_processed = 0

    while True:
        batch_num += 1

        # Process batch (this now handles its own progress bars)
        processed = await engine.process_batch()
        total_processed += processed

        if processed == 0:
            break

        # For multiple batches, suggest context reset periodically
        if batch_num % 5 == 0 and cli_args.workers == 1:
            print("\n[INFO] Consider restarting to clear context if quality degrades")

        # Brief pause between batches (only for single worker mode)
        if cli_args.workers == 1:
            await asyncio.sleep(2)

    # Final report
    print("\n[3/3] Processing complete!")

    stats = engine.db.get_statistics()
    print(f"""
    +==============================================================+
    |                      Final Results                          |
    +==============================================================+
    |  Total Files:        {stats['total']:5d}                              |
    |  Completed:          {stats['completed']:5d} ({stats['completed']/stats['total']*100 if stats['total'] > 0 else 0:.1f}%)                      |
    |  Failed:             {stats['failed']:5d}                              |
    |  Average Quality:    {stats['avg_quality']:.2%}                          |
    +==============================================================+
    """)

    if stats['failed'] > 0:
        print(f"\n[WARNING] {stats['failed']} files failed. Use -list-failed to view details.")
        print("You can retry failed files with: -retry-failed")

# ==============================================================================
# Entry Point
# ==============================================================================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
    except Exception as e:
        logging.error(f"Application error: {e}")
        raise