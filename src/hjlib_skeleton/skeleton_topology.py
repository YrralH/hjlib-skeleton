'''
Skeleton topology constants.

Names + index ordering belong to joint_name_maps; this module carries
the structural relations between joints (parent index per joint, bone
edges between joint indices).
'''

import numpy as np
from numpy.typing import NDArray


# Parent joint index for each SMPL_24 joint. Pelvis_SMPL (index 0) is
# the root, with parent -1. Aligned with the SMPL_24 ordering.
SMPL_PARENT: list[int] = [
    -1,  0,  0,  0,
     1,  2,  3,  4,  5,
     6,  7,  8,  9,
     9,  9, 12,
    13, 14,
    16, 17,
    18, 19,
    20, 21,
]
assert len(SMPL_PARENT) == 24, len(SMPL_PARENT)


# Bone edges for COCO_17 (visualization-oriented; ordering follows the
# historical convention used by vis_assoc). Each row is a pair of
# COCO_17 indices that should be drawn as a connected segment.
SKELETON_COCO_17: NDArray[np.int64] = np.array(
    [
        [15, 13], [13, 11], [16, 14], [14, 12], [11, 12], [ 5, 11], [ 6, 12], [ 5,  6],
        [ 5,  7], [ 6,  8], [ 7,  9], [ 8, 10], [ 1,  2], [ 0,  1], [ 0,  2], [ 1,  3], [ 2,  4], [ 3,  5], [ 4,  6],
    ],
    dtype=np.int64,
)
