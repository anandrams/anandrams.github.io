---
title: "TM-1"
code: TM-1
card_title: "TM-1: a simulated fixed-wing UAV for traffic monitoring"
summary: >-
  A 2.5 kg fixed-wing aircraft that plans and flies missions over downtown
  Chicago, built entirely in simulation, with requirements, tests and a gate
  review at every phase.

status: In progress
progress_note: "Phase 0 → M4 accepted"
updated: 2026-10-24

series_slug: tm1
series_window: "Oct 2026"

built_with: "Python, Blender, CesiumJS"
built_note: "Code written with Claude Code"
verified: "234 tests, named after requirements"
verified_note: "6 gate reviews passed"

repo:
  url: ""
  note: "Open source after public release."

card_image: /assets/articles/tm1/media/m4/model/render_front_quarter.jpg
card_image_alt: "Rendered three-quarter view of the TM-1 fixed-wing UAV."
home_image: /assets/articles/tm1/media/m3/screens/05_flythrough.jpg
home_image_alt: "A flight path drawn over a 3D map of downtown Chicago, with buildings and the route's altitude profile."

# Shown on the home-page card.
highlights:
  - "A six-degree-of-freedom flight model, each part checked against a result that can be derived on paper"
  - "A browser mission planner that checks every route against the aircraft's limits, buildings, terrain, airspace and the US small-UAS rules"
  - "A 3D replay with a Blender model and a gimbal camera, generated from the aircraft configuration rather than drawn by hand"

stack:
  - Python
  - NumPy / SciPy
  - pytest
  - Doorstop
  - Blender
  - CesiumJS
  - OpenStreetMap
  - USGS terrain
  - FAA airspace
  - Claude Code

# ---------- 01 Why ----------
why: |
  Traffic monitoring over a dense city is a plausible job for a small fixed-wing
  UAV: it can loiter for far longer than a multirotor and cover more road.
  Whether it is *allowed*, and whether it can actually see the road while obeying
  the rules, is a different question, and the rules are the hard part.

  I wanted to answer that without buying an airframe. Which meant the simulation
  had to be trustworthy enough that a negative result would be believed — not a
  demo that flies because the physics was tuned until it did.

constraints:
  - "US Part 107 rules as written, including the altitude limit and how it changes near a structure"
  - "Real city data: buildings, terrain and controlled airspace over downtown Chicago, not a flat plane"
  - "A 40-minute endurance target, which sets the aircraft size and therefore everything else"
  - "Every claim checkable: each number produced by a script, each test named after the requirement it covers"

# ---------- 02 What was built ----------
what: |
  Four pieces that work as one system: a planner that decides whether a mission
  is legal and flyable, a flight model and autopilot that fly it, a safety
  monitor that can end it, and a replay that makes the result visible.

diagram_caption: "How the pieces fit together"
diagram:
  - nodes:
      - { title: "OpenStreetMap", sub: "Building footprints and heights" }
      - { title: "USGS", sub: "Terrain elevation" }
      - { title: "FAA", sub: "Controlled airspace" }
      - { title: "Part 107", sub: "Altitude rule as written" }
    down: "become limit maps on a grid"
  - nodes:
      - title: "Mission planner, in the browser"
        sub: "Draws the route, predicts the path the aircraft will actually fly, and rejects what the aircraft or the rules will not allow — with a tested fix suggested for every failure"
        acc: true
    down: "mission JSON"
  - nodes:
      - { title: "Flight model", sub: "Six degrees of freedom, aerodynamics with stall, RK4" }
      - { title: "Autopilot", sub: "Cascaded loops, gains from the aircraft's own parameters" }
      - { title: "Safety monitor", sub: "Geofence, ceiling, battery; decides when to return home" }
      - { title: "Camera gimbal", sub: "Two axes, points at a ground target" }
    down: "100 Hz state log"
  - nodes:
      - { title: "3D replay", sub: "City, flown path, telemetry on one clock" }
      - { title: "Flight plots", sub: "Ground track, altitude, battery" }
      - { title: "Camera footprint", sub: "What the aircraft can actually see" }
      - { title: "Remote ID", sub: "Broadcast message set, simulated" }

sim_note: "Simulation only: no aircraft was built or flown, and nothing here describes a real-world flight."

