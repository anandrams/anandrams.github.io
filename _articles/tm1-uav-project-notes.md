---
title: "TM-1 UAV: the concepts behind it"
description: "The physics, the equations and the lessons behind a simulated fixed-wing UAV, explained from first principles: what six degrees of freedom means, why an aircraft turns by rolling, where the autopilot's gains come from, and how the US small-UAS altitude rule actually reads."
date: 2026-10-25 09:00:00 +0000
kind: Project Notes
series: "TM-1 UAV"
series_slug: tm1
project: "TM-1 UAV"
project_url: /projects/tm1/
theme: "Systems Engineering"
image: /assets/articles/tm1/media/m4/model/tm1_three_view.jpg
image_alt: "Three-view drawing of the TM-1 aircraft."
tags:
  - "UAV"
  - "flight dynamics"
  - "control systems"
  - "aircraft sizing"
  - "Part 107"
math: true
simnote: "TM-1 UAV, project notes. Simulation only: no real aircraft was built or flown."
---

This page is the companion to the TM-1 UAV series. The articles describe what
was built at each phase; this one explains the concepts underneath them, in
plain language, with the equation where the equation is the clearest way to say
it. It is as much a record of what I had to learn as a reference for anyone
reading the series.

It grows with the project. Where a number is an assumption rather than a
measured value, it says so — that distinction is the whole point of the
exercise.

## 1. Sizing the aircraft

**Wing loading** is the aircraft's weight divided by its wing area, in newtons
per square metre. It is the single most consequential number in a sizing,
because almost everything else follows from it. A small, heavily loaded wing has
less drag at cruise and so needs a smaller battery, but it has to fly faster to
stay in the air. A big, lightly loaded wing flies slowly but drags more.

TM-1 uses 50 N/m². The stall requirement would have allowed up to 105.8 N/m².
Choosing the lower figure buys a wide margin on the stall speed and pays for it
in battery mass.

**Aspect ratio** is the ratio of span to average chord — in effect, how long
and thin the wing is. A glider has a high aspect ratio; a fighter has a low one.
Long thin wings lose less energy to the vortices shed at the tips, so they are
more efficient, at the cost of structure and roll response. TM-1 uses 7.

With a weight W, wing loading W/S and aspect ratio AR, the wing follows
immediately:

$$S = \frac{W}{W/S} = 0.491\ \text{m}^2, \qquad b = \sqrt{AR \cdot S} = 1.853\ \text{m}$$

*(Part 1)*

**Stall speed** is the slowest speed at which the wing can still carry the
aircraft's weight. Lift grows with the square of speed and with the lift
coefficient, and the lift coefficient cannot exceed a maximum set by the
airfoil — past a certain angle the airflow separates from the upper surface and
the lift collapses. Setting lift equal to weight at that maximum gives the
slowest flyable speed:

$$V_s = \sqrt{\frac{2\,(W/S)}{\rho\, C_{L\max}}} = 8.25\ \text{m/s}$$

ρ is air density. Note that only the wing loading matters, not the size of the
aircraft: two aircraft with the same wing loading stall at the same speed.
*(Part 1)*

**Turn radius and bank angle.** An aircraft turns by rolling. There is no other
mechanism — the rudder yaws the nose but does not pull the aircraft round a
corner. When the wings bank by an angle φ, the lift vector tilts with them, and
its horizontal component is the force that bends the flight path into a circle:

$$R = \frac{V^2}{g \tan\varphi} = \frac{18^2}{9.81 \tan 35^\circ} = 47.2\ \text{m}$$

The wing does not appear in this at all. Turn radius depends only on speed and
bank angle, which is why a faster aircraft needs more room, and why the 35° bank
limit and the 18 m/s cruise speed together fix the tightest turn TM-1 can fly.
*(Parts 1 and 2)*

**The drag polar** says that an aircraft's drag has two parts that pull in
opposite directions. Profile drag, C_D0, is the cost of pushing a shape through
air; it grows with speed. Induced drag is the cost of making lift — the energy
left behind in the wingtip vortices — and it *falls* as speed rises, because a
faster wing needs a smaller lift coefficient. Adding them:

$$C_D = C_{D0} + \frac{C_L^2}{\pi e AR}$$

