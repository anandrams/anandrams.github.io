---
title: "Safety monitor and battery model for a simulated fixed-wing UAV"
description: "Milestone M1, stage B, of TM-1, a simulated fixed-wing UAV: a battery model that checks the 40-minute endurance, a safety monitor that decides when to return home, and a defect found by testing every flight instead of one."
date: 2026-10-18 04:00:00 +0000
part: 4
phase: "M1 stage B"
kind: Article
series: "TM-1 UAV"
series_slug: tm1
project: "TM-1 UAV"
project_url: /projects/tm1/
theme: "Safety"
image: /assets/articles/tm1/media/m1/figures/m1b_safety.jpg
image_alt: "Safety-monitor traces from a logged flight."
simnote: "TM-1 UAV, milestone M1, stage B. Simulation only: no real aircraft was built or flown."
tags:
  - "UAV"
  - "safety"
  - "battery"
  - "flight control"
  - "simulation"
math: true
# Add corrections here; the article shows them, dated.
# corrections:
#   - date: 2026-11-02
#     note: "What changed, and why."
---

<video src="/assets/articles/tm1/media/m1/safety/tm1_m1_safety.mp4" poster="/assets/articles/tm1/media/m1/safety/tm1_m1_safety.jpg" controls muted playsinline preload="metadata"></video>

*The safety scenarios: geofence, altitude ceiling, low battery and stall protection, each triggering a return home or a recovery. 70 s.*

TM-1 is a 2.5 kg fixed-wing UAV that I am developing in simulation. It has a six-degree-of-freedom flight model, a cascaded-loop autopilot, and a mission manager that flies waypoint legs, a loiter and a return home. The previous stage showed that it can fly a mission. This stage adds the functions that decide when it should stop: a battery model, a safety monitor, and a test for every requirement in the milestone.

| Result | Value | Requirement |
|---|---|---|
| Endurance, level cruise | 40.78 min | ≥ 40 min with 20% left |
| Endurance, 40-minute loiter at 29° bank | 40.44 min | same |
| Range limit, flying straight out | peak 491 m | ≤ 500 m |
| Altitude, mission planned at 130 m | peak 115.8 m | ≤ 120 m |
| Lowest speed in a stall recovery | 9.9 m/s | above the 8.2 m/s stall |
| Peak bank angle, all eight test flights | ≤ 34.0° | ≤ 35° |

## 1. Battery model and endurance

The battery is modelled as an ideal energy store: capacity is mass times specific energy (200 Wh/kg). Every 10 ms it is drained by the motor's electrical power plus an 8 W avionics load. The sizing made the same assumption, so the endurance test checks the aircraft's power draw rather than a different battery model.

The requirement is 40 minutes at cruise with 20% of the battery left at landing. The first check failed narrowly. The flight model needs 105.9 W at 18 m/s against 105.5 W in the hand sizing; the difference comes mainly from the elevator drag needed to trim. With the sized 0.44 kg battery that gives 39.87 minutes. I raised the battery to 0.45 kg, within the fixed total mass, which gives 40.78 minutes in level cruise and 40.44 minutes in a closed-loop loiter.

The margin is about 2%. Endurance scales with specific energy, so the requirement fails below 196 Wh/kg. I recorded this as an open assumption rather than a verified value.

## 2. The safety monitor

The monitor runs every control cycle, before the mission manager, and can override it.

![Four safety scenarios](/assets/articles/tm1/media/m1/figures/m1b_safety.jpg)
*(a) Geofence: the turn home starts at 433 m and peaks at 491 m. (b) Altitude ceiling and the 60 m floor. (c) Endurance with the low-battery return at 39.2 min. (d) Stall protection with the motor at 25% power.*

### Range limit: predict, then turn

A fixed rule such as "turn back at 400 m" is too blunt. It stops an aircraft that is flying along the boundary at 450 m, which is safe, and it barely protects one flying straight out. The monitor asks instead: if the aircraft started turning home now, how far out would it get?

