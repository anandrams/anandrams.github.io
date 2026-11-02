---
title: "Disc Brake"
code: "Disc Brake Thermal Optimization"
card_title: "Disc Brake Thermal Optimization: a cooler front rotor, no added mass"
summary: >-
  A C/D-segment SUV front brake rotor, redesigned for repeated hard braking:
  8.2% lower peak temperature and 0.92 kg lighter, run as a six-gate
  OEM-style programme with open-source CAD, FEA, CFD and optimisation tools.

status: In progress
# Shown on the home page; more than one project may carry this.
featured: true
progress_note: "G0 → G5 passed, G6 open"
updated: 2026-11-01

series_slug: discbrake
series_window: "Oct–Nov 2026"

built_with: "Python, CadQuery, CalculiX, OpenFOAM, Optuna"
built_note: "Code written with Claude Code"
verified: "3-D FEA + CFD on every finalist"
verified_note: "ASME V&V 20 uncertainty budget; 6 gate reviews"

repo:
  url: ""
  note: "Open source after public release."

report_pdf:
  url: /assets/articles/discbrake/media/discbrake_project_report.pdf
  label: "Project report (PDF, 24 pages)"

card_image: /assets/articles/discbrake/media/still_rotor_baseline_demo.png
card_image_alt: "Parametric CAD render of the baseline ventilated brake rotor."
home_image: /assets/articles/discbrake/media/cae_compare_c0_g5c_poster.jpg
home_image_alt: "Side-by-side 3-D thermal FEA of the baseline and the redesigned rotor through 15 hard stops, same colour scale."

hero_video: /assets/articles/discbrake/media/cae_compare_c0_g5c.mp4
hero_video_poster: /assets/articles/discbrake/media/cae_compare_c0_g5c_poster.jpg
hero_video_caption: "Baseline (left) and the frozen redesign G5C (right), 3-D thermal FEA through 15 hard stops, same colour scale."

# Shown on the home-page card.
highlights:
  - "A five-round optimisation search across roughly 4,600 designs, each finalist re-verified with its own CFD and 3-D FEA run, not just the search model"
  - "An ASME V&V 20 uncertainty budget alongside the result, not a single simulation number presented as fact"
  - "The frozen design is 8.2% cooler and 0.92 kg lighter, with a manufacturing-conservative fallback carried alongside it"
  - "Every AI-assisted step logged, including the three times the optimiser found a gap in the model before the real answer held"

stack:
  - Python
  - CadQuery
  - Gmsh
  - CalculiX
  - OpenFOAM
  - SciPy
  - Optuna
  - PyVista
  - Claude Code

# ---------- 01 Why ----------
why: |
  A brake rotor turns a car's kinetic energy into heat, stores it for a few
  seconds, then has to shed it before the next stop — and the shedding is
  almost entirely down to how the vanes pump air through the vent channels.
  More airflow cools faster; the metal that buys that airflow is metal taken
  out of the plates that store each stop's heat. I wanted to see whether that
  trade-off could be worked the way an OEM component programme would work it:
  requirements first, a verification plan, a frozen design with a decision
  record behind it — using only open-source tools and an AI coding assistant,
  start to finish.

  The honest version of that test needed a result that could come out wrong.
  A demo tuned until it looks good proves nothing. A design that survives its
  own verification plan, its own uncertainty budget, and an optimiser that got
  caught gaming the model three times before the real answer held, proves the
  process works.

constraints:
  - "No added mass and the same outside envelope: a drop-in replacement, not a clean-sheet rotor"
  - "Simulation only: representative geometry, no OEM drawings, no test data"
  - "Open-source tools only, each one qualified before use"
  - "Every result cross-checked by an independent route (a second model, an energy balance, a mesh study) before it counted"

# ---------- 02 What was built ----------
what: |
  Six gates, each with its own deliverable: a benchmark of real SUV rotors, a
  requirements and load-case set, a parametric CAD baseline, a fast concept
  model, 3-D thermal FEA with CFD-measured airflow, and a multi-objective
  optimisation search verified candidate by candidate.

diagram_caption: "How the programme moved from question to frozen design"
diagram:
  - nodes:
      - { title: "SUV parts catalogue", sub: "Six ventilated front rotors" }
      - { title: "UN R13-H, WLTC, NEDC", sub: "Load cases" }
      - { title: "Literature", sub: "Temperature limit, vane correlations" }
    down: "become requirements and a baseline"
  - nodes:
      - { title: "Parametric CAD baseline", sub: "CadQuery, Ø320 × 28 mm, six concepts on a lumped thermal model", acc: true }
    down: "two concepts carried to 3-D"
  - nodes:
      - { title: "3-D thermal FEA", sub: "CalculiX, periodic sector, ASME V&V 20 uncertainty budget" }
      - { title: "Vent airflow CFD", sub: "OpenFOAM, rotating reference frame" }
    down: "calibrate a fast two-zone model"
  - nodes:
      - { title: "NSGA-II search", sub: "~4,600 designs across five rounds, each closing a gap the last one exploited", acc: true }
    down: "candidates re-verified with their own CFD and 3-D FEA"
  - nodes:
      - { title: "Frozen design G5C", sub: "−8.2% peak temperature, 0.92 kg lighter; fallback G5D carried alongside it" }

sim_note: "Simulation only: no physical rotor was built or tested, and the geometry is representative of the vehicle class, not an OEM drawing."

