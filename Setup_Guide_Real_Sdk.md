# Complete Setup Guide: Claude Agent SDK for Note Synthesis

## Prerequisites & Installation

### Step 1: Install Claude Code CLI (Required)
```bash
# Install Node.js first if you don't have it
# Download from: https://nodejs.org/

# Install Claude Code CLI globally
npm install -g @anthropic-ai/claude-code

# Verify installation
claude-code --version
```

### Step 2: Login to Claude Code
```bash
# Login to Claude Code CLI (handles authentication)
claude-code login

# Verify you're logged in
claude-code whoami
```

### Step 3: Install Python SDK
```bash
# Install the SDK
pip install claude-agent-sdk

# Note: asyncio and pathlib are built-in to Python 3.7+
```

## Quick Test: Verify Everything Works

Create `test_sdk.py`:
```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def test():
    """Test that SDK is working"""
    try:
        async for message in query(prompt="Say 'SDK is working!'"):
            print(message)
        print("✓ SDK is working correctly!")
    except Exception as e:
        print(f"✗ Error: {e}")
        print("Check that Claude Code CLI is installed and you're logged in")
        print("Run: claude-code login")

if __name__ == "__main__":
    asyncio.run(test())
```

Run it:
```bash
python test_sdk.py
```

## The Complete Note Synthesis Solution

### Option 1: Simple Query-Based Approach
Best for: Straightforward synthesis without complex control flow

```python
#!/usr/bin/env python3
"""Simple synthesis using query() function"""

import asyncio
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock

async def synthesize_file(srt_path, course_name, lecture_name):
    # Read and clean SRT
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove timestamps
    lines = [l.strip() for l in content.split('\n') 
             if not l.strip().isdigit() and '-->' not in l and l.strip()]
    transcript = ' '.join(lines)
    
    # Configure options
    options = ClaudeAgentOptions(
        system_prompt="You are Kevin Burleigh, Java/Spring expert.",
        allowed_tools=["Read", "Write"],  # Limit tools
        disallowed_tools=["RunPython"],   # No automation
        max_turns=1
    )
    
    # Create synthesis prompt
    prompt = f"""Synthesize this transcript into comprehensive notes.
    
LECTURE: {lecture_name}
COURSE: {course_name}

TRANSCRIPT:
{transcript}

Create detailed markdown notes with headers, code blocks, and expert insights.
Minimum 1500 words."""
    
    # Get response
    full_response = ""
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    full_response += block.text
    
    # Save notes
    output_path = Path(srt_path).parent / f"{Path(srt_path).stem}_KevinTheAntagonizer_Notes.md"
    with open(output_path, 'w') as f:
        f.write(full_response)
    
    print(f"✓ Created: {output_path.name}")

# Run it
asyncio.run(synthesize_file(
    "path/to/lecture.srt",
    "Spring Boot Course",
    "Dependency Injection"
))
```

### Option 2: Interactive Client Approach
Best for: Complex workflows with multiple steps

```python
#!/usr/bin/env python3
"""Interactive synthesis using ClaudeSDKClient"""

import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

async def process_with_client(srt_path):
    options = ClaudeAgentOptions(
        system_prompt="You are Kevin, a Spring Boot expert.",
        allowed_tools=["Read", "Write", "Bash"],
        permission_mode='acceptEdits'  # Auto-accept file edits
    )
    
    async with ClaudeSDKClient(options=options) as client:
        # Send synthesis request
        await client.query(f"Read {srt_path} and create comprehensive notes")
        
        # Get response
        async for msg in client.receive_response():
            print(msg)
        
        # Follow up if needed
        await client.query("Add more code examples to the notes")
        
        async for msg in client.receive_response():
            print(msg)

asyncio.run(process_with_client("lecture.srt"))
```

### Option 3: Custom Tools with MCP Server
Best for: Maximum control and custom logic

```python
#!/usr/bin/env python3
"""Custom tools using SDK MCP server"""

from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeAgentOptions, ClaudeSDKClient

@tool("synthesize", "Create notes from transcript", {"transcript": str, "lecture": str})
async def synthesize_tool(args):
    # Your custom synthesis logic here
    return {
        "content": [{
            "type": "text",
            "text": f"# {args['lecture']}\n\nCustom synthesis here..."
        }]
    }

# Create MCP server with your tool
server = create_sdk_mcp_server(
    name="synthesis-tools",
    version="1.0.0",
    tools=[synthesize_tool]
)

# Use it
options = ClaudeAgentOptions(
    mcp_servers={"tools": server},
    allowed_tools=["mcp__tools__synthesize"]
)

async def main():
    async with ClaudeSDKClient(options=options) as client:
        await client.query("Use synthesize tool on this transcript: ...")
        async for msg in client.receive_response():
            print(msg)

asyncio.run(main())
```

## Running Your Complete Application

### 1. Prepare Your Files
```
N:\__Java.Web.Spring\___Masters.Unsorted\
├── ProcessFolderList.txt  # List of course paths
├── KevinTheAntagonizerClaudeCodeNotesMaker.py  # The main application
└── [Your course folders with .srt files]
```

