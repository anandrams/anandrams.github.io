---
title: "A 3D replay, an aircraft model and a pointing camera"
description: "Milestone M4 of TM-1, a simulated fixed-wing UAV for traffic monitoring over Chicago: a Blender model built from the aircraft configuration, a gimbal camera with a ground footprint, Remote ID, and a one-page 3D replay with telemetry."
date: 2026-10-24 07:00:00 +0000
part: 7
phase: "M4"
kind: Article
series: "TM-1 project notes"
series_slug: tm1
project: "TM-1"
project_url: /projects/tm1/
theme: "Visualization"
image: /assets/articles/tm1/media/m4/model/render_front_quarter.jpg
image_alt: "Rendered three-quarter view of the TM-1 aircraft."
simnote: "TM-1 project notes, milestone M4. Simulation only: no real aircraft was built or flown."
tags:
  - "UAV"
  - "simulation"
  - "Blender"
  - "CesiumJS"
  - "Remote ID"
  - "flight dynamics"
  - "systems engineering"
math: true
# Add corrections here; the article shows them, dated.
# corrections:
#   - date: 2026-11-02
#     note: "What changed, and why."
---

<video src="/assets/articles/tm1/media/m4/tm1_m4_flight.mp4" poster="/assets/articles/tm1/media/m4/tm1_m4_flight.jpg" controls muted playsinline preload="metadata"></video>

*The demonstration mission, first seen from high above Grant Park at 8× speed, then from the chase, alongside, ground, overhead and onboard-camera views. 52 s.*

TM-1 is a 2.5 kg fixed-wing UAV that I am developing entirely in simulation, for traffic monitoring over downtown Chicago. The earlier milestones produced a six-degree-of-freedom flight model, an autopilot with a safety monitor, and a browser mission planner that checks each route against buildings, terrain, airspace and the US small-UAS rules.

Until this milestone, a flown mission was a 100 Hz log file and a set of plots. M4 makes it visible, and adds two parts the traffic count will need: a camera that points at the road, and the Remote ID broadcast.

| Result | Value |
|---|---|
| Model wing span, measured on the built file | 1.8530 m (configuration: 1.853 m) |
| Camera footprint, straight down from 100 m | 115.5 m wide (sizing estimate: 115 m) |
| Target in the camera's view on the loiter circle | 100% of samples |
| Replay frame rate on an M1 Pro laptop | 60 fps (requirement: 30) |
| Automated tests passing | 234 |

## 1. The aircraft model

### Built from the configuration, not drawn by hand

The model is built in Blender 4.5 by a Python script that reads the same configuration file as the flight model. One command derives every dimension, builds the meshes, exports a 99 kB glTF file for the browser, measures the result and renders the stills. If the wing changes in the configuration, the drawing follows.

<video src="/assets/articles/tm1/media/m4/tm1_m4_model_promo.mp4" poster="/assets/articles/tm1/media/m4/tm1_m4_model_promo.jpg" controls muted playsinline preload="metadata"></video>

*The Blender model: turntable, wing planform, control surfaces moving, propeller and cowling, camera gimbal, details. Rendered frame by frame. 40 s.*

The wing keeps the baseline span and area and tapers 2:1. With span b = 1.853 m, area S = 0.491 m² and taper ratio λ = 0.5, the root chord is

$$c_r = \frac{2S}{b\,(1+\lambda)} = 0.353\ \text{m}, \qquad c_t = \lambda\, c_r = 0.177\ \text{m}$$

The tail is sized with tail volume coefficients, the usual rule of thumb for small conventional aircraft (Raymer, *Aircraft Design*, Section 6.4). With a tail arm of 0.80 m and V_h = 0.45, the horizontal tail needs 0.073 m².

![The TM-1 three-view drawing](/assets/articles/tm1/media/m4/model/tm1_three_view.jpg)
*Three-view, made from the model's own geometry.*

### Why the first version was wrong, although it did not matter to the flight

The first build had a rectangular wing with a symmetric NACA 0012 section. It looked like a radio-control trainer, which raised a fair question: does it matter?

For the simulation, it does not. The flight model computes lift and drag from coefficients, not from the drawing. But the drawing contradicted those coefficients. A symmetric section makes no lift at zero angle of attack, while the flight model's lift coefficient at zero angle is c_l0 = 0.23.

