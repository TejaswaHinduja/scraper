"use client";

import { useEffect, useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";

function slugify(value: string) {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

export default function CircularViewer() {
  const [markdown, setMarkdown] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadCircular() {
      try {
        const response = await fetch(
          "/structured_circular.md"
        );

        if (!response.ok) {
          throw new Error(
            "Could not load the circular"
          );
        }

        const markdownText =
          await response.text();

        setMarkdown(markdownText);
      } catch (error) {
        console.error(error);

        setError(
          "Could not load this circular."
        );
      } finally {
        setLoading(false);
      }
    }

    loadCircular();
  }, []);

  const headings = useMemo(() => {
  return markdown
    .split("\n")
    .map((line) => {
      const match = line.match(
        /^(#{1,6})\s+(.+)$/
      );

      if (!match) {
        return null;
      }

      const level = match[1].length;
      const title = match[2].trim();

      const id = slugify(title);

      return {
        title,
        level,
        id
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
      <div className="flex h-screen items-center justify-center">
        {error}
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-zinc-100 text-zinc-900">

      {/* Sidebar */}
      <aside className="hidden w-72 shrink-0 border-r border-zinc-200 bg-white text-zinc-900 lg:block">

        <div className="border-b border-zinc-200 p-6">
          <p className="text-xs font-medium uppercase tracking-wider text-zinc-500">
            Document
          </p>

          <h2 className="mt-2 font-semibold text-zinc-900">
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
                paddingLeft: `${heading.level * 10}px`
              }}
            >
              {heading.title}
            </a>
          ))}
        </nav>

      </aside>

      {/* Viewer */}
      <div className="flex min-w-0 flex-1 flex-col">

        {/* Toolbar */}
        <header className="flex h-16 shrink-0 items-center justify-between border-b bg-white px-6 text-zinc-900">

          <div>
            <p className="text-xs font-medium uppercase tracking-wider text-zinc-600">
              Structured Circular
            </p>

            <h1 className="font-semibold text-zinc-900">
              Circular Document
            </h1>
          </div>

        </header>

        {/* Scroll area */}
        <main className="flex-1 overflow-y-auto p-5 md:p-10">

          {/* Document paper */}
          <article className="mx-auto min-h-[1100px] max-w-4xl rounded-xl border border-zinc-200 bg-white px-7 py-10 shadow-sm md:px-14 md:py-16">

            <ReactMarkdown
              components={{
                h1: ({ children }) => {
                  const title = String(children);

                  return (
                    <h1 id={slugify(title)} className="mb-12 border-b border-zinc-200 pb-8 text-4xl font-bold text-zinc-900">
                      {children}
                    </h1>
                  );
                },

                h2: ({ children }) => {
                  const title = String(children);

                  const id = slugify(title);

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
                  const title = String(children);

                  return (
                    <h3 id={slugify(title)} className="mb-3 mt-8 text-lg font-semibold text-zinc-900">
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
                )
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