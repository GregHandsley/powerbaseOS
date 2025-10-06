// Use relative paths in dev so Vite proxy handles CORS/preflight.
// If a full URL is passed, fetch it as-is.

export async function api<T = unknown>(path: string, init?: RequestInit): Promise<T> {
  const isAbsolute = /^https?:\/\//i.test(path);
  const url = isAbsolute ? path : (path.startsWith("/") ? path : `/${path}`);
  const res = await fetch(url, {
    headers: { "content-type": "application/json", ...(init?.headers || {}) },
    ...init,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<T>;
}

export async function get<T = unknown>(path: string): Promise<T> {
  return api<T>(path);
}