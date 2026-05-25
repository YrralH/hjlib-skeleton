'''
Joint-name vocabularies.

Each public dict maps a human-readable joint name to its index inside one
specific format. Composite dicts (e.g. SMPL_ALL_54, COCO_BODY_WITH_FOOT_23)
are computed from their parts so the index ranges stay consistent.

The vocabularies here are pure name <-> index data with no behavior. For
cross-format index lookup, see index_transform.get_index_transform.
'''

SMPL_24: dict[str, int] = {
    'Pelvis_SMPL':  0, 'L_Hip_SMPL':  1, 'R_Hip_SMPL':  2, 'Spine_SMPL':  3,
    'L_Knee':       4, 'R_Knee':      5, 'Thorax_SMPL': 6, 'L_Ankle':     7,
    'R_Ankle':      8, 'Thorax_up_SMPL': 9,
    'L_Toe_SMPL':  10, 'R_Toe_SMPL': 11, 'Neck':       12, 'L_Collar':   13,
    'R_Collar':    14, 'Jaw':        15, 'L_Shoulder': 16, 'R_Shoulder': 17,
    'L_Elbow':     18, 'R_Elbow':    19, 'L_Wrist':    20, 'R_Wrist':    21,
    'L_Hand':      22, 'R_Hand':     23,
}

SMPL_EXTRA_30: dict[str, int] = {
    'Nose':      24, 'R_Eye':     25, 'L_Eye':     26, 'R_Ear':     27, 'L_Ear':     28,
    'L_BigToe':  29, 'L_SmallToe':30, 'L_Heel':    31, 'R_BigToe':  32, 'R_SmallToe':33,
    'R_Heel':    34,
    'L_Hand_thumb':  35, 'L_Hand_index':  36, 'L_Hand_middle': 37,
    'L_Hand_ring':   38, 'L_Hand_pinky':  39,
    'R_Hand_thumb':  40, 'R_Hand_index':  41, 'R_Hand_middle': 42,
    'R_Hand_ring':   43, 'R_Hand_pinky':  44,
    'R_Hip':     45, 'L_Hip':     46, 'Neck_LSP':  47, 'Head_top':  48,
    'Pelvis':    49, 'Thorax_MPII': 50,
    'Spine_H36M':51, 'Jaw_H36M':  52, 'Head':      53,
}

SMPL_ALL_54: dict[str, int] = {**SMPL_24, **SMPL_EXTRA_30}

OPENPOSE_18: dict[str, int] = {
    'Nose':       0, 'Neck':       1, 'R_Shoulder': 2, 'R_Elbow':    3,
    'R_Wrist':    4, 'L_Shoulder': 5, 'L_Elbow':    6, 'L_Wrist':    7,
    'R_Hip':      8, 'R_Knee':     9, 'R_Ankle':   10, 'L_Hip':     11,
    'L_Knee':    12, 'L_Ankle':   13, 'R_Eye':     14, 'L_Eye':     15,
    'R_Ear':     16, 'L_Ear':     17,
}

COCO_17: dict[str, int] = {
    'Nose':       0, 'L_Eye':      1, 'R_Eye':      2, 'L_Ear':      3,
    'R_Ear':      4, 'L_Shoulder': 5, 'R_Shoulder': 6, 'L_Elbow':    7,
    'R_Elbow':    8, 'L_Wrist':    9, 'R_Wrist':   10, 'L_Hip':     11,
    'R_Hip':     12, 'L_Knee':    13, 'R_Knee':    14, 'L_Ankle':   15,
    'R_Ankle':   16,
}

COCO_FOOT_6: dict[str, int] = {
    'L_BigToe':  17, 'L_SmallToe':18, 'L_Heel':    19,
    'R_BigToe':  20, 'R_SmallToe':21, 'R_Heel':    22,
}

COCO_BODY_WITH_FOOT_23: dict[str, int] = {**COCO_17, **COCO_FOOT_6}

VITPOSE_25: dict[str, int] = {
    'Nose':       0, 'Neck':       1, 'R_Shoulder': 2, 'R_Elbow':    3,
    'R_Wrist':    4, 'L_Shoulder': 5, 'L_Elbow':    6, 'L_Wrist':    7,
    'Mid_Hip':    8, 'R_Hip':      9, 'R_Knee':    10, 'R_Ankle':   11,
    'L_Hip':     12, 'L_Knee':    13, 'L_Ankle':   14, 'R_Eye':     15,
    'L_Eye':     16, 'R_Ear':     17, 'L_Ear':     18, 'L_BigToe':  19,
    'L_SmallToe':20, 'L_Heel':    21, 'R_BigToe':  22, 'R_SmallToe':23,
    'R_Heel':    24,
}