# ---------- 03 How it was built ----------
how: |
  The same loop at every phase, and nothing moves on until the gate passes. The
  Python is written with Claude Code; the requirements, the tests and the gate
  review are mine. That division is the point of the process: the agent writes,
  the requirement decides whether what it wrote is right.

loop_caption: "The loop, once per phase"
loop:
  - { title: "Requirement",     note: "Written first, with an ID" }
  - { title: "Decision record", note: "What was chosen, and why" }
  - { title: "Implementation",  note: "Written with an AI agent" }
  - { title: "Test",            note: "Named after the requirement" }
  - { title: "Gate review",     note: "Pass, or the phase does not close", acc: true }
  - { title: "Write-up",        note: "Published as one part" }
loop_note: "A failed test sends the work back to step 01, not step 03. Twice the requirement was the thing that was wrong."

# ---------- 04 Results ----------
results:
  - "The aircraft flies the demonstration mission over downtown Chicago, within the Part 107 altitude limit, and returns home on the safety monitor's own triggers"
  - "The model's measured wing span matches the configuration file it was generated from, to four decimal places"
  - "The camera's ground footprint matches the sizing estimate, and the target stays in view for the whole loiter"
  - "Every figure below is produced by a script and matches that phase's technical report"
results_caveat: >-
  No wind model beyond steady conditions, no hardware in the loop, and no
  comparison against a flown aircraft.

figures:
  - { value: "6",      label: "phases accepted" }
  - { value: "234",    label: "automated tests passing" }
  - { value: "2.5 kg", label: "aircraft, 1.853 m span" }
  - { value: "60 fps", label: "3D replay, target 30" }

gallery:
  - src: /assets/articles/tm1/media/m4/model/render_front_quarter.jpg
    alt: "Rendered three-quarter view of the TM-1 aircraft."
  - src: /assets/articles/tm1/media/m3/screens/05_flythrough.jpg
    alt: "The planner showing a route over a 3D view of downtown Chicago."
  - src: /assets/articles/tm1/media/m4/screens/04_camera.jpg
    alt: "The onboard camera view with its ground footprint drawn."

# ---------- 05 Decisions ----------
decisions:
  - claim: "The drawing disagreed with the model, and that counted as a defect"
    text: >-
      The first aircraft model used a symmetric wing section, which makes no lift
      at zero angle of attack — while the flight model's lift coefficient at zero
      angle was 0.23. It changed no simulation result. It was still wrong, so the
      geometry is now generated from the same configuration file the flight model
      reads.
  - claim: "The planner checks the flown path, not the drawn one"
    text: >-
      A route drawn on a map is not the route a fixed-wing aircraft flies: it
      cannot turn inside its own turn radius. The planner predicts the real path
      first, then tests that against the limits, which is why it can suggest a fix
      that actually works.
  - claim: "A map-data fix invalidated a published result"
    text: >-
      Correcting the building data moved a loiter that had previously passed the
      ground-risk rule. The mission was moved and re-flown rather than left
      standing, and the correction is recorded on the article it affects.

# ---------- 06 Phase log ----------
phase_log:
  - { date: 2026-10-24, phase: "M4 accepted.",      note: "3D replay, Blender model, camera footprint and Remote ID." }
  - { date: 2026-10-18, phase: "M3 accepted.",      note: "City selection, buildings, terrain and airspace; structure-based altitude ceiling and ground-risk checks." }
  - { date: 2026-10-18, phase: "M2 accepted.",      note: "Browser planner on a map of Chicago, with feasibility checks and JSON export." }
  - { date: 2026-10-18, phase: "M1 accepted.",      note: "Autopilot, guidance, logging, flight plots, safety monitor and battery model." }
  - { date: 2026-10-17, phase: "M0 accepted.",      note: "Flight core: six-degree-of-freedom dynamics, aerodynamics, RK4 and trim." }
  - { date: 2026-10-17, phase: "Phase 0 accepted.", note: "Aircraft benchmark, TM-1 baseline sizing and requirements." }

next_up: >-
  M5: a monitoring target with an automatic stand-off loiter, clearer city detail
  in the planner and the 3D view, a traffic source and camera counting with an
  accuracy report.

credits: "Map data © OpenStreetMap contributors. Terrain from the USGS. Airspace from the FAA's open data."
---
