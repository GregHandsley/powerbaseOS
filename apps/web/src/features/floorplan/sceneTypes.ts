export type NodeType = "rack" | "label" | "zone";

export interface SceneNode {
  id: string;
  type: NodeType;
  x: number;   // px
  y: number;   // px
  rot?: number; // deg
  w?: number;  // px (optional for zones/labels)
  h?: number;  // px
  text?: string;
  name?: string;
  rack_id?: number;
}

export interface Scene {
  nodes: SceneNode[];
}

export const emptyScene: Scene = { nodes: [] };

// Simple snap
export const snap = (value: number, grid = 10) => Math.round(value / grid) * grid;