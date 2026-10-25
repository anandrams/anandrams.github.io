---
title: "A six-degree-of-freedom flight model, checked against hand calculations"
description: "Milestone M0 of TM-1, a simulated fixed-wing UAV: rigid-body dynamics, aerodynamics with stall, electric thrust, an RK4 integrator and a trim solver, each verified against a result that can be derived on paper."
date: 2026-10-17 02:00:00 +0000
part: 2
phase: "M0"
kind: Article
series: "TM-1 UAV"
series_slug: tm1
project: "TM-1 UAV"
project_url: /projects/tm1/
theme: "Flight Dynamics"
image: /assets/articles/tm1/media/m0/m0_turn.jpg
image_alt: "A plot of the aircraft turning."
simnote: "TM-1 UAV, milestone M0. Simulation only: no real aircraft was built or flown."
tags:
  - "UAV"
  - "flight dynamics"
  - "simulation"
  - "numerical methods"
  - "verification"
math: true
# Add corrections here; the article shows them, dated.
# corrections:
#   - date: 2026-11-02
#     note: "What changed, and why."
---

TM-1 is a 2.5 kg fixed-wing UAV that I sized in the previous phase for a traffic-monitoring mission over Chicago. This milestone makes it fly in software: a six-degree-of-freedom (6-DOF) flight model, written from the equations rather than taken from an existing simulator.

Writing the equations is the easier half. The harder question is how to show that the result is right. Each part of the model was therefore checked against a result that can be derived by hand.

| Check | Model | Hand calculation | Allowed |
|---|---|---|---|
| 1 g stall speed | 8.207 m/s | 8.244 m/s (−0.44%) | ±2% |
| Turn radius, 18 m/s and 35° bank | 47.169 m | 47.168 m | ±2% |
| Total energy with drag off, 60 s glide | constant to 9 × 10⁻¹⁰ | constant | 10⁻³ |
| Integrator order | 3.9 | 4 | ≈ 4 |
| Steady flight found from 15 to 22 m/s | every speed | — | — |

## 1. What the model contains

**State.** Thirteen numbers describe the aircraft at any instant: position in north-east-down axes (3), velocity in the aircraft's own body axes (3), attitude as a unit quaternion (4), and rotation rates (3).

**Attitude as a quaternion.** Roll, pitch and yaw angles are easy to read but become undefined when the nose points straight up. A quaternion never does. The model integrates the quaternion and converts to angles only for display.

**Rigid-body motion.** Newton's and Euler's laws, written in the rotating body axes (Beard and McLain, *Small Unmanned Aircraft*, Chapter 3). With velocity v, rotation rate ω, mass m and inertia matrix J:

$$\dot{\mathbf v} = \frac{\mathbf F}{m} - \boldsymbol\omega \times \mathbf v, \qquad \dot{\boldsymbol\omega} = J^{-1}\left(\mathbf M - \boldsymbol\omega \times J\boldsymbol\omega\right)$$

The cross-product terms appear because the axes themselves rotate with the aircraft.

**Aerodynamics.** Lift, drag and the three moments come from coefficients (Beard and McLain, Chapter 4). Lift rises linearly with angle of attack and then breaks away at the stall, here at C_Lmax = 1.2:

$$L = \tfrac{1}{2}\rho V^2 S\, C_L(\alpha)$$

![Lift and drag coefficients against angle of attack](/assets/articles/tm1/media/m0/m0_lift_drag.jpg)
*Lift and drag coefficients against angle of attack. The stall is at 11.5°, where C_L reaches 1.2.*

**Propulsion.** Thrust is limited by the motor's power, with the same propeller efficiency as the sizing, so the flight model and the sizing agree on cruise power.

**Integration.** A fourth-order Runge–Kutta step at 100 Hz advances the state. A trim solver finds the control positions for steady flight, level or turning.

## 2. Checks that are not circular

A check is only useful if the model is not simply being compared with itself. Two examples:

**The turn.** The trim solver is given a speed and a bank angle and asked for steady flight. It is not told the turn rate. It finds the controls and the turn rate by balancing forces and moments. The flown circle then matches the textbook radius R = V²/(g tan φ) to within a millimetre. That is independent evidence that the force model, the rotation and the integration fit together.

![Flown turn on top of the analytic circle](/assets/articles/tm1/media/m0/m0_turn.jpg)
*The 6-DOF model flying a 35° bank turn at 18 m/s with trimmed controls (blue), on top of the analytic circle (grey).*

**Energy.** With drag switched off, the aircraft can only exchange speed for height: the sum of kinetic and potential energy must stay constant. Over a 60 s glide the aircraft climbs 5.6 m and slows down, and the total changes by less than one part in a billion. A sign error in a force, or a frame mix-up, would show up here at once.

![Kinetic and potential energy in a drag-free glide](/assets/articles/tm1/media/m0/m0_energy.jpg)
*Drag-free glide: kinetic energy falls as potential energy rises; the total (black) stays constant.*

**The integrator.** On a problem with a known exact solution, halving the step reduces the error by a factor of about 2⁴, as a fourth-order method should. At 100 Hz the position error is 0.0001 mm.

## 3. A coefficient that did not transfer

The aerodynamic coefficients come from a well-documented textbook aircraft. I did not take them from memory: the values were checked against the authors' published simulation code, and two differed from what I would have assumed.

One property did not transfer well: pitch stability. The textbook aircraft is very nose-heavy, with a static margin of about 49% of the chord. Applied to TM-1, the elevator would need −26.6° to reach the stall angle, but it only moves 25°. The aircraft could never reach its maximum lift, and the stall check would fail by 4.4%.

I set a static margin of 10%, typical for small UAVs, and recorded it as a design decision that applies to this weight class only. Coefficients are not universal constants; they belong to a particular airframe.

## 4. What the checks do and do not show

These checks show that the model is consistent: it reproduces the stall and turn relations it is built on, and it conserves energy. They do not show that a real TM-1 wing would reach C_Lmax = 1.2, or that the borrowed roll and yaw coefficients describe this aircraft. Those remain recorded assumptions.

Every module has an explanation page with its equations, their source and their assumptions. The milestone ended with 64 automated tests, each named after the requirement it checks, and 99% test coverage of the flight model.

## Next

The next milestone adds an autopilot and a mission manager, so the aircraft can fly a mission on its own, and the first way to see a flight.

---

*TM-1 is a simulation. No aircraft was built or flown, and nothing in this project describes a real-world flight. Figures were generated from the project's own flight model.*
