#!/usr/bin/env python3
"""
Import project articles into this site.

The articles are written in the project repository, not here. This script
copies them into `_articles/`, copies the media they reference into
`assets/articles/<project>/`, and adds the few front-matter keys the site
needs that the source files don't carry (series, theme, alt text).

Run it after a new phase is written up:

    python3 tools/sync_articles.py \
        --source ~/Documents/HDD/08_ClaudeCowork/projects/UAV_FW_TM/docs/website_articles

What it does to each file:
  * keeps the source front matter (title, description, date, part, phase, …)
  * drops the body's H1, because the layout prints the title itself
  * lifts the italic "simulation only" line into a `simnote` key, so the
    layout can show it as a standing caveat instead of body text
  * rewrites every `media/...` path to the site's asset path
  * adds `series`, `series_slug`, `kind`, `theme`, `image_alt` and `math`

Nothing is invented: `theme` and `image_alt` come from PHASES below, which
is the one table to extend when a new phase is written.

It is safe to re-run: it overwrites one file per source article, named
after that article's `slug`, and copies the media. It never deletes, and
it leaves every other file in `_articles/` alone — so a hand-written
piece such as the project-notes page survives, as long as its filename
does not collide with a source slug. Only standard library.
"""

import argparse
import os
import re
import shutil
import sys

# ----------------------------------------------------------------------
# The one table to edit when a new phase is written up.
#   phase        the `phase:` value in the source front matter
#   display      how the phase is labelled on the Writing index
#   theme        the filter chip; reuse an existing one where it fits
#   image_alt    alt text for the index thumbnail (the `image:` file)
# ----------------------------------------------------------------------

PROJECT = {
    "slug": "tm1",
    "series": "TM-1 UAV",
    "project": "TM-1 UAV",
    "project_url": "/projects/tm1/",
}

# The source articles open with "TM-1 project notes, milestone M4. …".
# On the site "Project Notes" is a format of its own, so that phrase is
# rewritten to the series name as the caveat line is lifted out. Delete
# this once the source articles say the same thing.
SIMNOTE_FIXES = [
    ("TM-1 project notes", PROJECT["series"]),
]

PHASES = {
    "Phase 0": {
        "display": "Phase 0",
        "theme": "Systems Engineering",
        "image_alt": "A wing-loading sizing chart.",
    },
    "M0": {
        "display": "M0",
        "theme": "Flight Dynamics",
        "image_alt": "A plot of the aircraft turning.",
    },
    "M1 (stage A)": {
        "display": "M1 stage A",
        "theme": "Controls",
        "image_alt": "The ground track of a logged flight.",
    },
    "M1 (stage B)": {
        "display": "M1 stage B",
        "theme": "Safety",
        "image_alt": "Safety-monitor traces from a logged flight.",
    },
    "M2": {
        "display": "M2",
        "theme": "Mission Planning",
        "image_alt": "The planner rejecting a route whose turn is too tight.",
    },
    "M3": {
        "display": "M3",
        "theme": "Airspace & Rules",
        "image_alt": "A flight path over a 3D view of downtown Chicago.",
    },
    "M4": {
        "display": "M4",
        "theme": "Visualization",
        "image_alt": "Rendered three-quarter view of the TM-1 aircraft.",
    },
}

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The media tree keeps its shape under the site's assets, so a path in a
# source article only needs this prefix in front of it.
ASSET_PREFIX = "/assets/articles/%s/media/" % PROJECT["slug"]

# ----------------------------------------------------------------------


def split_front_matter(text):
    """Return (front-matter lines, body). Raises if the file has no header."""
    if not text.startswith("---"):
        raise ValueError("no YAML front matter")
    end = text.index("\n---", 3)
    head = text[4:end].strip("\n").split("\n")
    body = text[end + 4:].lstrip("\n")
    return head, body


def parse_front_matter(lines):
    """
    Read the flat `key: value` header the project writes. Flow lists
    (`tags: [a, b]`) are kept as a list; everything else stays a string.
    Quotes around a value are stripped.
    """
    out = {}
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            items = [v.strip().strip("'\"") for v in value[1:-1].split(",")]
            out[key] = [v for v in items if v]
        else:
            if len(value) > 1 and value[0] == value[-1] and value[0] in "'\"":
                value = value[1:-1]
            out[key] = value
    return out


def yaml_quote(value):
    """Double-quote a scalar for YAML, escaping what must be escaped."""
    return '"%s"' % str(value).replace("\\", "\\\\").replace('"', '\\"')


def strip_title_and_note(body):
    """
    Remove the body's H1 and the italic caveat line under it, returning
    (body, simnote). The layout prints the title and shows the caveat in
    its own block, so leaving them in the body would duplicate both.
    """
    lines = body.split("\n")
    simnote = ""
    out = []
    i = 0
    seen_h1 = False

    while i < len(lines):
        line = lines[i]

        if not seen_h1 and line.startswith("# "):
            seen_h1 = True
            i += 1
            # Skip blank lines, then take the italic line if there is one.
            while i < len(lines) and not lines[i].strip():
                i += 1
            stripped = lines[i].strip() if i < len(lines) else ""
            if stripped.startswith("*") and stripped.endswith("*") and not stripped.startswith("**"):
                simnote = stripped.strip("*").strip()
                for old, new in SIMNOTE_FIXES:
                    simnote = simnote.replace(old, new)
                i += 1
            continue

        out.append(line)
        i += 1

    return "\n".join(out).lstrip("\n"), simnote


