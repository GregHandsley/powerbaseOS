import * as React from "react";
import Renderer from "../Renderer";
import { useCanvasDrag } from "../hooks/useCanvasDrag";
import { floorplanStore } from "../store";
import type { Scene } from "../sceneTypes";

export default function Canvas({
  scene,
  selectedId,
}: {
  scene: Scene;
  selectedId: string | null;
}) {
  const { onPointerDown, onPointerMove, onPointerUp } = useCanvasDrag();

  return (
    <div
      className="relative border rounded-md"
      onMouseDown={onPointerDown}
      onMouseMove={onPointerMove}
      onMouseUp={onPointerUp}
      onMouseLeave={onPointerUp}
      onDragStart={(e) => e.preventDefault()}
    >
      <Renderer
        scene={scene}
        selectedId={selectedId ?? undefined}
        onSelect={(id) => floorplanStore.select(id)}
      />
    </div>
  );
}