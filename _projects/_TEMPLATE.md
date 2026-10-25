---
# ---------------------------------------------------------------------
# Project case study — copy this file, rename it, fill it in.
#
#   cp _projects/_TEMPLATE.md _projects/<slug>.md
#
# The file name becomes the URL: _projects/tm1.md -> /projects/tm1/
# Leading underscore means Jekyll ignores this file, so the template
# never appears on the site.
#
# Every project uses the same seven sections, in the same order, so two
# projects can be read the same way. Delete any key you have nothing to
# say for yet and that section simply doesn't appear — a project can go
# up with Why and What alone and grow from there.
#
# `why`, `what` and `how` are Markdown: anything after `|` is indented
# two spaces and may run to several paragraphs, with *italics*, links
# and lists.
# ---------------------------------------------------------------------

title: ""                 # short name, used in the breadcrumb
code: ""                  # the project's code, e.g. TM-1
card_title: ""            # the full headline, used on the cards and at the top
summary: >-
  One or two sentences: what it is and what it does. Shown under the title
  and on both cards.

status: In progress       # Concept | In progress | Shipped
progress_note: ""         # e.g. "Phase 0 → M4 accepted"
updated: 2026-01-01       # sorts the projects index; bump it on each change

series_slug: ""           # must match `series_slug` in the articles, which
                          # is what pulls the write-ups into section 07
series_window: ""         # e.g. "Oct 2026"

built_with: ""            # the one-line version, for the glance strip
built_note: ""
verified: ""              # how it is checked, one line
verified_note: ""

repo:
  url: ""                 # leave empty until the repository is public
  note: "Open source after public release."

card_image: /assets/...   # projects index card, roughly 3:2
card_image_alt: ""
home_image: /assets/...   # home-page card; omit to reuse card_image
home_image_alt: ""

# Three or four bullets, shown on the home-page card only.
highlights:
  - ""

stack:
  - ""

# ---------- 01 Why ----------
why: |
  Why this project exists, and what question it answers. Write it for a
  reader who has to decide in thirty seconds whether it is worth their
  time.

constraints:
  - "The rules, limits or targets that shaped every later decision"

# ---------- 02 What was built ----------
what: |
  What the thing actually is, in a paragraph.

# Fig. 1: a block diagram, drawn from this list rather than an image, so
# it stays sharp and readable in both themes. Each row is a band of
# boxes; `down` labels the arrow to the next band. `acc: true` marks the
# box that matters most. One box in a row spans the full width.
diagram_caption: "How the pieces fit together"
diagram:
  - nodes:
      - { title: "", sub: "" }
      - { title: "", sub: "" }
    down: "what passes to the next band"
  - nodes:
      - { title: "", sub: "", acc: true }

sim_note: ""              # any standing caveat about what this is not

# ---------- 03 How it was built ----------
how: |
  The method, and what made it trustworthy.

# Fig. 2: the build loop. Numbered automatically.
loop_caption: "The loop, once per phase"
loop:
  - { title: "", note: "" }
loop_note: ""             # the one line about what happens when a step fails

# ---------- 04 Results ----------
results:
  - "What it does, stated so that it could be checked"
results_caveat: >-
  What this does not show. Keep it: it is the part a reviewer trusts.

figures:                  # the measured numbers, shown as a block of four
  - { value: "", label: "" }

gallery:                  # three images, 3:2, side by side
  - { src: /assets/..., alt: "" }

# ---------- 05 Decisions ----------
decisions:
  - claim: "A sentence someone could disagree with"
    text: >-
      What was decided, and the reasoning. Include the ones that turned out
      to be wrong.

# ---------- 06 Phase log ----------
phase_log:
  - { date: 2026-01-01, phase: "Phase name.", note: "What it delivered." }

next_up: >-
  What the next phase does.

credits: ""               # data sources and attributions, if any
---

Anything written below the front matter appears as a closing note at the
end of the case study. Usually leave it empty.
