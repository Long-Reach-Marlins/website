from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = ROOT / "templates" / "base.html"
PAGES_PATH = ROOT / "templates" / "pages"
OUTPUT_PATH = ROOT / "src"


@dataclass(frozen=True)
class Page:
    filename: str
    title: str
    section_class: str
    canonical_url: str
    head_meta: str = ""
    footer_extra: str = ""


PAGES = (
    Page(
        filename="index.html",
        title="Long Reach Marlins, Inc.",
        section_class="wrap",
        canonical_url="https://www.longreachmarlins.org",
        head_meta=(
            '  <meta name="description"\n'
            '    content="Long Reach Marlins, Inc. is a registered 501(c)(3) nonprofit organization that supports the Long Reach Marlins swim team in Columbia, MD." />\n'
            '  <meta name="author" content="Long Reach Marlins, Inc." />\n'
            '  <meta name="robots" content="index, follow" />\n'
            '  <meta name="keywords" content="Long Reach Marlins, swim team, Columbia MD, youth swimming, nonprofit, 501(c)(3)" />'
        ),
        footer_extra=' See <a href="legal.html">Legal</a> for details.',
    ),
    Page(
        filename="legal.html",
        title="Legal — Long Reach Marlins, Inc.",
        section_class="wrap legal",
        canonical_url="https://www.longreachmarlins.org/legal.html",
    ),
    Page(
        filename="resources.html",
        title="Swim Team Resources — Long Reach Marlins, Inc.",
        section_class="wrap resources",
        canonical_url="https://www.longreachmarlins.org/resources.html",
    ),
)


def render_page(template: str, page: Page) -> str:
    content = (PAGES_PATH / page.filename).read_text(encoding="utf-8").rstrip()
    values = {
        "title": page.title,
        "head_meta": page.head_meta,
        "canonical_url": page.canonical_url,
        "section_class": page.section_class,
        "content": content,
        "footer_extra": page.footer_extra,
    }

    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{ " + key + " }}", value)

    if "{{" in rendered or "}}" in rendered:
        raise ValueError(f"Unresolved template token in {page.filename}")

    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the static HTML pages.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if generated pages are missing or out of date.",
    )
    args = parser.parse_args()

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    stale_pages: list[str] = []

    for page in PAGES:
        rendered = render_page(template, page)
        output_file = OUTPUT_PATH / page.filename

        if args.check:
            if not output_file.exists() or output_file.read_text(encoding="utf-8") != rendered:
                stale_pages.append(page.filename)
        else:
            output_file.write_text(rendered, encoding="utf-8", newline="\n")
            print(f"Built {output_file.relative_to(ROOT)}")

    if stale_pages:
        print("Out-of-date generated pages: " + ", ".join(stale_pages))
        return 1

    if args.check:
        print("Generated pages are up to date.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
