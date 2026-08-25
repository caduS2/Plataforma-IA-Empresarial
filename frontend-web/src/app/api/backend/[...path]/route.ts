import { cookies } from "next/headers";
import { NextRequest } from "next/server";

import { BACKEND_REQUEST_TIMEOUT_MS, backendEndpoint, isSecureRequest, SESSION_COOKIE } from "@/lib/backend";

type RouteContext = { params: Promise<{ path: string[] }> };

async function proxy(request: NextRequest, context: RouteContext) {
  const { path } = await context.params;
  if (!path.length || path.some((part) => part === ".." || part.includes("/"))) {
    return Response.json({ detail: "Caminho de API inválido." }, { status: 400 });
  }
  const token = (await cookies()).get(SESSION_COOKIE)?.value;
  const incomingUrl = new URL(request.url);
  const headers = new Headers({ Accept: request.headers.get("accept") ?? "application/json" });
  const contentType = request.headers.get("content-type");
  if (contentType) headers.set("Content-Type", contentType);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const init: RequestInit = {
    method: request.method,
    headers,
    cache: "no-store",
    signal: AbortSignal.timeout(BACKEND_REQUEST_TIMEOUT_MS),
  };
  if (!["GET", "HEAD"].includes(request.method)) init.body = await request.arrayBuffer();
  try {
    const backendResponse = await fetch(backendEndpoint(`/${path.join("/")}${incomingUrl.search}`), init);
    const response = new Response(await backendResponse.arrayBuffer(), {
      status: backendResponse.status,
      headers: { "Content-Type": backendResponse.headers.get("content-type") ?? "application/json" },
    });
    if (backendResponse.status === 401) {
      const secure = isSecureRequest(request) ? "; Secure" : "";
      response.headers.append("Set-Cookie", `${SESSION_COOKIE}=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0${secure}`);
    }
    return response;
  } catch {
    return Response.json({ detail: "Backend indisponível. Tente novamente em instantes." }, { status: 503 });
  }
}

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const PATCH = proxy;
export const DELETE = proxy;
