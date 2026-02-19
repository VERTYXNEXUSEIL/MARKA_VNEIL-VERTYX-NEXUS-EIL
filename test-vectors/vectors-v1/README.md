# PCA Test Vectors v1

Deterministic vectors for PCA-TEST v1.

## Included vectors

- `T1_pc_replay`: replay nonce must trigger `RC_PC_REPLAY`.
- `T2_domain_separation`: digest domain labels must stay separated.
- `T3_constraints_mismatch`: runtime constraints mismatch must fallback.
- `T4_reason_stability`: repeated evaluation must keep identical reason code output.
- `T5_toctou`: TOCTOU drift must trigger `RC_TOCTOU`.
- `T6_effective_time`: evaluation outside effective window must trigger `RC_EFFECTIVE_TIME`.
- `T7_optional_field_omission`: optional `pc` fields set to `null`/`None` (e.g. `merkle_root`, `metadata`) must be pruned during canonicalization so the resulting PC digest matches an equivalent payload where those fields are omitted.
- `T8_conflict_detector`: conflict detector trip must trigger `RC_CONFLICT`.
- `T9_merkle_proof`: invalid merkle proof state must trigger `RC_MERKLE_PROOF`.
- `T10_brs_gate`: high BRS score over threshold must trigger `RC_BRS_GATE`.
- `T11_ood_tripwire`: OOD tripwire must trigger `RC_OOD_TRIPWIRE`.
- `T12_disclosure_budget`: disclosure usage above budget must trigger `RC_DISCLOSURE_BUDGET`.
