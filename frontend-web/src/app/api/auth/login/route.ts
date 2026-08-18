import { NextResponse } from "next/server";
import { z } from "zod";

import { BACKEND_REQUEST_TIMEOUT_MS, backendEndpoint, isSecureRequest, SESSION_COOKIE } from "@/lib/backend";

const credentialsSchema = z.object({ email: z.email(), senha: z.string().min(8).max(128) });

export async function POST(request: Request) {
  const parsed = credentialsSchema.safeParse(await request.json().catch(() => null));
  if (!parsed.success) {
    return NextResponse.json({ detail: "Informe um e-mail válido e uma senha com pelo menos 8 caracteres." }, { status: 422 });
  }
  try {
    const backendResponse = await fetch(backendEndpoint("/auth/login"), {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(parsed.data),
      cache: "no-store",
      signal: AbortSignal.timeout(BACKEND_REQUEST_TIMEOUT_MS),
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
