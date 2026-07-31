"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { fetchCirculars, type CircularSummary } from "@/lib/api";

export default function Home() {
  const [circulars, setCirculars] = useState<CircularSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadCirculars() {
      try {
        const data = await fetchCirculars();
        setCirculars(data);
      } catch (err) {
        console.error(err);
        setError("Could not load circulars. Is the API running?");
      } finally {
        setLoading(false);
      }
    }

    loadCirculars();
  }, []);

  return (
    <div className="min-h-screen bg-zinc-100 text-zinc-900">
      <header className="border-b border-zinc-200 bg-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-6">
          <div>
            <p className="text-xs font-medium uppercase tracking-wider text-zinc-500">
              MCA Circulars
            </p>
            <h1 className="mt-1 text-2xl font-semibold tracking-tight">
              Current Circulars
            </h1>
          </div>
          <p className="text-sm text-zinc-500">
            {loading ? "Loading…" : `${circulars.length} available`}
          </p>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-6 py-10">
        {loading && (
          <p className="text-zinc-600">Loading circulars…</p>
        )}

        {error && (
          <p className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800">
            {error}
          </p>
        )}

        {!loading && !error && circulars.length === 0 && (
          <p className="text-zinc-600">
            No structured circulars found yet. Run the scraper pipeline first.
          </p>
        )}

        <div className="grid gap-3">
          {circulars.map((circular) => (
            <Link
              key={circular.id}
              href={`/dashboard/${encodeURIComponent(circular.id)}`}
              className="block border border-zinc-200 bg-white px-5 py-4 transition hover:border-zinc-400 hover:bg-zinc-50"
            >
              <p className="text-xs font-medium uppercase tracking-wider text-zinc-500">
                {circular.id}
              </p>
              <h2 className="mt-1 text-lg font-semibold text-zinc-900">
                {circular.title}
              </h2>
            </Link>
          ))}
        </div>
      </main>
    </div>
  );
}
