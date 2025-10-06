import * as React from "react";
import { floorplanStore } from "./store";
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import type { SceneNode } from "./sceneTypes";

export type RackOption = { id: number; name: string };

export default function Inspector({ racks }: { racks: RackOption[] }) {
  const [, setTick] = React.useState(0);
  React.useEffect(() => floorplanStore.subscribe(() => setTick(t => t + 1)), []);

  const id = floorplanStore.selected;
  const node: SceneNode | undefined = id ? floorplanStore.getNode(id) : undefined;
  if (!node) return <div className="text-sm text-muted-foreground p-4">Select a node</div>;

  const selectedRackId = typeof node.rack_id === "number" ? String(node.rack_id) : "";

  return (
    <div className="p-4 space-y-4">
      <div>
        <label className="text-xs">Node ID</label>
        <div className="text-sm text-muted-foreground">{node.id}</div>
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium">Display name</label>
        <Input
          value={node.type === "label" ? (node.text ?? "") : (node.name ?? "")}
          onChange={(e) => {
            const v = e.target.value;
            if (node.type === "label") floorplanStore.updateNode(node.id, { text: v });
            else floorplanStore.updateNode(node.id, { name: v });
          }}
          placeholder={node.type === "label" ? "Label text" : "Rack name"}
        />
      </div>

      {node.type === "rack" && (
        <div className="space-y-2">
          <label className="text-sm font-medium">Bind to Rack</label>
          <Select
            value={selectedRackId}
            onValueChange={(val) => {
              const rid = parseInt(val, 10);
              floorplanStore.updateNode(node.id, { rack_id: rid });
              // optional: if empty name, copy from rack option
              const r = racks.find(r => r.id === rid);
              if (r && !node.name) floorplanStore.updateNode(node.id, { name: r.name });
            }}
          >
            <SelectTrigger><SelectValue placeholder="Choose rack…" /></SelectTrigger>
            <SelectContent>
              {racks.map(r => (
                <SelectItem key={r.id} value={String(r.id)}>{r.name}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          <p className="text-xs text-muted-foreground">
            Links this node to a real rack so kiosk status can be shown.
          </p>
        </div>
      )}
    </div>
  );
}