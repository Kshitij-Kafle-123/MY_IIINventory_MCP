from storage.db import get_connection
from memory.user_memory import set_memory

def register(mcp):
    @mcp.tool()
    def add_item(
        user_id: str,
        name: str,
        category: str,
        location: str,
        container: str,
        container_number: int
    ) -> str:
        """
        Add an item to inventory.
        Item names are unique.
        """
        try:
            with get_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO items (name, category, location, container, container_number)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (name, category, location, container, container_number),
                )

            # Save some memory per user
            set_memory(user_id, "last_item", name)
            set_memory(user_id, "preferred_location", location)

            return f"Added {name} to {location}"

        except Exception:
            return f"Item '{name}' already exists"
