---
title: "Disc Brake Thermal Optimization: the concepts behind it"
description: "The physics, the methods and the lessons behind a six-gate brake-rotor redesign, explained from first principles: what a lumped thermal model actually assumes, why a rotating-frame CFD run works, how a multi-objective search finds a Pareto front, and why a design freeze isn't the same as a finished part."
date: 2026-10-28 09:00:00 +0000
kind: Project Notes
series: "Disc Brake Thermal Optimization"
series_slug: discbrake
project: "Disc Brake Thermal Optimization"
project_url: /projects/discbrake/
theme: "Systems Engineering"
image: /assets/articles/discbrake/media/section_compare.png
image_alt: "Friction-ring sections of the baseline and redesigned rotors, same scale."
tags:
  - "brakes"
  - "thermal"
  - "CFD"
  - "optimization"
  - "systems engineering"
math: true
simnote: "Disc Brake Thermal Optimization, project notes. Simulation only: no physical rotor was built or tested."
---

This page is the companion to the Disc Brake Thermal Optimization series.
The articles describe what was built and verified at each gate; this one
explains the concepts underneath them, in plain language, with the
equation where the equation is the clearest way to say it.

It grows with the project. Where a number is this project's own assumption
rather than a measured or published value, it says so — that distinction
is most of what separates this process from a demo tuned until it looks
good.

## 1. Where the heat comes from, and where it has to go

**Braking energy.** A stop converts the vehicle's kinetic energy into heat
at the friction surface over the stop's duration. For a given speed,
deceleration and friction-ring area, the surface heat flux is

$$q''(t) = \frac{1}{2}\,\frac{m v\, \dot v}{A_{friction}}, \qquad t \in [0, t_{stop}]$$

with the one-half accounting for the two friction faces sharing the load
equally. Everything downstream of this project — the thermal model, the
FEA, the optimisation objective — exists to answer one question about this
heat pulse: does it get out before the next one arrives? *(Part 3)*

**The lumped two-zone model.** Before committing to an expensive 3-D run on
every candidate, the project needed a model cheap enough to run thousands
of times: one that splits the rotor into a friction-ring mass, which
absorbs the heat pulse directly, and a vent-channel zone, which carries it
away by convection, connected through a single conduction path and a
convective coefficient:

$$m_{ring}\,c_p\,\frac{dT_{ring}}{dt} = \dot Q_{brake}(t) - hA_{conv}\,(T_{ring}-T_{air})$$

The model is honest about what it is for: ranking concepts against each
other under shared assumptions, not certifying an absolute temperature. The
one input that mattered most and was least trustworthy at first — the
convective coefficient $h$ — is exactly the one Part 4's CFD run went back
and measured. *(Parts 2 and 4)*

**Why the peak matters more than the average.** Across fifteen stops
back-to-back, the friction-ring temperature does not settle to a steady
state; each stop adds more heat than the gap before it removes, so the peak
climbs stop over stop and lands on the final stop, not an earlier or
average one. A requirement written against an average temperature would
miss the thing that actually causes brake fade. *(Parts 2 and 3)*

## 2. Why a mesh study and an uncertainty budget come before the result

**The periodic sector.** A vented rotor's geometry, heat input and
convective boundary all repeat around the vane pattern, so a transient
thermal or flow simulation of the whole 360° disc is mostly wasted
computation: one sector, with periodic boundary conditions on the cut
faces, carries the same physics for a fraction of the mesh. *(Parts 3 and
4)*

**Mesh independence, the honest way to run it.** A single mesh gives a
number; it says nothing about whether that number has converged. Running
the same case at three mesh densities and extrapolating to the limit (a
Richardson extrapolation) estimates what an infinitely fine mesh would have
found, and the gap between that limit and the mesh actually used becomes
the discretisation-uncertainty term. *(Part 3)*

**ASME V&V 20, in one sentence.** A simulated result is only as useful as
the error bar attached to it. The V&V 20 framework builds that bar from two
independent sources — numerical (the mesh study above) and input-parameter
(how much the result moves if the assumed material properties or boundary
conditions are varied within their own uncertainty) — combined in
quadrature:

$$u_{total} = \sqrt{u_{discretisation}^2 + u_{input}^2}$$

Two designs are only counted as different, anywhere later in this project,
if the gap between their central estimates clears this combined band.
*(Part 3)*

## 3. What a rotating-frame CFD run is actually doing

**The MRF trick.** The vent channels move with the disc; the surrounding
air, in the lab frame, is effectively still. Rather than meshing a
literally spinning geometry and advancing it in tiny time steps, a Moving
Reference Frame (MRF) simulation solves the flow in a frame that rotates
with the channel, adding the Coriolis and centrifugal terms the rotation
introduces — the standard approach for turbomachinery-style internal flows,
and far cheaper than a fully transient rotating mesh for the airflow
numbers this project needed. *(Part 4)*

**From a flow field to one number.** The thermal model in Section 1 needs a
single effective heat-transfer coefficient per channel; the CFD run
resolves a full 3-D temperature and velocity field. Reconciling the two
means integrating the measured convective heat flux over the channel
surface against the surface-to-mean-air temperature difference:

$$h_{eff} = \frac{\dot Q_{conv}}{A_{channel}\,(T_{wall} - T_{air,\,mean})}$$

The CFD-measured value replaced the assumed vane correlation everywhere it
had been used, and it did not agree with the correlation either in
magnitude or in how evenly it applied along the channel — the warming
measured in the heat-channel video is concentrated toward the rim end, a
pattern a single averaged coefficient cannot represent. *(Part 4)*

