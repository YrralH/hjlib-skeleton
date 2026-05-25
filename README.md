# hjlib-skeleton

Joint-name vocabularies (SMPL / COCO / H36M / MPI / JTA / OpenPose /
VitPose) and a single cross-format index transform, for the hjlib
family.

Leaf lib: pure data + a couple of tiny helpers, no internal hjlib
dependencies.

## Install

```bash
conda activate hjlib_py312    # py3.12 + torch 2.8 + cu12.8
cd hjlib-skeleton
pip install -e .
```

## 30-second example

```python
from hjlib_skeleton import SMPL_ALL_54, COCO_17, get_index_transform

# Pick the source slots whose joint name also appears in the target
# vocabulary, in the target's key-iteration order.
idx = get_index_transform(SMPL_ALL_54, COCO_17)
# joints_smpl54: np.ndarray of shape (N, 54, ...)
joints_coco17 = joints_smpl54[:, idx]            # shape (N, 17, ...)
```

For the full vocabulary list, the `get_jta_22_with_smpl_names` helper,
and the topology constants — see [docs/usage/README.md](docs/usage/README.md).

## Docs

- [docs/usage/](docs/usage/) — how to call: the vocabularies, the
  transform, the topology constants
- [docs/design/](docs/design/) — how to modify: scope, conventions,
  migration record

## Repo

- GitHub: <https://github.com/YrralH/hjlib-skeleton>
- Family conventions live in [Code_as_Libs/CLAUDE.md](../CLAUDE.md) and
  user-level memory under `~/.claude/projects/.../memory/`.
