#!/usr/bin/env python3
"""
Advanced Note Synthesis with Custom Tools and SDK MCP Server
=============================================================
This version uses the Claude Agent SDK's in-process MCP server feature
to create custom tools that enforce synthesis quality.

Authentication is handled through Claude Code CLI login.
This gives you programmatic control over what the agent can and cannot do.
"""

import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional
import logging

from claude_agent_sdk import (
    ClaudeAgentOptions,
    ClaudeSDKClient,
    tool,
    create_sdk_mcp_server,
    AssistantMessage,
    TextBlock,
    HookMatcher
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==============================================================================
# Custom Tools for Note Synthesis
# ==============================================================================

# Global state for tracking
synthesis_stats = {
    'files_processed': 0,
    'total_quality': 0,
    'current_file': None
}

@tool(
    name="synthesize_transcript",
    description="Synthesize a technical transcript into comprehensive notes",
    input_schema={
        "type": "object",
        "properties": {
            "transcript": {"type": "string", "description": "The transcript text to synthesize"},
            "lecture_name": {"type": "string", "description": "Name of the lecture"},
            "course_name": {"type": "string", "description": "Name of the course"}
        },
        "required": ["transcript", "lecture_name", "course_name"]
    }
)
async def synthesize_transcript(args):
    """
    Custom tool that enforces synthesis constraints
    This runs IN-PROCESS, giving you full control
    """
    transcript = args['transcript']
    lecture_name = args['lecture_name']
    course_name = args['course_name']
    
    # Track what we're processing
    synthesis_stats['current_file'] = lecture_name
    
    # Build the synthesis prompt with constraints
    synthesis_prompt = f"""
# {lecture_name}
## Course: {course_name}

Create comprehensive learning notes from this transcript.
Extract EVERY concept, pattern, technique, and best practice.
Add expert commentary and real-world insights.
Use clear markdown structure with headers, code blocks, and emphasis.
Be thorough, opinionated, and practical.

Transcript:
{transcript}
"""
    
    # Return instructions for Claude to synthesize
    return {
        "content": [
            {
                "type": "text",
                "text": synthesis_prompt
            }
        ]
    }

@tool(
    name="check_quality",
    description="Check if synthesized notes meet quality standards",
    input_schema={
        "type": "object",
        "properties": {
            "content": {"type": "string", "description": "The synthesized content to check"},
            "lecture_name": {"type": "string", "description": "Name of the lecture"}
        },
        "required": ["content", "lecture_name"]
    }
)
async def check_quality(args):
    """
    Quality control tool that validates synthesis
    """
    content = args['content']
    lecture_name = args['lecture_name']
    
    issues = []
    score = 0.0
    
    # Length check
    if len(content) >= 1500:
        score += 0.25
    else:
        issues.append(f"Too short: {len(content)} chars")
    
    # Structure check
    if '##' in content or '###' in content:
        score += 0.25
    else:
        issues.append("Missing headers")
    
    # Kevin's voice
    kevin_phrases = ['production', 'real-world', 'actually', 'gotcha']
    if any(phrase in content.lower() for phrase in kevin_phrases):
        score += 0.25
    else:
        issues.append("Missing personality")
    
    # No automation markers
    bad_markers = ['automated', 'script', 'processed files']
    if not any(marker in content.lower() for marker in bad_markers):
        score += 0.25
    else:
        issues.append("AUTOMATION DETECTED")
        score = 0
    
    # Update stats
    synthesis_stats['total_quality'] += score
    synthesis_stats['files_processed'] += 1
    
    result = {
        "quality_score": score,
        "passes": score >= 0.7,
        "issues": issues
    }
    
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(result, indent=2)
            }
        ]
    }

@tool(
    name="save_notes",
    description="Save synthesized notes to a markdown file",
    input_schema={
        "type": "object",
        "properties": {
            "content": {"type": "string", "description": "The markdown content to save"},
            "srt_path": {"type": "string", "description": "Path to the original SRT file"}
        },
        "required": ["content", "srt_path"]
    }
)
async def save_notes(args):
    """
    Save notes with the correct naming convention
    """
    content = args['content']
    srt_path = Path(args['srt_path'])
    
    output_path = srt_path.parent / f"{srt_path.stem}_KevinTheAntagonizer_Notes.md"
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Notes saved to: {output_path}"
                }
            ]
        }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error saving notes: {e}"
                }
            ]
        }

# ==============================================================================
# Custom Hooks for Process Control
# ==============================================================================

async def prevent_automation_hook(input_data, tool_use_id, context):
    """
    Hook that prevents Claude from writing automation scripts
    """
    tool_name = input_data.get("tool_name", "")
    
    # Block Python execution and script creation
    if tool_name in ["RunPython", "CreatePythonScript"]:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Automation scripts are not allowed. You must synthesize manually."
            }
        }
    
    # Allow other tools
    return {}