The revised wing uses a cambered NACA 2412 section, whose zero-lift angle is about −2.1°. With a lift-curve slope of 4.82 per radian, a lift coefficient of 0.23 needs the wing 2.7° above its zero-lift angle:

$$\alpha = \frac{c_{l0}}{c_{l\alpha}} = \frac{0.23}{4.82} = 0.048\ \text{rad} \approx 2.7^\circ \quad\Rightarrow\quad i_w = 2.7^\circ - 2.1^\circ = 0.6^\circ$$

So the wing is set at 0.6° incidence, with 3° of dihedral and rounded tips. The flight model is unchanged; the drawing now agrees with it.

Before rebuilding, I compared the old and new wing on a quick 2D mockup, which took seconds instead of a rebuild. A second round added the details a real small UAS carries:

- a registration mark, `FA-SIM0001`, which is a placeholder (US rules require the registration number on an external surface);
- an anti-collision strobe on the fin;
- GPS, telemetry antenna and a pitot tube;
- a shaped, twisted propeller and a motor cowling;
- wing-root fairings;
- a high-visibility orange fin and wingtips.

![TM-1 rendered from the front quarter](/assets/articles/tm1/media/m4/model/render_front_quarter.jpg)
*Eevee render of the final model.*

### Moving parts, and getting the signs right

The ailerons, elevator, rudder, propeller and the camera gimbal are separate parts, driven by the values in the flight log. On a tapered wing with dihedral the aileron hinge lines are swept and tilted, so each part is rotated in Blender until one of its own axes lies exactly along its hinge. The browser then turns it with a single rotation.

Sign conventions are easy to get wrong and hard to spot on screen. In the convention the log follows (Beard and McLain, *Small Unmanned Aircraft*), a positive elevator command moves the trailing edge down. The tests therefore open the real model file, turn each part by +20° the way the browser does, and measure which way the trailing edge moves:

| Positive command | Expected | Measured |
|---|---|---|
| Aileron | right trailing edge up, left down | 21 mm up, 21 mm down |
| Elevator | trailing edge down | 16 mm down |
| Rudder | trailing edge left | 24 mm left |

A sign slip in the model or in its rig file now fails a test instead of only looking odd.

## 2. The camera

The camera sits on a two-axis gimbal under the fuselage and is pointed at a ground target. At every control step the line of sight to the target is turned into the aircraft's own axes, which gives the pan and tilt angles directly. The four image corners are then projected down to the ground to give the footprint:

```python
d_b = r_body_to_ned.T @ d_n                      # line of sight in body axes
pan = atan2(d_b[1], d_b[0])                      # right of the nose is positive
tilt = atan2(d_b[2], hypot(d_b[0], d_b[1]))      # below the body plane is positive
# both clamped to the gimbal limits: tilt -10° to 90°, pan ±180°
rays = r_body_to_ned @ Rz(pan) @ Ry(-tilt) @ corners_camera
```

Straight down from 100 m, with a 60° horizontal field of view, the footprint is 2 × 100 × tan 30° = 115.5 m wide. The sizing estimate in the first phase was 115 m.

![The view through the onboard camera](/assets/articles/tm1/media/m4/screens/04_camera.jpg)
*The replay's camera view, with the target held in the centre.*

### Watching a road from beside it

The demonstration mission points the camera at Lake Shore Drive while the aircraft circles 120 m to the west of it. It does not circle over the road: the planner's rules from the previous milestone exclude sustained flight over moving traffic, so the aircraft watches from beside it.

On the loiter circle, 120–290 m from the target, the camera held the road in view for every sample. Over the whole 161 s flight, it lost the target for 9% of the samples. All of those were steep turns away from a distant target. At 400 m and 100 m altitude, the road sits only atan(100/400) ≈ 14° below the horizon. A 30–34° bank away from it raises it above the gimbal's −10° limit, and the camera can no longer reach it.

> **Correction, 24 October 2026.** A data defect from the previous milestone (map features mapped as multipolygon relations were downloaded without their geometry) hid several pedestrian plazas in Grant Park. With the data corrected, a loiter 120 m from Lake Shore Drive spends just over the 5 s limit above a plaza, and the nearest legal loiter is 250 m west of the road. Re-flown from there, the camera held the road in view for 97% of the loiter samples (218–330 m from the target) and 90% of the whole flight. The figures above are from the original flight.

