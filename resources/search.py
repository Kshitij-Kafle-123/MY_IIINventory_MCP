from storage.db import get_connection

def register(mcp):
    @mcp.resource("inventory://search/{query}")
    def search_items(query: str):
        """
        Search items by name, category, or location.
        Read-only resource.
        """
        q = f"%{query.lower()}%"

        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT name, category, location, container, container_number
                FROM items
                WHERE LOWER(name) LIKE ?
                   OR LOWER(category) LIKE ?
                   OR LOWER(location) LIKE ?
                """,
                (q, q, q),
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
