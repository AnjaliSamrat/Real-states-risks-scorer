# Project Roadmap (Real Estate Risk Scorer)

This is an India-first roadmap for making the product feel *real*: accurate location handling, credible data sources, transparent scoring, and repeatable validation.

## Product Goals

- **Trust**: Every score must be explainable (“why”) and attributable (“source + granularity + timestamp”).
- **Usefulness**: Outputs should be actionable for a buyer/investor (not just a number).
- **Reliability**: Works in dev and production without flaky external dependencies.
- **Validation**: Regression tests prevent accidental score drift.

## Scope (MVP v1)

- Input: Address search (OSM) + optional lat/lon
- Output: Overall risk score + 4 category scores (climate/crime/economic/infrastructure)
- Explainability: Top drivers + points per category
- Provenance: Source + granularity + units + generated timestamp
- India focus: Real data where feasible (NCRB/data.gov.in, NASA POWER, OSM Overpass)

## Current Status

### Done

- Address search UX with explicit selection and correct lat/lon
- Dashboard “Analyze Risk” flow (POST `/api/risk-assessment/analyze`)
- Risk scoring with deterministic fallback behavior
- Real-data plumbing (with graceful fallbacks):
	- Crime: optional NCRB via data.gov.in (State/UT level)
	- Climate: NASA POWER climatology signal
	- Infrastructure: OSM Overpass amenity counts (best-effort)
	- Economic: optional data.gov.in provider plumbing (dataset mapping)
- Explainability + provenance surfaced in UI (Dashboard + Property Detail)
- **Validation started**: India benchmark regression suite (offline deterministic) + baseline table in `docs/BENCHMARKS.md`

## Roadmap by Milestone

### Milestone 1 — “Credible MVP” (ship-ready)

**Goal**: Product works end-to-end and is transparent, even on fallbacks.

**Deliverables**
- Stable UX: address → map → analyze → results (no 404 spam, no hidden dropdowns)
- Explainability: “Why this score?” shows top drivers and points
- Provenance: source/granularity/unit/year shown consistently
- Benchmarks: baseline file + regression tests pass locally

**Success Criteria**
- Same address produces stable output across runs (offline + online)
- UI never shows empty/unknown without a clear reason

**Status**: Done

### Milestone 2 — “Data Quality Upgrade” (India realism)

**Goal**: Improve realism without adding new UI complexity.

**Deliverables**
- Economic: select 1–2 official datasets on data.gov.in and map fields (median income / unemployment / poverty)
- Crime: expand to include a second dataset if available (e.g., property crime proxy) OR clearly label limitation
- Climate: add 1–2 India-relevant hazard heuristics (e.g., heat stress indicator from climatology)

**Success Criteria**
- For India cities, category scores vary meaningfully and align with intuitive expectations
- Provenance indicates when a category is “demo” vs “real”

**Status**: Next

### Milestone 3 — “Calibration & Benchmarks” (prevent score drift)

**Goal**: Make scoring stable and defensible.

**Deliverables**
- Expand benchmark set (10–20 → 30–50) including Tier 2/3 cities and coastal/inland variety
- Add a “ranking stability” test (not just exact values) to allow controlled evolution
- Add a lightweight script/report that compares current results vs baseline (delta report)

**Success Criteria**
- A scoring change requires an intentional baseline update
- CI-style run stays fast and offline by default

**Status**: In progress

### Milestone 4 — “Production Hardening”

**Goal**: Reliable performance and low operational risk.

**Deliverables**
- Caching strategy documented for Nominatim/Overpass (or hosted alternatives)
- Timeouts + retries + rate-limit backoff where appropriate
- Observability: basic logging for provider failures and fallbacks

**Success Criteria**
- App remains usable when public APIs throttle
- Clear logs show which provider failed and why

**Status**: Later

## Engineering Backlog (Now / Next / Later)

### Now (high ROI, low risk)

- Expand benchmark dataset and ensure it covers flood/coastal + Himalayan quake band
- Add a delta report that highlights score changes between baselines
- Document `OFFLINE_MODE` usage in docs (tests + scripts)

### Next

- Choose and lock an India economic dataset + field mapping (data.gov.in)
- Add “as-of year” and “unit” consistently to all category metas
- Add an internal “confidence” signal per category (based on granularity + real/demo)

### Later

- District/city-level crime if reliable dataset is available
- India-specific flood hazard layers (replace heuristic zones)
- Official seismic zoning (zone II–V mapping)
- Better health/schools quality metrics (official open datasets)
- Model-learned calibration (weights learned with explainable output)

## Notes / Operating Principles

- Public APIs (Nominatim/Overpass) are rate-limited; production should use caching and/or paid/hosted instances.
- “Real” does not mean “perfect”—it means **traceable sources + correct units + honest granularity**.
- Benchmarks run offline by default so validation is fast and deterministic.
