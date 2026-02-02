from storage.db import get_connection

def register(mcp):
    @mcp.resource("inventory://items")
    def list_items():
        """
        List all items.
        """
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
