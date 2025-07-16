import { NextRequest, NextResponse } from "next/server";
import { generateLevels } from "@/mcp/generateLevelsTool";

// Handle both GET (SSE) and POST (JSON-RPC) requests
export async function GET(req: NextRequest) {
  // Handle SSE connection for MCP Inspector
  const response = new NextResponse(
    new ReadableStream({
      start(controller) {
        // Send SSE headers
        controller.enqueue(
          new TextEncoder().encode(
            "data: " + JSON.stringify({ event: "connected" }) + "\n\n"
          )
        );

        // Keep connection alive
        const interval = setInterval(() => {
          controller.enqueue(
            new TextEncoder().encode(": keepalive\n\n")
          );
        }, 30000);

        // Clean up on close
        req.signal.addEventListener("abort", () => {
          clearInterval(interval);
          controller.close();
        });
      },
    }),
    {
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Cache-Control",
      },
    }
  );

  return response;
}

export async function POST(req: NextRequest) {
  let id: any = null;
  let body: any = null;

  // Log all request details for debugging
  console.log(
    "[MCP] Request headers:",
    Object.fromEntries(req.headers.entries())
  );
  console.log("[MCP] Request method:", req.method);
  console.log("[MCP] Request URL:", req.url);

  try {
    body = await req.json();
    console.log("[MCP] Raw request body:", JSON.stringify(body, null, 2));
    const { jsonrpc, method, id: reqId, params } = body;
    id = typeof reqId !== "undefined" ? reqId : null;

    // Validate JSON-RPC 2.0
    if (
      jsonrpc !== "2.0" ||
      typeof method !== "string" ||
      typeof id === "undefined"
    ) {
      const response = {
        jsonrpc: "2.0",
        id,
        error: {
          code: -32600,
          message: "Invalid Request",
        },
      };
      console.log(
        "[MCP] Outgoing invalid request response:",
        JSON.stringify(response, null, 2)
      );
      return NextResponse.json(response, { status: 200 });
    }

    // Support the "initialize" method for MCP handshake
    if (method === "initialize") {
      const response = {
        jsonrpc: "2.0",
        id,
        result: {
          protocolVersion: "2025-03-26",
          capabilities: { 
            tools: { listChanged: true },
            resources: { listChanged: true },
            prompts: { listChanged: true }
          },
          serverInfo: { name: "Realentless MCP", version: "0.0.1" },
        },
      };
      console.log(
        "[MCP] Outgoing initialize response:",
        JSON.stringify(response, null, 2)
      );
      return NextResponse.json(response, { status: 200 });
    }

    if (method === "tools/list") {
      const response = {
        jsonrpc: "2.0",
        id,
        result: {
          tools: [
            {
              name: "generateLevels",
              description:
                "Generate personalized levels and exercises for a user. Use only the available exercises provided in the context.",
              parameters: {
                type: "object",
                properties: {
                  userId: {
                    type: "string",
                    description: "The user's unique ID",
                  },
                  levels: {
                    type: "array",
                    items: {
                      type: "object",
                      properties: {
                        id: { type: "string" },
                        title: {
                          type: "object",
                          properties: {
                            en: { type: "string" },
                            fr: { type: "string" },
                          },
                        },
                        subtitle: {
                          type: "object",
                          properties: {
                            en: { type: "string" },
                            fr: { type: "string" },
                          },
                        },
                        message: {
                          type: "object",
                          properties: {
                            en: { type: "string" },
                            fr: { type: "string" },
                          },
                        },
                        position: { type: "number" },
                        availableAt: { type: "string" },
                        userId: { type: "string" },
                        bodyExercisesPerRound: { type: "number" },
                        bodyIntensity: { type: "number" },
                        bodyMessage: {
                          type: "object",
                          properties: {
                            en: { type: "string" },
                            fr: { type: "string" },
                          },
                        },
                        bodyRounds: { type: "number" },
                        mindIntensity: { type: "number" },
                        mindMessage: {
                          type: "object",
                          properties: {
                            en: { type: "string" },
                            fr: { type: "string" },
                          },
                        },
                        mindRounds: { type: "number" },
                      },
                    },
                    description:
                      "Array of level objects with multilingual titles, messages, and workout configuration",
                  },
                  exercises: {
                    type: "array",
                    items: {
                      type: "object",
                      properties: {
                        id: { type: "string" },
                        exerciseId: {
                          type: "string",
                          description:
                            "Must be a valid exercise ID from the available exercises in the context",
                        },
                        repetitions: { type: "number", nullable: true },
                        duration: { type: "number", nullable: true },
                        type: {
                          type: "string",
                          enum: ["BODY", "MIND"],
                        },
                        userLevelId: { type: "string" },
                      },
                    },
                    description:
                      "Array of exercise objects. The exerciseId must reference a valid exercise from the available exercises provided in the context.",
                  },
                },
                required: ["userId", "levels", "exercises"],
              },
            },
          ],
        },
      };
      console.log(
        "[MCP] Outgoing tools/list response:",
        JSON.stringify(response, null, 2)
      );
      return NextResponse.json(response, { status: 200 });
    }

    if (method === "notifications/initialized") {
      const response = {
        jsonrpc: "2.0",
        id,
        result: {},
      };
      console.log(
        "[MCP] Outgoing notifications/initialized response:",
        JSON.stringify(response, null, 2)
      );
      return NextResponse.json(response, { status: 200 });
    }

    if (method === "tools/call") {
      // Handle tool calls from MCP Inspector
      const { name, arguments: args } = params;
      
      if (name === "generateLevels") {
        console.log(
          "[MCP] Calling generateLevels with params:",
          JSON.stringify(args, null, 2)
        );
        const result = await generateLevels(args);
        const response = {
          jsonrpc: "2.0",
          id,
          result: {
            content: [
              {
                type: "text",
                text: JSON.stringify(result, null, 2)
              }
            ]
          },
        };
        console.log("[MCP] Outgoing response:", JSON.stringify(response, null, 2));
        return NextResponse.json(response, { status: 200 });
      }
    }

    if (
      method !== "generateLevels" &&
      method !== "initialize" &&
      method !== "tools/list" &&
      method !== "tools/call" &&
      method !== "notifications/initialized"
    ) {
      const response = {
        jsonrpc: "2.0",
        id,
        error: {
          code: -32601,
          message: "Method not found",
        },
      };
      console.log(
        "[MCP] Outgoing method not found response:",
        JSON.stringify(response, null, 2)
      );
      return NextResponse.json(response, { status: 200 });
    }

    // Legacy support for direct generateLevels method
    if (method === "generateLevels") {
      console.log(
        "[MCP] Calling generateLevels with params:",
        JSON.stringify(params, null, 2)
      );
      const result = await generateLevels(params);
      const response = {
        jsonrpc: "2.0",
        id,
        result,
      };
      console.log("[MCP] Outgoing response:", JSON.stringify(response, null, 2));
      return NextResponse.json(response, { status: 200 });
    }
  } catch (error: any) {
    console.error("[MCP] Error:", error);
    console.error("[MCP] Error stack:", error?.stack);
    const response = {
      jsonrpc: "2.0",
      id,
      error: {
        code: -32603,
        message: "Internal error",
        data: error?.message || "Unknown error",
      },
    };
    console.log(
      "[MCP] Outgoing error response:",
      JSON.stringify(response, null, 2)
    );
    return NextResponse.json(response, { status: 200 });
  }
} 