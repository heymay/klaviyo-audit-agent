import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // API requests to Python backend are proxied through Next.js API routes
  // so the browser never talks directly to FastAPI
  env: {
    NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL ?? "http://localhost:3000",
  },
};

export default nextConfig;
