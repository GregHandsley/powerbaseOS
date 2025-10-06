import React, { useEffect, useState } from "react";
import Renderer from "./Renderer";
import type { Scene } from "./sceneTypes";

const facilityId = 1;

export default function RendererKiosk() {
  const [scene, setScene] = useState<Scene>({ nodes: [] });

  useEffect(() => {
    (async () => {
      const res = await fetch(`/floorplans/kiosk/latest?facility_id=${facilityId}`);
      if (res.ok) {
        const data = await res.json();
        setScene(data.scene_json ?? { nodes: [] });
      }
    })();
  }, []);

  return <Renderer scene={scene} />;
}