## 4. How a search finds a trade-off instead of a single answer

**Pareto dominance.** With two objectives in play — peak temperature and
mass — there is no single "best" design unless one objective is allowed to
dominate the other, which this project deliberately avoided. Design $x$ is
said to dominate design $y$ when it is at least as good on both objectives
and strictly better on one:

$$x \text{ dominates } y \iff T_{peak}(x) \le T_{peak}(y)\ \text{and}\ m(x) \le m(y),\ \text{with at least one strict}$$

The set of designs no other design dominates is the Pareto front — not one
answer, but the menu of trade-offs actually available. *(Part 5)*

**NSGA-II, briefly.** The search (Deb et al.'s NSGA-II algorithm) evolves a
population of candidate designs generation by generation, keeping the
non-dominated front each round and using it to guide where the next
generation samples. It is good at finding that front efficiently; it has no
way to know whether the model it is evaluating designs against is honest
about the physics — which is exactly what the three model gaps in Part 5
exposed. *(Part 5)*

**Why an optimiser finds a model's gaps before anyone else does.** An
optimisation search is, by construction, hunting for whatever region of the
input space scores best under the model it is given — and a region where
the model is wrong in a *favourable* direction looks, to the search, exactly
like a real improvement. Three times in this project, the search converged
on exactly such a region: an extrapolation past the CFD data a regression
was fit on, an unphysically high fitted coefficient, and a vent-channel
width no foundry could cast. None of the three was caught by the search
itself; each was caught by checking the optimum against something outside
the model that proposed it — the same principle, applied one level up, that
the uncertainty budget in Section 2 applies to a single simulation result.
*(Part 5)*

## 5. Manufacturability is not a simulated quantity

**Why a thermally optimal design can still be the wrong one.** Nothing in
the thermal model, the CFD run or the optimisation objective knows what a
foundry can actually cast. The minimum castable vent-channel width added in
Part 5 — 6 mm — is this project's own conservative assumption, since no
single published minimum-section figure for a grey-iron brake disc was
found during the project; it is not a verified foundry limit, and the
frozen design's 6.2 mm narrowest section sits close enough to that
assumption that a real foundry review, not another simulation, is what
should settle the final choice between it and its fallback. *(Parts 5 and
6)*

**A headline number is not the whole result.** The frozen design's 8.2%
cooler peak temperature is a single-point, single-stop comparison — the
hottest stop of fifteen. Across the earlier stops the same design actually
runs hotter than the baseline, because its higher airflow trades an early
cost for a later benefit. Reporting only the peak, without also reporting
where it isn't the better design, would be the same kind of overclaim this
whole process is built to avoid. *(Part 6)*

## 6. What the project has taught me

Collected from the end of each article, because these are the parts I
expect to reuse on work that has nothing to do with brake rotors.

- **A fast model is for ranking, not for certifying.** Every number the
  screening and search models produced was re-checked in 3-D FEA or CFD
  before it was trusted for anything beyond "this one looks better than
  that one."
- **An optimiser will find a model's gaps before it finds the real
  answer.** Three rounds in a row converged on a region where the model
  was wrong in a direction that happened to look like an improvement.
  Checking the optimum against something outside the model, every round,
  is what caught each one.
- **A number with no uncertainty attached invites exactly the overclaim
  this process is trying to avoid.** The ASME V&V 20 budget on the thermal
  FEA results is what let "both finalists are close enough that neither
  wins yet" be a defensible statement rather than a shrug.
- **A headline figure can hide the part that matters.** "8.2% cooler at
  peak" is true and also incomplete without "and hotter for the first six
  stops" sitting right next to it.
- **A frozen design is not a finished one.** G5C and G5D were both carried
  forward with their open manufacturability question written down, rather
  than one being picked to manufacture a false sense of closure.
- **The agent writes and runs; the requirement and the independent check
  decide.** Claude Code wrote the CAD, meshing, solver and optimisation
  scripts throughout. What kept the results trustworthy was never the
  agent's judgement about whether a result looked right — it was every
  verification step in Sections 1 through 5 above, each one designed before
  the result it would check existed.

## References

The sources this series actually draws on:

- **UN Regulation No. 13-H** — the fade-test load profile (LC-04) used
  throughout this series.
- **WLTC and NEDC** — the duty-cycle load cases used to shape the
  requirements in Part 2.
- **ASME V&V 20-2009** — *Standard for Verification and Validation in
  Computational Fluid Dynamics and Heat Transfer* — the uncertainty-budget
  framework applied in Part 3.
- **Deb, K., Pratap, A., Agarwal, S. and Meyarivan, T.** — "A Fast and
  Elitist Multiobjective Genetic Algorithm: NSGA-II," *IEEE Transactions on
  Evolutionary Computation*, 2002. The search algorithm used in Part 5.
- **Limpert, R.** — *Brake Design and Safety*, SAE International. Vane
  heat-transfer correlations and brake thermal fundamentals, used as the
  starting assumption that Part 4's CFD run later corrected.
- **CadQuery, Gmsh, CalculiX and OpenFOAM** — the open-source CAD, meshing,
  FEA and CFD tools this project is built on; each qualified against a
  problem with a known closed-form answer before use (Part 1).

---

*Disc Brake Thermal Optimization is a simulation study. No physical rotor
was built or tested, and nothing in this project describes a real-world
on-vehicle measurement.*
