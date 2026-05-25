# Joint-name semantics

The vocabularies in hjlib-skeleton are not orthogonal. Several joint
names appear with two different physical meanings under different
prefixes, and one composite vocabulary (`SMPL_ALL_54`) carries both
flavours side by side. This page is the canonical guide to choosing
the right name.

If you are writing a downstream consumer (dataset reader, SMPL fit,
joint-name visualization, monocular regression), read this page before
calling `get_index_transform`.

## The two flavours

Inside `SMPL_ALL_54` (= `SMPL_24` ∪ `SMPL_EXTRA_30`) every "anchor
point on the body" exists in up to two slots:

| Flavour | Where it comes from | What it represents | Where it lives in 3D |
|---|---|---|---|
| **SMPL kinematic** — `*_SMPL` suffix (or no suffix for joints that only exist in this flavour, e.g. `Neck`, `Jaw`, `L_Knee`, ...) | `SMPL_24` (indices 0..23). Outputs of the SMPL kinematic chain. | The rotation centres used by SMPL skinning. Parents in `SMPL_PARENT` are kinematic parents. | **Inside** the body — joints sit in the pelvic cavity, shoulder socket, knee centre, etc. |
| **LSP-style regressor** — no `_SMPL` suffix, often disambiguated with `_H36M` / `_MPII` / `_LSP` for non-standard variants | `SMPL_EXTRA_30` (indices 24..53). Outputs of a LSP-style joint regressor applied to SMPL mesh vertices. | Surface-aligned anchor points that match how 2D datasets (COCO / H36M / LSP / MPII) actually annotate joints. | **On / near the body surface** — at the bony landmark a human annotator would click on a photo. |

Crucial: **these two flavours are NOT the same 3D point.** For hips
the LSP-style sits roughly on the iliac crest area (visible
landmark); the SMPL kinematic sits ~5–8 cm inboard at the hip
rotation centre. For pelvis the gap is even larger (root joint sits
in the pelvic cavity; the surface anchor sits between the iliac
crests). Plugging the wrong flavour into a 2D-pixel comparison
silently distorts SMPL pose estimates.

## Full ambiguity table

Every name pair where the same anatomical region has two slots in
`SMPL_ALL_54`. **`SMPL_ALL_54` lookup column** shows what
`SMPL_ALL_54[key]` actually resolves to.

| Anatomical region | SMPL kinematic name (slot in `SMPL_24`) | LSP-style name (slot in `SMPL_EXTRA_30`) | Both names coexist in `SMPL_ALL_54`? |
|---|---|---|---|
| Pelvis (root) | `Pelvis_SMPL` (0) | `Pelvis` (49) | ✓ |
| Left hip | `L_Hip_SMPL` (1) | `L_Hip` (46) | ✓ |
| Right hip | `R_Hip_SMPL` (2) | `R_Hip` (45) | ✓ |
| Lower spine | `Spine_SMPL` (3) | `Spine_H36M` (51) | ✓ |
| Thorax / chest | `Thorax_SMPL` (6) | `Thorax_MPII` (50) | ✓ |
| Upper thorax | `Thorax_up_SMPL` (9) | (no LSP-style counterpart) | n/a |
| Neck | `Neck` (12) | `Neck_LSP` (47) | ✓ |
| Jaw | `Jaw` (15) | `Jaw_H36M` (52) | ✓ |

Joints **without** an ambiguity pair (knees, ankles, elbows, wrists,
shoulders, collars, hands, toes, eyes, ears, nose, head, head_top,
fingers, heels, big/small toes) appear in exactly one slot and need
no disambiguation — their `SMPL_ALL_54` lookup is unique.

⚠️ **Watch out**: the heuristic "no `_SMPL` suffix means LSP-style"
is **not** universal. `Neck` (SMPL_ALL_54 index 12) is the SMPL
kinematic neck despite having no suffix; the LSP variant is the
explicitly-named `Neck_LSP` (index 47). Same shape for `Jaw` (15,
SMPL kinematic) vs `Jaw_H36M` (52). Always cross-check this table,
not the suffix.

## Selection guidance

