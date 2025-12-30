#!/usr/bin/env python3
"""
MINIMAL Claude Code Authentication Template
============================================

The absolute minimum code needed to use Claude via Claude Code CLI.
No API keys - uses your Claude Code subscription.

SETUP (one-time):
  npm install -g @anthropic-ai/claude-code
  claude-code login
  pip install claude-agent-sdk
"""

import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock


async def ask_claude(prompt: str) -> str:
    """Send a prompt to Claude, get a response. That's it."""

    options = ClaudeAgentOptions(
        model="claude-sonnet-4-5-20250929",  # or any model you prefer
        max_turns=1
    )

    response = ""
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    response += block.text

    return response


# Usage
if __name__ == "__main__":
    result = asyncio.run(ask_claude("What is Python?"))
    print(result)
