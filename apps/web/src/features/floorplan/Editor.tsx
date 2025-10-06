import React, { useEffect, useRef, useState } from "react";
import { floorplanStore } from "./store";
import { emptyScene } from "./sceneTypes";
import Canvas from "./components/Canvas";
import EditorToolbar from "./components/EditorToolbar";
import RenameDialog from "./components/RenameDialog";
import Inspector, { type RackOption } from "./Inspector";
import { api } from "@/lib/api"; // ← use centralized API helper

const facilityId = 1;

export default function Editor() {
  const [, setTick] = useState(0);
  const selected = () => floorplanStore.selected;
  const scene = () => floorplanStore.scene;
  const draftId = useRef<number | null>(null);

  const [renameOpen, setRenameOpen] = useState(false);
  const [renameValue, setRenameValue] = useState("");
  const [racks, setRacks] = useState<RackOption[]>([]);
  const [creatingDraft, setCreatingDraft] = useState(false); // ← guard

  useEffect(() => floorplanStore.subscribe(() => setTick((t) => t + 1)), []);

  const loadRacks = async () => {
    try {
      const rows = await api<{ id: number; name: string }[]>(`/racks?facility_id=${facilityId}`);
      setRacks((rows ?? []).map((r: { id: number; name: string }) => ({ id: r.id, name: r.name })));
    } catch {
      setRacks([]);
    }
  };

  const newDraft = async () => {
    if (creatingDraft) return;     // ← ignore if already in-flight
    setCreatingDraft(true);
    try {
      const fp = await api<{ id: number }>(
        `/floorplans/draft?facility_id=${facilityId}`,
        { method: "POST" }
      );
      draftId.current = fp.id;
      floorplanStore.load(emptyScene);
      await loadRacks();
    } finally {
      setCreatingDraft(false);     // ← re-enable button
    }
  };

  const saveScene = async () => {
    if (!draftId.current) return;
    await api(`/floorplans/${draftId.current}/scene`, {
      method: "PATCH",
      body: JSON.stringify(scene()),
    });
  };

  const publish = async () => {
    if (!draftId.current) return;
    await api(`/floorplans/${draftId.current}/publish`, { method: "POST" });
  };

  const addRack = () =>
    floorplanStore.add({ type: "rack", x: 100, y: 100, w: 60, h: 40 });

  const openRename = () => {
    const id = floorplanStore.selected;
    if (!id) return;
    const n = floorplanStore.getNode(id);
    if (!n) return;
    setRenameValue(n.type === "rack" ? n.name ?? "" : n.text ?? "");
    setRenameOpen(true);
  };

  const confirmRename = () => {
    const id = floorplanStore.selected;
    if (!id) return;
    const n = floorplanStore.getNode(id);
    if (!n) return;
    const value = renameValue.trim();
    if (n.type === "rack") floorplanStore.setName(id, value);
    else if (n.type === "label") floorplanStore.updateNode(id, { text: value });
    setRenameOpen(false);
  };

  return (
    <div className="space-y-4">
      <EditorToolbar
        onNewDraft={newDraft}
        onAddRack={addRack}
        onSave={saveScene}
        onPublish={publish}
        onRename={openRename}
        disabled={!draftId.current}      // buttons that need a draft
        newDraftDisabled={creatingDraft} // only New Draft disabled while posting
      />

      <div className="grid grid-cols-[1fr_280px] gap-4">
        <Canvas scene={scene()} selectedId={selected() ?? null} />
        <aside className="border rounded-md bg-card">
          <Inspector racks={racks} />
        </aside>
      </div>

      <RenameDialog
        open={renameOpen}
        title={`Rename ${
          selected()
            ? floorplanStore.getNode(selected()!)?.type ?? "node"
            : "node"
        }`}
        value={renameValue}
        onChange={setRenameValue}
        onCancel={() => setRenameOpen(false)}
        onConfirm={confirmRename}
      />
    </div>
  );
}