def rewrite_media(body):
    """Point every relative media reference at the site's asset path."""
    body = re.sub(r'(?<=\]\()media/', ASSET_PREFIX, body)
    body = re.sub(r'(?<=["\'])media/', ASSET_PREFIX, body)
    return body


def referenced_media(body):
    """Every media path the body uses, so only those files are copied."""
    return set(re.findall(r'%s([^\s"\')]+)' % re.escape(ASSET_PREFIX), body))


def build(source, dry_run=False):
    source = os.path.abspath(os.path.expanduser(source))
    if not os.path.isdir(source):
        sys.exit("source folder not found: %s" % source)

    articles_dir = os.path.join(SITE_ROOT, "_articles")
    media_dir = os.path.join(SITE_ROOT, "assets", "articles", PROJECT["slug"], "media")

    names = sorted(
        f for f in os.listdir(source)
        if f.endswith(".md") and f != "README.md"
    )
    if not names:
        sys.exit("no articles found in %s" % source)

    if not dry_run:
        os.makedirs(articles_dir, exist_ok=True)

    wanted_media = set()
    written = []

    for name in names:
        path = os.path.join(source, name)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()

        try:
            head, body = split_front_matter(text)
        except ValueError as exc:
            print("  skipped %-12s %s" % (name, exc))
            continue

        fm = parse_front_matter(head)
        for required in ("title", "description", "date", "part", "phase", "slug"):
            if required not in fm:
                sys.exit("%s: front matter has no '%s'" % (name, required))

        phase = PHASES.get(fm["phase"])
        if phase is None:
            sys.exit(
                "%s: phase %r is not in the PHASES table in this script.\n"
                "Add it (display, theme, image_alt) and run again."
                % (name, fm["phase"])
            )

        body, simnote = strip_title_and_note(body)
        body = rewrite_media(body)
        wanted_media |= referenced_media(body)

        image = fm.get("image", "")
        if image.startswith("media/"):
            image = ASSET_PREFIX + image[len("media/"):]
            wanted_media.add(image[len(ASSET_PREFIX):])

        # Several parts can share a completion date. Giving each one an
        # hour equal to its part number keeps the series in order wherever
        # the site sorts by date, without inventing a different date.
        hour = min(int(fm["part"]), 23)
        stamped_date = "%s %02d:00:00 +0000" % (fm["date"], hour)

        out = ["---"]
        out.append("title: %s" % yaml_quote(fm["title"]))
        out.append("description: %s" % yaml_quote(fm["description"]))
        out.append("date: %s" % stamped_date)
        out.append("part: %s" % fm["part"])
        out.append("phase: %s" % yaml_quote(phase["display"]))
        out.append("kind: Article")
        out.append("series: %s" % yaml_quote(PROJECT["series"]))
        out.append("series_slug: %s" % PROJECT["slug"])
        out.append("project: %s" % yaml_quote(PROJECT["project"]))
        out.append("project_url: %s" % PROJECT["project_url"])
        out.append("theme: %s" % yaml_quote(phase["theme"]))
        if image:
            out.append("image: %s" % image)
            out.append("image_alt: %s" % yaml_quote(phase["image_alt"]))
        if simnote:
            out.append("simnote: %s" % yaml_quote(simnote))
        if fm.get("tags"):
            out.append("tags:")
            out.extend("  - %s" % yaml_quote(t) for t in fm["tags"])
        # KaTeX is loaded only where there is an equation to render.
        out.append("math: %s" % ("true" if "$$" in body else "false"))
        out.append("# Add corrections here; the article shows them, dated.")
        out.append("# corrections:")
        out.append("#   - date: 2026-11-02")
        out.append('#     note: "What changed, and why."')
        out.append("---")
        out.append("")
        out.append(body.rstrip() + "\n")

        target = os.path.join(articles_dir, "%s.md" % fm["slug"])
        if not dry_run:
            with open(target, "w", encoding="utf-8") as fh:
                fh.write("\n".join(out))

        written.append((fm["part"], fm["slug"], name))

    print("articles (%d):" % len(written))
    for part, slug, name in sorted(written, key=lambda r: int(r[0])):
        print("  part %-2s  %-24s  <- %s" % (part, slug, name))

    copied = 0
    skipped = []
    for rel in sorted(wanted_media):
        src = os.path.join(source, "media", rel)
        dst = os.path.join(media_dir, rel)
        if not os.path.isfile(src):
            skipped.append(rel)
            continue
        if not dry_run:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
        copied += 1

    print("media: %d files -> assets/articles/%s/media/" % (copied, PROJECT["slug"]))
    if skipped:
        print("MISSING from the source folder (%d):" % len(skipped))
        for rel in skipped:
            print("  media/%s" % rel)

    if dry_run:
        print("\n(dry run: nothing was written)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument(
        "--source",
        required=True,
        help="the project's docs/website_articles folder",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="report what would happen, write nothing",
    )
    args = ap.parse_args()
    build(args.source, dry_run=args.dry_run)
