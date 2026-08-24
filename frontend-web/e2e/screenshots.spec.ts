import { test } from "@playwright/test";

const EMAIL = process.env.E2E_EMAIL ?? "admin@demo.com";
const SENHA = process.env.E2E_SENHA ?? "DemoSenha@123";

test.describe("Screenshots", () => {
  test("captura landing page", async ({ page }) => {
    await page.goto("/");
    await page.waitForTimeout(1500);
    await page.screenshot({ path: "test-results/screenshots/landing.png", fullPage: true });
  });

  test("captura dashboard overview", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel("E-mail profissional").fill(EMAIL);
    await page.getByLabel("Senha").fill(SENHA);
    await page.getByRole("button", { name: /Entrar na plataforma/ }).click();
    await page.waitForURL(/\/dashboard/, { timeout: 15_000 });
    await page.waitForTimeout(3000);
    await page.screenshot({ path: "test-results/screenshots/dashboard.png", fullPage: true });
  });

  test("captura assistente e documentos", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel("E-mail profissional").fill(EMAIL);
    await page.getByLabel("Senha").fill(SENHA);
    await page.getByRole("button", { name: /Entrar na plataforma/ }).click();
    await page.waitForURL(/\/dashboard/, { timeout: 15_000 });
    await page.getByRole("button", { name: "Assistente" }).click();
    await page.waitForTimeout(1000);
    await page.screenshot({ path: "test-results/screenshots/assistant.png", fullPage: true });
    await page.getByRole("button", { name: "Documentos" }).click();
    await page.waitForTimeout(1000);
    await page.screenshot({ path: "test-results/screenshots/documents.png", fullPage: true });
  });
});
