import { defineConfig, type Plugin } from "vite";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";
import tailwindcss from "@tailwindcss/vite";
import path from "path";
import { pathToFileURL } from "node:url";
import type { IncomingMessage, ServerResponse } from "node:http";

const serverModuleUrl = "/src/server.ts";
const managedGameRoutes = new Set([
  "/game/start",
  "/game/state",
  "/game/add-card",
  "/game/bingo",
  "/game/leave",
  "/game/config",
]);

function isServerManagedPath(pathname: string) {
  if (pathname.startsWith("/api/") || pathname.startsWith("/bot/")) return true;
  if (!pathname.startsWith("/game/")) return false;
  return managedGameRoutes.has(pathname.replace(/\/+$/, ""));
}

function readRequestBody(req: IncomingMessage): Promise<Buffer> {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    req.on("data", (chunk: Buffer) => chunks.push(chunk));
    req.on("end", () => resolve(Buffer.concat(chunks)));
    req.on("error", reject);
  });
}

function apiMiddlewarePlugin(): Plugin {
  return {
    name: "boombingoo-api",
    apply: "serve",
    configureServer(server) {
      server.middlewares.use(async (req, res, next) => {
        const pathname = req.url?.split("?")[0] ?? "";
        if (!isServerManagedPath(pathname)) {
          return next();
        }

        try {
          const serverModule = await server.ssrLoadModule(serverModuleUrl);
          const serverHandler = serverModule?.default ?? serverModule;
          const host = req.headers.host ?? "localhost:8083";
          const fullUrl = `http://${host}${req.url}`;

          const headers = new Headers();
          for (const [key, value] of Object.entries(req.headers)) {
            if (value == null) continue;
            if (Array.isArray(value)) {
              value.forEach((entry) => headers.append(key, entry));
            } else {
              headers.set(key, value);
            }
          }

          let bodyText: string | undefined;
          if (req.method && !["GET", "HEAD"].includes(req.method)) {
            const body = await readRequestBody(req);
            bodyText = body.length > 0 ? body.toString("utf8") : undefined;
          }
          console.log("FORWARDED BODY", bodyText);

          const request = new Request(fullUrl, {
            method: req.method,
            headers,
            body: bodyText,
            duplex: "half",
          } as RequestInit & { duplex?: "half" });

          const response = await serverHandler.fetch(request, {}, {});
          await pipeWebResponse(response, res);
        } catch (error) {
          console.error("API middleware error:", error);
          next(error);
        }
      });
    },
  };
}

async function pipeWebResponse(response: Response, res: ServerResponse) {
  res.statusCode = response.status;
  response.headers.forEach((value, key) => {
    if (key.toLowerCase() === "transfer-encoding") return;
    res.setHeader(key, value);
  });
  const buffer = Buffer.from(await response.arrayBuffer());
  res.end(buffer);
}

export default defineConfig({
  plugins: [react(), tsconfigPaths(), tailwindcss(), apiMiddlewarePlugin()],
  server: {
    host: "::",
    allowedHosts: true,
    port: 8083,
    hmr: false,
    preTransformRequests: true,
  },
  build: {
    outDir: "dist",
    sourcemap: true,
  },
  resolve: {
    alias: {
      "node:async_hooks": path.resolve(__dirname, "src/lib/async-local-storage-stub.ts"),
    },
  },
  define: {
    global: "globalThis",
  },
});
