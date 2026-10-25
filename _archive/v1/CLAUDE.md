# CLAUDE.md — Project Context & Tracking

This file helps Claude Code maintain context across sessions for the `anandrams.github.io` portfolio site.

---

## Repository Overview

- **Type:** Personal portfolio website (Jekyll-based static site)
- **Hosting:** GitHub Pages (`anandrams.github.io`)
- **Theme:** Custom Toha-inspired layout with dark/light mode
- **Key files:**
  - `index.md` — Home / landing page
  - `projects.md` — Project cards grid
  - `experience.md` — Work experience timeline
  - `education.md` — Education section
  - `_config.yml` — Jekyll site configuration
  - `_layouts/` — Page layout templates
  - `assets/` — Images, logos, CSS, fonts
  - `projects/` — Individual project detail pages (Markdown + inline HTML)

---

## Project: HSD Load Body Structural Design Benchmarking

**File:** `projects/hsd-load-body.md`
**Card in:** `projects.md` (legacy section)

### Key Details
- **Type:** Lean Six Sigma Green Belt (LSSGB) project using APS (Advanced Problem Solving) methodology
- **Company:** Ashok Leyland CQ-NPQ
- **Product:** ICV BOSS HSD (High Side Deck) Load Body
- **Scope:** BOSS ICV HSD Load Body only (Haulage & Tipper excluded)
- **Methodology:** DMADV / PDCA — Problem → Observation → Analysis → Action → Check → Standardize → Conclude

### Assets
All images are in `assets/LoadBody/`:
- `Fig1CompetitorTrucks.png` — Benchmark targets (Tata, Eicher, BharatBenz, AL)
- `Fig2LoadBodyStructure.png` — Load body component overview
- `Fig3-6CustomerUsage1-4.png` — Field visit / customer usage patterns
- `Fig7KanoModel.png` — Kano Model classification results
- `Fig8CustomerNeeds.png` — Customer needs analysis
- `Fig9Benchmarking.png` — Labeled component diagram
- `Fig10StructuralAnalysis.png` — Pillar cross-section comparison
- `Fig11StructuralStrength.png` — F = E × I bending stiffness
- `Fig12MOI.png` — Moment of Inertia profiles
- `Fig13EvaluationTracker.png` — Improvement ideas evaluation tracker
- `Fig14APSMethod.png` — APS methodology diagram
- `Fig15HSD.jpeg` — **Card image** — Final HSD Load Body product photo

### Privacy / Sanitization Rules
The following information has been **intentionally removed** from this project page and must NOT be re-added:
- Specific dates (project timeline dates, milestone dates)
- Personal names of team members (CFT members)
- Project sponsor name
- Internal project code numbers

### Key Results
- **18%** warranty failure reduction through structural design improvements
- **7** competitors benchmarked (physical teardown)
- **107** features analyzed across Kano categories
- **4** potential competitive differentiators identified

---

## Project: Disc Brake Rotor Vane Optimization

**File:** `projects/brake-rotor.md`
**Assets:** `assets/DiscBrake/` (Fig1–Fig6, `brake-rotor-cfd.png`, `DiscBrakeProjectReport.pdf`)

### Notes
- `brake-rotor-cfd.png` is the **hero/title image** — CFD velocity overlay on the rotor
- Hero image path: `/assets/DiscBrake/brake-rotor-cfd.png`

---

## Project: Hybrid Truck Power-Split Control

**File:** `projects/hybrid-truck-control.md`
**Assets:** `assets/Hybrid/` (Fig1–Fig5, `Powersplit.png`, `THS_Powersplit_Reference.pdf`)

### Key Details
- **Type:** University of Michigan graduate course project
- **Instructor / Paper Author:** Prof. Huei Peng
- **Scope:** The project closely replicates the methodology and control strategies from Prof. Peng's THS power-split reference paper
- **Title image:** `Powersplit.png` — THS planetary gear / power-split architecture diagram
- **Reference PDF:** `THS_Powersplit_Reference.pdf` — Prof. Peng's paper on THS power-split control

### Privacy / Sanitization Rules
- Prof. Peng's name is **intentionally kept** — it is an academic citation, not a personal team member
- No other personal names should be added

---

## Project: SAE India aSOP

**File:** `projects/sae-india-asop.md` (renamed from `reverse-eng.md`)
**Assets:** `assets/SAEIndia/` (`aSOP.png`, `TataACE.png`)

### Key Details
- **Program:** SAE India Automotive Student Orientation Program (aSOP)
- **Industry Partner:** WABCO India Pvt. Ltd.
- **6 modules:** QRV RE → Market Analysis → Tata Ace LDT teardown → Vehicle Concept → Sub-system Definition → Design & Prototype
- **Card image:** `aSOP.png` (program roadmap overview)

---

## Asset Folder Map

| Folder | Project |
|---|---|
| `assets/LoadBody/` | HSD Load Body (hsd-load-body.md) |
| `assets/DiscBrake/` | Disc Brake Rotor (brake-rotor.md) |
| `assets/Hybrid/` | Hybrid Truck Control (hybrid-truck-control.md) |
| `assets/SAEIndia/` | SAE India aSOP (sae-india-asop.md) |

---

## Development Notes

