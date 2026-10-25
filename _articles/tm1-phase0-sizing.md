---
title: "Sizing a small fixed-wing UAV from its mission"
description: "Phase 0 of TM-1, a simulated fixed-wing UAV for traffic monitoring over Chicago: writing the mission requirements first, screening real aircraft against them, and sizing a new aircraft when none fitted."
date: 2026-10-17 01:00:00 +0000
part: 1
phase: "Phase 0"
kind: Article
series: "TM-1 project notes"
series_slug: tm1
project: "TM-1"
project_url: /projects/tm1/
theme: "Systems Engineering"
image: /assets/articles/tm1/media/phase0/figures/sizing_wing_loading.jpg
image_alt: "A wing-loading sizing chart."
simnote: "TM-1 project notes, Phase 0. Simulation only: no real aircraft was built or flown."
tags:
  - "UAV"
  - "aircraft sizing"
  - "requirements"
  - "systems engineering"
  - "simulation"
math: true
# Add corrections here; the article shows them, dated.
# corrections:
#   - date: 2026-11-02
#     note: "What changed, and why."
---

I am learning aerospace engineering by building a project: a simulated fixed-wing UAV that flies a traffic-monitoring mission over downtown Chicago. The finished system has a flight model, an autopilot, a mission planner that checks every route before flight, a 3D view, and a simulated camera that counts traffic.

I am building it with an AI coding agent (Claude Code). The agent writes and tests the code. I write and own the requirements, make the decisions, and have to be able to explain each equation before a phase is accepted. One aim of the project is to find out whether that way of working can move quickly without my losing track of what was built.

This first phase came before any flight code. Its question: what aircraft is being simulated?

| Result | Value |
|---|---|
| Aircraft | TM-1, sized for the mission; no existing product passed every requirement |
| Mass | 2.5 kg, including a 0.5 kg camera |
| Wing span and area | 1.853 m, 0.491 m² |
| Stall speed | 8.25 m/s (limit 12 m/s) |
| Turn radius at 18 m/s and 35° bank | 47.2 m (limit 50 m) |
| Battery for 40 min with 20% left | 0.44 kg |
| System requirements written | 67, each with a verification method |

## 1. Requirements before the aircraft

The usual shortcut is to choose a known drone and copy its specifications. I did it the other way round: I wrote down what the mission needs, then looked for an aircraft that meets it.

- **Operating class:** under 25 kg, below 120 m above the ground, within the operator's visual line of sight. This is the US small-UAS class (14 CFR Part 107), fixed in the first decision record.
- **Slow flight:** stall at 12 m/s or below, so the aircraft can fly slowly near an observation point.
- **Turning:** a turn radius of 50 m or less at 18 m/s, to manoeuvre inside a 3 km urban area.
- **Endurance:** 40 minutes, with 20% of the battery still unused at landing.
- **Payload:** a 0.5 kg camera.

These became numbered requirements (MP-04 to MP-08 among them), kept in a requirements tool (Doorstop) with a verification method for each.

## 2. Screening real aircraft

I then screened published aircraft against these limits, among them a survey drone, a hobby flying wing and a research UAV. Each data source was graded by how trustworthy it was: a manufacturer's datasheet ranks above a retailer listing, which ranks above a forum post.

No candidate passed every limit with well-sourced data. The closest did not publish its payload capacity. Others were too heavy, took off vertically, or had only retailer data. The decision record lists three options; I chose to size a new aircraft, TM-1, from the requirements, and to use the screened aircraft only as a reference class.

## 3. Sizing TM-1

The sizing starts from a few design choices and derives everything else. The choices are a total mass of 2.5 kg, a cruise speed of 18 m/s, a maximum bank of 35°, a wing aspect ratio of 7 and a wing loading of 50 N/m². The derivations use first-order relations from standard texts (Beard and McLain, *Small Unmanned Aircraft*; Raymer, *Aircraft Design*).

