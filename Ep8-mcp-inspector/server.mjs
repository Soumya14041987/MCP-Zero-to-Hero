import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "weather", version: "1.0.0" });
const DATA = { Kolkata: 31, Pune: 27 };

server.registerTool(
  "get_forecast",
  { description: "Today's temperature for a city", inputSchema: { city: z.string() } },
  async ({ city }) => {
    if (!(city in DATA)) {
      return { isError: true, content: [{ type: "text", text: `Unknown city: ${city}` }] };
    }
    return { content: [{ type: "text", text: `${city}: ${DATA[city]}°C` }] };
  }
);

await server.connect(new StdioServerTransport());