- **Working branch:** `main` (user merges claude/* PRs to main; changes may be committed directly to main)
- **Claude PR branch convention:** `claude/<description>-<5-char-id>` — push to this, user merges to main
- **Push target for PRs:** `origin/claude/sanitize-project-data-QJEFb`

---

## Design System Notes

- CSS variables: `--primary-color`, `--bg-primary`, `--bg-secondary`, `--text-primary`, `--text-secondary`, `--border-color`, `--radius-md`, `--radius-lg`, `--shadow-md`, `--shadow-lg`
- Project badge color for LSSGB: `linear-gradient(135deg, #27ae60, #1e8449)` (green)
- Standard project badge: `rgba(255,255,255,0.2)` (white translucent on dark hero)
- Legacy project cards use class `project-card legacy`
- Featured project cards use class `project-card featured`

---

## Completed Tasks

- [x] Removed all dates and personal names from `hsd-load-body.md`
- [x] Updated project badge to "Lean Six Sigma Green Belt Project" with green styling
- [x] Added LSSGB highlight section and Evaluation Tracker section
- [x] Changed HSD card image to `Fig15HSD.jpeg`
- [x] Rewrote `reverse-eng.md` → `sae-india-asop.md` with correct 6-module aSOP content (WABCO India, no dates/names)
- [x] Renamed `assets/LCV/` → `assets/SAEIndia/`; removed old `assets/LCV/` folder
- [x] Updated `projects.md` SAE India card — new link, image, title, description, tags
- [x] Updated `brake-rotor.md` hero image path → `/assets/DiscBrake/brake-rotor-cfd.png`
- [x] Added `Powersplit.png` as hero/title image to `hybrid-truck-control.md`
- [x] Added "Course Context & Reference" section to `hybrid-truck-control.md` with THS PDF download
- [x] Removed GKN Driveline internship from experience.md
- [x] Updated Siemens titles to Engineering Services Engineer / Senior Engineering Services Engineer
- [x] Removed stats cards (9+ years, $10M+, etc.) from About section

---

## Research & Publication Ideas

**Context:**
- Target roles: Senior/Staff Systems Engineer at OEMs and software-leaning companies (Waymo, Lucid, Rivian)
- Key constraint: no client data, no permission needed, buildable independently
- Available tools: MATLAB/Simulink, Amesim, Polarion, Rhapsody, System Modeling Workbench, System Architect, System Analyst
- Existing built work: Polarion-Amesim connector, Simulink MIL testing framework, SA/Analyst testing framework, SA-Polarion connector

**Guiding principle:** One coherent reference system project (EV TMS) that produces multiple papers and a live interview demo. Do not scatter across unrelated systems.

**Reference System: EV Thermal Management System (TMS)**
- Chosen over AWD (already have real Bronco story) and BMS (do as phase 2)
- Public reference architectures exist; Amesim is the natural tool for 1D thermal-fluid modeling
- Direct relevance to Lucid/Rivian interview conversations
- Controls problem: multi-mode switching, predictive thermal control

### Idea List

| # | Title | Core contribution | Tools | Target venue | Status |
|---|---|---|---|---|---|
| 1 | MIL Testing Framework for ASPICE Compliance | Architecture + open-source tool that auto-generates ASPICE work products | Simulink, Polarion | SAE Technical Paper / IEEE ICSTW | Existing work to package |
| 2 | Bidirectional Requirements-Simulation Traceability | Systematic method + connector for live traceability: requirements ↔ model ↔ test results | Polarion, Amesim, SA | MODELSWARD / INCOSE IS | Existing connectors to package |
| 3 | Full-stack Digital Twin Reference (EV TMS) | Reproducible end-to-end MBSE+MBD workflow on open reference system | Rhapsody/SMW + Amesim + Simulink | IEEE Access / IEEE Systems Journal | Main project |
| 4 | Amesim-Simulink Co-simulation Methodology | Best practices + numerical accuracy benchmarks, open reference architecture | Amesim, Simulink, FMI/FMU | Simulation Modelling Practice and Theory | Spin-off from Idea 3 |
| 5 | SysML Model → Auto-generate MIL Test Cases | Pipe Rhapsody/SMW model into existing MIL test framework | Rhapsody/SMW, Simulink, Polarion | INCOSE IS / MODELSWARD | Connects Ideas 1+3 |
| 6 | Executable SysML for Early V&V | Validate system behavior at architecture level before plant model exists | Rhapsody | INCOSE IS | Spin-off from Idea 3 |
| 7 | HARA Derivation from SysML Functional Architecture | Semi-formal HARA from Rhapsody model instead of spreadsheet | Rhapsody | SAE Technical Paper | Add if targeting safety-critical roles |

### Sequencing
1. **Start:** Idea 3 (EV TMS reference system) — forces deep tool learning, generates all others
2. **Quick wins from existing work:** Ideas 1 and 2 — package what's already built
3. **Natural spin-offs as Idea 3 progresses:** Ideas 4, 5, 6
4. **Optional:** Idea 7 if targeting ISO 26262 / safety-critical openings

### Interview alignment
- **Demo artifact:** Live EV TMS model stack (Idea 3) — most candidates have nothing to show
- **Senior roles:** Demo + methodology story is sufficient
- **Staff roles:** Published methodology (Ideas 1/2/3) signals above-delivery level