The span efficiency e (0.85 for TM-1, an assumption) says how close the wing is
to the ideal elliptical lift distribution. Because the two terms move
oppositely, there is a speed of minimum drag, and it is the reason an aircraft
has a best cruise speed at all. *(Part 1)*

**Battery sizing, and a reserve defined two ways.** This one is worth reading
carefully, because it is an arithmetic trap rather than a physics one. "Keep a
20% reserve" can mean two different things. Sizing the battery as 1.2 × the
mission energy leaves 1 − 1/1.2 = 16.7% at landing, not 20%. To actually land
with a fifth of the battery unused:

$$E_{batt} = \frac{E_{mission}}{1 - 0.20}$$

The difference was 0.42 kg against 0.44 kg of battery. Small — but it was found
only because the requirement had been written down before the calculation.
*(Part 1)*

## 2. How it flies

**Six degrees of freedom.** A rigid body moving freely has exactly six
independent ways to move: three slides (forward/back, left/right, up/down) and
three rotations (roll, pitch, yaw). Nothing else is possible — every motion is
some combination of those six.

A simpler model tracks three, treating the aircraft as a point that always
points where it is going. That is useless for a turn, because the turn *is* a
roll. If the model has no roll, it cannot turn for the right reason, and
anything you conclude about how much room the aircraft needs is guesswork.

Six degrees of freedom costs thirteen numbers at every instant in TM-1: position
(3), velocity in the aircraft's own axes (3), attitude as a quaternion (4), and
rotation rates (3). *(Part 2)*

**Body axes and north-east-down axes.** Two coordinate frames are in play. The
world frame is fixed to the ground — north, east, down. The body frame is bolted
to the aircraft: x out of the nose, y out of the right wing, z down through the
belly. Aerodynamic forces are naturally expressed in body axes (the wing does
not care which way north is); position is naturally expressed in world axes.
Most sign errors in a flight model are a confusion between the two.

**Quaternions.** Attitude can be described by roll, pitch and yaw angles, which
are easy to read — and which break when the nose points straight up, where roll
and yaw become the same rotation and the maths divides by zero. A quaternion is
a four-number description of the same rotation that never has that problem. TM-1
integrates the quaternion and converts to angles only for display. *(Part 2)*

**The rigid-body equations.** Newton's law for the three translations and
Euler's for the three rotations, written in the rotating body frame. With
velocity **v**, rotation rate **ω**, mass m, inertia matrix J, force **F** and
moment **M**:

$$\dot{\mathbf v} = \frac{\mathbf F}{m} - \boldsymbol\omega \times \mathbf v, \qquad \dot{\boldsymbol\omega} = J^{-1}\left(\mathbf M - \boldsymbol\omega \times J\boldsymbol\omega\right)$$

The cross-product terms exist only because the axes themselves rotate with the
aircraft. In a fixed frame they vanish. *(Part 2; Beard and McLain, Ch. 3)*

**Angle of attack and the stall.** The angle of attack α is the angle between
the wing and the air actually flowing over it — not the pitch angle, and not the
climb angle. Lift rises almost linearly with α until the flow separates from the
upper surface, at which point lift drops sharply. TM-1's model stalls at 11.5°,
where the lift coefficient reaches its assumed maximum of 1.2.

$$L = \tfrac{1}{2}\rho V^2 S\, C_L(\alpha)$$

*(Part 2)*

**Load factor** is how many times its own weight the wing is carrying,
n = 1/cos φ in a level turn. At 60° of bank the wing carries double, which is
why the stall speed rises in a turn:

$$V_{stall}(\varphi) = V_{stall,1g}\sqrt{\frac{1}{\cos\varphi}}$$

For TM-1 that is 8.2 m/s wings-level and about 9.1 m/s at 34° of bank — the
reason the safety monitor's low-speed warning moves with bank angle. *(Part 4)*

**Trim** is the set of control positions and throttle that holds steady flight
at a given speed and bank — the aircraft neither accelerating nor rotating. A
trim solver searches for them rather than being told. That makes it a genuine
test: give it a speed and a bank angle, and the turn rate it produces can be
compared with the textbook turn radius. TM-1's flown circle matched the analytic
one to within a millimetre, which is independent evidence that the forces, the
rotations and the integration all agree. *(Part 2)*

