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

## Cross-lib verification

Real-world correctness of `get_index_transform` and the vocabularies
ultimately manifests in downstream consumers (dataset-raw, vis,
network loss).

The family's canonical cross-lib test repo is
[`hjlib-integration-tests`](https://github.com/YrralH/hjlib-integration-tests)
(spec: `Code_as_Libs/hjlib-integration-tests/docs/design/spec.md`,
family intro: `hjlibm/docs/hjlib_standard/cross_lib_test_spec.md`).
It supersedes the older `hjlib-migration-tests/<lib>/{parity,behavior}`
pattern for new ports from 2026-05-25 onward. hjlib-skeleton's
verification path goes through it, not through hjlib-migration-tests.

Two skeleton-relevant case shapes are expected to land there:

1. 2D joints + name overlay on a real dataset frame — validates that
   each vocabulary's `name → index` actually corresponds to the
   anatomical point a downstream caller expects.
2. Monocular SMPL fit from 2D joints using `get_index_transform` —
   eye-checks that the LSP-style vs SMPL-kinematic disambiguation
   from
   [docs/usage/joint_name_semantics.md](../usage/joint_name_semantics.md)
   produces visually-correct fits.

Both cases hard-depend on hjlib-dataset-raw / hjlib-vis-2d /
hjlib-smpl (per the `dataset-raw-uplift` multi-lib plan in
`hjlibm/docs/migration_progress/multi_lib_plans/`). Until those land,
hjlib-skeleton's verification is smoke-only + caller-side correctness:
downstream libs' own tests catch any vocabulary regression that
breaks their outputs.

## Smoke files

| File | Covers |
|---|---|
| `test_joint_name_maps.py` | Every vocab dict's key-uniqueness, index contiguity, and composite-equals-union invariants; explicit name→index pins (incl. the LSP-style vs SMPL kinematic hip / pelvis / spine / neck / jaw resolutions in `SMPL_ALL_54`); cross-vocab guard that `get_index_transform(SMPL_ALL_54, COCO_17)` resolves to the LSP-style hip slots; both branches of `get_jta_22_with_smpl_names`. |
| `test_index_transform.py` | Typical SMPL_ALL_54 → COCO_17 / COCO_BODY_WITH_FOOT_23 transforms; target-key iteration order; missing-target skip; empty / no-overlap edge cases; source-equals-target identity. |
| `test_skeleton_topology.py` | `SMPL_PARENT` shape + root invariant + DAG ordering; `SKELETON_COCO_17` dtype + shape + index range + no self-loops. |
| `test_all_func.py` | Master runner; calls every `smoke_test_*` and prints a single pass line. |
| `clean_test_data.py` | `LIST_PATH_CLEAN = []` — this lib emits no transient files. |
