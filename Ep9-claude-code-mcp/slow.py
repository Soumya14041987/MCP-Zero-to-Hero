import time
time.sleep(5)  # slow start, like a server that loads a big model
from mcp.server.mcpserver import MCPServer
MCPServer("slow").run()
