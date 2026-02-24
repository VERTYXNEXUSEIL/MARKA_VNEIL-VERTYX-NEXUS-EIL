# Kontekst repozytorium PCA-SPEC (dla asystentów AI i współtwórców)

Ten plik opisuje strukturę i konwencje repozytorium, aby ułatwić naprawy, rozbudowę i spójność z normą.

## Czym jest PCA/CAE

- **PCA** = Proof-Carrying Autonomy  
- **CAE** = Certified Agentic Execution  

Standard techniczny (neutralny produktowo) do **deterministycznego, certyfikowalnego wykonywania działań autonomicznych**: planowanie jest opatrzone dowodem (Plan Certificate, PC), a wykonawca weryfikuje integralność, ograniczenia i czas ważności przed wykonaniem. W razie niezgodności zwracany jest deterministyczny kod przyczyny (reason code).

## Struktura repozytorium

| Ścieżka | Zawartość |
|--------|-----------|
| `spec/` | Dokumenty normatywne (EN): PCA-SPEC-v1.0.md, PCA-RC-v1.md, PCA-TEST-v1.md, PCA-GLOSSARY.md, PCA-FAQ.md |
| `pl/spec/` | Tłumaczenia specyfikacji na język polski (identyfikatory techniczne bez zmian) |
| `schemas/` | Schematy JSON (pc.schema.json, action_ir.schema.json, constraints.schema.json, evidence_capsule.schema.json) |
| `test-vectors/vectors-v1/` | Wektory testowe T1–T13 (JSON); używane przez doctor i testy |
| `reference/python/` | Implementacja referencyjna w Pythonie (pca.*), wymaga `pip install -e .[dev]` z tego katalogu |
| `reference/cli/` | Skrypt CLI `pca_cli.py` |
| `tools/doctor.py` | Skrypt zdrowia: walidacja schematów na wektorach, uruchomienie wektorów, pytest, ruff, opcjonalnie node T13 |
| `.github/workflows/` | CI (doctor), release, provenance, proof-html, auto-assign |

## Kluczowe pojęcia (zgodnie ze specyfikacją)

- **Plan Certificate (PC)** – obiekt łączący dowód planowania z krokami wykonania; zawiera `constraints_version_id`, `constraints_digest`, `effective_time`, `steps` (Action IR).
- **Domain-separated hashing** – etykiety: `STATEv1`, `GOALv1`, `CONSv1`, `POLv1`, `CFGv1`, `STEPv1`, `PLANv1`, `PCv1`, `AIRv1`; hasz SHA-256 nad `label || ":" || canonical_json`.
- **Reason codes** – stabilne identyfikatory z PCA-RC-v1 (np. `RC_OK`, `RC_TOCTOU`, `INTEGRITY_MISMATCH`). Nie zmieniać semantyki po publikacji.
- **Profile zgodności**: Bronze (linear plan digest, mandatory checks), Silver (+ Merkle, T1–T10), Gold (+ OOD tripwire, disclosure budget, T1–T13).

## Jak uruchomić testy i doctor

Z katalogu głównego repozytorium:

```bash
cd reference/python
python -m pip install -e .[dev]
pytest -q
```

Z katalogu głównego (wymaga zainstalowanego pakietu z `reference/python`):

```bash
python tools/doctor.py
```

Doctor wykonuje: validate-schemas (wektory vs schematy), run-vectors (execute_certified vs expected), pytest, ruff; opcjonalnie node T13 jeśli istnieje `reference/node/package.json` z skryptem `t13:check`.

## Konwencje przy zmianach

1. **Specyfikacja** (`spec/`, `pl/spec/`): zachować język normatywny (MUST/SHOULD/MAY); nie zmieniać reason code IDs ani etykiet haszowania w tłumaczeniach.
2. **Schematy**: zmiany w `schemas/*.schema.json` muszą być zgodne z wektorami w `test-vectors/vectors-v1/` i z opisem w PCA-SPEC-v1.0.
3. **Python**: kod w `reference/python/pca/` – formatowanie ruff (line-length 100), testy w `pca/tests/` i `reference/python/tests/`; zależności tylko w `reference/python/pyproject.toml` (jedna lista `dependencies`).
4. **Changelog**: aktualizować `CHANGELOG.md` w sekcji **Unreleased** przy istotnych zmianach.

## Częste problemy

- **pip install fails (Cannot overwrite a value)** – w `reference/python/pyproject.toml` nie może być dwóch kluczy `dependencies`; połączyć w jedną listę.
- **Schema validation / import errors** – `pca.schemas` zakłada, że katalog `schemas/` jest w `Path(__file__).resolve().parents[3] / "schemas"` (trzy poziomy nad `pca/schemas.py` = katalog główny repo).
- **Doctor uruchamiany z niewłaściwego katalogu** – doctor musi być wywoływany z katalogu głównego repozytorium (gdzie są `tools/`, `test-vectors/`, `reference/`).

## Dokumentacja użytkownika

- Wejście: `README.md` (krótkie, linki do PL/EN).
- Pełny opis EN: `README_EN.md`.
- Polska: `pl/README_PL.md`, indeks `pl/docs/index.md`.

## Repozytorium kanoniczne i wycofanie TSVNE

- **Kanoniczne repo:** [https://github.com/VERTYXNEXUSEIL/PCA-SPEC](https://github.com/VERTYXNEXUSEIL/PCA-SPEC) — tu prowadzony jest cały rozwój i wydania.
- **TSVNE** ([VERTYXNEXUSEIL/TSVNE](https://github.com/VERTYXNEXUSEIL/TSVNE)) jest **wycofane**; ma zostać usunięte. Wszystkie zmiany, narzędzia (`tools/doctor.py`), kontekst (`AGENTS.md`) i wektory (T1–T13) są wyłącznie w PCA-SPEC. Przed usunięciem TSVNE z GitHub można wrzucić tam minimalny README z przekierowaniem (szablon: `docs/README-for-TSVNE-repo.md`).
