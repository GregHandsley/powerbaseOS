// apps/web/vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath, URL } from "node:url";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    proxy: {
      // proxy API requests to the FastAPI container (service name "api" in docker-compose)
      "/floorplans": { target: "http://api:8000", changeOrigin: true },
      "/health":     { target: "http://api:8000", changeOrigin: true },
      "/events":     { target: "http://api:8000", changeOrigin: true },
      "/timeslots":  { target: "http://api:8000", changeOrigin: true },
      "/auth":       { target: "http://api:8000", changeOrigin: true },
    },
  },
});