# ---------- 03 How it was built ----------
how: |
  The same gate loop at every stage, and nothing moves on until the gate
  passes. Claude Code wrote the CAD, meshing, solver and optimisation
  scripts; the requirements, the gate decisions, and what to trust from a
  result stayed mine. That division is the point of the process: the agent
  writes and runs, the requirement and the independent check decide whether
  what it produced is right.

loop_caption: "The loop, once per gate"
loop:
  - { title: "Requirement",     note: "Written first, with an ID" }
  - { title: "Decision record", note: "What was chosen, and why" }
  - { title: "Implementation",  note: "Written with an AI agent" }
  - { title: "Verification",    note: "An independent check: a second model, energy balance, mesh study" }
  - { title: "Gate review",     note: "Pass, or the gate does not close", acc: true }
  - { title: "Write-up",        note: "Published as one part" }
loop_note: "The optimiser produced a gate-ready number three times before Round 4's result actually held. Each earlier one had found a gap in the model, caught by checking the optimum against CFD or a manufacturing rule — never by the search itself."

# ---------- 04 Results ----------
results:
  - "The frozen design G5C runs 8.2% cooler at peak (LC-04, 15 stops, 3-D FEA) and 0.92 kg lighter than the baseline, verified in CFD and 3-D FEA, not only the search model"
  - "A manufacturing-conservative fallback, G5D, keeps about half the gain with wider vent channels, in case G5C's 6.2 mm sections turn out not castable"
  - "G5C moves 2.2× the baseline's vent airflow; it runs hotter than the baseline for the first six stops and cooler from stop seven onward"
  - "Every chart below is produced by a script and matches the gate report it came from"
results_caveat: >-
  G5C is the best design found for one objective (fade-test peak temperature,
  no added mass) with this project's models. Noise, thermal cracking, pumping
  loss, cost and castability were not optimised, and a CFD heat-transfer check
  disagrees with the correlation the thermal model uses. It is not a
  production recommendation.

figures:
  - { value: "−8.2%", label: "peak temperature, G5C vs. baseline" }
  - { value: "0.92 kg",    label: "mass saved" }
  - { value: "~4,600",     label: "designs searched, 5 rounds" }
  - { value: "23",         label: "gate reports filed" }

gallery:
  - src: /assets/articles/discbrake/media/still_rotor_baseline_demo.png
    alt: "Parametric CAD render of the baseline ventilated brake rotor."
  - src: /assets/articles/discbrake/media/still_heat_channel.png
    alt: "CFD of one vent channel: air entering cool and warming as it flows to the rim."
  - src: /assets/articles/discbrake/media/section_compare.png
    alt: "Friction-ring sections of the baseline and redesigned rotors, same scale."

# ---------- 05 Decisions ----------
decisions:
  - claim: "Straight vanes won the search, which cuts against how curved-vane rotors are usually sold"
    text: >-
      Straight radial vanes pump more air than backward-curved ones at the
      same speed, and the CFD agrees. But two things in the model favour
      straight vanes beyond that real effect: the curved vanes studied bend at
      a constant rate with no designed inlet angle, and the heat-transfer
      correlation treats channels as straight, missing the secondary flows a
      curved channel produces. The result holds for this study's models; it
      is not a general verdict on curved vanes.
  - claim: "A castability rule was added only after the optimiser had already exploited its absence three times"
    text: >-
      Round 1 found a gap in the textbook airflow estimate. Round 2 found an
      unbounded heat-transfer coefficient. Round 3 converged on 3.2 mm vent
      channels no foundry could cast — found only once the optimum was
      checked against a minimum-section rule, not by the search itself. Round
      4, with that rule in place, is the result that held.
  - claim: "The production choice between the two frozen candidates is left open, not settled by simulation"
    text: >-
      G5C is the larger gain; G5D is the safer bet if G5C's 3.3 mm vanes and
      6 mm channels turn out not castable. No published minimum section for a
      grey-iron brake disc was found, so the 6 mm limit used to separate them
      is this project's own assumption. The actual choice needs a foundry
      review this project does not have.

# ---------- 06 Phase log ----------
phase_log:
  - { date: 2026-11-01, phase: "G5 passed.",  note: "Design frozen at G5C (−8.2%, 0.92 kg lighter); fallback G5D verified; the production-variant choice between them left open, pending a foundry review." }
  - { date: 2026-10-31, phase: "G5 optimisation.", note: "Two-zone thermal model, CFD-based airflow regression, NSGA-II search across five rounds and roughly 4,600 designs." }
  - { date: 2026-10-30, phase: "G4b passed.", note: "Vent airflow measured with OpenFOAM CFD; the cooling correlation updated from an assumed value to the measured one." }
  - { date: 2026-10-30, phase: "G4 passed.",  note: "3-D transient thermal FEA and an ASME V&V 20 uncertainty budget accepted." }
  - { date: 2026-10-27, phase: "G3 concept down-select.", note: "Six concepts compared on a fast lumped thermal model; two carried forward to 3-D FEA." }
  - { date: 2026-10-27, phase: "G0–G2 passed.", note: "Tools qualified; benchmark of six SUV rotors; requirements, load cases and a verification plan written." }

next_up: >-
  G6: the wear-limit case, the remaining load cases run in 3-D, a
  thermal-stress check, and the foundry review that decides between G5C and
  its fallback G5D.

credits: "Benchmark data from a public parts catalogue. Load cases from UN R13-H, WLTC and NEDC. Vane heat-transfer correlation from Limpert, Brake Design and Safety."
---
