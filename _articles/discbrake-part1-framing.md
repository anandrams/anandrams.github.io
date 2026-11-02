---
title: "Framing a brake rotor like an OEM programme"
description: "Part 1 of the Disc Brake Thermal Optimization project: qualifying an open-source tool chain, benchmarking six SUV front rotors, and writing the gate structure the rest of the programme follows."
date: 2026-10-27 01:00:00 +0000
part: 1
phase: "G0–G1"
kind: Article
series: "Disc Brake Thermal Optimization"
series_slug: discbrake
project: "Disc Brake Thermal Optimization"
project_url: /projects/discbrake/
theme: "Systems Engineering"
image: /assets/articles/discbrake/media/benchmark.png
image_alt: "Peak temperature and mass for six benchmarked SUV front brake rotors."
simnote: "Disc Brake Thermal Optimization, G0–G1. Simulation only: no physical rotor was built or tested, and the geometry is representative of the vehicle class, not an OEM drawing."
tags:
  - "brakes"
  - "thermal"
  - "benchmarking"
  - "systems engineering"
  - "simulation"
math: false
---

A disc brake's whole job, thermally, is to take the kinetic energy of a stop,
turn it into heat at the friction surface, and get rid of that heat before
the next stop needs the same rotor again. Everything else — the vane shape,
the plate thickness, the choice between a cast-iron rotor and something
lighter — is in service of that one loop. I wanted to run a redesign of that
loop as a real OEM component programme would run it: a stage-gated process
with requirements, decision records, and an independent check on every
result, built entirely with open-source tools and an AI coding agent.

This first gate did none of the interesting engineering. It qualified the
tools, benchmarked the competition, and wrote down the structure the rest of
the programme would follow — the unglamorous work that decides whether a
later result can be trusted.

| Result | Value |
|---|---|
| Programme structure | Seven gates, G0 through G6, each with a written decision record |
| Tool chain | CadQuery, Gmsh, CalculiX, OpenFOAM, SciPy, Optuna, PyVista — all open source, each qualified before use |
| Benchmark | Six ventilated front rotors from a public SUV parts catalogue |
| Baseline chosen | A representative C/D-segment front rotor, Ø320 × 28 mm |
| Load-case sources | UN R13-H fade test, WLTC and NEDC duty cycles |

## 1. Why a gate structure

The easy way to run a personal engineering project is to pick a CAD tool,
sketch something, simulate it, and call it done when the numbers look good.
That produces a result nobody else can check. A gate structure forces the
opposite order: a requirement is written before the design that answers it,
a verification method is chosen before the result that needs verifying, and
a decision record captures what was chosen and why — including, later in
this programme, several decisions that turned out to be wrong.

Seven gates were planned at the outset:

- **G0** — qualify the tools and freeze the stack.
- **G1** — benchmark the competition.
- **G2** — write requirements and load cases.
- **G3** — screen concepts on a fast model.
- **G4 / G4b** — verify the finalists in 3-D FEA and CFD.
- **G5** — search the design space and freeze a design.
- **G6** — close the remaining load cases and hand off for a manufacturing review.

Each gate ends with a written report; none of the later gates in this series
opened without the previous one's report being signed off first.

## 2. Qualifying the tools

Every tool in the chain had to earn its place before being trusted with a
real result: CadQuery for parametric CAD, Gmsh for meshing, CalculiX for
finite-element solving, OpenFOAM for CFD, SciPy and Optuna for the numerical
and optimisation work, and PyVista and Matplotlib for everything that needed
a picture. Each was run once against a problem with a known closed-form
answer — a simple conduction slab for CalculiX, laminar pipe flow for
OpenFOAM — before being used on the actual rotor. A tool that could not
reproduce its own textbook case did not get a second chance on this
programme.

Claude Code wrote the CAD, meshing, solver and automation scripts
throughout. That division of labour — the agent writes and runs, I set the
requirement and read the result — is the same one the TM-1 project uses, and
it is the one this programme leans on for everything that follows.

## 3. Benchmarking six rotors

Six ventilated front rotors from production C/D-segment SUVs were pulled
from a public parts catalogue and compared on diameter, thickness, mass and
published vane geometry, each entry graded by how trustworthy its source was
— a manufacturer spec sheet outranks a listing page, which outranks a forum
estimate. No single rotor in the set was an outlier in every dimension; the
set as a whole set the envelope the redesign had to respect: outside
diameter, hat height, and bolt pattern unchanged, mass not increased.

A representative baseline was built from that envelope — Ø320 mm, 28 mm
thick, a conventional straight-vane vented section — rather than copying any
one manufacturer's part exactly. The baseline is a stand-in for the vehicle
class, not a reverse-engineered drawing of a real product, which is also why
every later comparison in this series is to that baseline and not to a named
part.

## 4. What a load case has to come from

A brake rotor's temperature history depends entirely on how hard and how
often it is asked to stop, so the load cases needed a source that was not
this project's own guess. Three were chosen: the UN R13-H fade test, which
is the regulatory worst case for repeated hard stops; and the WLTC and NEDC
duty cycles, which represent ordinary driving rather than a track day. The
fade test — fifteen stops from a set speed at a fixed deceleration, back to
back — became the load case used throughout the rest of this series,
referred to from here on as LC-04.

## 5. What G0–G1 actually produced

- A qualified, open-source tool chain, each tool checked against a problem with a known answer.
- A six-rotor benchmark with graded sources and a representative baseline geometry.
- Three load cases pulled from regulation and standard duty cycles, not invented.
- A seven-gate programme structure, written down before any CAD was opened.

## Next

Part 2 turns the benchmark and load cases into numbered requirements, then
screens six vent-channel concepts against them on a fast thermal model —
the step that decides which two designs are worth the cost of 3-D FEA.

---

*Disc Brake Thermal Optimization is a simulation study. No physical rotor
was built or tested, and the baseline geometry represents the vehicle class
rather than any one manufacturer's part. Figures were generated from the
project's own benchmark and CAD scripts.*
