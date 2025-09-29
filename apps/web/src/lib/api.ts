const baseURL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function get<T = unknown>(path: string): Promise<T> {
  const res = await fetch(`${baseURL}${path}`);
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`);
  return res.json() as Promise<T>;
}

// Example usage:
// const health = await get<{status:string}>("/health/live");