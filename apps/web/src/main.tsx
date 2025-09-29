import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./state/queryClient";
import RootLayout from "./app/layout/RootLayout";

import DashboardPage from "./app/routes/dashboard";
import BookPage from "./app/routes/book";
import RacksPage from "./app/routes/racks";
import KioskPage from "./app/routes/kiosk";
import AdminPage from "./app/routes/admin";
import ReportsPage from "./app/routes/reports";
import SettingsPage from "./app/routes/settings";

import "./index.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: "dashboard", element: <DashboardPage /> },
      { path: "book", element: <BookPage /> },
      { path: "racks", element: <RacksPage /> },
      { path: "kiosk", element: <KioskPage /> },
      { path: "admin", element: <AdminPage /> },
      { path: "reports", element: <ReportsPage /> },
      { path: "settings", element: <SettingsPage /> },
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