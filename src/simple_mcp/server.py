"""Simple MCP Server for value lookup operations."""

import json
import sys
from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP
from mcp import types


class ValueStore:
    """Simple in-memory key-value store for the MCP server."""
    
    def __init__(self) -> None:
        self._store: Dict[str, Any] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value by key."""
        return self._store.get(key)
    
    def set(self, key: str, value: Any) -> None:
        """Set a value for a key."""
        self._store[key] = value
    
    def delete(self, key: str) -> bool:
        """Delete a key-value pair. Returns True if key existed."""
        if key in self._store:
            del self._store[key]
            return True
        return False
    
    def list_keys(self) -> list[str]:
        """List all keys in the store."""
        return list(self._store.keys())
    
    def clear(self) -> None:
        """Clear all key-value pairs."""
        self._store.clear()
    
    def size(self) -> int:
        """Get the number of key-value pairs."""
        return len(self._store)


# Initialize the global value store
value_store = ValueStore()

# Create the FastMCP server
app = FastMCP(
    name="simple-mcp-server",
    instructions="""A simple MCP server that provides value lookup operations.
    
Available operations:
- get_value: Retrieve a value by key
- set_value: Store a key-value pair  
- delete_value: Remove a key-value pair
- list_keys: List all available keys
- clear_values: Clear all stored values
- get_store_info: Get information about the store
"""
)


@app.tool()
def get_value(key: str) -> str:
    """Get a value from the store by key.
    
    Args:
        key: The key to look up
        
    Returns:
        The value associated with the key, or an error message if not found
    """
    value = value_store.get(key)
    if value is None:
        return f"Key '{key}' not found in store"
    
    # Convert value to string representation for return
    if isinstance(value, (dict, list)):
        return json.dumps(value, indent=2)
    return str(value)


@app.tool()
def set_value(key: str, value: str) -> str:
    """Set a key-value pair in the store.
    
    Args:
        key: The key to store
        value: The value to store (will be parsed as JSON if possible)
        
    Returns:
        Confirmation message
    """
    # Try to parse as JSON, fall back to string
    try:
        parsed_value = json.loads(value)
        value_store.set(key, parsed_value)
        return f"Set key '{key}' to JSON value: {json.dumps(parsed_value)}"
    except json.JSONDecodeError:
        value_store.set(key, value)
        return f"Set key '{key}' to string value: {value}"


@app.tool()
def delete_value(key: str) -> str:
    """Delete a key-value pair from the store.
    
    Args:
        key: The key to delete
        
    Returns:
        Confirmation message
    """
    if value_store.delete(key):
        return f"Deleted key '{key}' from store"
    else:
        return f"Key '{key}' not found in store"


@app.tool()
def list_keys() -> str:
    """List all keys in the store.
    
    Returns:
        A formatted list of all keys in the store
    """
    keys = value_store.list_keys()
    if not keys:
        return "Store is empty"
    
    return f"Keys in store ({len(keys)} total):\n" + "\n".join(f"  - {key}" for key in sorted(keys))


@app.tool()
def clear_values() -> str:
    """Clear all key-value pairs from the store.
    
    Returns:
        Confirmation message
    """
    size = value_store.size()
    value_store.clear()
    return f"Cleared all {size} key-value pairs from store"


@app.tool()
def get_store_info() -> str:
    """Get information about the current state of the store.
    
    Returns:
        Information about the store including size and sample keys
    """
    size = value_store.size()
    keys = value_store.list_keys()
    
    info = f"Store Information:\n"
    info += f"  Size: {size} key-value pairs\n"
    
    if keys:
        sample_keys = sorted(keys)[:5]  # Show up to 5 keys as samples
        info += f"  Sample keys: {', '.join(sample_keys)}"
        if len(keys) > 5:
            info += f" (and {len(keys) - 5} more)"
    else:
        info += "  Store is empty"
    
    return info


def main():
    """Main entry point for the MCP server."""
    # Initialize with some sample data for demonstration
    value_store.set("greeting", "Hello, World!")
    value_store.set("pi", 3.14159)
    value_store.set("colors", ["red", "green", "blue"])
    value_store.set("user", {"name": "Alice", "age": 30, "city": "New York"})
    
    print(f"Starting simple-mcp-server with {value_store.size()} sample values...", file=sys.stderr)
    
    # Run the server using stdio transport - FastMCP handles the asyncio loop
    app.run("stdio")


def cli_main():
    """CLI entry point."""
    main()


if __name__ == "__main__":
    cli_main()