For the next milestone this matters: vehicles will be counted only while the target is in view.

## 3. Remote ID

US rules (14 CFR Part 89) require most drones to broadcast their identity, position, altitude, velocity, a time mark, an emergency status and the operator's position. The simulator writes these fields into every telemetry record. It uses a placeholder identity and a simulated clock starting at 2026-06-01 15:00 UTC, so every run is reproducible. Nothing is transmitted.

## 4. The replay

The replay is one browser page with the 3D scene and the telemetry on a common clock. The terrain and buildings come from the same cached open data that the planner checks against, so what you see is what the checks used.

<video src="/assets/articles/tm1/media/m4/tm1_m4_ui_walkthrough.mp4" poster="/assets/articles/tm1/media/m4/tm1_m4_ui_walkthrough.jpg" controls muted playsinline preload="metadata"></video>

*A walkthrough of the replay page: telemetry and charts, gimbal and Remote ID, the layer menu, the views and the city. Real-time recording. 100 s.*

The scene shows the model with its moving parts, the flown and planned paths, the camera footprint and view lines, the geofence as a wall up to the 120 m ceiling, and the ceiling along the flight path. The panel has live values, six charts with a cursor on the clock, the Remote ID fields and the safety events. There are six views, including one from the gimbal itself.

Every group of drawn elements is a layer that can be switched off, from the airspace volumes to the labels and the panel. A recording or a display loop can be kept clean with a single setting in the page address.

![The replay page with the whole mission in view](/assets/articles/tm1/media/m4/screens/03_wide.jpg)
*Wide view: flown path, planned route, loiter circle and camera footprint over Grant Park.*

**Frame rate.** On an M1 Pro laptop the page runs at 60 frames per second in both the close and the wide view, the display's limit. The requirement was 30.

**Videos.** The replay exports to MP4. The page's clock is stepped one frame at a time, drawn, and captured, so the video is smooth however fast the browser renders. The walkthrough above is the exception: it is a real-time recording, because it shows the page being used.

## 5. How it is checked

Each requirement has tests named after it, and the milestone is accepted only when they pass. The four main requirements of this milestone:

| Requirement | What it asks | Result |
|---|---|---|
| VIS-01 | Replay at 30 fps or more | 60 fps |
| VIS-02 | Model span within 2% of the configuration; moving parts | 0.0%; signs measured on the file |
| VIS-03 | Camera footprint from position and attitude | 115.5 m nadir check; boresight within 10⁻⁶ m |
| REG-04 | Remote ID message elements in every record | All elements present; position within 5 cm |

The concept of operations and the requirements were also revised in this milestone (version 1.1), and are now generated as formal PDF documents from their source files, with a traceability table that links each requirement to its tests and their latest result. Of 71 requirements, 57 have named tests, all passing; the rest are verified by analysis, demonstration or inspection.

## 6. What I took from this milestone

- **A drawing that has no effect on the physics should still agree with it.** The symmetric wing did no harm to the simulation, but it described a different aircraft. Making the drawing derive from the configuration removed that kind of drift.
- **Test the signs on the real file.** A control surface that moves the wrong way looks plausible in a moving picture. A test that measures the trailing edge does not.
- **Check every claim against the log.** One draft video caption described a 30° bank where the aircraft was in fact flying level. The log showed it, and the shot was moved to the turn where the bank really was 33–34°.
- **Small interface bugs hide in convenience features.** The replay address dropped every setting except the run when it redirected, so a "clean" recording link never worked. It is now covered by a test.

## Next

The next milestone lets the operator pick a monitoring target, a point or a stretch of road, and has the planner propose a stand-off loiter beside it. It then generates simulated traffic on the road network and counts vehicles inside the camera footprint, compared against the simulation's ground truth. Counts only: no images of vehicles, plates or people are stored.

---

*TM-1 is a simulation. No aircraft was built or flown, and nothing in this project describes a real-world flight. The registration mark and Remote ID identity are placeholders. Map data © OpenStreetMap contributors; terrain from the USGS. All images and videos were rendered from the project's own models and data.*
