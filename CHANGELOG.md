# Changelog

All notable changes to this project will be documented here.

## [Unreleased]

(None.)

## [1.0.0] - 2026-02-24

- **Release v1.0.0** — repozytorium kanoniczne [VERTYXNEXUSEIL/PCA-SPEC](https://github.com/VERTYXNEXUSEIL/PCA-SPEC); TSVNE wycofane. Dokumentacja (README, README_EN, AGENTS.md), szablon przekierowania w `docs/README-for-TSVNE-repo.md`.
- **Fix:** `reference/python/pyproject.toml` — jedna lista `dependencies` (jsonschema, referencing).
- **Fix:** `reference/python/pca/schemas.py` — jedna definicja `validate`, walidator formatu `date-time` (RFC 3339), import z jsonschema.
- **Fix:** Usunięto lokalny pakiet `jsonschema`; CLI używa `legacy_schema_stub`; `pca.schemas` używa zainstalowanego jsonschema.
- **Fix:** `reference/cli/pca_cli.py` — import z `legacy_schema_stub`, ścieżka do `reference/python`.
- **Fix:** `schemas/pc.schema.json` — `merkle_root` i `metadata` mogą być `null` (T7).
- **Fix:** `tools/doctor.py` — ASCII zamiast Unicode, `python -m pytest`/`ruff`, UTF-8 na Windows.
- **Docs:** AGENTS.md, rozszerzony README z tabelą i linkami, `docs/REPO-PROTECTION.md` (zalecenia zabezpieczenia repo).
- Initial normative PCA/CAE specification, schemas, test vectors T1–T13, reference implementation (v1.0 disclosure 2026-02-17).
