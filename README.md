# PCA-SPEC

Strona wejściowa dokumentacji projektu **Proof-Carrying Autonomy (PCA) / Certified Agentic Execution (CAE)** — standardu technicznego do deterministycznego, certyfikowalnego wykonywania działań autonomicznych.

**Repozytorium kanoniczne:** [GitHub VERTYXNEXUSEIL/PCA-SPEC](https://github.com/VERTYXNEXUSEIL/PCA-SPEC) · **Strona:** [pca-spec.github.io](https://pca-spec.github.io)

Repozytorium **TSVNE** ([VERTYXNEXUSEIL/TSVNE](https://github.com/VERTYXNEXUSEIL/TSVNE)) jest wycofane; cała treść, rozwój i wydania są w PCA-SPEC.

## Dokumentacja

- **Polska dokumentacja (primary): [`pl/README_PL.md`](pl/README_PL.md)** — indeks: [`pl/docs/index.md`](pl/docs/index.md)
- **English documentation: [`README_EN.md`](README_EN.md)**

## Najważniejsze sekcje repozytorium

| Sekcja | Opis |
|--------|------|
| [`spec/`](spec/) | Specyfikacja normatywna (EN): PCA-SPEC-v1.0, reason codes, testy, słownik, FAQ |
| [`pl/spec/`](pl/spec/) | Tłumaczenia specyfikacji (PL) |
| [`schemas/`](schemas/) | Schematy JSON: PC, Action IR, constraints, evidence capsule |
| [`test-vectors/vectors-v1/`](test-vectors/vectors-v1/) | Wektory testowe T1–T13 |
| [`reference/python/`](reference/python/) | Implementacja referencyjna (Python); quickstart: `pip install -e .[dev]` → `pytest -q` |
| [`reference/cli/`](reference/cli/) | Narzędzie CLI |
| [`tools/doctor.py`](tools/doctor.py) | Skrypt zdrowia (schematy, wektory, pytest, ruff) — uruchamiać z katalogu głównego repo |
| [`CHANGELOG.md`](CHANGELOG.md) | Historia zmian |
| [`CONTRIBUTING.md`](CONTRIBUTING.md), [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) | Wkład i zasady |
| [`SECURITY.md`](SECURITY.md) | Zasady bezpieczeństwa |

## Kontekst dla asystentów i współtwórców

Szczegółowy opis struktury, konwencji i typowych problemów: **[`AGENTS.md`](AGENTS.md)**.

Aby uzyskać pełny opis w języku angielskim (zakres standardu, quickstart, integralność i release), przejdź do [`README_EN.md`](README_EN.md).