MPI_INF_28: dict[str, int] = {
    'spine3_mpi_28':         0, 'spine4_mpi_28':         1,
    'spine2_mpi_28':         2, 'spine_mpi_28':          3,
    'Pelvis':                4, 'Neck':                  5,
    'Head':                  6, 'Head_top':              7,
    'left_clavicle_mpi_28':  8, 'L_Shoulder':            9,
    'L_Elbow':              10, 'L_Wrist':              11,
    'L_Hand':               12, 'right_clavicle_mpi_28':13,
    'R_Shoulder':           14, 'R_Elbow':              15,
    'R_Wrist':              16, 'R_Hand':               17,
    'L_Hip':                18, 'L_Knee':               19,
    'L_Ankle':              20, 'L_SmallToe':           21,
    'L_BigToe':             22, 'R_Hip':                23,
    'R_Knee':               24, 'R_Ankle':              25,
    'R_SmallToe':           26, 'R_BigToe':             27,
}

H36M_32: dict[str, int] = {
    'Hip_H36M':              0, 'R_Hip':                 1, 'R_Knee':            2,
    'R_Ankle':               3, 'R_BigToe':              4, 'R_SmallToe':        5,
    'L_Hip':                 6, 'L_Knee':                7, 'L_Ankle':           8,
    'L_BigToe':              9, 'L_SmallToe':           10, 'Pelvis':           11,
    'Spine_H36M':           12, 'Neck1_H36M':           13, 'Jaw_H36M':         14,
    'Head':                 15, 'Neck2_H36M':           16, 'L_Shoulder':       17,
    'L_Elbow':              18, 'L_Wrist':              19, 'L_HandThumb_H36M': 20,
    'L_OuterThigh_H36M':    21, 'L_Wrist_End_H36M':     22, 'L_Hand_H36M':      23,
    'Neck':                 24, 'R_Shoulder':           25, 'R_Elbow':          26,
    'R_Wrist':              27, 'R_HandThumb_H36M':     28, 'R_OuterThigh_H36M':29,
    'R_Wrist_End_H36M':     30, 'R_Hand_H36M':          31,
}

# JTA-22 native ordering (positional list). JTA_22 is the dict view.
name_joint_jta_22: list[str] = [
    'head_top',
    'head_center',
    'neck',
    'right_clavicle',
    'right_shoulder',
    'right_elbow',
    'right_wrist',
    'left_clavicle',
    'left_shoulder',
    'left_elbow',
    'left_wrist',
    'spine0',
    'spine1',
    'spine2',
    'spine3',
    'spine4',
    'right_hip',
    'right_knee',
    'right_ankle',
    'left_hip',
    'left_knee',
    'left_ankle',
]
assert len(name_joint_jta_22) == 22, len(name_joint_jta_22)
JTA_22: dict[str, int] = {name_joint_jta_22[i]: i for i in range(len(name_joint_jta_22))}


def get_jta_22_with_smpl_names(include_hips: bool = True) -> dict[str, int]:
    '''
    JTA-22 joint format relabeled so that joints semantically corresponding
    to SMPL_24 keys carry the SMPL_24 name (cross-matchable via
    get_index_transform). Joints unique to JTA (head_top, head_center,
    spine0..spine4) get the prefix `jta_unique_` to make them clearly
    non-shared.

    Hip behaviour is flag-controlled (include_hips):
        True  : right_hip / left_hip aliased to R_Hip_SMPL / L_Hip_SMPL
                (count as cross-matchable trustworthy joint pair).
        False : tagged jta_unique_right_hip / jta_unique_left_hip
                (excluded from name-matching cross-validation).

    @return Dict[str, int] of length 22, keys = joint names, values =
    JTA-22 native indices.

    Note: name-matched joints with SMPL_24 are
    (Neck, L_Collar, R_Collar, L/R_Shoulder, L/R_Elbow, L/R_Wrist,
     L/R_Knee, L/R_Ankle) plus optionally (L/R_Hip_SMPL):
        include_hips=True  -> 15 cross-matched
        include_hips=False -> 13 cross-matched
    '''
    return {
        'jta_unique_head_top':                                            0,
        'jta_unique_head_center':                                         1,
        'Neck':                                                           2,
        'R_Collar':                                                       3,
        'R_Shoulder':                                                     4,
        'R_Elbow':                                                        5,
        'R_Wrist':                                                        6,
        'L_Collar':                                                       7,
        'L_Shoulder':                                                     8,
        'L_Elbow':                                                        9,
        'L_Wrist':                                                       10,
        'jta_unique_spine0':                                             11,
        'jta_unique_spine1':                                             12,
        'jta_unique_spine2':                                             13,
        'jta_unique_spine3':                                             14,
        'jta_unique_spine4':                                             15,
        ('R_Hip_SMPL' if include_hips else 'jta_unique_right_hip'):      16,
        'R_Knee':                                                        17,
        'R_Ankle':                                                       18,
        ('L_Hip_SMPL' if include_hips else 'jta_unique_left_hip'):       19,
        'L_Knee':                                                        20,
        'L_Ankle':                                                       21,
    }
