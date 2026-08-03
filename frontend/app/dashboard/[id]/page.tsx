"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import ReactMarkdown from "react-markdown";
import { fetchCircular } from "@/lib/api";

function slugify(value: string) {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

export default function CircularViewer() {
  const params = useParams<{ id: string }>();
  const circularId = decodeURIComponent(params.id ?? "");

  const [title, setTitle] = useState("");
  const [markdown, setMarkdown] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadCircular() {
      if (!circularId) {
        setError("Missing circular id.");
        setLoading(false);
        return;
      }

      try {
        const circular = await fetchCircular(circularId);
        setTitle(circular.title);
        setMarkdown(circular.content);
      } catch (err) {
        console.error(err);
        setError("Could not load this circular.");
      } finally {
        setLoading(false);
      }
    }

    loadCircular();
  }, [circularId]);

  const headings = useMemo(() => {
    return markdown
      .split("\n")
      .map((line) => {
        const match = line.match(/^(#{1,6})\s+(.+)$/);

        if (!match) {
          return null;
        }

        const level = match[1].length;
        const headingTitle = match[2].trim();
        const id = slugify(headingTitle);

        return {
          title: headingTitle,
          level,
          id,
        };
      })
      .filter(
        (
          heading
        ): heading is {
          title: string;
          level: number;
          id: string;
        } => heading !== null
      );
  }, [markdown]);

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        Loading circular...
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-screen flex-col items-center justify-center gap-4">
        <p>{error}</p>
        <Link href="/" className="text-sm text-zinc-600 underline">
          Back to circulars
        </Link>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-zinc-100 text-zinc-900">
      <aside className="hidden w-72 shrink-0 border-r border-zinc-200 bg-white text-zinc-900 lg:block">
        <div className="border-b border-zinc-200 p-6">
          <Link
            href="/"
            className="text-xs font-medium uppercase tracking-wider text-zinc-500 hover:text-zinc-800"
          >
            ← All circulars
          </Link>

          <h2 className="mt-3 font-semibold text-zinc-900">
            Table of Contents
          </h2>
        </div>

        <nav className="space-y-1 p-4">
          {headings.map((heading) => (
            <a
              key={heading.id}
              href={`#${heading.id}`}
              className="block rounded-md px-3 py-2 text-sm font-medium text-zinc-900 transition hover:bg-zinc-200 hover:text-black"
              style={{
                paddingLeft: `${heading.level * 10}px`,
              }}
            >
              {heading.title}
            </a>
          ))}
        </nav>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-16 shrink-0 items-center justify-between border-b bg-white px-6 text-zinc-900">
          <div>
            <p className="text-xs font-medium uppercase tracking-wider text-zinc-600">
              {circularId}
            </p>

            <h1 className="font-semibold text-zinc-900">{title}</h1>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-5 md:p-10">
          <article className="mx-auto min-h-275 max-w-4xl rounded-xl border border-zinc-200 bg-white px-7 py-10 shadow-sm md:px-14 md:py-16">
            <ReactMarkdown
              components={{
                h1: ({ children }) => {
                  const headingTitle = String(children);

                  return (
                    <h1
                      id={slugify(headingTitle)}
                      className="mb-12 border-b border-zinc-200 pb-8 text-4xl font-bold text-zinc-900"
                    >
                      {children}
                    </h1>
                  );
                },

                h2: ({ children }) => {
                  const headingTitle = String(children);
                  const id = slugify(headingTitle);

                  return (
                    <h2
                      id={id}
                      className="mb-5 mt-14 scroll-mt-8 text-2xl font-semibold text-zinc-900"
                    >
                      {children}
                    </h2>
                  );
                },

                h3: ({ children }) => {
                  const headingTitle = String(children);

                  return (
                    <h3
                      id={slugify(headingTitle)}
                      className="mb-3 mt-8 text-lg font-semibold text-zinc-900"
                    >
                      {children}
                    </h3>
                  );
                },

                p: ({ children }) => (
                  <p className="mb-5 text-[17px] leading-8 text-zinc-800">
                    {children}
                  </p>
                ),

                ul: ({ children }) => (
                  <ul className="mb-6 list-disc space-y-2 pl-6">
                    {children}
                  </ul>
                ),

                ol: ({ children }) => (
                  <ol className="mb-6 list-decimal space-y-2 pl-6">
                    {children}
                  </ol>
                ),
              }}
            >
              {markdown}
            </ReactMarkdown>
          </article>
        </main>
      </div>
    </div>
  );
}
