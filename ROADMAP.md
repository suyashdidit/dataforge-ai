# DataForge AI Roadmap

## Completed milestones

- [x] CLI wrapper with `setup-demo` and `analyze-change`
- [x] Installable entrypoint via `dataforge`
- [x] dbt project scanner with model metadata and lineage detection
- [x] Git change analyzer to detect changed dbt models
- [x] Impact analysis engine with downstream exposure and risk scoring
- [x] Markdown report generation for readable PR comments
- [x] GitHub Actions workflow to post reports on pull requests
- [x] Demo project fixtures and integration tests
- [x] End-to-end developer experience documentation

## Near-term planned milestones

- [ ] enrich lineagedb analysis with multi-package dbt support
- [ ] add automatic tests/documentation coverage detection in dbt metadata
- [ ] improve GitHub Actions comment deduplication and report freshness
- [ ] support optional JSON output for API consumption
- [ ] add a lightweight web dashboard for impact summaries

## Longer-term vision

- [ ] integrate with data quality platforms and warehouse metadata stores
- [ ] provide a visual drift report for data model changes
- [ ] add configurable risk policies and custom scoring rules
- [ ] support native dbt Cloud and enterprise workflows