$$d_{pred} = d + V\cos\theta \cdot t_{lag} + R_{min}\,(1 - \sin\theta)$$

Here d is the current distance from home, θ the angle between the course and the outward direction, t_lag = 1 s the time the control loops need to react, and R_min = V²/(g tan 34°) = 49 m the tightest turn. Flying straight out (θ = 0), the prediction adds 18 m + 49 m, so the turn starts at 433 m; the aircraft peaked at 491 m. Flying along the boundary (θ = 90°), nothing is added and there is no early trigger. A fixed 400 m trigger, which I tried first, stopped a legitimate mission whose corner lies 461 m from home.

### Low battery

The return home is triggered when the energy needed to get back, with a safety factor of 1.25, would cut into the 20% reserve:

$$E_{left} - 1.25\, E_{return} \le 0.20\, E_{batt}$$

In the endurance flight this fired at 39.2 minutes, and the aircraft finished with 21.5%.

### Low airspeed

In a turn the wing carries more than the aircraft's weight, so the stall speed rises with the load factor n = 1/cos φ:

$$V_{stall}(\varphi) = V_{stall,1g}\sqrt{\frac{1}{\cos\varphi}}$$

The warning speed is 1.3 times that: 10.7 m/s wings level and 11.8 m/s at 34° of bank. A warning raises the speed command, limits the bank and stops any climb. If it lasts 3 s, the aircraft enters a recovery mode (wings level, full throttle) and then returns home. With the motor cut to 25% power, the recovery lasted 1.8 s and the lowest speed was 9.9 m/s.

### Altitude

The return home triggers at 115 m, 5 m below the 120 m ceiling. Commands below 60 m are held at 60 m during the mission.

## 3. A defect found by testing every flight

Testing the 35° bank limit on all eight test flights, not only the nominal mission, showed peaks of 35.1–35.7° on the slower flights. This was a steady error, not an overshoot. In a turn, the yaw rate creates a rolling moment that deepens the bank, and a proportional roll loop can only resist it by holding an error. That error grows roughly with the inverse square of airspeed: 0.9° at 18 m/s, 1.9° at 12 m/s.

I added a feed-forward term that calculates, from the aircraft's own coefficients, the aileron needed to cancel this moment at the commanded bank:

$$\delta_{a,ff} = -\frac{C_{l_r}}{C_{l_{\delta a}}} \cdot \frac{b}{2V}\, r_c, \qquad r_c = \frac{g \sin\varphi_c}{V}$$

Peak bank is now 34.0° or less on every flight, including the nominal one, which had reached 34.85°.

## 4. Verification

- **127 automated tests**, each named after the requirement it checks.
- **Eight closed-loop scenario flights**, read back from the 100 Hz log, plus the 40-minute endurance flight.
- **98% test coverage** of the flight core.
- **A parameter register** for every assumed aircraft value: 12 checked by a requirement-level test, 21 traced to a published reference, and 11 that a simulation cannot verify, such as the avionics power and the battery's specific energy.

The distinction matters. A passing test shows that the model behaves consistently with its parameters. It does not show that the parameters describe a real aircraft.

## 5. What I took from this stage

- **A limit should be predicted, not just measured.** The range trigger depends on heading, because what matters is where the turn home will end, not where the aircraft is now.
- **Test the whole set, not the nominal case.** The bank-limit defect appeared only on the slower flights.
- **Record a thin margin as an assumption.** A 2% endurance margin depends entirely on one battery number that the simulation cannot check.

## Next

The next milestone is the mission planner. It checks each leg before flight for turn radius, stall margin, climb and the range limit, including the corner overshoot that the guidance does not smooth.

---

*TM-1 is a simulation. No aircraft was built or flown, and nothing in this project describes a real-world flight. Videos and figures were rendered from the project's own flight logs.*
