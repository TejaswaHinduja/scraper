import pymupdf4llm

markdown = pymupdf4llm.to_markdown("downloads/circular1.pdf")

with open("output.md", "w", encoding="utf-8") as f:
    f.write(markdown)