| You want… | Use the name in this column |
|---|---|
| **Compare against 2D dataset annotations** (COCO / H36M / MPII / LSP joint pixels) | LSP-style (`Pelvis`, `L_Hip`, `R_Hip`, `Spine_H36M`, `Thorax_MPII`, `Neck_LSP`, ...) |
| **Drive SMPL forward pass / fit SMPL pose parameters** | SMPL kinematic (`Pelvis_SMPL`, `L_Hip_SMPL`, `R_Hip_SMPL`, `Spine_SMPL`, `Thorax_SMPL`, `Neck`, ...) |
| **Build a kinematic parent chain** (visualize bones, compute joint angles) | SMPL kinematic — pair with `SMPL_PARENT` (which is indexed against `SMPL_24`, not `SMPL_ALL_54`) |
| **Render 2D bone edges** (skeleton overlay on RGB) | `SKELETON_COCO_17` (uses COCO indices, surface-aligned) |

## Why `get_index_transform(SMPL_ALL_54, COCO_17)` is currently correct

COCO-17 reports surface-aligned joint pixels. The 2D annotation for
"left hip" is the iliac-crest area, not the rotation centre. So the
expected mapping COCO `L_Hip` → SMPL_ALL_54 slot **46** (LSP-style),
not slot 1 (kinematic).

Today this resolves correctly **by accident of dict construction**:

```python
SMPL_ALL_54 = {**SMPL_24, **SMPL_EXTRA_30}
```

- The key `L_Hip` exists **only** in `SMPL_EXTRA_30` (value 46).
- The key `L_Hip_SMPL` exists **only** in `SMPL_24` (value 1).
- The two keys do not collide; both end up in `SMPL_ALL_54` under
  their respective names.
- COCO_17 asks for `L_Hip` → finds 46. ✓

If someone refactored `SMPL_EXTRA_30` to rename `L_Hip` → `L_Hip_SMPL`
(thinking "let's be consistent and add the suffix everywhere"), the
composite would become `{**SMPL_24, **SMPL_EXTRA_30}` with
`L_Hip_SMPL` colliding — and the later (EXTRA_30, value 46) would
shadow the earlier (SMPL_24, value 1). COCO_17's `L_Hip` lookup
would then **fail** (KeyError-style: it would be skipped by
`get_index_transform`, silently shrinking `len(idx)` from 17 to 15).

Smoke test `test_known_name_index_pins` (in
`test_smoke/test_joint_name_maps.py`) explicitly pins
`SMPL_ALL_54['L_Hip'] == 46` and the cross-vocab guard
`test_index_transform_respects_known_smpl_to_coco_pins` pins
`get_index_transform(SMPL_ALL_54, COCO_17)[<L_Hip slot>] == 46`. Any
refactor that breaks the LSP-style → idx 46 invariant will turn smoke
red.

## Common pitfalls

1. **Using `SMPL_24` (not `SMPL_ALL_54`) as the source vocabulary**
   when you want to map 2D dataset joints back. `SMPL_24` does not
   contain `L_Hip` / `R_Hip` / `Pelvis` (only their `_SMPL`
   counterparts), so `get_index_transform(SMPL_24, COCO_17)` will
   skip those names and return a shorter list than expected. Use
   `SMPL_ALL_54`.
2. **Mixing flavours in one downstream array.** If a model returns
   SMPL forward outputs in `SMPL_24` indexing (kinematic), don't
   compute distance to a GT array in COCO-17 indexing by directly
   indexing; first run the model output through the SMPL regressor
   to get a 54-vector, then `get_index_transform(SMPL_ALL_54,
   COCO_17)` to pick the 17 LSP-style slots that align with COCO
   pixels.
3. **Assuming `SMPL_PARENT` works for `SMPL_ALL_54` indices.**
   `SMPL_PARENT[i]` is the parent of `SMPL_24[i]`, not
   `SMPL_ALL_54[i]`. The regressor-output joints (indices 24..53)
   have no defined kinematic parent in this lib.

## When to revisit this doc

If a new flavour shows up (e.g. someone adds DensePose-style
landmarks), or if a vocabulary inside SMPL_EXTRA_30 gets renamed,
update this table and re-run the smoke pins.

CLT-5 in `hjlib-integration-tests` (monocular SMPL fit + visual
sanity check) is the first downstream consumer that exercises the
LSP-vs-kinematic distinction in a real pipeline; its test report
will likely flag whichever pitfall above bites first.
