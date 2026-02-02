# MY_IIINventory_MCP

A **Model Context Protocol (MCP) server** built in Python for managing a personal inventory system with SQLite.  
This project demonstrates the use of **tools**, **resources**, and **memory** in MCP, allowing clients like **Claude Desktop** to interact with your inventory programmatically.

---

## Features

- Add, move, and remove items with MCP tools
- List all items or by location with MCP resources
- Search items by name, category, or location
- Persistent storage using SQLite
- User-specific memory (e.g., last added item, preferred location)
- Fully MCP-compliant for client integration

---

## Project Structure

```
MY_IIINventory_MCP/
├── server.py                # Main MCP server entry point
├── storage/
│   └── db.py                # SQLite initialization and connection
├── memory/
│   └── user_memory.py       # User memory management
├── tools/
│   ├── add_item.py          # Add item tool
│   ├── move_item.py         # Move item tool
│   └── remove_item.py       # Remove item tool
├── resources/
│   ├── items.py             # List all items resource
│   ├── locations.py         # List items by location resource
│   └── search.py            # Search items resource
├── venv/                    # Python virtual environment
└── closet.db                # SQLite database (auto-created)
```

---

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPO_URL>
cd MY_IIINventory_MCP
```

### 2. Create a virtual environment and activate it

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# OR
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install uvicorn mcp-server
```

### 4. Initialize database

SQLite will automatically create `closet.db` the first time you run the server.  
You can initialize it manually using `storage/db.py`.

---

## MCP Server Configuration

`server.py` initializes the MCP server and registers all tools and resources.  
Ensure your MCP client (e.g., Claude Desktop) points to the Python executable in your virtual environment:

```json
{
  "mcpServers": {
    "inventory-mcp": {
      "command": "/.../.../MY_IIINventory_MCP/venv/bin/python",
      "args": [
        "/.../.../MY_IIINventory_MCP/server.py"
      ]
    }
  }
}
```

⚠️ **Make sure the path points to your venv Python and the server.py location.**

---

## Running the MCP Server

### 1. Activate your virtual environment:

```bash
source venv/bin/activate   # macOS/Linux
```

### 2. Run the server via uv with MCP transport:

```bash
uv run --with mcp server.py --transport stdio
```

- `--with mcp` → enables MCP server mode
- `--transport stdio` → standard input/output transport for clients

You should see logs like:

```
Server started and connected successfully
```

---

## Tools

| Tool | Description |
|------|-------------|
| `add_item` | Add a new item to the inventory |
| `move_item` | Move an item to a different location |
| `remove_item` | Delete an item from inventory |

**Note:** Use `@mcp.tool()` (with parentheses) when decorating tools.

### Example Tool: `add_item.py`

```python
from storage.db import get_connection
from memory.user_memory import set_memory
from server import mcp

@mcp.tool()
def add_item(
    user_id: str,
    name: str,
    category: str,
    location: str,
    container: str,
    container_number: int
) -> str:
    """Add an item to inventory."""
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO items (name, category, location, container, container_number) VALUES (?, ?, ?, ?, ?)",
                (name, category, location, container, container_number),
            )

        set_memory(user_id, "last_item", name)
        set_memory(user_id, "preferred_location", location)

        return f"Added {name} to {location}"

    except Exception:
        return f"Item '{name}' already exists"
```

---

## Resources

| Resource URI | Description |
|--------------|-------------|
| `inventory://items` | List all items |
| `inventory://location/{location}` | List items by location |
| `inventory://search/{query}` | Search items by name/category/location |

**Note:** Use `@mcp.resource(...)` (with parentheses) when decorating resources.

### Example Resource: `items.py`

```python
from server import mcp
from storage.db import get_connection

@mcp.resource("inventory://items")
def list_items():
    """List all items."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT name, category, location, container, container_number FROM items"
        ).fetchall()

    return [
        {
            "name": r[0],
            "category": r[1],
            "location": r[2],
            "container": r[3],
            "container_number": r[4],
        }
        for r in rows
    ]
```

---

## Memory Example

User memory is stored in `memory/user_memory.py`

Example functions: `set_memory(user_id, key, value)` and `get_memory(user_id, key)`

---

## Tips & Best Practices

- **Avoid circular imports** — always use the `register(mcp)` pattern in tools/resources.
- SQLite database is thread-safe when used with Python context managers.
- Test your MCP server with a client (e.g., Claude Desktop) to ensure tools/resources are detected correctly.
- Use `@mcp.tool()` and `@mcp.resource(...)` with parentheses — otherwise MCP will throw a `TypeError`.

---

## License

MIT License © 2026

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
