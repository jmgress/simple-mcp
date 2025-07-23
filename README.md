# Simple MCP Server

A simple Model Context Protocol (MCP) server that provides value lookup operations. This server implements a basic key-value store that can be accessed by MCP-compatible AI assistants and clients.

## Features

- **In-memory key-value store**: Store and retrieve data during the session
- **JSON support**: Automatically parses and formats JSON values
- **Multiple operations**: Get, set, delete, list, and clear operations
- **MCP protocol compliance**: Uses the standard MCP protocol for communication
- **Easy integration**: Can be used with any MCP-compatible client

## Available Tools

The server provides the following tools that can be called by MCP clients:

### `get_value`
Retrieve a value from the store by key.
- **Parameters**: `key` (string) - The key to look up
- **Returns**: The value associated with the key, or an error message if not found

### `set_value`
Store a key-value pair in the store.
- **Parameters**: 
  - `key` (string) - The key to store
  - `value` (string) - The value to store (automatically parsed as JSON if valid)
- **Returns**: Confirmation message

### `delete_value`
Remove a key-value pair from the store.
- **Parameters**: `key` (string) - The key to delete
- **Returns**: Confirmation message

### `list_keys`
List all keys currently in the store.
- **Parameters**: None
- **Returns**: A formatted list of all keys

### `clear_values`
Clear all key-value pairs from the store.
- **Parameters**: None
- **Returns**: Confirmation message

### `get_store_info`
Get information about the current state of the store.
- **Parameters**: None
- **Returns**: Store statistics and sample keys

## Installation

1. Clone this repository:
```bash
git clone https://github.com/jmgress/simple-mcp.git
cd simple-mcp
```

2. Install dependencies:
```bash
pip install -e .
```

## Usage

### Running the Server

Start the MCP server using stdio transport:

```bash
simple-mcp-server
```

Or run directly with Python:

```bash
python -m simple_mcp.server
```

### Testing the Server

You can test the server functionality using the included test script:

```bash
python test_server.py
```

This will demonstrate all available operations and show you how the server responds.

### Using with MCP Clients

The server can be used with any MCP-compatible client. Configure your client to connect to this server using stdio transport.

Example client configuration (varies by client):
```json
{
  "servers": {
    "simple-mcp": {
      "command": "simple-mcp-server",
      "transport": "stdio"
    }
  }
}
```

## Example Operations

Here are some example operations you can perform:

```python
# Store a simple string value
set_value(key="greeting", value="Hello, World!")

# Store JSON data
set_value(key="user", value='{"name": "Alice", "age": 30}')

# Retrieve values
get_value(key="greeting")  # Returns: "Hello, World!"
get_value(key="user")      # Returns formatted JSON

# List all keys
list_keys()  # Returns: "Keys in store (2 total): greeting, user"

# Get store information
get_store_info()  # Returns current store statistics

# Clean up
delete_value(key="greeting")
clear_values()  # Removes all data
```

## Architecture

The server is built using:
- **FastMCP**: A high-level MCP server framework
- **JSON-RPC 2.0**: For client-server communication
- **Pydantic**: For data validation and serialization
- **asyncio**: For asynchronous operation

The value store is currently in-memory only, meaning data is lost when the server restarts. This makes it suitable for temporary storage and demonstration purposes.

## Development

To set up for development:

```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
python test_server.py

# Format code
black src/

# Lint code
ruff check src/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
