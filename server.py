from mcp.server.fastmcp import FastMCP
from storage.db import init_db

# Create MCP instance
mcp = FastMCP("My Inventory <MY_IIINVENTORY_MCP> MCP with SQLite")

# Initialize DB
init_db()

# Import tools and resources
import tools.add_item
import tools.move_item
import tools.remove_item

import resources.items
import resources.locations
import resources.search

# Register tools
tools.add_item.register(mcp)
tools.move_item.register(mcp)
tools.remove_item.register(mcp)

# Register resources
resources.items.register(mcp)
resources.locations.register(mcp)
resources.search.register(mcp)

if __name__ == "__main__":
    mcp.run()
