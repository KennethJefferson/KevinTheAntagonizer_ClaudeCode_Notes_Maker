"""
CLI Argument Parser for KevinTheAntagonizerClaudeCodeNotesMaker

This module handles all command-line argument parsing and validation.
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Optional


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
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        return Path(__file__).parent / f"runID.{timestamp}.log"


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
        required=True,
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
    return validate_args(args)


def print_configuration(cli_args: CLIArgs):
    """Print configuration summary for user validation"""

    print("\n" + "="*70)
    print("KevinTheAntagonizerClaudeCodeNotesMaker - Configuration")
    print("="*70)

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


if __name__ == "__main__":
    # Test the CLI parser
    cli_args = parse_arguments()
    print_configuration(cli_args)
