import React from "react";
import type { Scene, SceneNode } from "./sceneTypes";
import { Badge } from "@/components/ui/badge";
import {
  HoverCard,
  HoverCardTrigger,
  HoverCardContent,
} from "@/components/ui/hover-card";

type Availability = {
  status: "available" | "held" | "reserved" | "in_use";
  by?: string;
  until?: string; // ISO
};

type Props = {
  scene: Scene;
  selectedId?: string | null;
  onSelect?: (id: string) => void;
  availabilityByRack?: Record<number, Availability>; // rack_id -> availability
  kioskMode?: boolean;
};

// Small, neutral chip with optional hover details
function StatusChip({ a }: { a: Availability }) {
  const label =
    a.status === "in_use"
      ? "In use"
      : a.status === "reserved"
      ? "Reserved"
      : a.status === "held"
      ? "Held"
      : "Available";

  const cls =
    a.status === "available"
      ? "bg-muted text-muted-foreground"
      : a.status === "held"
      ? "bg-yellow-500/15 text-yellow-600 border-yellow-600/30"
      : a.status === "reserved"
      ? "bg-[rgb(var(--primary))]/15 text-[rgb(var(--primary))] border-[rgb(var(--primary))]/30"
      : "bg-destructive/15 text-destructive border-destructive/30";

  const chip = <Badge className={`border ${cls}`}>{label}</Badge>;

  if (!a.by && !a.until) return chip;

  return (
    <HoverCard>
      <HoverCardTrigger asChild>{chip}</HoverCardTrigger>
      <HoverCardContent className="text-xs space-y-1">
        {a.by && (
          <div>
            <span className="text-muted-foreground">By:</span> {a.by}
          </div>
        )}
        {a.until && (
          <div>
            <span className="text-muted-foreground">Until:</span>{" "}
            {new Date(a.until).toLocaleTimeString()}
          </div>
        )}
      </HoverCardContent>
    </HoverCard>
  );
}

const NodeView: React.FC<{
  n: SceneNode;
  selected?: boolean;
  onClick?: () => void;
  kioskMode?: boolean;
  availabilityByRack?: Record<number, Availability>;
}> = ({ n, selected, onClick, kioskMode, availabilityByRack }) => {
  const style: React.CSSProperties = {
    position: "absolute",
    left: n.x,
    top: n.y,
    width: n.w ?? 60,
    height: n.h ?? 40,
    transform: `rotate(${n.rot ?? 0}deg)`,
    border: selected
      ? "2px solid rgb(var(--ring))"
      : "1px solid rgb(var(--border))",
    background: "rgb(var(--card))",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    WebkitUserSelect: "none",
    userSelect: "none",
    cursor: "grab",
  };

  const rackAvail =
  kioskMode && typeof n.rack_id === "number"
    ? availabilityByRack?.[n.rack_id]
    : undefined;

  return (
    <div
      style={style}
      onClick={onClick}
      onMouseDown={(e) => {
        // prevent text selection while dragging
        e.preventDefault();
      }}
      draggable={false}
      data-node-id={n.id}
      aria-label={`node-${n.id}`}
    >
      {/* Status chip (kiosk mode only) */}
      {rackAvail && (
        <div className="absolute left-1 top-1">
          <StatusChip a={rackAvail} />
        </div>
      )}

      {/* Center label */}
      {n.type === "rack"
        ? n.name ?? "Rack"
        : n.type === "label"
        ? n.text ?? "Label"
        : "Zone"}

      {/* Resize handles (only when selected). NOTE: no stopPropagation so the editor sees the event on the canvas */}
      {selected && (
        <>
          <div
            data-resize="nw"
            style={{
              position: "absolute",
              left: -6,
              top: -6,
              width: 12,
              height: 12,
              borderRadius: 2,
              background: "rgb(var(--primary))",
              cursor: "nwse-resize",
            }}
            draggable={false}
          />
          <div
            data-resize="ne"
            style={{
              position: "absolute",
              right: -6,
              top: -6,
              width: 12,
              height: 12,
              borderRadius: 2,
              background: "rgb(var(--primary))",
              cursor: "nesw-resize",
            }}
            draggable={false}
          />
          <div
            data-resize="sw"
            style={{
              position: "absolute",
              left: -6,
              bottom: -6,
              width: 12,
              height: 12,
              borderRadius: 2,
              background: "rgb(var(--primary))",
              cursor: "nesw-resize",
            }}
            draggable={false}
          />
          <div
            data-resize="se"
            style={{
              position: "absolute",
              right: -6,
              bottom: -6,
              width: 12,
              height: 12,
              borderRadius: 2,
              background: "rgb(var(--primary))",
              cursor: "nwse-resize",
            }}
            draggable={false}
          />
        </>
      )}
    </div>
  );
};

export const Renderer: React.FC<Props> = ({
  scene,
  onSelect,
  selectedId,
  kioskMode,
  availabilityByRack,
}) => {
  return (
    <div className="relative w-full h-[600px] bg-[rgb(var(--muted))]">
      {/* grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(0,0,0,0.05)_1px,transparent_1px),linear-gradient(to_bottom,rgba(0,0,0,0.05)_1px,transparent_1px)] bg-[size:10px_10px]" />
      {scene.nodes.map((n) => (
        <NodeView
          key={n.id}
          n={n}
          selected={n.id === selectedId}
          onClick={() => onSelect?.(n.id)}
          kioskMode={kioskMode}
          availabilityByRack={availabilityByRack}
        />
      ))}
    </div>
  );
};

export default Renderer;