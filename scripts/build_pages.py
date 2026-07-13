from __future__ import annotations

import argparse
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = ROOT / "templates" / "base.html"
PAGES_PATH = ROOT / "templates" / "pages"
SOURCE_PATH = ROOT / "src"
OUTPUT_PATH = ROOT / "out"
GENERATED_PAGE_NAMES = frozenset({"index.html", "legal.html", "resources.html"})


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


def build_site(output_path: Path) -> None:
    if output_path.exists():
        shutil.rmtree(output_path)

    shutil.copytree(
        SOURCE_PATH,
        output_path,
        ignore=lambda _directory, names: GENERATED_PAGE_NAMES.intersection(names),
    )
    shutil.copy2(ROOT / "CNAME", output_path / "CNAME")

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    for page in PAGES:
        rendered = render_page(template, page)
        output_file = output_path / page.filename
        output_file.write_text(rendered, encoding="utf-8", newline="\n")
        print(f"Built {output_file.relative_to(ROOT) if output_path == OUTPUT_PATH else page.filename}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the static HTML pages.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate that the site can be built without writing repository output.",
    )
    args = parser.parse_args()

    if args.check:
        with tempfile.TemporaryDirectory() as temporary_directory:
            build_site(Path(temporary_directory) / "out")
        print("Site build validation passed.")
    else:
        build_site(OUTPUT_PATH)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
