'''
Smoke: skeleton topology constants have the expected shape and
internal consistency.
'''

import numpy as np

from hjlib_skeleton import SMPL_PARENT, SKELETON_COCO_17, SMPL_24, COCO_17


def test_smpl_parent_aligned_with_smpl_24():
    assert len(SMPL_PARENT) == len(SMPL_24) == 24, (len(SMPL_PARENT), len(SMPL_24))
    # Exactly one root.
    assert SMPL_PARENT.count(-1) == 1, SMPL_PARENT.count(-1)
    # Root sits at index 0 (Pelvis_SMPL).
    assert SMPL_PARENT[0] == -1
    # Every non-root parent index is a valid SMPL_24 joint index and
    # strictly less than the child (kinematic DAG ordered root-first).
    for child, parent in enumerate(SMPL_PARENT):
        if parent == -1:
            continue
        assert 0 <= parent < len(SMPL_PARENT), (child, parent)
        assert parent < child, (child, parent)


def test_skeleton_coco_17_shape_and_range():
    assert SKELETON_COCO_17.dtype == np.int64, SKELETON_COCO_17.dtype
    assert SKELETON_COCO_17.ndim == 2, SKELETON_COCO_17.ndim
    assert SKELETON_COCO_17.shape[1] == 2, SKELETON_COCO_17.shape
    n_joints = len(COCO_17)
    assert int(SKELETON_COCO_17.min()) >= 0
    assert int(SKELETON_COCO_17.max()) < n_joints, (SKELETON_COCO_17.max(), n_joints)
    # No self-loop edges.
    for a, b in SKELETON_COCO_17:
        assert int(a) != int(b), (a, b)


def smoke_test_skeleton_topology():
    test_smpl_parent_aligned_with_smpl_24()
    test_skeleton_coco_17_shape_and_range()


if __name__ == '__main__':
    smoke_test_skeleton_topology()
    print('test_skeleton_topology: ok')
