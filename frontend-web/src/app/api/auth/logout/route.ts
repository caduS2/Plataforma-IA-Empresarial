import { NextResponse } from "next/server";

import { isSecureRequest, SESSION_COOKIE } from "@/lib/backend";

export async function POST(request: Request) {
  const response = NextResponse.json({ success: true });
  response.cookies.set(SESSION_COOKIE, "", {
    httpOnly: true,
    secure: isSecureRequest(request),
    expires: new Date(0),
    sameSite: "lax",
    path: "/",
  });
  return response;
}
