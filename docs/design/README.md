# Design

How to modify hjlib-skeleton. This is the contributor / Claude
onboarding doc.

## Scope

hjlib-skeleton exists so every hjlib-* downstream that needs to talk
about joint names, joint indices, or convert between joint-name
vocabularies uses the **same source of truth** instead of each
project carrying its own copy of `SMPL_24` / `COCO_17` / ...

The lib carries exactly three kinds of thing:

1. **Joint-name vocabularies** — `dict[str, int]` mapping joint name to
   index in one specific format (SMPL / COCO / H36M / MPI / JTA / ...).
2. **Cross-format lookup** — the single `get_index_transform` function
   that builds a source-index list given two vocabularies.
3. **Light topology constants** — `SMPL_PARENT` (kinematic parent
   indices) and `SKELETON_COCO_17` (bone edges for visualization).

There are no per-format conversion helpers: every name-aware reorder
is expressible as `kps[..., get_index_transform(SRC, TGT), :]`.

The lib does **not** know about:

- SMPL forward / mesh geometry — those live in `hjlib-smpl` (planned)
- bone-edge rendering or 2D visualization — those live in
  `hjlib-vis-2d` (planned)
- dataset-specific labels, calibration, or file I/O — those live in
  per-dataset libs (e.g. `hjlib-dataset-raw`, planned)

## Repo layout

```
hjlib-skeleton/
├── README.md                              30s pitch + install + hello
├── src/hjlib_skeleton/                    package code (only this ships)
│   ├── __init__.py                        re-exports the 16 public symbols
│   ├── joint_name_maps.py                 11 vocab dicts + 1 positional list +
│   │                                      get_jta_22_with_smpl_names
│   ├── index_transform.py                 get_index_transform
│   └── skeleton_topology.py               SMPL_PARENT + SKELETON_COCO_17
├── docs/
│   ├── usage/                             how to call
│   └── design/                             how to modify (this dir)
├── test_smoke/                            no external data; runs anywhere
│   ├── test_joint_name_maps.py
│   ├── test_index_transform.py
│   ├── test_skeleton_topology.py
│   ├── test_all_func.py                   master runner
│   └── clean_test_data.py                 LIST_PATH_CLEAN = [] (no transient output)
├── test/                                  empty; see test.md for why
├── test_data/                             gitignored: would-be sample data + tmp outputs
├── pyrightconfig.json                     typeCheckingMode = strict
├── pyproject.toml
└── .gitignore
```

## Must-read

- [../usage/joint_name_semantics.md](../usage/joint_name_semantics.md)
  — the two-flavour problem (SMPL kinematic vs LSP-style regressor):
  full ambiguity table, selection guidance, why
  `get_index_transform(SMPL_ALL_54, COCO_17)` resolves to the
  LSP-style slots, and what refactors would silently break that. Any
  edit to `joint_name_maps.py` must keep this doc + the value-pin
  smoke tests honest.
- [test.md](test.md) — why this lib is smoke-only and where data-driven
  cross-lib verification will eventually live.
- [migration.md](migration.md) — what was ported from monolith, with
  bug-fix and divergence record.

## Family conventions inherited (links to memory)

These are enforced family-wide; the per-repo content is just a thin link
because all the substance lives in user memory.

- `typeCheckingMode = "strict"` — `pyrightconfig.json` at repo root,
  always 0 errors (memory: `pyright-strict-default`).
- `test_smoke/` no-data + `test/` data-required-FAIL-not-skip
  (memory: `test-layout-smoke-vs-data`). This lib has no `test/`
  content yet — see [test.md](test.md).
- 4-space indent; single quotes; `'%s' %` style; English comments only;
  underscore prefix only for "external call forbidden"
  (memory: `feedback_indentation`, `feedback_underscore_naming`).
- No `utils_*.py` / `_internal/utils_*.py` modules — stdlib first, then
  inline, then concrete-named module
  (memory: `avoid-utils-modules`).

## State of the world

- pyright strict: **0 errors** across `src/ + test_smoke/`.
- `pytest test_smoke/`: 16 cases passing.
- `test/`: empty. Cross-lib data-driven verification is **pending a new
  family-wide cross-lib test standard** (TBD by user) — see
  [test.md](test.md).
- Remote: pending first push.

## Known future consumers

- `lib_dynamic_hvip.constants_skeleton` (the monolith this port came
  from): many in-monolith callers continue to use the old import path;
  they will swap to `from hjlib_skeleton import ...` as part of
  `dataset-raw-uplift` and any downstream lib that depends on raw
  datasets.
- `lib_crowd3d.constants_skeleton` (a second monolith, in
  `~/Repo/crowd-top-down`): a strict content subset of the
  `lib_dynamic_hvip` source, plus one unrelated numerical sentinel
  (`LARGE_NUMBER`, not absorbed here). When that monolith eventually
  ports to hjlib-*, it should swap its own `constants_skeleton`
  imports to `hjlib-skeleton`; the `LARGE_NUMBER` constant has no
  skeleton semantics and stays a per-monolith concern.

## What's open

- **Cross-lib test pending new family standard.** This lib's
  vocabularies and `get_index_transform` are exercised end-to-end only
  by downstream consumers (planned hjlib-dataset-raw etc.). The
  existing `hjlib-migration-tests/<lib>/` pattern requires data
  convenience this project lacks; the user is drafting a replacement.
  When that standard lands, revisit Phase 2 verification for this lib
  and create the appropriate cross-lib test surface.
