#!/usr/bin/env python3
"""
Claude Code CLI Authentication Template
========================================

This template demonstrates how to use Claude Agent SDK with Claude Code CLI
authentication instead of direct API keys. This approach uses your Claude Code
subscription (via npm package) rather than paying separately for API usage.

AUTHENTICATION FLOW:
--------------------
1. User installs Claude Code CLI: npm install -g @anthropic-ai/claude-code
2. User logs in once: claude-code login (opens browser for OAuth)
3. Python SDK automatically uses CLI authentication - NO API KEY NEEDED
4. All API calls are billed through Claude Code subscription

PREREQUISITES:
--------------
1. Node.js installed (for npm)
2. Claude Code CLI: npm install -g @anthropic-ai/claude-code
3. Login once: claude-code login
4. Python SDK: pip install claude-agent-sdk

BENEFITS:
---------
- No API key management in code or environment variables
- Uses existing Claude Code subscription billing
- Automatic token refresh handled by CLI
- Same models available as direct API

Author: Template generated from KevinTheAntagonizerClaudeCodeNotesMaker
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, Dict, List

# =============================================================================
# CLAUDE AGENT SDK IMPORTS
# =============================================================================
# These are the core imports needed for Claude Code CLI authentication

from claude_agent_sdk import (
    # Main query function - the primary way to interact with Claude
    query,

    # Options container for configuring agent behavior
    ClaudeAgentOptions,

    # Response types for parsing Claude's responses
    AssistantMessage,
    TextBlock,

    # Error types for proper exception handling
    ClaudeSDKError,       # Base error class
    CLINotFoundError,     # Claude Code CLI not installed
    ProcessError,         # CLI process failed
    CLIJSONDecodeError    # Response parsing failed
)

# =============================================================================
# AVAILABLE MODELS
# =============================================================================
# These are the models available through Claude Code CLI
# The SDK will automatically use these via CLI authentication

AVAILABLE_MODELS = {
    # Claude 3 Family
    "opus": "claude-3-opus-20240229",           # Most capable, highest cost
    "sonnet": "claude-3-sonnet-20240229",       # Balanced performance/cost
    "haiku": "claude-3-haiku-20240307",         # Fast, cheapest

    # Claude 3.5 (Better than Claude 3)
    "sonnet-3.5": "claude-3-5-sonnet-20241022", # Recommended for most tasks

    # Claude 4.5 (Latest generation)
    "sonnet-4.5": "claude-sonnet-4-5-20250929", # Latest, best quality
}

DEFAULT_MODEL = "sonnet-4.5"


# =============================================================================
# AUTHENTICATION VERIFICATION
# =============================================================================

def verify_cli_installation() -> bool:
    """
    Verify Claude Code CLI is installed and accessible.

    Returns:
        bool: True if CLI is available, False otherwise
    """
    import shutil

    cli_path = shutil.which('claude-code')
    if cli_path:
        print(f"[OK] Claude Code CLI found at: {cli_path}")
        return True
    else:
        print("[ERROR] Claude Code CLI not found!")
        print("Install with: npm install -g @anthropic-ai/claude-code")
        return False


def verify_cli_login() -> bool:
    """
    Verify user is logged into Claude Code CLI.

    Returns:
        bool: True if logged in, False otherwise
    """
    import subprocess

    try:
        result = subprocess.run(
            ['claude-code', 'whoami'],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print(f"[OK] Logged in as: {result.stdout.strip()}")
            return True
        else:
            print("[ERROR] Not logged in to Claude Code CLI!")
            print("Login with: claude-code login")
            return False

    except subprocess.TimeoutExpired:
        print("[ERROR] CLI login check timed out")
        return False
    except FileNotFoundError:
        print("[ERROR] Claude Code CLI not found")
        return False


# =============================================================================
# BASIC QUERY EXAMPLE
# =============================================================================

async def simple_query(prompt: str, model: str = DEFAULT_MODEL) -> Optional[str]:
    """
    Make a simple query to Claude using Claude Code CLI authentication.

    This is the most basic usage pattern. The SDK automatically handles
    authentication through the CLI - no API key needed!

    Args:
        prompt: The prompt to send to Claude
        model: Model alias from AVAILABLE_MODELS (default: sonnet-4.5)

    Returns:
        Claude's response text, or None if failed
    """

    # Resolve model alias to full model ID
    model_id = AVAILABLE_MODELS.get(model, AVAILABLE_MODELS[DEFAULT_MODEL])

    # Configure agent options
    # NOTE: No API key! Authentication happens through Claude Code CLI
    options = ClaudeAgentOptions(
        model=model_id,
        max_turns=1,  # Single response (no conversation)
        cwd=Path.cwd()  # Working directory for file operations
    )

    try:
        # The query() function is async and yields response chunks
        full_response = ""

        async for message in query(prompt=prompt, options=options):
            # Extract text from assistant messages
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        full_response += block.text

        return full_response if full_response else None

    except CLINotFoundError:
        print("[ERROR] Claude Code CLI not installed or not in PATH")
        print("Install: npm install -g @anthropic-ai/claude-code")
        return None

    except ProcessError as e:
        print(f"[ERROR] CLI process failed with exit code: {e.exit_code}")
        return None

    except CLIJSONDecodeError as e:
        print(f"[ERROR] Failed to parse response: {e}")
        return None

    except Exception as e:
        print(f"[ERROR] Query failed: {e}")
        return None


# =============================================================================
# ADVANCED QUERY WITH SYSTEM PROMPT
# =============================================================================

async def query_with_persona(
    prompt: str,
    system_prompt: str,
    model: str = DEFAULT_MODEL,
    allowed_tools: List[str] = None,
    disallowed_tools: List[str] = None
) -> Optional[str]:
    """
    Query Claude with a custom system prompt (persona) and tool configuration.

    This pattern is useful for creating specialized agents with specific
    personalities or capabilities.

    Args:
        prompt: User prompt to send
        system_prompt: Custom system prompt defining agent behavior
        model: Model alias from AVAILABLE_MODELS
        allowed_tools: List of tools agent CAN use (e.g., ["Read", "Write"])
        disallowed_tools: List of tools agent CANNOT use

    Returns:
        Claude's response text, or None if failed
    """

    model_id = AVAILABLE_MODELS.get(model, AVAILABLE_MODELS[DEFAULT_MODEL])

    # Configure with system prompt and tool restrictions
    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        model=model_id,
        allowed_tools=allowed_tools or [],
        disallowed_tools=disallowed_tools or [],
        permission_mode='default',  # Respect allowed/disallowed tools
        max_turns=1,
        cwd=Path.cwd()
    )

    try:
        full_response = ""

        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        full_response += block.text

        return full_response if full_response else None

    except (CLINotFoundError, ProcessError, CLIJSONDecodeError) as e:
        print(f"[ERROR] Query failed: {e}")
        return None


# =============================================================================
# STREAMING RESPONSE EXAMPLE
# =============================================================================

async def streaming_query(prompt: str, model: str = DEFAULT_MODEL):
    """
    Stream Claude's response chunk by chunk.

    Useful for displaying real-time output to users.

    Args:
        prompt: The prompt to send
        model: Model alias

    Yields:
        Text chunks as they arrive
    """

    model_id = AVAILABLE_MODELS.get(model, AVAILABLE_MODELS[DEFAULT_MODEL])

    options = ClaudeAgentOptions(
        model=model_id,
        max_turns=1,
        cwd=Path.cwd()
    )

    try:
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        yield block.text

    except (CLINotFoundError, ProcessError, CLIJSONDecodeError) as e:
        print(f"[ERROR] Streaming failed: {e}")


# =============================================================================
# MAIN EXAMPLE USAGE
# =============================================================================

async def main():
    """
    Example usage demonstrating Claude Code CLI authentication.
    """

    print("\n" + "="*60)
    print("Claude Code CLI Authentication Demo")
    print("="*60 + "\n")

    # Step 1: Verify prerequisites
    print("[1/3] Checking prerequisites...")

    if not verify_cli_installation():
        print("\nSetup Instructions:")
        print("  1. Install Node.js from https://nodejs.org")
        print("  2. Run: npm install -g @anthropic-ai/claude-code")
        print("  3. Run: claude-code login")
        sys.exit(1)

    if not verify_cli_login():
        print("\nPlease login:")
        print("  Run: claude-code login")
        sys.exit(1)

    print()

    # Step 2: Simple query
    print("[2/3] Making a simple query...")

    response = await simple_query(
        prompt="What is 2 + 2? Reply with just the number.",
        model="haiku"  # Use cheapest model for demo
    )

    if response:
        print(f"Response: {response.strip()}")
    else:
        print("Query failed!")
        sys.exit(1)

    print()

    # Step 3: Query with persona
    print("[3/3] Query with custom persona...")

    expert_prompt = """You are a Python expert.
    When asked about code, provide concise, practical answers.
    Focus on best practices and real-world usage."""

    response = await query_with_persona(
        prompt="What's the best way to read a JSON file in Python?",
        system_prompt=expert_prompt,
        model="haiku",
        allowed_tools=["Read"],  # Only allow file reading
        disallowed_tools=["Write", "Bash"]  # Prevent modifications
    )

    if response:
        print(f"Expert Response:\n{response[:500]}...")  # Truncate for demo

    print("\n" + "="*60)
    print("Demo Complete!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
