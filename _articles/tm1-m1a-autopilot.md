---
title: "An autopilot with gains calculated from the aircraft model"
description: "Milestone M1, stage A, of TM-1, a simulated fixed-wing UAV: a cascaded-loop autopilot whose gains are derived from the aircraft's own parameters, path-following guidance, a mission manager, flight logging and the first replay videos."
date: 2026-10-17 03:00:00 +0000
part: 3
phase: "M1 stage A"
kind: Article
series: "TM-1 project notes"
series_slug: tm1
project: "TM-1"
project_url: /projects/tm1/
theme: "Controls"
image: /assets/articles/tm1/media/m1/figures/m1_ground_track.jpg
image_alt: "The ground track of a logged flight."
simnote: "TM-1 project notes, milestone M1, stage A. Simulation only: no real aircraft was built or flown."
tags:
  - "UAV"
  - "autopilot"
  - "control systems"
  - "guidance"
  - "simulation"
math: true
# Add corrections here; the article shows them, dated.
# corrections:
#   - date: 2026-11-02
#     note: "What changed, and why."
---

<video src="/assets/articles/tm1/media/m1/tm1_m1_promo.mp4" poster="/assets/articles/tm1/media/m1/tm1_m1_promo.jpg" controls muted playsinline preload="metadata"></video>

*The demonstration mission: four legs, a climb and a descent, two loiter laps, and the return home. Rendered frame by frame from the flight log. 49 s.*

TM-1 is a 2.5 kg fixed-wing UAV with a six-degree-of-freedom flight model, verified in the previous milestone against hand calculations. This stage gives it an autopilot, so that it can fly a whole mission on its own: four waypoint legs, a climb and a descent, two laps of a loiter circle, then home. The autopilot runs at 100 Hz on top of the flight model.

| Demo mission (217 s) | Result | Requirement |
|---|---|---|
| Airspeed error, steady cruise | ≤ 0.01 m/s | ±1 m/s |
| Altitude error after a commanded change | ≤ 1.76 m | ±3 m |
| Distance off the line on straight legs | ≤ 0.54 m | ≤ 10 m |
| Loiter radius error, once captured | 0.1 m | ±10 m |
| Peak bank angle | 34.85° | ≤ 35° |

## 1. Loops inside loops

A fixed-wing autopilot is a stack of simple feedback loops, each producing the command for the one inside it (successive loop closure; Beard and McLain, *Small Unmanned Aircraft*, Chapter 6):

- **course → bank → aileron:** to turn, the aircraft banks; to bank, it moves the ailerons;
- **altitude → pitch → elevator:** to climb, it pitches up; to pitch up, it moves the elevator;
- **airspeed → throttle;**
- **sideslip → rudder**, to keep turns coordinated.

Each inner loop is designed to be much faster than the loop outside it, so each loop can be designed as if the inner one were perfect. Altitude changes are ramped at 2 m/s, so a 20 m change becomes a steady climb instead of a sharp pitch-up that would lose airspeed.

## 2. Where the gains come from

The gains are not tuned by hand. Each loop is written as a simple second-order model whose coefficients come from the aircraft's own parameters at the 18 m/s trim point. The gains are then chosen to give a chosen speed of response and damping. For roll:

$$\ddot\varphi = -a_{\varphi1}\,\dot\varphi + a_{\varphi2}\,\delta_a, \qquad a_{\varphi1} = 61.8\ \text{s}^{-1},\quad a_{\varphi2} = 402\ \text{s}^{-2}$$

The first coefficient is the aircraft's natural roll damping, the second the aileron's power. The roll gain is chosen so that full aileron (25°) is used at a 15° bank error:

$$k_\varphi = \frac{\delta_{a,\max}}{e_{\varphi,\max}} = \frac{25^\circ}{15^\circ} = 1.67$$