### 2. Run the Application
```bash
cd N:\__Java.Web.Spring\___Masters.Unsorted
python KevinTheAntagonizerClaudeCodeNotesMaker.py
```

### 3. Monitor Progress
The application will:
- Create `synthesis_tasks.db` for tracking
- Process files in batches of 10
- Show quality scores for each file
- Save notes as `*_KevinTheAntagonizer_Notes.md`

## Troubleshooting

### Issue: "Claude Code CLI not found"
```bash
# Reinstall Claude Code
npm uninstall -g @anthropic-ai/claude-code
npm install -g @anthropic-ai/claude-code
```

### Issue: "Not logged in to Claude Code"
```bash
# Login to Claude Code CLI
claude-code login

# Verify login status
claude-code whoami
```

### Issue: "Process failed with exit code"
```python
# Add error handling
from claude_agent_sdk import CLINotFoundError, ProcessError

try:
    async for message in query(prompt="..."):
        pass
except CLINotFoundError:
    print("Install Claude Code CLI first")
except ProcessError as e:
    print(f"Error code {e.exit_code}: {e}")
```

### Issue: "Quality check failures"
```python
# Strengthen the prompt
prompt = """CRITICAL: You must manually synthesize this transcript.
Do NOT write automation scripts.
Be Kevin Burleigh - detailed, opinionated, practical.
Minimum 1500 words of real synthesis."""
```

## Advanced Features

### Hooks for Process Control
```python
async def prevent_scripts(input_data, tool_use_id, context):
    if input_data.get("tool_name") == "RunPython":
        return {
            "hookSpecificOutput": {
                "permissionDecision": "deny",
                "permissionDecisionReason": "No automation allowed"
            }
        }

options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="*", hooks=[prevent_scripts])]}
)
```

### Parallel Processing (Note on Limitations)
```python
# Note: Parallel processing with Claude Code CLI is limited
# since authentication is handled at the CLI level.
# For true parallel processing, consider:
# 1. Running multiple instances with different Claude Code sessions
# 2. Using session forking (see below)
# 3. Processing sequentially with efficient batching

async def process_sequential_batch(files):
    """Process files efficiently in sequence"""
    results = []
    for file in files:
        result = await synthesize_file(file)
        results.append(result)
        await asyncio.sleep(1)  # Rate limiting
    return results
```

### Session Forking for Context Management
```python
# Process in isolated sessions to prevent context pollution
async with ClaudeSDKClient(options=options) as client:
    for file in files[:50]:  # First 50 files
        # Each file gets fresh context
        forked = await client.fork()
        await forked.query(f"Process {file}")
```

## Best Practices

### 1. Prevent Automation
- Always use `disallowed_tools=["RunPython", "CreatePythonScript"]`
- Add hooks to block script creation
- Use explicit anti-automation language in prompts

### 2. Maintain Quality
- Check output length (>1500 chars)
- Verify markdown structure
- Look for Kevin's voice/personality
- Reject automation markers

### 3. Manage Context
- Process in batches of 10-20 files
- Consider restarting every 50 files
- Use session forking for isolation

### 4. Handle Errors Gracefully
```python
for attempt in range(3):
    try:
        result = await synthesize_file(path)
        if result:
            break
    except Exception as e:
        logger.error(f"Attempt {attempt+1} failed: {e}")
        await asyncio.sleep(5)  # Wait before retry
```

## Performance Tips

1. **Rate Limiting**: Add delays between API calls
```python
await asyncio.sleep(1)  # 1 second between calls
```

2. **Database for State**: Use SQLite, not text files
```python
import sqlite3
conn = sqlite3.connect("progress.db")
```

3. **Quality Gates**: Reject bad outputs immediately
```python
if len(output) < 1500 or "automated" in output.lower():
    return False  # Retry with stronger prompt
```

4. **Token Optimization**: Clean SRT files thoroughly
```python
# Remove all timestamps, numbers, empty lines
clean_text = ' '.join([l for l in lines if l and not l.isdigit()])
```

## Ready-to-Run Commands

```bash
# 1. Setup environment
npm install -g @anthropic-ai/claude-code
claude-code login
pip install claude-agent-sdk

# 2. Test SDK
python -c "import claude_agent_sdk; print('SDK ready')"

# 3. Run synthesis
cd N:\__Java.Web.Spring\___Masters.Unsorted
python KevinTheAntagonizerClaudeCodeNotesMaker.py

# 4. Check progress
sqlite3 synthesis_tasks.db "SELECT COUNT(*) FROM tasks WHERE status='completed'"

# 5. Retry failed files
sqlite3 synthesis_tasks.db "UPDATE tasks SET status='pending', attempts=0 WHERE status='failed'"
python KevinTheAntagonizerClaudeCodeNotesMaker.py
```

## Next Steps

1. **Start Small**: Test with 5 files first
2. **Verify Quality**: Check the output manually
3. **Scale Up**: Process in batches of 10-20
4. **Monitor**: Watch for quality degradation
5. **Optimize**: Adjust prompts based on results

The SDK approach eliminates all the manual orchestration complexity you experienced before. No more guessing about subagent invocation - just clean API calls!
