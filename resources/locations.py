from storage.db import get_connection

def register(mcp):
    @mcp.resource("inventory://location/{location}")
    def items_by_location(location: str):
        """
        List items in a specific location.
        """
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT name, category, container, container_number FROM items WHERE location=?",
                (location,),
            ).fetchall()

        return [
            {
                "name": r[0],
                "category": r[1],
                "container": r[2],
                "container_number": r[3],
            }
            for r in rows
        ]
