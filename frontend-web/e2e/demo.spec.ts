import { expect, test } from "@playwright/test";

/**
 * Fluxo E2E do Recruiter Demo Mode.
 *
 * O recrutador abre a landing, clica em "Experimentar demonstração" e cai no
 * workspace de uma empresa demo isolada — sem precisar de credenciais.
 */
test.describe("Demo Mode (P1)", () => {
  test("landing exibe o botão de demonstração", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { name: /Conhecimento empresarial transformado em ação/ })).toBeVisible();
    await expect(page.getByRole("button", { name: /Experimentar demonstração/ })).toBeVisible();
  });

  test("experimentar demonstração leva ao workspace demo", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: /Experimentar demonstração/ }).first().click();
    await page.waitForURL(/\/dashboard/, { timeout: 15_000 });
    await expect(page).toHaveURL(/\/dashboard/);
  });

  test("rota protegida segue bloqueada para quem não entrou", async ({ page }) => {
    await page.goto("/dashboard");
    await expect(page).toHaveURL(/\/login/);
  });
});
