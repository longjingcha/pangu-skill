# pangu-skill Release Notes v0.1.0

## Overview

This release establishes the first publishable version of `pangu-skill` as a packaged, installable AI skill distillation tool.

## What’s Included

- Unified skill schema (`skill_schema.yaml`)
- Static `SKILL.md` output template
- Configurable distillation pipeline
- Multi-material comparison
- Conflict detection
- Structured evidence output
- CLI package entrypoint (`pangu-skill`)
- Module entrypoint (`python -m pangu_skill`)
- Example materials and example schema
- Basic unit tests for exporter and CLI
- `pyproject.toml` packaging configuration

## Primary Commands

```bash
pangu-skill validate --schema examples/example_skill.yaml
pangu-skill export --schema examples/example_skill.yaml --output generated/SKILL.md
pangu-skill distill \
  --input examples/raw_material_1.txt examples/raw_material_2.txt \
  --schema-output generated/distilled_skill.yaml \
  --markdown-output generated/SKILL.md \
  --name "Generated Skill" \
  --skill-id "pangu.generated.001" \
  --config distill_config.yaml
```

## Release Checklist

Before publishing `v0.1.0`, verify the following:

### Functional Checks

- [ ] `python -m unittest discover -s tests` passes
- [ ] `pangu-skill validate --schema examples/example_skill.yaml` succeeds
- [ ] `pangu-skill export --schema examples/example_skill.yaml --output generated/SKILL.md` succeeds
- [ ] `pangu-skill distill` succeeds end to end on the example inputs
- [ ] Generated YAML is valid and includes `validation.evidence` and `validation.conflicts`
- [ ] Generated Markdown renders correctly and includes all major sections

### Packaging Checks

- [ ] `pyproject.toml` metadata is correct
- [ ] Console script entry point works after install
- [ ] `python -m pangu_skill` works from the source tree
- [ ] Dependencies are limited to required runtime packages
- [ ] Package layout follows `src/` structure

### Documentation Checks

- [ ] `README.md` matches the current CLI and package entrypoints
- [ ] `RELEASE.md` reflects the shipped features
- [ ] Example commands are accurate and runnable
- [ ] The schema documentation matches the current YAML structure

### Artifact Checks

- [ ] Generated files are not committed unless intentionally released
- [ ] `generated/` output is ignored or treated as disposable
- [ ] Example inputs are present and readable
- [ ] No stale references remain in docs or code

## Test Plan

Run the full test suite before packaging:

```bash
python -m unittest discover -s tests
```

Recommended pre-release checks:

1. Run exporter tests
2. Run CLI smoke tests
3. Run a sample distillation end to end
4. Verify generated YAML and Markdown artifacts
5. Confirm packaging metadata in `pyproject.toml`

## Release Notes

`pangu-skill v0.1.0` is the first publishable release of the project. It introduces a complete but lightweight pipeline for turning raw materials into structured skill artifacts. The release includes a unified skill schema, a Markdown export template, a configurable distillation engine, and a packaged CLI interface for validation, export, and distillation workflows.

This version focuses on establishing the foundation:

- a stable schema for distilled skills
- a repeatable export pipeline
- evidence-backed field generation
- conflict detection for competing themes
- a usable command-line interface
- a package-ready project layout

## Release Announcement Copy

`pangu-skill v0.1.0` is now available.

This first release turns raw materials into structured skill artifacts through a configurable distillation pipeline, a unified schema, and a packaged CLI.

What’s new:

- Distill raw notes into structured skill schemas
- Export schemas to readable `SKILL.md` documents
- Compare multiple materials and surface conflicts
- Track evidence behind the extracted claims
- Validate and package the tool as a standard Python project

Install and try it:

```bash
pip install -r requirements.txt
pangu-skill validate --schema examples/example_skill.yaml
pangu-skill export --schema examples/example_skill.yaml --output generated/SKILL.md
```

For a full distillation run:

```bash
pangu-skill distill \
  --input examples/raw_material_1.txt examples/raw_material_2.txt \
  --schema-output generated/distilled_skill.yaml \
  --markdown-output generated/SKILL.md \
  --name "Generated Skill" \
  --skill-id "pangu.generated.001" \
  --config distill_config.yaml
```

## Packaging Notes

- Python >= 3.8
- Dependency: `PyYAML>=6.0.2`
- Console script: `pangu-skill`
- Package source root: `src/`

## Known Scope

This version is intentionally lightweight and heuristic-driven. It is designed as a strong foundation for future improvements in:

- clustering
- better conflict resolution
- source weighting
- feedback loops
- interactive review workflows

## Version

- Release: `v0.1.0`
- Status: release candidate
