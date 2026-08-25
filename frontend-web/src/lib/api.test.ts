import { describe, expect, it } from "vitest";

import { formatBytes } from "./api";
import { BACKEND_REQUEST_TIMEOUT_MS, isSecureRequest } from "./backend";

describe("formatBytes", () => {
  it("formata bytes, kilobytes e megabytes", () => {
    expect(formatBytes(900)).toBe("900 B");
    expect(formatBytes(2048)).toBe("2.0 KB");
    expect(formatBytes(2 * 1024 * 1024)).toBe("2.0 MB");
  });
});

describe("isSecureRequest", () => {
  it("mantém cookies locais compatíveis com HTTP", () => {
    expect(isSecureRequest(new Request("http://localhost:3000/api/auth/login"))).toBe(false);
  });

  it("protege cookies em HTTPS direto ou encaminhado pelo proxy", () => {
    expect(isSecureRequest(new Request("https://app.example.com/api/auth/login"))).toBe(true);
    expect(
      isSecureRequest(
        new Request("http://frontend:3000/api/auth/login", { headers: { "x-forwarded-proto": "https" } }),
      ),
    ).toBe(true);
  });
});

describe("BACKEND_REQUEST_TIMEOUT_MS", () => {
  it("tolera a inicialização a frio do Render Free", () => {
    expect(BACKEND_REQUEST_TIMEOUT_MS).toBeGreaterThanOrEqual(60_000);
  });
});
