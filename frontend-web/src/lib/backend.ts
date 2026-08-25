const rawBackendUrl = process.env.BACKEND_URL ?? "http://127.0.0.1:8000";

export const BACKEND_URL = rawBackendUrl.replace(/\/$/, "");
export const SESSION_COOKIE = "nucleo_access_token";
// Render Free can take 50 seconds or more to wake an inactive service.
export const BACKEND_REQUEST_TIMEOUT_MS = 75_000;

export function backendEndpoint(path: string): string {
  if (!path.startsWith("/") || path.includes("..")) throw new Error("Caminho de API inválido.");
  return `${BACKEND_URL}${path}`;
}

export function isSecureRequest(request: Request): boolean {
  const forwardedProtocol = request.headers.get("x-forwarded-proto")?.split(",")[0]?.trim().toLowerCase();
  if (forwardedProtocol) return forwardedProtocol === "https";
  return new URL(request.url).protocol === "https:";
}