**Wing.** The weight is W = m·g = 24.5 N. The wing loading gives the area, and the aspect ratio gives the span:

$$S = \frac{W}{W/S} = 0.491\ \text{m}^2, \qquad b = \sqrt{AR \cdot S} = 1.853\ \text{m}$$

**Stall.** The wing stalls when the lift coefficient reaches its maximum, assumed to be C_Lmax = 1.2:

$$V_s = \sqrt{\frac{2\,(W/S)}{\rho\, C_{L\max}}} = 8.25\ \text{m/s}$$

**Turn.** In a level turn the lift vector tilts by the bank angle φ; its horizontal part pulls the aircraft round the circle:

$$R = \frac{V^2}{g \tan\varphi} = \frac{18^2}{9.81 \tan 35^\circ} = 47.2\ \text{m}$$

The turn radius does not depend on the wing at all, only on speed and bank. The margin to the 50 m limit is 6%, the smallest in the sizing.

**Power and battery.** At cruise the lift coefficient is 0.252, and the drag coefficient follows from a drag polar with assumed profile drag C_D0 = 0.03 and span efficiency e = 0.85:

$$C_D = C_{D0} + \frac{C_L^2}{\pi e AR} = 0.0334, \qquad D = \tfrac{1}{2}\rho V^2 S\, C_D = 3.25\ \text{N}$$

With an assumed propeller efficiency of 0.6, cruise needs 97.5 W, plus 8 W for the avionics. Forty minutes of that, with 20% of the battery left at landing, needs 87.9 Wh: 0.44 kg of battery at an assumed 200 Wh/kg.

![Stall speed and battery mass against wing loading](/assets/articles/tm1/media/phase0/figures/sizing_wing_loading.jpg)
*Stall speed and battery mass against wing loading for a 2.5 kg aircraft. TM-1 is the orange point.*

The figure shows the main trade-off. A smaller, more heavily loaded wing has less drag at this speed, so it needs a smaller battery. It also stalls at a higher speed. The stall requirement allows a wing loading of up to 105.8 N/m². I chose 50 N/m², which keeps the stall speed at 8.25 m/s, well clear of the limit, at the cost of a larger battery. The figure uses first-order relations only; it does not include the extra structural mass of a larger wing.

## 4. A reserve defined two ways

The first version of the sizing computed the battery energy as the mission energy × 1.2, for a "20% reserve". That is not what the requirement says. If the battery holds 1.2 E and the mission uses E, the aircraft lands with 1 − 1/1.2 = 16.7% left, not 20%. The requirement asks for 20% remaining at landing, so the correct relation is

$$E_{batt} = \frac{E_{mission}}{1 - 0.20}$$

which raised the battery from 0.42 kg to 0.44 kg. The difference is small, but it is the kind of mismatch between a requirement's wording and its arithmetic that is hard to find later. It was caught because the requirement was written down before the calculation.

## 5. What is assumed, and what is not

Each value in the sizing is graded: a design choice, a derived value, or an assumption still to be verified. Six inputs are assumptions: C_Lmax, the span efficiency, the profile drag, the propeller efficiency, the avionics power and the battery's specific energy. Endurance is most sensitive to the profile drag and the propeller efficiency; a 20% change in profile drag changes the cruise power by about 15%. These are the first values the flight model is used to check.

Phase 0 ended with:

- 67 system requirements, each with a verification method;
- written decision records, including the operating class and the choice to size a new aircraft;
- a sizing script that reads every number from a configuration file;
- tests named after the requirements they check;
- a gate report that I signed before any flight code was written.

## Next

The next phase turns TM-1 from a table of numbers into a six-degree-of-freedom flight model, and checks the model against relations that can be worked out by hand.

---

*TM-1 is a simulation. No aircraft was built or flown, and nothing in this project describes a real-world flight. Figures were generated from the project's own sizing equations.*