**Runge–Kutta integration (RK4).** The equations give the rate of change of the
state; the simulation needs the state itself, so it steps forward in small
increments. The crude way takes the rate at the start of the step and assumes it
holds — error falls only in proportion to step size. RK4 samples the rate four
times across the step and combines them, and its error falls with the *fourth
power* of the step: halve the step and the error drops roughly sixteen-fold.
TM-1 measured 3.9 against a theoretical 4, and at 100 Hz the position error on a
problem with a known answer is 0.0001 mm. *(Part 2)*

**Static margin** is how far the centre of gravity sits ahead of the point where
aerodynamic forces effectively act, as a fraction of the wing chord. It measures
how strongly the aircraft resists being pitched — nose-heavy aircraft are stable
and sluggish, tail-heavy ones are agile and can be uncontrollable.

This is where borrowed coefficients bit. The textbook aircraft TM-1's
coefficients came from has a static margin of about 49%, which is very
nose-heavy. Applied unchanged, TM-1's elevator would have needed −26.6° to reach
the stall angle and it only travels 25° — the aircraft could never have reached
maximum lift. Setting 10%, typical for small UAVs, fixed it. Aerodynamic
coefficients belong to a particular airframe; they are not constants of nature.
*(Part 2)*

## 3. How it controls itself

**Successive loop closure** is the standard way to build a fixed-wing autopilot:
a stack of simple feedback loops, each one producing the command for the loop
inside it.

- course → bank → aileron (to turn, bank; to bank, move the ailerons)
- altitude → pitch → elevator
- airspeed → throttle
- sideslip → rudder, to keep the turn coordinated

Each inner loop is made much faster than the one outside it, so each can be
designed as though the inner one were perfect. That is what makes the problem
tractable: four easy loops instead of one hard multivariable controller.
*(Part 3; Beard and McLain, Ch. 6)*

**Gains derived, not tuned.** The usual approach is to twiddle gains until the
response looks right. Instead, each loop is written as a second-order model whose
coefficients come from the aircraft's own parameters at the cruise trim point,
and the gains follow from a chosen speed of response and damping. For roll:

$$\ddot\varphi = -a_{\varphi1}\,\dot\varphi + a_{\varphi2}\,\delta_a$$

where a<sub>φ1</sub> = 61.8 s⁻¹ is the aircraft's natural roll damping and
a<sub>φ2</sub> = 402 s⁻² the ailerons' authority. Choosing to spend full aileron
(25°) at a 15° bank error gives the gain directly:

$$k_\varphi = \frac{\delta_{a,\max}}{e_{\varphi,\max}} = \frac{25^\circ}{15^\circ} = 1.67$$

The payoff: change the aircraft, regenerate the gains with one command.
*(Part 3)*

**Path following.** Flying to a waypoint is not the same as flying *along a
line*. The guidance law computes a commanded course from the aircraft's
perpendicular distance from the line, e<sub>py</sub>:

$$\chi_c = \chi_q - \chi_\infty \cdot \tfrac{2}{\pi}\arctan\left(k_{path}\, e_{py}\right)$$

Far away, the aircraft converges at χ∞ = 60°; close in, the approach flattens
smoothly onto the line instead of overshooting. For the loiter circle a
feed-forward bank holds the turn without needing a standing error:

$$\varphi_{ff} = \arctan\frac{V^2}{g\rho} = 28.8^\circ$$

*(Part 3; Beard and McLain, Ch. 10)*

**Integral windup, and why integral action is not a free fix.** An integral term
accumulates past error and so removes steady offsets — the textbook reason to
add one. But if the loop saturates during a manoeuvre, the integrator keeps
accumulating error it cannot act on, and discharges it as overshoot afterwards.
Added to TM-1's roll loop to cure a 37° bank against a 35° limit, it made things
worse: 40–43°. A stiffer proportional loop fixed it instead. *(Part 3)*

**The yaw-rate rolling moment.** In a steady turn the aircraft is also yawing,
which makes the outer wing travel faster than the inner one. The outer wing
makes more lift, and the aircraft rolls further into the bank. A proportional
roll loop can only resist this by holding a standing error, which grows roughly
with the inverse square of airspeed — 0.9° at 18 m/s, 1.9° at 12 m/s. The cure
is a feed-forward term computed from the aircraft's own coefficients:

