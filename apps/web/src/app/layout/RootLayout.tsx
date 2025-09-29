import { Outlet, NavLink } from "react-router-dom";
import { Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Toaster } from "@/components/ui/sonner";
import Nav from "@/components/Nav";
import Sidebar from "@/components/Sidebar";

export default function RootLayout() {
  return (
    <div className="min-h-screen grid grid-cols-[240px_1fr]">
      <aside className="border-r bg-card">
        <Sidebar />
      </aside>

      <main className="min-h-screen">
        <header className="sticky top-0 z-10 border-b bg-card">
          <div className="flex items-center gap-2 px-4 h-14">
            <Button variant="ghost" size="icon" aria-label="Menu">
              <Menu className="h-5 w-5" />
            </Button>

            <Nav />

            <nav className="ml-auto flex items-center gap-3">
              <NavLink
                className="text-sm text-muted-foreground hover:text-fg"
                to="/settings"
              >
                Settings
              </NavLink>
            </nav>
          </div>
        </header>

        <div className="p-6">
          <Outlet />
        </div>

        {/* Global toast portal for shadcn/sonner */}
        <Toaster richColors />
      </main>
    </div>
  );
}