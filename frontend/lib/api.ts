const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type CircularSummary = {
  id: string;
  title: string;
};

export type CircularDetail = CircularSummary & {
  content: string;
};

export async function fetchCirculars(): Promise<CircularSummary[]> {
  const response = await fetch(`${API_BASE_URL}/circulars`, {
  });

  if (!response.ok) {
    throw new Error("Could not load circulars");
  }

  return response.json();
}

export async function fetchCircular(id: string): Promise<CircularDetail> {
  const response = await fetch(
    `${API_BASE_URL}/circulars/${encodeURIComponent(id)}`,
    
  );

  if (!response.ok) {
    throw new Error("Could not load this circular");
  }

  return response.json();
}