$$\delta_{a,ff} = -\frac{C_{l_r}}{C_{l_{\delta a}}} \cdot \frac{b}{2V}\, r_c, \qquad r_c = \frac{g \sin\varphi_c}{V}$$

*(Part 4)*

## 4. Knowing when to stop

**Predicting a limit rather than measuring it.** A rule like "turn back at 400 m
from home" is simultaneously too strict and too loose. It stops an aircraft
flying *along* the boundary at 450 m, which is perfectly safe, and barely
protects one flying straight out, which needs room to turn. The better question
is: if it began turning home right now, how far out would it get?

$$d_{pred} = d + V\cos\theta \cdot t_{lag} + R_{min}\,(1 - \sin\theta)$$

θ is the angle between the aircraft's course and the outward direction,
t<sub>lag</sub> = 1 s the control response time, and R<sub>min</sub> = 49 m the
tightest turn. Flying straight out, the trigger fires at 433 m and the aircraft
peaks at 491 m against a 500 m limit. Flying along the boundary, nothing is
added and nothing fires. *(Part 4)*

**The low-battery trigger** is the same idea applied to energy: return home when
the energy needed to get back, with a 1.25 safety factor, would start eating
into the reserve.

$$E_{left} - 1.25\, E_{return} \le 0.20\, E_{batt}$$

*(Part 4)*

## 5. Checking a mission before it flies

**The drawn route is not the flown route.** An operator draws straight lines
between waypoints. The aircraft cannot fly them, because it cannot turn inside
its own 49 m radius. At a right-angle corner it swings roughly 50 m past the new
leg before settling back onto it. A planner that checks only the drawn lines
will approve missions that, in flight, bust the range limit or never settle onto
a short leg at all.

So the planner predicts the flown path, running the autopilot's own guidance on
a simplified model — a coordinated turn with a lag on the bank response:

$$\dot\varphi = \frac{\varphi_c - \varphi}{\tau}, \quad \tau = 0.4\ \text{s}, \qquad \dot\chi = \frac{g\tan\varphi}{V}$$

The lag τ was calibrated against the full simulation. Predicted against flown,
the error is within 9.3 m, averaging 1.8 m. *(Part 5)*

**Limits that are derived rather than chosen.** The planner's ceiling is 112 m,
not the legal 120 m, because the safety monitor returns home at 115 m and the
autopilot holds altitude to ±3 m. Its minimum airspeed is 13.7 m/s because at
34° of bank the stall warning is at 11.7 m/s and the monitor keeps 2 m/s above
it. A limit traced back to the limit that causes it cannot drift out of
agreement with it. *(Part 5)*

## 6. The city and the rules

**The Part 107 altitude rule, as written.** The limit is 400 ft (122 m) *above
ground level* — not above sea level, and not above the launch point. And within
400 ft horizontally of a structure, the aircraft may climb to 400 ft above that
structure's top. A flat ceiling is therefore both too strict beside a tower and
too loose over a hillside. Reading the rule as written, rather than as
remembered, changed the planner's behaviour across the whole map. *(Part 6;
14 CFR Part 107)*

**Impact energy** is why flight over uninvolved people is restricted. At cruise
TM-1 carries roughly ½mV² = ½ × 2.5 × 18² ≈ 405 J — more than ten times the
threshold for the categories that do not require a certified aircraft. This is
the number that pushes the mission to watching roads from beside them rather
than above them. *(Part 6)*

**Limit maps on a grid, and which way the error falls.** Buildings, terrain,
airspace and roads are rasterised onto a 10 m grid. Any distance measured on a
grid can be wrong by up to half a cell diagonal:

$$\tfrac{1}{2}\sqrt{10^2 + 10^2} \approx 7\ \text{m}$$

That error is unavoidable. Which direction it falls in is a choice. TM-1 handles
it asymmetrically: the zone demanding extra height is enlarged, and the zone
granting the higher structure-ceiling is shrunk. Both errors push toward caution.
*(Part 6)*

**Knowing which data is weak.** Half of Chicago's buildings in OpenStreetMap
carry no height at all and are assigned an assumed 15 m. Rather than hide that,
every report states how much of the flight path depends on an assumed building
height. *(Part 6)*

