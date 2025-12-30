# Claude Code CLI Authentication Prompt

Use this prompt when starting a new Claude Agent project that should use Claude Code subscription authentication instead of API keys.

---

## The Prompt

```
I need to create a Python application that uses Claude AI through the Claude Agent SDK.

IMPORTANT REQUIREMENTS:
1. Use Claude Code CLI authentication (NOT direct API keys)
2. Authentication happens through `claude-code login` (npm package)
3. No API key management needed in code or environment variables
4. Uses existing Claude Code subscription billing

Please use the templates in `__templates/` as reference:
- `claude_code_auth_template.py` - Full documented template with examples
- `claude_code_auth_minimal.py` - Bare minimum code to get started
- `claude_code_auth_with_error_handling.py` - Production-ready with retries

KEY PATTERNS TO FOLLOW:
1. Import from `claude_agent_sdk` (not `anthropic`)
2. Use `query()` async function for Claude interactions
3. Use `ClaudeAgentOptions` for configuration
4. Handle these error types: CLINotFoundError, ProcessError, CLIJSONDecodeError
5. No API key needed - CLI handles authentication

PREREQUISITES (user must do once):
```bash
npm install -g @anthropic-ai/claude-code
claude-code login
pip install claude-agent-sdk
```

The core pattern is:
```python
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock

async def ask_claude(prompt):
    options = ClaudeAgentOptions(model="claude-sonnet-4-5-20250929", max_turns=1)
    response = ""
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    response += block.text
    return response
```
```

---

## Quick Reference

### Available Models
```python
AVAILABLE_MODELS = {
    "opus": "claude-3-opus-20240229",           # Most capable
    "sonnet": "claude-3-sonnet-20240229",       # Balanced
    "haiku": "claude-3-haiku-20240307",         # Fast/cheap
    "sonnet-3.5": "claude-3-5-sonnet-20241022", # Better than opus
    "sonnet-4.5": "claude-sonnet-4-5-20250929", # Latest (DEFAULT)
}
```

### Required Imports
```python
from claude_agent_sdk import (
    query,                  # Main function to call Claude
    ClaudeAgentOptions,     # Configuration container
    AssistantMessage,       # Response type
    TextBlock,              # Text content type
    CLINotFoundError,       # CLI not installed
    ProcessError,           # CLI process failed
    CLIJSONDecodeError      # Response parsing failed
)
```

### Key Differences from Direct API

| Aspect | Direct API (anthropic) | Claude Code CLI (claude_agent_sdk) |
|--------|------------------------|-----------------------------------|
| Auth | API key in code/env | `claude-code login` (one-time) |
| Package | `pip install anthropic` | `pip install claude-agent-sdk` + npm CLI |
| Billing | Separate API billing | Claude Code subscription |
| Function | `client.messages.create()` | `async for msg in query()` |
| Response | `message.content` | Iterate through `AssistantMessage` |

### Template Files

1. **`claude_code_auth_template.py`** - Start here
   - Full documentation
   - Verification functions
   - Simple and advanced examples
   - Streaming example

2. **`claude_code_auth_minimal.py`** - Quickest start
   - Under 30 lines
   - Just the essentials
   - Copy-paste ready

3. **`claude_code_auth_with_error_handling.py`** - Production ready
   - Prerequisite checking
   - Retry logic with exponential backoff
   - Timeout handling
   - Custom exception classes

---

## Common Issues

### "Claude Code CLI not found"
```bash
npm install -g @anthropic-ai/claude-code
```

### "Not logged in"
```bash
claude-code login
```

### "Permission denied" on Windows
Run terminal as administrator for npm global install, or use:
```bash
npm install -g @anthropic-ai/claude-code --prefix %APPDATA%\npm
```

### Rate limiting
- Add delays between requests: `await asyncio.sleep(1)`
- Use exponential backoff on retries
- Consider using `haiku` model for high-volume tasks
