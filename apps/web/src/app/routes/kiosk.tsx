import React, { useEffect, useState } from "react";
import Renderer from "@/features/floorplan/Renderer";
import type { Scene } from "@/features/floorplan/sceneTypes";

type Availability = {
  status: "available" | "held" | "reserved" | "in_use";
  by?: string;
  until?: string;
};

function isScene(x: unknown): x is Scene {
  return typeof x === "object" && x !== null && "nodes" in (x as Record<string, unknown>);
}

export default function Kiosk() {
  const [scene, setScene] = useState<Scene>({ nodes: [] });
  const [avail, setAvail] = useState<Record<number, Availability>>({});

  useEffect(() => {
    (async () => {
      const fp = await fetch("/floorplans/kiosk/latest?facility_id=1").then(r => r.json());
      setScene(isScene(fp.scene_json) ? fp.scene_json : { nodes: [] });
      const a = await fetch("/kiosk/availability?facility_id=1").then(r => r.json());
      const map: Record<number, Availability> = {};
      for (const r of a.racks ?? []) map[r.rack_id] = { status: r.status, by: r.by, until: r.until };
      setAvail(map);
    })();
  }, []);

  return (
    <div className="p-4">
      <Renderer scene={scene} kioskMode availabilityByRack={avail} />
      <div className="mt-3 text-xs text-muted-foreground flex gap-3">
        <span className="inline-flex items-center gap-1"><span className="inline-block w-2 h-2 rounded-full bg-muted-foreground/40"></span> Available</span>
        <span className="inline-flex items-center gap-1"><span className="inline-block w-2 h-2 rounded-full bg-yellow-500"></span> Held</span>
        <span className="inline-flex items-center gap-1"><span className="inline-block w-2 h-2 rounded-full bg-[rgb(var(--primary))]"></span> Reserved</span>
        <span className="inline-flex items-center gap-1"><span className="inline-block w-2 h-2 rounded-full bg-destructive"></span> In Use</span>
      </div>
    </div>
  );
}