## 7. Seeing it

**Gimbal pointing.** To aim a camera at a point on the ground, take the line of
sight in world axes, rotate it into the aircraft's body axes, and read the pan
and tilt angles off directly:

```python
d_b  = r_body_to_ned.T @ d_n                      # line of sight in body axes
pan  = atan2(d_b[1], d_b[0])                      # right of the nose is positive
tilt = atan2(d_b[2], hypot(d_b[0], d_b[1]))       # below the body plane is positive
```

Both are then clamped to what the gimbal can physically reach: tilt −10° to 90°,
pan ±180°. That clamp has consequences — in a steep turn away from a distant
target, the target rises above the −10° limit and the camera simply cannot see
it. *(Part 7)*

**Camera footprint.** Projecting the four image corners onto the ground gives
the patch the camera sees. Straight down from height h with a horizontal field
of view θ, the width is 2h·tan(θ/2): from 100 m with a 60° field of view, 115.5 m.
The Phase 0 estimate was 115 m. *(Part 7)*

**Remote ID.** US rules (14 CFR Part 89) require most drones to broadcast
identity, position, altitude, velocity, a time mark, emergency status and the
operator's position. TM-1 writes these fields into every telemetry record using
a placeholder identity and a simulated clock. Nothing is transmitted. *(Part 7)*

## 8. What the project has taught me

Collected from the end of each article, because these are the parts I expect to
reuse on work that has nothing to do with aircraft.

- **Write the requirement before the arithmetic.** The 20%-reserve error was
  caught only because the words existed before the calculation did.
- **A check that never fails needs a test that makes it fail.** The planner's
  first turn check passed everything, for a reason that was obvious in
  retrospect: at the moment of switching legs, the aircraft is by definition on
  the new leg.
- **Test the whole set, not the nominal case.** The bank-limit defect appeared
  only on the slower flights.
- **Integral action is not a general fix.** In a loop that saturates during a
  manoeuvre, it stores up overshoot.
- **A limit should be predicted, not measured.** What matters is where the turn
  home will end, not where the aircraft is now.
- **Look at the outputs, not only the test results.** Two of the three defects in
  one milestone were found by watching a screen recording, not by a test.
- **Put unavoidable errors on the safe side.** A 7 m grid error cannot be
  removed; which way it falls is a decision.
- **A passing test shows the model is consistent with its parameters.** It says
  nothing about whether those parameters describe a real aircraft. Of TM-1's
  assumed values, 12 are checked by a requirement-level test, 21 are traced to a
  published reference, and 11 — among them the avionics power and the battery's
  specific energy — a simulation cannot verify at all.
- **A drawing that cannot affect the physics should still agree with it.** The
  first aircraft model used a symmetric wing section, which makes no lift at zero
  angle of attack, while the flight model's lift coefficient at zero angle was
  0.23. It changed no result. It was still wrong.

## References

The sources the series actually draws on:

- **Beard, R. W. and McLain, T. W.** — *Small Unmanned Aircraft: Theory and
  Practice*, Princeton University Press. Ch. 3 (rigid-body motion), Ch. 4
  (aerodynamic coefficients), Ch. 6 (autopilot loop closure), Ch. 10 (path
  following). The backbone of the flight model, the autopilot and the guidance.
- **Raymer, D. P.** — *Aircraft Design: A Conceptual Approach*, AIAA. Section 6.4
  for tail sizing by volume coefficient; first-order sizing relations.
- **14 CFR Part 107** — the US small-UAS operating rules: altitude, operations
  over people, controlled airspace.
- **14 CFR Part 89** — Remote ID.
- **OpenStreetMap** (buildings, roads, gathering places, via the Overpass API),
  **USGS 3DEP** (terrain), and the **FAA's open airspace data**.

Worth reading alongside them, though the project does not cite them directly:

- **Stevens, B. L., Lewis, F. L. and Johnson, E. N.** — *Aircraft Control and
  Simulation*. A heavier treatment of the same rigid-body and control material.
- **Anderson, J. D.** — *Fundamentals of Aerodynamics*. Where the lift and drag
  coefficients come from in the first place.

---

*TM-1 is a simulation. No aircraft was built or flown, and nothing in this
project describes a real-world flight.*
