from storage.db import get_connection
from memory.user_memory import set_memory

def register(mcp):
    @mcp.tool()
    def move_item(user_id: str, name: str, new_location: str) -> str:
        """
        Move an existing item to a new location.
        """
        with get_connection() as conn:
            cur = conn.execute(
                "UPDATE items SET location=? WHERE name=?",
                (new_location, name),
            )

            if cur.rowcount == 0:
                return f"Item '{name}' not found"

        # Update user memory
        set_memory(user_id, "last_item", name)
        return f"Moved {name} to {new_location}"
