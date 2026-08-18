import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import { SESSION_COOKIE } from "@/lib/backend";

export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  if (!(await cookies()).has(SESSION_COOKIE)) redirect("/login");
  return children;
}
