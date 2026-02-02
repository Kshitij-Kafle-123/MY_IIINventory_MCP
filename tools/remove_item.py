from storage.db import get_connection

def register(mcp):
    @mcp.tool()
    def remove_item(name: str) -> str:
        """
        Remove an item from inventory.
        """
        with get_connection() as conn:
            cur = conn.execute("DELETE FROM items WHERE name=?", (name,))
            if cur.rowcount == 0:
                return f"Item '{name}' not found"

        return f"Removed {name}"
