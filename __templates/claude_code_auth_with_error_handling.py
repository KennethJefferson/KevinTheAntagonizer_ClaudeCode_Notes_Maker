#!/usr/bin/env python3
"""
Claude Code Authentication Template with Production Error Handling
===================================================================

This template includes comprehensive error handling for production use.
Handles all common failure scenarios with actionable error messages.

SETUP:
  npm install -g @anthropic-ai/claude-code
  claude-code login
  pip install claude-agent-sdk
"""

import asyncio
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    CLINotFoundError,
    ProcessError,
    CLIJSONDecodeError,
    ClaudeSDKError
)


# =============================================================================
# ERROR HANDLING UTILITIES
# =============================================================================

class ClaudeAuthError(Exception):
    """Custom exception for authentication issues"""
    pass


def check_prerequisites() -> None:
    """
    Verify all prerequisites are met. Raises ClaudeAuthError if not.

    Call this at application startup to fail fast with clear messages.
    """

    # Check 1: Claude Code CLI installed
    cli_path = shutil.which('claude-code')
    if not cli_path:
        raise ClaudeAuthError(
            "Claude Code CLI not found!\n\n"
            "Install with:\n"
            "  npm install -g @anthropic-ai/claude-code\n\n"
            "Then login:\n"
            "  claude-code login"
        )

    # Check 2: User is logged in
    try:
        result = subprocess.run(
            ['claude-code', 'whoami'],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            raise ClaudeAuthError(
                "Not logged in to Claude Code!\n\n"
                "Login with:\n"
                "  claude-code login\n\n"
                "This will open your browser for authentication."
            )

    except subprocess.TimeoutExpired:
        raise ClaudeAuthError(
            "Claude Code CLI timed out checking login status.\n"
            "Try running 'claude-code whoami' manually."
        )
    except FileNotFoundError:
        raise ClaudeAuthError("Claude Code CLI not found in PATH")


# =============================================================================
# QUERY FUNCTION WITH FULL ERROR HANDLING
# =============================================================================

async def safe_query(
    prompt: str,
    model: str = "claude-sonnet-4-5-20250929",
    system_prompt: str = None,
    max_retries: int = 3,
    timeout_seconds: int = 120
) -> Optional[str]:
    """
    Query Claude with comprehensive error handling and retries.

    Args:
        prompt: User prompt to send
        model: Full model ID (e.g., "claude-sonnet-4-5-20250929")
        system_prompt: Optional system prompt for agent persona
        max_retries: Number of retry attempts on transient failures
        timeout_seconds: Maximum time to wait for response

    Returns:
        Claude's response text, or None if all retries failed

    Raises:
        ClaudeAuthError: If authentication is not set up
    """

    # Configure options
    options = ClaudeAgentOptions(
        model=model,
        max_turns=1,
        cwd=Path.cwd()
    )

    if system_prompt:
        options.system_prompt = system_prompt

    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            full_response = ""

            # Use asyncio.wait_for for timeout
            async def do_query():
                nonlocal full_response
                async for message in query(prompt=prompt, options=options):
                    if isinstance(message, AssistantMessage):
                        for block in message.content:
                            if isinstance(block, TextBlock):
                                full_response += block.text

            await asyncio.wait_for(do_query(), timeout=timeout_seconds)

            if full_response:
                return full_response
            else:
                print(f"[WARNING] Empty response on attempt {attempt}/{max_retries}")

        except CLINotFoundError:
            # This is a setup issue, not transient - don't retry
            raise ClaudeAuthError(
                "Claude Code CLI not found!\n"
                "Install: npm install -g @anthropic-ai/claude-code\n"
                "Login: claude-code login"
            )

        except ProcessError as e:
            last_error = e
            if e.exit_code == 1:
                # Exit code 1 often means auth issue
                print(f"[ERROR] CLI process failed (exit code 1)")
                print("This often means you need to re-login:")
                print("  claude-code login")
                # Could be transient, retry
            else:
                print(f"[ERROR] CLI process failed with code {e.exit_code}")

            if attempt < max_retries:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"[RETRY] Waiting {wait_time}s before retry {attempt + 1}...")
                await asyncio.sleep(wait_time)

        except CLIJSONDecodeError as e:
            last_error = e
            print(f"[ERROR] Failed to parse response: {e}")

            if attempt < max_retries:
                wait_time = 2 ** attempt
                print(f"[RETRY] Waiting {wait_time}s before retry {attempt + 1}...")
                await asyncio.sleep(wait_time)

        except asyncio.TimeoutError:
            last_error = TimeoutError(f"Query timed out after {timeout_seconds}s")
            print(f"[ERROR] Request timed out after {timeout_seconds} seconds")

            if attempt < max_retries:
                print(f"[RETRY] Attempt {attempt + 1}/{max_retries}...")

        except ClaudeSDKError as e:
            last_error = e
            print(f"[ERROR] SDK error: {e}")

            if attempt < max_retries:
                wait_time = 2 ** attempt
                await asyncio.sleep(wait_time)

        except Exception as e:
            last_error = e
            print(f"[ERROR] Unexpected error: {type(e).__name__}: {e}")

            if attempt < max_retries:
                wait_time = 2 ** attempt
                await asyncio.sleep(wait_time)

    # All retries exhausted
    print(f"[FAILED] All {max_retries} attempts failed. Last error: {last_error}")
    return None


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

async def main():
    """Example showing production-ready error handling"""

    print("Claude Code Authentication - Production Example\n")

    # Step 1: Check prerequisites at startup (fail fast)
    try:
        check_prerequisites()
        print("[OK] Prerequisites verified\n")
    except ClaudeAuthError as e:
        print(f"[SETUP ERROR]\n{e}")
        sys.exit(1)

    # Step 2: Make a query with full error handling
    response = await safe_query(
        prompt="Explain Python decorators in one sentence.",
        model="claude-3-haiku-20240307",  # Cheapest for demo
        max_retries=3,
        timeout_seconds=30
    )

    if response:
        print(f"Response: {response.strip()}")
    else:
        print("Query failed after all retries")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
