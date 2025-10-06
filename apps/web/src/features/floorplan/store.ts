import { snap, type Scene, type SceneNode } from "./sceneTypes";

type Listener = () => void;

class FloorplanStore {
  private _scene: Scene = { nodes: [] };
  private listeners: Listener[] = [];
  private selectedId: string | null = null;

  subscribe(fn: Listener) { this.listeners.push(fn); return () => this.unsubscribe(fn); }
  unsubscribe(fn: Listener) { this.listeners = this.listeners.filter(l => l !== fn); }
  private emit() { this.listeners.forEach(l => l()); }

  get scene() { return this._scene; }
  get selected() { return this.selectedId; }

  load(scene: Scene) { this._scene = scene; this.emit(); }
  select(id: string | null) { this.selectedId = id; this.emit(); }

  add(node: Omit<SceneNode, "id">) {
    const id = crypto.randomUUID();
    this._scene.nodes.push({ id, ...node });
    this.select(id);
  }

  move(id: string, dx: number, dy: number, grid = 10) {
    const n = this._scene.nodes.find(n => n.id === id); if (!n) return;
    n.x = snap((n.x ?? 0) + dx, grid);
    n.y = snap((n.y ?? 0) + dy, grid);
    this.emit();
  }

  getNode(id: string) {
    return this._scene.nodes.find(n => n.id === id);
  }

  setRect(id: string, x: number, y: number, w: number, h: number, grid = 10) {
    const n = this._scene.nodes.find(n => n.id === id); if (!n) return;
    const minW = 20, minH = 20;
    const sx = snap(x, grid);
    const sy = snap(y, grid);
    const sw = Math.max(minW, snap(w, grid));
    const sh = Math.max(minH, snap(h, grid));
    n.x = sx; n.y = sy; n.w = sw; n.h = sh;
    this.emit();
  }

  updateNode(id: string, patch: Partial<SceneNode>) {
    const n = this._scene.nodes.find(n => n.id === id); if (!n) return;
    Object.assign(n, patch);
    this.emit();
  }
  
  setName(id: string, name: string) {
    const n = this._scene.nodes.find(n => n.id === id); if (!n) return;
    n.name = name;
    this.emit();
  }
}

export const floorplanStore = new FloorplanStore();