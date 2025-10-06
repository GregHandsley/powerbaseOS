import * as React from "react";
import { floorplanStore } from "../store";

type DragMode = "none" | "move" | "resize";
type Handle = "nw" | "ne" | "sw" | "se" | null;

export function useCanvasDrag() {
  const dragMode = React.useRef<DragMode>("none");
  const dragId = React.useRef<string | null>(null);
  const resizeHandle = React.useRef<Handle>(null);
  const startX = React.useRef(0);
  const startY = React.useRef(0);
  const origX = React.useRef(0);
  const origY = React.useRef(0);
  const origW = React.useRef(0);
  const origH = React.useRef(0);

  const onPointerDown = (e: React.MouseEvent) => {
    const el = e.target as HTMLElement;
    const nodeRoot = el.closest("[data-node-id]") as HTMLElement | null;
    const nodeId = nodeRoot?.getAttribute("data-node-id") ?? null;
    const handle = (el.getAttribute("data-resize") as Handle) ?? null;

    window.getSelection()?.removeAllRanges();
    e.preventDefault();

    if (handle && nodeId) {
      dragMode.current = "resize";
      dragId.current = nodeId;
      resizeHandle.current = handle;
      startX.current = e.clientX;
      startY.current = e.clientY;
      const n = floorplanStore.getNode(nodeId)!;
      origX.current = n.x;
      origY.current = n.y;
      origW.current = n.w ?? 60;
      origH.current = n.h ?? 40;
      document.body.style.cursor =
        handle === "se" || handle === "nw" ? "nwse-resize" : "nesw-resize";
      return;
    }

    if (nodeId) {
      dragMode.current = "move";
      dragId.current = nodeId;
      floorplanStore.select(nodeId);
      startX.current = e.clientX;
      startY.current = e.clientY;
      document.body.style.cursor = "grabbing";
      return;
    }

    floorplanStore.select(null);
  };

  const onPointerMove = (e: React.MouseEvent) => {
    if (dragMode.current === "none" || !dragId.current) return;
    const dx = e.clientX - startX.current;
    const dy = e.clientY - startY.current;

    if (dragMode.current === "move") {
      floorplanStore.move(dragId.current, dx, dy, 10);
      startX.current = e.clientX;
      startY.current = e.clientY;
      return;
    }

    // resize
    const id = dragId.current;
    let x = origX.current, y = origY.current, w = origW.current, h = origH.current;
    switch (resizeHandle.current) {
      case "se": w = origW.current + dx; h = origH.current + dy; break;
      case "ne": y = origY.current + dy; h = origH.current - dy; w = origW.current + dx; break;
      case "sw": x = origX.current + dx; w = origW.current - dx; h = origH.current + dy; break;
      case "nw": x = origX.current + dx; y = origY.current + dy; w = origW.current - dx; h = origH.current - dy; break;
    }
    floorplanStore.setRect(id, x, y, w, h, 10);
  };

  const onPointerUp = () => {
    dragMode.current = "none";
    dragId.current = null;
    resizeHandle.current = null;
    document.body.style.cursor = "";
  };

  return { onPointerDown, onPointerMove, onPointerUp };
}