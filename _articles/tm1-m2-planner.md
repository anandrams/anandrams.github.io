---
title: "A mission planner that checks the path the aircraft will actually fly"
description: "Milestone M2 of TM-1, a simulated fixed-wing UAV: a browser mission planner on a map of Chicago that predicts the flown path, checks it against the aircraft's limits and the safety monitor's own triggers, and suggests a tested fix for every failure."
date: 2026-10-18 05:00:00 +0000
part: 5
phase: "M2"
kind: Article
series: "TM-1 UAV"
series_slug: tm1
project: "TM-1 UAV"
project_url: /projects/tm1/
theme: "Mission Planning"
image: /assets/articles/tm1/media/m2/screens/01_turn_too_tight.jpg
image_alt: "The planner rejecting a route whose turn is too tight."
simnote: "TM-1 UAV, milestone M2. Simulation only: no real aircraft was built or flown."
tags:
  - "UAV"
  - "mission planning"
  - "geospatial"
  - "simulation"
  - "systems engineering"
math: true
# Add corrections here; the article shows them, dated.
# corrections:
#   - date: 2026-11-02
#     note: "What changed, and why."
---

<video src="/assets/articles/tm1/media/m2/tm1_m2_planner_walkthrough.mp4" poster="/assets/articles/tm1/media/m2/tm1_m2_planner_walkthrough.jpg" controls muted playsinline preload="metadata"></video>

*The planner in use: waypoints placed on the map, a turn that is too tight and an altitude above the ceiling rejected with fixes, then a feasible mission approved and flown. 90 s.*

TM-1 is a 2.5 kg fixed-wing UAV that I am developing in simulation. Earlier milestones produced a six-degree-of-freedom flight model, an autopilot and a safety monitor. This milestone adds the operator's tool: a browser mission planner on a map of downtown Chicago. It checks each mission against the aircraft's limits before the mission can be approved.

| Result | Value |
|---|---|
| Predicted path against the full simulation, reference mission | within 9.3 m (1.8 m on average) |
| Predicted farthest point from home | 1 m beyond the flown one (errs on the safe side) |
| Time for a full check | about 0.1 s; 0.22 s for 50 waypoints |
| Reference mission, approved and flown in the full simulation | no safety events |

## 1. The drawn route is not the flown route

The autopilot switches to the next leg when it reaches a waypoint, then turns at its bank limit. At 18 m/s and 34° of bank that is a 49 m radius. A right-angle corner is therefore not flown as drawn: the aircraft swings about 50 m beyond the new leg before it settles back onto it. A planner that checks only the drawn lines would approve missions that, in flight, cross the 500 m range limit or never settle onto a short leg.

The planner therefore predicts the flown path. It runs the autopilot's own guidance and mode logic on a simplified aircraft model: a coordinated turn with a lag on the bank response.

$$\dot\varphi = \frac{\varphi_c - \varphi}{\tau}, \quad \tau = 0.4\ \text{s}, \qquad \dot\chi = \frac{g\tan\varphi}{V}$$

I calibrated the lag τ against the full simulation. The prediction is fast enough to rerun on every edit.

![A turn rejected as too tight](/assets/articles/tm1/media/m2/screens/01_turn_too_tight.jpg)
*After the 90° turn at the second waypoint, the next leg is too short for the aircraft to get back on the line. The planner says by how much to lengthen it.*

## 2. The checks

Each check reports a reason code and a specific fix:

- altitude between 60 m and 112 m;
- airspeed between 13.7 and 28 m/s;
- climb gradient of 2 m/s or less;
- the distance needed to regain the line after each corner;
- holding the loiter circle;
- the range limit;
- energy;
- the 3 km operating area.

**The turn rule.** A short preview flies one corner of each angle at the mission speed and measures how far along the new leg the aircraft is back within 10 m of the line:

| Turn angle | 30° | 60° | 90° | 120° | 150° | 180° |
|---|---|---|---|---|---|---|
| Distance to regain the line at 18 m/s | 44 m | 110 m | 145 m | 158 m | 152 m | 130 m |

The leg after the corner must be at least that plus 10 m. For a right angle this is about three turn radii, because the aircraft swings out 49 m and then has to come back.

## 3. Limits derived, not chosen

Several limits follow from earlier design decisions rather than being set directly:

- **The ceiling is 112 m, not 120 m.** The safety monitor returns the aircraft home at 115 m, and the autopilot holds altitude within ±3 m.
- **The minimum airspeed is 13.7 m/s.** At 34° of bank the stall-warning speed is 1.3 × 8.2 × √(1/cos 34°) = 11.7 m/s, and the safety monitor keeps 2 m/s above that. Below 13.7 m/s, the autopilot would override the planned speed in every turn.
- **Range and energy use the safety monitor's own trigger formulas** along the predicted path. For range: d + V cos θ · 1 s + R(1 − sin θ) must stay below 500 m. A mission the planner accepts is therefore not cut short by the geofence or the low-battery return.

The suggested fixes are tested too. For each failure type, a test applies the suggested fix and confirms that the failure clears.

![A feasible mission](/assets/articles/tm1/media/m2/screens/03_feasible.jpg)
*Every check passes: predicted time, energy and farthest point are shown, and the mission can be approved.*

Restricted airspace is not checked yet. The Loop lies under the O'Hare and Midway airspace, and the planner reports airspace as "not checked" rather than as a pass until the next milestone adds it.

## 4. Errors found during development

- **The coordinate conversion.** A hand-written local tangent-plane conversion was 0.7 m off at 3 km. A test against an independent geodesic library caught it. I replaced it with an azimuthal equidistant projection centred on home, in which the distance from home is exact.
- **The first turn check accepted everything,** because at the moment of switching the aircraft is, by definition, on the new leg.
- **The screen recording exposed two defects the tests had missed:** the replay viewer could not read the new mission format, and the page ignored the first click after a point was dragged. Both now have tests.

![The approved mission flown](/assets/articles/tm1/media/m2/screens/04_flown.jpg)
*The approved mission flown in the full simulation: no safety events, and the planner's prediction held.*

## 5. What I took from this milestone

- **Check the behaviour, not the drawing.** The useful object to check is the predicted flight path, not the lines the operator drew.
- **Reuse the safety logic in the planner.** When the planner uses the safety monitor's own formulas, an approved mission and a flown mission cannot disagree about the limits.
- **A check that never fails needs a test that makes it fail.** The first turn check passed everything, and only a failing case showed it.

## Next

The next milestone adds city selection, building data from OpenStreetMap and the airspace overlay, so that restricted airspace becomes a real check.

---

*TM-1 is a simulation. No aircraft was built or flown, and nothing in this project describes a real-world flight. Map data © OpenStreetMap contributors.*
