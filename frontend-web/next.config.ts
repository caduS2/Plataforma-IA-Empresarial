import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  poweredByHeader: false,
  typedRoutes: true,
  allowedDevOrigins: ["127.0.0.1"],
};

export default nextConfig;
