# Usage

hjlib-skeleton is pure data + one cross-format helper. There is no
runtime object, no construction, no configuration: import a vocabulary
or `get_index_transform` and use them.

**Before calling `get_index_transform` against `SMPL_ALL_54`**, read
[joint_name_semantics.md](joint_name_semantics.md) — several joint
names (hip, pelvis, spine, thorax, neck, jaw) carry two distinct
flavours (SMPL kinematic vs LSP-style regressor), and picking the
wrong one silently distorts downstream SMPL fits / 2D comparisons.

## Vocabulary overview

Every joint-name dict maps `name -> index`, with indices contiguous
from 0 to N-1.

| Symbol | Type | N | Purpose |
|---|---|---|---|
| `SMPL_24` | `dict[str, int]` | 24 | SMPL body kinematic joints (root = Pelvis_SMPL) |
| `SMPL_EXTRA_30` | `dict[str, int]` | 30 | Face / hand / foot / extra body joints (indices 24..53) |
| `SMPL_ALL_54` | `dict[str, int]` | 54 | `SMPL_24` ∪ `SMPL_EXTRA_30` |
| `OPENPOSE_18` | `dict[str, int]` | 18 | OpenPose body keypoints |
| `COCO_17` | `dict[str, int]` | 17 | COCO body keypoints |
| `COCO_FOOT_6` | `dict[str, int]` | 6 | COCO foot extension (indices 17..22) |
| `COCO_BODY_WITH_FOOT_23` | `dict[str, int]` | 23 | `COCO_17` ∪ `COCO_FOOT_6` |
| `VITPOSE_25` | `dict[str, int]` | 25 | ViTPose keypoints |
| `MPI_INF_28` | `dict[str, int]` | 28 | MPI-INF-3DHP keypoints |
| `H36M_32` | `dict[str, int]` | 32 | Human3.6M keypoints |
| `JTA_22` | `dict[str, int]` | 22 | JTA native-name keypoints |
| `name_joint_jta_22` | `list[str]` | 22 | JTA positional list (source of `JTA_22`) |
| `get_jta_22_with_smpl_names(include_hips=True)` | `(bool) -> dict[str, int]` | 22 | JTA-22 with SMPL-style names where semantically aligned |

## Cross-format index lookup

```python
from hjlib_skeleton import get_index_transform, SMPL_ALL_54, COCO_17

idx = get_index_transform(SMPL_ALL_54, COCO_17)
# idx[k] is the SMPL_ALL_54 source index for the k-th COCO_17 target
# slot whose name exists in SMPL_ALL_54. Target-only names are silently
# skipped, so len(idx) <= len(COCO_17).
joints_coco17 = joints_smpl54[:, idx]
```

The iteration follows the **target's** key order (Python dict
insertion order), not the source's. Names present only in the target
are silently skipped — callers that need an exact-length guarantee
should assert on `len(idx)`.

## Topology

| Symbol | Type | Shape | Purpose |
|---|---|---|---|
| `SMPL_PARENT` | `list[int]` | (24,) | Parent SMPL_24 index per joint; root (Pelvis_SMPL) = -1 |
| `SKELETON_COCO_17` | `np.ndarray[int64]` | (19, 2) | Bone edges as pairs of COCO_17 indices (for vis) |

## Composing transforms

For a typical "SMPL_ALL_54 prediction -> COCO_17 GT comparison"
pipeline, the entire setup is:

```python
from hjlib_skeleton import get_index_transform, SMPL_ALL_54, COCO_17

idx = get_index_transform(SMPL_ALL_54, COCO_17)            # length 17
pred_coco17 = joints_pred_smpl54[..., idx, :]              # (..., 17, C)
```

That is the full surface. Anything more involved (geometric transforms,
SMPL forward, mesh sampling) belongs to other hjlib-* libs, not here.
