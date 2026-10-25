#!/usr/bin/env python3
"""
Build the site's icon set from the style guide's monogram.

The mark is the "AR" monogram in DM Mono Medium, paper-coloured on an
ink rounded square, with the background baked in so the mark does not
disappear against dark browser chrome.

Outputs, into assets/:
    favicon.svg            the mark as outlines, so no font is needed
    favicon.ico            16 and 32 px
    apple-touch-icon.png   180 x 180
    icon-192.png           for the web manifest
    icon-512.png           for the web manifest
    og-default.jpg         1200 x 630 link preview

Needs the two fonts and Pillow; re-run only when the mark changes.

    python3 tools/make_icons.py --fonts <folder with the .ttf files>
"""

import argparse
import os

from PIL import Image, ImageDraw, ImageFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

INK = (22, 25, 28)        # --ink
PAPER = (245, 242, 234)   # --bg
MUTED = (120, 130, 138)
ACCENT = (184, 66, 12)    # --accent

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(SITE, "assets")


def rounded_icon(size, text, font_path, radius_ratio=0.2, text_ratio=0.38):
    """The monogram on an ink rounded square, drawn at 4x then downsampled."""
    scale = 4
    s = size * scale
    img = Image.new("RGB", (s, s), PAPER)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * radius_ratio), fill=INK)

    font = ImageFont.truetype(font_path, int(s * text_ratio))
    box = d.textbbox((0, 0), text, font=font)
    d.text(
        ((s - (box[2] - box[0])) / 2 - box[0], (s - (box[3] - box[1])) / 2 - box[1]),
        text,
        font=font,
        fill=PAPER,
    )
    return img.resize((size, size), Image.LANCZOS)


def svg_monogram(font_path, text="AR", box=64, radius=13):
    """
    The same mark as an SVG, with the letters converted to outlines so it
    renders identically wherever it is opened.
    """
    font = TTFont(font_path)
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    upem = font["head"].unitsPerEm
    hmtx = font["hmtx"]

    names = [cmap[ord(ch)] for ch in text]
    advance = sum(hmtx[n][0] for n in names)

    size = box * 0.38 * 2.0   # cap height tuned to match the PNG icons
    scale = size / upem

    paths = []
    x = 0
    for name in names:
        pen = SVGPathPen(glyph_set)
        glyph_set[name].draw(pen)
        d = pen.getCommands()
        if d:
            paths.append((d, x))
        x += hmtx[name][0]

    # Centre the run of glyphs in the box, flipping the y axis.
    width = advance * scale
    cap = font["OS/2"].sCapHeight if hasattr(font["OS/2"], "sCapHeight") else upem * 0.7
    left = (box - width) / 2
    baseline = (box + cap * scale) / 2

    body = "\n".join(
        '    <path transform="translate(%.3f %.3f) scale(%.5f -%.5f)" d="%s"/>'
        % (left + x * scale, baseline, scale, scale, d)
        for d, x in paths
    )

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="%s">\n'
        '  <title>%s</title>\n'
        '  <rect width="%d" height="%d" rx="%d" fill="rgb(%d,%d,%d)"/>\n'
        '  <g fill="rgb(%d,%d,%d)">\n%s\n  </g>\n'
        '</svg>\n'
        % (box, box, text, text, box, box, radius, *INK, *PAPER, body)
    )


def og_image(fonts, path):
    """A plain typographic link preview: name, role line, site address."""
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(img)

    # A faint grid, the same 32px module the site uses.
    for x in range(0, w, 32):
        d.line([(x, 0), (x, h)], fill=(236, 231, 218), width=1)
    for y in range(0, h, 32):
        d.line([(0, y), (w, y)], fill=(236, 231, 218), width=1)

    disp = ImageFont.truetype(os.path.join(fonts, "BricolageGrotesque-Bold.ttf"), 76)
    mono_sm = ImageFont.truetype(os.path.join(fonts, "DMMono-Regular.ttf"), 25)
    mono_xs = ImageFont.truetype(os.path.join(fonts, "DMMono-Regular.ttf"), 22)

    pad = 84
    d.text((pad, 150), "MBSE, CONTROLS &", font=mono_sm, fill=ACCENT)
    d.text((pad, 190), "AI-AUGMENTED ENGINEERING", font=mono_sm, fill=ACCENT)
    d.text((pad, 258), "Anand Ram", font=disp, fill=INK)
    d.text((pad, 342), "Sathyanarayanan", font=disp, fill=INK)
    d.line([(pad, 462), (w - pad, 462)], fill=(216, 210, 194), width=2)
    d.text((pad, 486), "Systems Engineer  ·  over a decade in automotive", font=mono_xs, fill=MUTED)
    d.text((pad, 522), "anandrams.github.io", font=mono_xs, fill=INK)

    mark = rounded_icon(104, "AR", os.path.join(fonts, "DMMono-Regular.ttf"))
    img.paste(mark, (w - pad - 104, 150))

    img.save(path, "JPEG", quality=88, optimize=True)


def main(fonts):
    os.makedirs(OUT, exist_ok=True)
    mono = os.path.join(fonts, "DMMono-Regular.ttf")

    with open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8") as fh:
        fh.write(svg_monogram(mono))

    # At 16px the two letters close up, so the .ico uses a single A there,
    # exactly as the style guide says.
    small = rounded_icon(16, "A", mono, radius_ratio=0.25, text_ratio=0.52)
    mid = rounded_icon(32, "AR", mono, radius_ratio=0.22, text_ratio=0.40)
    mid.save(
        os.path.join(OUT, "favicon.ico"),
        sizes=[(16, 16), (32, 32)],
        append_images=[small],
    )

    rounded_icon(180, "AR", mono).save(os.path.join(OUT, "apple-touch-icon.png"), optimize=True)
    rounded_icon(192, "AR", mono).save(os.path.join(OUT, "icon-192.png"), optimize=True)
    rounded_icon(512, "AR", mono).save(os.path.join(OUT, "icon-512.png"), optimize=True)
    og_image(fonts, os.path.join(OUT, "og-default.jpg"))

    for name in ("favicon.svg", "favicon.ico", "apple-touch-icon.png",
                 "icon-192.png", "icon-512.png", "og-default.jpg"):
        p = os.path.join(OUT, name)
        print("  %-22s %6.1f kB" % (name, os.path.getsize(p) / 1024))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument(
        "--fonts",
        default="/mnt/skills/examples/canvas-design/canvas-fonts",
        help="folder holding DMMono-Regular.ttf and BricolageGrotesque-Bold.ttf",
    )
    main(ap.parse_args().fonts)