async def enforce_quality_hook(input_data, tool_use_id, context):
    """
    Hook that enforces quality standards on Write operations
    """
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    
    if tool_name == "Write":
        content = tool_input.get("content", "")
        
        # Check for automation markers
        if any(marker in content.lower() for marker in ['automated', 'batch processed', 'script generated']):
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "Content appears to be auto-generated. Manual synthesis required."
                }
            }
    
    return {}

# ==============================================================================
# Main Synthesis Application
# ==============================================================================

class AdvancedSynthesisApp:
    """
    Advanced synthesis using SDK MCP servers and custom tools
    """
    
    def __init__(self):
        # Create an in-process MCP server with our custom tools
        self.mcp_server = create_sdk_mcp_server(
            name="synthesis-tools",
            version="1.0.0",
            tools=[synthesize_transcript, check_quality, save_notes]
        )
        
        # Configure agent options
        self.options = ClaudeAgentOptions(
            system_prompt="""You are Kevin Burleigh, a battle-tested Java/Spring Boot architect.
You synthesize transcripts into comprehensive learning notes.
You MUST use the provided synthesis tools.
You CANNOT write automation scripts.""",
            
            # Register our MCP server
            mcp_servers={"synthesis": self.mcp_server},
            
            # Allow our custom tools
            allowed_tools=[
                "mcp__synthesis__synthesize_transcript",
                "mcp__synthesis__check_quality", 
                "mcp__synthesis__save_notes",
                "Read",
                "Write"
            ],
            
            # Explicitly disallow automation tools
            disallowed_tools=["RunPython", "CreatePythonScript", "Bash"],
            
            # Add hooks for additional control
            hooks={
                "PreToolUse": [
                    HookMatcher(matcher="*", hooks=[prevent_automation_hook, enforce_quality_hook])
                ]
            },
            
            permission_mode='default'  # Use default permission handling
        )
    
    async def process_file(self, srt_path: str, course_name: str, lecture_name: str):
        """
        Process a single file using our custom synthesis pipeline
        """
        logger.info(f"Processing: {lecture_name}")
        
        # Read and clean the SRT content
        transcript = self.clean_srt(srt_path)
        
        if not transcript:
            logger.error(f"Failed to read {srt_path}")
            return False
        
        # Check size
        if len(transcript) > 50000:
            logger.warning(f"File too large: {lecture_name}")
            return False
        
        # Use SDK client for interactive processing
        async with ClaudeSDKClient(options=self.options) as client:
            # Send the synthesis request
            prompt = f"""Process this transcript using the synthesis tools:
            
1. Use synthesize_transcript tool with:
   - transcript: (provided below)
   - lecture_name: "{lecture_name}"
   - course_name: "{course_name}"

2. Check the quality with check_quality tool

3. If quality passes, save with save_notes tool to: {srt_path}

Transcript:
{transcript}"""
            
            await client.query(prompt)
            
            # Collect the response
            full_response = ""
            async for msg in client.receive_response():
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, TextBlock):
                            full_response += block.text
            
            # Check if successful
            if "saved to" in full_response.lower():
                logger.info(f"✓ Completed: {lecture_name}")
                return True
            else:
                logger.warning(f"Failed to process: {lecture_name}")
                return False
    
    def clean_srt(self, srt_path: str) -> Optional[str]:
        """Clean SRT file content"""
        try:
            with open(srt_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            lines = []
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.isdigit() and '-->' not in line:
                    lines.append(line)
            
            return ' '.join(lines)
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return None
    
    async def process_batch(self, files: List[Dict]):
        """Process a batch of files"""
        success_count = 0
        
        for file_info in files:
            if await self.process_file(
                file_info['srt_path'],
                file_info['course_name'],
                file_info['lecture_name']
            ):
                success_count += 1
            
            # Brief pause between files
            await asyncio.sleep(1)
        
        avg_quality = synthesis_stats['total_quality'] / max(synthesis_stats['files_processed'], 1)
        logger.info(f"Batch complete: {success_count}/{len(files)} successful")
        logger.info(f"Average quality: {avg_quality:.2%}")
        
        return success_count

# ==============================================================================
# Example Usage
# ==============================================================================

async def main():
    """
    Example of using the advanced synthesis app
    """
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║  Advanced Synthesis with Custom Tools & MCP Servers      ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Initialize the app
    app = AdvancedSynthesisApp()
    
    # Example files to process
    test_files = [
        {
            'srt_path': r"N:\__Java.Web.Spring\___Masters.Unsorted\Spring Boot Basics\lecture1.srt",
            'course_name': "Spring Boot Basics",
            'lecture_name': "Introduction to Dependency Injection"
        },
        # Add more files here
    ]
    
    # Process the batch
    await app.process_batch(test_files)
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║                      Results                             ║
    ╠══════════════════════════════════════════════════════════╣
    ║  Files Processed: {synthesis_stats['files_processed']:3d}                                     ║
    ║  Average Quality: {synthesis_stats['total_quality'] / max(synthesis_stats['files_processed'], 1):.2%}                                  ║
    ╚══════════════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    asyncio.run(main())
