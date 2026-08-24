import { NextResponse } from "next/server";

import { backendEndpoint, isSecureRequest, SESSION_COOKIE } from "@/lib/backend";

export async function POST(request: Request) {
  try {
    const backendResponse = await fetch(backendEndpoint("/auth/demo"), {
      method: "POST",
      headers: { Accept: "application/json" },
      cache: "no-store",
      signal: AbortSignal.timeout(10_000),
    });
    const data = await backendResponse.json().catch(() => ({ detail: "O servidor devolveu uma resposta inválida." }));
    if (!backendResponse.ok) return NextResponse.json(data, { status: backendResponse.status });
    const response = NextResponse.json({ success: true });
    response.cookies.set(SESSION_COOKIE, data.access_token, {
      httpOnly: true,
      secure: isSecureRequest(request),
      sameSite: "lax",
      maxAge: 60 * 60,
      path: "/",
    });
    return response;
  } catch {
    return NextResponse.json({ detail: "Backend indisponível. Tente novamente em instantes." }, { status: 503 });
  }
}
