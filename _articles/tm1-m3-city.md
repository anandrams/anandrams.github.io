---
title: "Adding buildings, terrain and airspace to a small-UAS mission planner"
description: "Milestone M3 of TM-1, a simulated fixed-wing UAV: OpenStreetMap buildings, USGS terrain and FAA airspace turned into limit maps, the Part 107 altitude rule as written, and what that leaves of downtown Chicago for routine flight."
date: 2026-10-18 06:00:00 +0000
part: 6
phase: "M3"
kind: Article
series: "TM-1 UAV"
series_slug: tm1
project: "TM-1 UAV"
project_url: /projects/tm1/
theme: "Airspace & Rules"
image: /assets/articles/tm1/media/m3/screens/05_flythrough.jpg
image_alt: "A flight path over a 3D view of downtown Chicago."
simnote: "TM-1 UAV, milestone M3. Simulation only: no real aircraft was built or flown."
tags:
  - "UAV"
  - "Part 107"
  - "mission planning"
  - "OpenStreetMap"
  - "geospatial"
  - "simulation"
math: true
# Add corrections here; the article shows them, dated.
# corrections:
#   - date: 2026-11-02
#     note: "What changed, and why."
---

<video src="/assets/articles/tm1/media/m3/tm1_m3_city_walkthrough.mp4" poster="/assets/articles/tm1/media/m3/tm1_m3_city_walkthrough.jpg" controls muted playsinline preload="metadata"></video>

*The city in the planner: buildings, roads and airspace; the previous reference mission failing; a new mission passing and flown; a second city. 68 s.*

TM-1 is a 2.5 kg fixed-wing UAV that I am developing in simulation for traffic monitoring over downtown Chicago. The previous milestone produced a mission planner that checked each mission against the aircraft's limits on a flat, empty map. This milestone adds the city: buildings, terrain, roads, places where people gather, and controlled airspace. It also replaces the fixed altitude ceiling with the rule as written in the US small-UAS regulations.

| Result | Value |
|---|---|
| Building volumes, Chicago / San Francisco | 26,388 / 44,711 |
| Chicago buildings with an assumed height | 50% (15 m assumed) |
| Previous reference mission on the city map | fails 5 checks |
| New reference mission: check time | 88 ms |
| New reference mission flown: closest approach | 103 m above any obstacle, 11.6 m below the ceiling |
| Flown path against the prediction | within 6.2 m |

## 1. Regulatory basis

Before changing the planner I reviewed the rules for an aircraft of this class (14 CFR Part 107):

- **Altitude.** The limit is 400 ft (122 m) above ground level. Within 400 ft horizontally of a structure, the aircraft may fly up to 400 ft above the structure's top. Beyond that, only a waiver allows more.
- **People and vehicles.** Flight over people who are not involved is restricted by impact energy. At cruise TM-1 carries about ½mV² = ½ · 2.5 · 18² ≈ 405 J, more than ten times the limits of the categories that do not need a certified aircraft. Sustained flight over moving vehicles is likewise not permitted.
- **Controlled airspace.** Class B, C, D and surface Class E airspace require an authorisation.

These became planner rules:

- the ceiling under the aircraft is 120 m above the ground, or 120 m above a structure within 122 m;
- a simulated waiver record can raise the ceiling to at most 183 m, and it is labelled as an assumption in every report;
- entry into controlled airspace is rejected unless a simulated authorisation is recorded;
- the predicted path may not spend more than 5 s continuously over roads or gathering places;
- the path must keep 30 m above any roof within 50 m.

The legal limits come from the regulations. The last two numbers are my own design choices, since the regulations give none.

I also considered flying between buildings to watch streets from below roof level. It is not practical for this aircraft. Streets in the Loop are 20–30 m wide, the aircraft needs a 49 m turn radius at cruise, and buildings would block the operator's line of sight.

![A mission rejected above the legal ceiling](/assets/articles/tm1/media/m3/screens/03_ceiling_rejected.jpg)
*Rejected: the loiter is above the ceiling that applies at that point (120 m above the ground, or above a structure within 122 m).*

## 2. Data

All data is open, downloaded once, and stored with its date:

