# Migration record: lib_dynamic_hvip.constants_skeleton → hjlib-skeleton

## 1. Source

- Monolith repo: `~/Repo/dynamic_hvip`
- Source subdir: `lib_dynamic_hvip/constants_skeleton.py` (single file)
- Capture date: 2026-05-24
- Monolith sha (pinned): `2bc42db41613420a8311cb9a8877b7c2de298e09`

A second monolith — `~/Repo/crowd-top-down/lib_crowd3d/constants_skeleton.py`
— carries a strict content subset of the same symbols (plus one
unrelated numeric sentinel, `LARGE_NUMBER`, not absorbed). It is
recorded here as a known future consumer (see
[design/README.md "Known future consumers"](README.md#known-future-consumers))
but is not part of the port surface.

## 2. Destination

- Lib name: `hjlib-skeleton`
- Distribution: `hjlib-skeleton` (PyPI-style hyphen)
- Import name: `hjlib_skeleton`
- src path: `src/hjlib_skeleton/`
- Initial commit: `dbf1b4dfd847708b056ec5a47f8ae51bdb00fdd0` (2026-05-25)

## 3. Equivalence model

Uniform parity is the contract: every ported symbol is identical in
value to its monolith counterpart, modulo deliberate divergences
recorded in §6. See
[`hjlibm/docs/hjlib_standard/migration_protocol.md`](../../../hjlibm/docs/hjlib_standard/migration_protocol.md)
for the family-wide equivalence model (parity + behavior + divergence).

This is a port style **file-mapping** (single source file →
semantically partitioned src tree).

## 4. What was ported

The monolith file was split across three modules in src by semantic
role; every public symbol that survives the cull (§5) lives in exactly
one of them and is re-exported at top-level.

| Source symbol (`lib_dynamic_hvip.constants_skeleton`) | Dest module | Notes |
|---|---|---|
| `SMPL_24` | `joint_name_maps.py` | Verbatim. Reformatted to multi-line for readability. |
| `SMPL_EXTRA_30` | `joint_name_maps.py` | Verbatim. |
| `SMPL_ALL_54` | `joint_name_maps.py` | Verbatim. |
| `OPENPOSE_18` | `joint_name_maps.py` | Verbatim. |
| `COCO_17` | `joint_name_maps.py` | Verbatim. |
| `COCO_FOOT_6` | `joint_name_maps.py` | Verbatim. |
| `COCO_BODY_WITH_FOOT_23` | `joint_name_maps.py` | Verbatim. |
| `VITPOSE_25` | `joint_name_maps.py` | Verbatim. |
| `MPI_INF_28` | `joint_name_maps.py` | Verbatim. |
| `H36M_32` | `joint_name_maps.py` | Verbatim. |
| `name_joint_jta_22` | `joint_name_maps.py` | Verbatim. |
| `JTA_22` | `joint_name_maps.py` | Verbatim (built from `name_joint_jta_22`). |
| `get_jta_22_with_smpl_names` | `joint_name_maps.py` | Verbatim, with return-type annotation `dict[str, int]` added (was untyped). |
| `get_index_transform` | `index_transform.py` | Verbatim logic. Parameter + return type annotations added (was untyped). |
| `SMPL_PARENT` | `skeleton_topology.py` | Verbatim. |
| `SKELETON_COCO_17` | `skeleton_topology.py` | Verbatim. Re-typed as `NDArray[np.int64]`. |

## 5. What was NOT ported

| Source symbol | Reason | Suggested home for any future caller |
|---|---|---|
| `eval_scenes_dict` | Not a skeleton vocabulary — it is a dataset eval-scene name list. Zero callers in monolith. | Inline into the eval script that needs it, or move to the dataset-specific lib. |
| `Skeleton_Format` (class) | Half-implemented stub whose `__init__` only asserts a `name_type` string. Zero callers in monolith; conflicts with the dict-based vocabulary design. | Drop; no replacement needed. |
| `SKELETON_FOOT` (`np.ndarray`, bone edges) | Zero callers in monolith. | If needed later, add back to `skeleton_topology.py` alongside `SKELETON_COCO_17`. |
| `TARGE_SMPL_KP_WORLDPOSE_FROM_54` (`np.ndarray`) | Hard-binds to WorldPose evaluation semantics, not a generic skeleton vocabulary. One monolith caller. | Owned by the WorldPose-specific code path (e.g. `lib_dynamic_hvip/test_moving_camera/...`). |
| `LARGE_NUMBER` (only in `lib_crowd3d.constants_skeleton`, value `99999999.`) | Not a skeleton concept; misplaced numerical sentinel. Zero out-of-file callers. | Inline at the use site in whichever lib needs it. |
| `change_dwpose_18_to_coco17` (function) | Not a primitive of this lib — it is one specific instance of `get_index_transform`'s pattern. The monolith implementation used an in-place scatter-then-truncate idiom (`kps[:, dwpose_18_idx] = kps[:, coco_17_idx]; kps[:, :17, :]`) that obscures the underlying name-based mapping and forced an awkward "in-place mutation + truncated view" dual contract. Three monolith callers (`align_ground`, `estimate_2d`, `crop_to_camera`), none in dataset-raw scope. | When the first downstream caller migrates: add a `DWPOSE_18: dict[str, int]` vocabulary to `joint_name_maps.py` (with the actual DWPose-18 joint names, which the monolith did not record — only integer slot indices), then use `kps[:, get_index_transform(DWPOSE_18, COCO_17), :]` at the call site. Do not revive the helper. |

## 6. Intentional API divergences

| ID | What changed | Why |
|---|---|---|
| SKL-1 | All previously-untyped public symbols now carry explicit type annotations (`dict[str, int]`, `list[int]`, `NDArray[...]`). | The family standard is `typeCheckingMode = strict`; untyped public surface forces every downstream consumer into untyped propagation. Values and runtime behavior are unchanged. |
| SKL-2 | `SKELETON_COCO_17` is typed `NDArray[np.int64]` instead of the monolith's bare `np.ndarray`. | Same rationale as SKL-1; narrows the contract from "any ndarray" to the actually-supported dtype. No runtime check is added; behaviour is identical. |

These are not behavior changes — values and array contents are
identical. Parity tests against the monolith (when cross-lib testing
lands; see [test.md](test.md)) will compare values directly and ignore
declared types.

## 7. Bug fixes during the port

None. The monolith `constants_skeleton.py` had no observable bugs in
the ported surface.

## 8. Where verification lives

Cross-lib verification for hjlib-skeleton lives in
[`hjlib-integration-tests`](https://github.com/YrralH/hjlib-integration-tests)
(the family's canonical cross-lib test repo, **replacing** the older
`hjlib-migration-tests/<lib>/{parity,behavior}` pattern for new ports
from 2026-05-25 onward; family intro at
`hjlibm/docs/hjlib_standard/cross_lib_test_spec.md`, full spec at
`hjlib-integration-tests/docs/design/spec.md`).

Two skeleton-relevant case shapes are expected to land there once
upstream deps exist:

1. 2D joints + name overlay on a real dataset frame (validates
   `vocabulary index → actual joint position` correspondence).
2. Monocular SMPL fit from 2D joints using `get_index_transform`,
   eye-checking that the LSP-style vs SMPL-kinematic hip/pelvis/spine
   disambiguation described in
   [docs/usage/joint_name_semantics.md](../usage/joint_name_semantics.md)
   produces visually-correct fits.

Both cases hard-depend on hjlib-dataset-raw / hjlib-vis-2d / hjlib-smpl,
which are themselves pending per the `dataset-raw-uplift` multi-lib
plan in `hjlibm/docs/migration_progress/multi_lib_plans/`. Phase 2
hinges on those landing first; the standard itself is not blocking.

## 9. Migration test status

- [x] Phase 1 — code lives in new lib; pyright + smoke green;
      initial commit landed *(initial commit `dbf1b4d` 2026-05-25;
      pyright strict 0 errors; pytest test_smoke/ 16 cases green)*
- [ ] Phase 2 — skeleton-relevant cases landed in
      `hjlib-integration-tests` (the family's canonical cross-lib test
      repo, superseding `hjlib-migration-tests/<lib>/` for new ports);
      baseline PNGs eye-checked against expected.md per the spec at
      `hjlib-integration-tests/docs/design/spec.md`.

      *Pending hjlib-dataset-raw / hjlib-vis-2d / hjlib-smpl
      (per `dataset-raw-uplift` plan steps 1 / 2 / 7). Standard
      itself is not blocking. Current state is smoke-only.*

- [ ] Phase 3 — absorbed; `behavior/` + per-lib `conftest.py` +
      `local_setting_test.py` + readers moved into
      `hjlib-<name>/test/`; `parity/` and `divergence/` deleted;
      `hjlib-migration-tests/<lib>/` subdir removed
      (absorb date: YYYY-MM-DD)
