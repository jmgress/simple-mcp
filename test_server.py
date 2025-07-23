#!/usr/bin/env python3
"""
Test script for the simple MCP server.
This script demonstrates how to interact with the MCP server programmatically.
"""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from simple_mcp.server import app, value_store


async def test_all_tools():
    """Test all available tools in the MCP server."""
    print("=== Testing Simple MCP Server ===\n")
    
    # Test get_store_info
    print("1. Getting store info:")
    result = await app.call_tool('get_store_info', {})
    print(f"   {result[1]['result']}\n")
    
    # Test set_value with string
    print("2. Setting string value:")
    result = await app.call_tool('set_value', {'key': 'greeting', 'value': 'Hello, MCP!'})
    print(f"   {result[1]['result']}\n")
    
    # Test set_value with JSON
    print("3. Setting JSON value:")
    result = await app.call_tool('set_value', {'key': 'config', 'value': '{"timeout": 30, "retries": 3}'})
    print(f"   {result[1]['result']}\n")
    
    # Test get_value
    print("4. Getting values:")
    for key in ['greeting', 'config']:
        result = await app.call_tool('get_value', {'key': key})
        print(f"   {key}: {result[1]['result']}")
    print()
    
    # Test list_keys
    print("5. Listing all keys:")
    result = await app.call_tool('list_keys', {})
    print(f"   {result[1]['result']}\n")
    
    # Test get_value with non-existent key
    print("6. Getting non-existent key:")
    result = await app.call_tool('get_value', {'key': 'nonexistent'})
    print(f"   {result[1]['result']}\n")
    
    # Test delete_value
    print("7. Deleting a value:")
    result = await app.call_tool('delete_value', {'key': 'greeting'})
    print(f"   {result[1]['result']}\n")
    
    # Test list_keys after deletion
    print("8. Listing keys after deletion:")
    result = await app.call_tool('list_keys', {})
    print(f"   {result[1]['result']}\n")
    
    # Test clear_values
    print("9. Clearing all values:")
    result = await app.call_tool('clear_values', {})
    print(f"   {result[1]['result']}\n")
    
    # Test list_keys after clearing
    print("10. Listing keys after clearing:")
    result = await app.call_tool('list_keys', {})
    print(f"    {result[1]['result']}\n")
    
    print("=== All tests completed successfully! ===")


if __name__ == "__main__":
    asyncio.run(test_all_tools())