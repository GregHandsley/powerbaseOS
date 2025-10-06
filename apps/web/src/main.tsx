// apps/web/src/main.tsx
import React from "react";
import "./index.css";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./state/queryClient";
import RootLayout from "./app/layout/RootLayout";

// PAGES
import Dashboard from "./app/routes/dashboard";
import Book from "./app/routes/book";
import Racks from "./app/routes/racks";
import Kiosk from "./app/routes/kiosk";
import Admin from "./app/routes/admin";
import Reports from "./app/routes/reports";
import Settings from "./app/routes/settings";

// FLOORPLAN EDITOR (new)
import FloorplanEditor from "./features/floorplan/Editor";

// (optional) a simple error boundary element
export function RouteError() {
  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold mb-2">Something went wrong</h1>
      <p className="text-sm text-muted-foreground">
        This page could not be loaded. Use the sidebar to navigate elsewhere.
      </p>
    </div>
  );
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    errorElement: <RouteError />, // optional, nicer UX than the default 💿 screen
    children: [
      { index: true, element: <Dashboard /> },
      { path: "dashboard", element: <Dashboard /> },
      { path: "book", element: <Book /> },
      { path: "racks", element: <Racks /> },
      { path: "kiosk", element: <Kiosk /> },
      { path: "admin", element: <Admin /> },
      { path: "admin/floorplan", element: <FloorplanEditor /> }, // ← ADD THIS
      { path: "reports", element: <Reports /> },
      { path: "settings", element: <Settings /> },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>
);