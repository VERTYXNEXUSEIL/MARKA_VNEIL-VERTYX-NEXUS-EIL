# Zabezpieczenie repozytorium PCA-SPEC (GitHub)

Rekomendacje dla [VERTYXNEXUSEIL/PCA-SPEC](https://github.com/VERTYXNEXUSEIL/PCA-SPEC).

## Branch protection (Settings → Branches → Add rule)

- **Branch name pattern:** `main`
- **Require a pull request before merging:** włączone (opcjonalnie: 1 approval).
- **Require status checks to pass:** włączone; wybierz workflow **CI** (doctor, testy).
- **Do not allow bypassing the above settings** — włączone dla maintainerów (opcjonalnie).
- **Restrict who can push to matching branches:** tylko zaufani maintainerzy (opcjonalnie).

## Oznaczenie release

- Tag **v1.0.0** powinien wskazywać na commit wydania 1.0.0.
- W GitHub: **Releases** → **Create a new release** → tag `v1.0.0`, tytuł "PCA/CAE v1.0.0", opis z CHANGELOG [1.0.0].

## Zasoby

- **Strona:** [pca-spec.github.io](https://pca-spec.github.io)
- **Bezpieczeństwo:** zgłoszenia zgodnie z [SECURITY.md](../SECURITY.md)