- **Buildings, roads and gathering places:** OpenStreetMap, through the Overpass API.
- **Terrain:** USGS 3DEP. It matters in San Francisco, where the ground rises 278 m above the bay.
- **Airspace:** the FAA's open data layers, last edited 2026-09-28.

Building heights are the weakest part of the data. In Chicago, only 565 buildings carry an explicit height and 12,549 a number of floors. The remaining 13,274 (50%) are given an assumed 15 m. Every report states how much of the path passes near such a building.

## 3. Method: limit maps on a grid

The data is rasterised into limit maps on a 10 m grid: ground height, building tops, minimum safe height, the applicable ceiling, the airspace floor, and road cells.

A distance measured on a grid can be wrong by up to half a cell diagonal:

$$\tfrac{1}{2}\sqrt{10^2 + 10^2} \approx 7\ \text{m}$$

I handled this asymmetrically, so the error always falls on the safe side:

- the zone that requires extra height is enlarged;
- the zone in which the higher structure ceiling is granted is reduced.

A test confirms that the higher ceiling is never granted beyond 122 m from a structure.

The planner checks the predicted flight path against these maps. It also checks a straight return home from every point along the path, because the safety monitor can trigger a return at any time. The flight simulation uses the same maps for its altitude triggers and records a collision if the aircraft falls below a building top.

## 4. Results

The mission used as the reference in the previous milestone, planned on a flat map, now fails five checks:

- two legs pass below the rooftops along Michigan Avenue, one of them 71 m below the top of a 183 m building;
- a return home started from one of those legs would cross buildings 114 m above the aircraft's altitude;
- one leg spends 14 s, and the loiter circle 6 s, continuously over roads.

A new reference mission flies a box over Grant Park, crossing roads rather than following them. It then circles 140 m west of Lake Shore Drive, where a camera can observe the road from the side. It passes every check in 88 ms. In the full six-degree-of-freedom simulation it flew 161 s with no safety events.

![The new reference mission flown](/assets/articles/tm1/media/m3/screens/05_flythrough.jpg)
*The new reference mission flown over Grant Park, replayed at 10× speed: a 34° bank in the turns and a loiter beside Lake Shore Drive.*

> **Correction, 24 October 2026.** While building the map layers for the next milestone, I found a defect in the data download used here. OpenStreetMap features mapped as multipolygon relations were requested without their geometry, so 99 buildings and 202 gathering places in the Chicago area were missing from the limit maps. With the data corrected, this reference mission fails the ground-risk check by a fraction of a second: the loiter spends 5.3 s, and the return home 5.1 s, over pedestrian plazas in Grant Park (limit 5 s). Moving the loiter to 250 m west of Lake Shore Drive makes the mission pass again, and the re-flown mission has no safety events. A test now checks that every relation is downloaded with its geometry.

The same configuration-driven pipeline builds a second city from a configuration file alone.

![San Francisco in the planner](/assets/articles/tm1/media/m3/screens/05_san_francisco.jpg)
*Second city: downtown San Francisco, with the terrain rising from the bay.*

## 5. Observations

Once buildings, roads and the altitude rule are included, much of the area within the 500 m range limit of a Grant Park launch point is unavailable for routine flight. Legal, clear routes are found over parks and water, observing roads from beside them. This constrains the camera in the next milestone: it will view traffic obliquely from a stand-off position, not from directly above.

## 6. What I took from this milestone

- **Read the rule as written.** "400 ft" is relative to the ground, and a structure nearby raises it. A flat 120 m ceiling was both too strict and too loose in different places.
- **Put grid errors on the safe side.** A 7 m discretisation error is unavoidable; which way it falls is a choice.
- **State the weak data.** Half the buildings have an assumed height, so every report says how much of the path depends on that assumption.

## Next

The next milestone adds a 3D view of the flight with terrain, a Blender model of the aircraft, the camera footprint, a telemetry panel, and the Remote ID fields.

---

*TM-1 is a simulation. No aircraft was built or flown, and nothing in this project describes a real-world flight. Map data © OpenStreetMap contributors; terrain from the USGS; airspace from the FAA's open data.*
