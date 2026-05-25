# Test layout

## Two trees (family policy)

The hjlib family standard is two trees:

- `test_smoke/` — no external data; runs anywhere, every commit.
- `test/` — requires real data; FAIL (not skip) when missing.

See family memory `test-layout-smoke-vs-data` for the rationale.

## Why this lib is smoke-only

hjlib-skeleton is pure vocabulary + a tiny pure function. Every
behavior of every public symbol can be exercised with synthetic inputs
(or no input at all — many tests just assert dict invariants). There
is no realistic input that needs to come from disk.

Therefore:

- `test_smoke/` covers every public symbol (see the file list below).
- `test/` exists as an empty directory with a `.gitkeep`, so the
  family-standard tree shape is preserved. No `reader_*.py` and no
  `local_setting_test.py` are present, deliberately — adding them
  would mislead a future contributor into thinking data-driven
  verification is expected here.

## Cross-lib verification (deferred)

Real-world correctness of `get_index_transform` and the vocabularies
ultimately manifests in downstream consumers (dataset-raw, vis,
network loss). The migration-protocol's existing answer for this is
`hjlib-migration-tests/<lib>/{parity,behavior}` against the monolith.

That pattern is not used here. The user is drafting a new cross-lib
test standard better suited to this project's data-access reality.
When it lands, this section will be updated with the concrete location
of skeleton-relevant cross-lib coverage and any monolith-vs-hjlib
parity gates.

Until then: smoke-only + caller-side correctness (the downstream lib's
own tests catch any vocabulary regression that breaks its outputs).

## Smoke files

| File | Covers |
|---|---|
| `test_joint_name_maps.py` | Every vocab dict's key-uniqueness, index contiguity, and composite-equals-union invariants; explicit name→index pins (incl. the LSP-style vs SMPL kinematic hip / pelvis / spine / neck / jaw resolutions in `SMPL_ALL_54`); cross-vocab guard that `get_index_transform(SMPL_ALL_54, COCO_17)` resolves to the LSP-style hip slots; both branches of `get_jta_22_with_smpl_names`. |
| `test_index_transform.py` | Typical SMPL_ALL_54 → COCO_17 / COCO_BODY_WITH_FOOT_23 transforms; target-key iteration order; missing-target skip; empty / no-overlap edge cases; source-equals-target identity. |
| `test_skeleton_topology.py` | `SMPL_PARENT` shape + root invariant + DAG ordering; `SKELETON_COCO_17` dtype + shape + index range + no self-loops. |
| `test_all_func.py` | Master runner; calls every `smoke_test_*` and prints a single pass line. |
| `clean_test_data.py` | `LIST_PATH_CLEAN = []` — this lib emits no transient files. |
