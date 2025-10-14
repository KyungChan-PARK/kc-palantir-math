#!/usr/bin/env python3
"""
Obsidian MCP Server for Claude Code CLI
Wraps Obsidian REST API to provide MCP protocol access
"""

import asyncio
import json
import os
import sys
from typing import Any
import urllib3

# Disable SSL warnings for self-signed certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    import httpx
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
except ImportError:
    print("Error: Required packages not installed. Run: pip install mcp httpx", file=sys.stderr)
    sys.exit(1)

# Configuration from environment variables
API_KEY = os.getenv("OBSIDIAN_API_KEY", "e317ef44c1b5523c92d111fd0cb1a6c057304b7c8a1b0f426c96b98d2c7b8204")
API_URL = os.getenv("OBSIDIAN_API_URL", "https://127.0.0.1:27124")

# Create MCP server
server = Server("obsidian-mcp-server")

# HTTP client with SSL verification disabled for self-signed cert
http_client = httpx.AsyncClient(
    verify=False,
    headers={"Authorization": f"Bearer {API_KEY}"},
    timeout=30.0
)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available Obsidian tools"""
    return [
        types.Tool(
            name="obsidian_list_notes",
            description="List all notes in the Obsidian vault",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="obsidian_get_note",
            description="Get content of a specific note by filename",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Filename of the note (e.g., 'MyNote.md')"
                    }
                },
                "required": ["filename"]
            }
        ),
        types.Tool(
            name="obsidian_search",
            description="Search for notes containing specific text",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="obsidian_create_note",
            description="Create a new note or update existing note",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Filename for the note (e.g., 'NewNote.md')"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content of the note in Markdown format"
                    }
                },
                "required": ["filename", "content"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests"""

    try:
        if name == "obsidian_list_notes":
            # List all notes
            response = await http_client.get(f"{API_URL}/vault/")
            response.raise_for_status()
            data = response.json()
            files = data.get("files", [])

            # Filter for markdown files
            md_files = [f for f in files if f.endswith('.md')]

            return [types.TextContent(
                type="text",
                text=f"Found {len(md_files)} notes:\n" + "\n".join(f"- {f}" for f in md_files[:50])
            )]

        elif name == "obsidian_get_note":
            filename = arguments.get("filename")
            if not filename:
                raise ValueError("filename is required")

            # Get note content
            response = await http_client.get(f"{API_URL}/vault/{filename}")
            response.raise_for_status()
            content = response.text

            return [types.TextContent(
                type="text",
                text=f"Content of {filename}:\n\n{content}"
            )]

        elif name == "obsidian_search":
            query = arguments.get("query")
            if not query:
                raise ValueError("query is required")

            # Search notes
            response = await http_client.post(
                f"{API_URL}/search/simple/",
                json={"query": query}
            )
            response.raise_for_status()
            results = response.json()

            result_text = f"Search results for '{query}':\n\n"
            for result in results[:10]:
                filename = result.get("filename", "Unknown")
                score = result.get("score", 0)
                result_text += f"- {filename} (score: {score})\n"

            return [types.TextContent(
                type="text",
                text=result_text
            )]

        elif name == "obsidian_create_note":
            filename = arguments.get("filename")
            content = arguments.get("content")

            if not filename or not content:
                raise ValueError("filename and content are required")

            # Create or update note
            response = await http_client.put(
                f"{API_URL}/vault/{filename}",
                content=content,
                headers={"Content-Type": "text/markdown"}
            )
            response.raise_for_status()

            return [types.TextContent(
                type="text",
                text=f"Successfully created/updated note: {filename}"
            )]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error executing {name}: {str(e)}"
        )]


async def main():
    """Run the MCP server"""
    # Test connection
    try:
        response = await http_client.get(f"{API_URL}/")
        response.raise_for_status()
        print(f"Connected to Obsidian API at {API_URL}", file=sys.stderr)
    except Exception as e:
        print(f"Warning: Could not connect to Obsidian API: {e}", file=sys.stderr)

    # Run server
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="obsidian-mcp-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