The derivative gains come out at zero. TM-1's own aerodynamic damping already exceeds what the design asks for, so the design adds none. If the aircraft changes, the gains are regenerated from the new parameters with one command.

## 3. Following lines and circles

**Straight legs.** The guidance computes a commanded course from the distance to the line, e_py (Beard and McLain, Chapter 10):

$$\chi_c = \chi_q - \chi_\infty \cdot \tfrac{2}{\pi}\arctan\left(k_{path}\, e_{py}\right), \qquad \chi_\infty = 60^\circ$$

Far from the line the aircraft approaches at 60°; close to it the approach flattens onto the line. A leg ends when the aircraft crosses a plane through the waypoint.

**Circles.** For the loiter and the return home, a similar rule converges onto a 60 m circle. A feed-forward bank angle holds the circle without needing a steady error:

$$\varphi_{ff} = \arctan\frac{V^2}{g\rho} = 28.8^\circ \quad (V = 18\ \text{m/s},\ \rho = 60\ \text{m})$$

The aircraft held the circle at a steady 29°.

![Ground track of the demo mission](/assets/articles/tm1/media/m1/figures/m1_ground_track.jpg)
*Ground track of the demonstration mission: planned legs, flown path, the loiter circle and the return home.*

## 4. Two problems found by watching the flight

**The bank angle overshot the limit.** The first flight reached 37° in turns, against a 35° limit. The cause is real flight physics: in a steady turn the yaw rate makes the outer wing faster than the inner one, and the extra lift rolls the aircraft further into the bank. My first idea was to add an integrator to the roll loop. That made it worse, 40–43°, because the integrator wound up while the aircraft was still rolling in. The fix was a stiffer roll loop (full aileron at 15° of error instead of 35°) and a 1° margin on the bank command. Peak bank fell to 34.85°.

**The aircraft looped around the circle before settling.** The circle-following gain was too aggressive for a 60 m circle when the tightest turn the aircraft can fly is 49 m: it could not follow what it was asked to do. A sweep of four gain values picked one that captures the circle in 23 s instead of 33 s, with no crossing through the centre.

Neither problem showed up in the unit tests. Both were obvious as soon as the flight could be seen.

<video src="/assets/articles/tm1/media/m1/clips/03_turn_chase.mp4" poster="/assets/articles/tm1/media/m1/clips/03_turn_chase.jpg" controls muted loop playsinline preload="metadata"></video>

*Chase camera through the 34° coordinated turn at the first waypoint, with the live instrument panel and an attitude inset.*

## 5. Logging and replay

Every control cycle writes one record: time, mode, the full state, every command, the path error and the four control positions. A 217 s flight gives 21,729 records. Each run folder also holds a manifest with the code version and checksums of the configuration files, so any run can be traced to its exact inputs.

From the log the project generates an interactive replay page and videos rendered frame by frame, with a chase camera, captions and an instrument panel.

![Telemetry of the demo mission](/assets/articles/tm1/media/m1/figures/m1_telemetry.jpg)
*Telemetry from the flight log by mission phase: airspeed, altitude, bank and pitch (flown and commanded), throttle and control surfaces. Dashed red lines are the bank and pitch limits.*

## 6. What I took from this stage

- **Integral action is not a general fix.** It removes steady errors, but in a loop that saturates during a manoeuvre it stores up overshoot.
- **A guidance gain has to respect what the aircraft can do.** Asking for a convergence the aircraft cannot fly produces loops, not faster capture.
- **Look at the outputs, not only at the test results.** In this stage the agent also caught its own mistakes: a figure drawn turning the wrong way, a misquoted number in a decision record, and a video pipeline that silently rendered stale frames. Each was found by checking the actual output.

## Next

The second stage of this milestone adds a battery model and a safety monitor, which decide when the aircraft must stop the mission and return home.

---

*TM-1 is a simulation. No aircraft was built or flown, and nothing in this project describes a real-world flight. Videos and figures were rendered from the project's own flight logs.*
