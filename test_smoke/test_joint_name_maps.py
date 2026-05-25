'''
Smoke: joint-name vocabularies are internally self-consistent.

Each top-level dict must have unique keys, contiguous integer indices
starting at 0 (or composing cleanly onto its base), and composite dicts
must equal the union of their parts.
'''

from hjlib_skeleton import (
    SMPL_24,
    SMPL_EXTRA_30,
    SMPL_ALL_54,
    OPENPOSE_18,
    COCO_17,
    COCO_FOOT_6,
    COCO_BODY_WITH_FOOT_23,
    VITPOSE_25,
    MPI_INF_28,
    H36M_32,
    name_joint_jta_22,
    JTA_22,
    get_jta_22_with_smpl_names,
    get_index_transform,
)


def assert_contiguous_from_zero(name: str, m: dict[str, int]) -> None:
    values = sorted(m.values())
    expected = list(range(len(m)))
    assert values == expected, '%s: expected contiguous 0..%d, got %s' % (
        name, len(m) - 1, values,
    )


def assert_keys_unique(name: str, m: dict[str, int]) -> None:
    # Building the dict literal already enforces key uniqueness at
    # parse time; this check guards against later programmatic
    # construction (e.g. JTA_22).
    assert len(set(m.keys())) == len(m), '%s: duplicate keys' % name


def test_atomic_vocabs_contiguous_from_zero():
    for name, m in [
        ('SMPL_24',     SMPL_24),
        ('OPENPOSE_18', OPENPOSE_18),
        ('COCO_17',     COCO_17),
        ('VITPOSE_25',  VITPOSE_25),
        ('MPI_INF_28',  MPI_INF_28),
        ('H36M_32',     H36M_32),
        ('JTA_22',      JTA_22),
    ]:
        assert_keys_unique(name, m)
        assert_contiguous_from_zero(name, m)


def test_extension_index_ranges():
    # Extension dicts pick up where their base leaves off.
    smpl_extra_values = sorted(SMPL_EXTRA_30.values())
    assert smpl_extra_values == list(range(24, 54)), smpl_extra_values

    coco_foot_values = sorted(COCO_FOOT_6.values())
    assert coco_foot_values == list(range(17, 23)), coco_foot_values


def test_composite_vocabs_equal_union():
    # SMPL_ALL_54 = SMPL_24 + SMPL_EXTRA_30 with no key collisions.
    assert SMPL_ALL_54 == {**SMPL_24, **SMPL_EXTRA_30}
    assert len(SMPL_ALL_54) == len(SMPL_24) + len(SMPL_EXTRA_30), (
        'SMPL_24 and SMPL_EXTRA_30 share a key'
    )
    assert_contiguous_from_zero('SMPL_ALL_54', SMPL_ALL_54)

    # COCO_BODY_WITH_FOOT_23 = COCO_17 + COCO_FOOT_6.
    assert COCO_BODY_WITH_FOOT_23 == {**COCO_17, **COCO_FOOT_6}
    assert len(COCO_BODY_WITH_FOOT_23) == len(COCO_17) + len(COCO_FOOT_6)
    assert_contiguous_from_zero('COCO_BODY_WITH_FOOT_23', COCO_BODY_WITH_FOOT_23)


def test_jta_22_native_ordering():
    # JTA_22 is built from name_joint_jta_22 list; indices must match
    # positional ordering.
    assert len(name_joint_jta_22) == 22
    assert len(JTA_22) == 22
    for i, name in enumerate(name_joint_jta_22):
        assert JTA_22[name] == i, (i, name, JTA_22[name])


def test_known_name_index_pins():
    # Pin a handful of well-known name->index pairs per vocabulary.
    # Structural invariants (contiguity, uniqueness, composite=union)
    # would all survive a silent transpose of two indices inside a
    # vocab; these explicit pins guard against that drift until the
    # cross-lib parity layer comes online.
    #
    # Picks: root joint + one mid joint + one tail joint per vocab.
    # For SMPL_ALL_54 the duplicated 'hip' / 'pelvis' / 'neck' / 'jaw'
    # / 'spine' / 'thorax' name pairs are pinned because cross-format
    # downstream consumers rely on the LSP-style (suffix-less) slot
    # resolving to the higher indices, not the SMPL kinematic slot.
    assert SMPL_24['Pelvis_SMPL'] == 0
    assert SMPL_24['L_Hip_SMPL'] == 1
    assert SMPL_24['R_Hip_SMPL'] == 2
    assert SMPL_24['Neck'] == 12
    assert SMPL_24['R_Wrist'] == 21
    assert SMPL_24['R_Hand'] == 23

    assert SMPL_EXTRA_30['Nose'] == 24
    assert SMPL_EXTRA_30['R_Hip'] == 45
    assert SMPL_EXTRA_30['L_Hip'] == 46
    assert SMPL_EXTRA_30['Neck_LSP'] == 47
    assert SMPL_EXTRA_30['Pelvis'] == 49
    assert SMPL_EXTRA_30['Spine_H36M'] == 51
    assert SMPL_EXTRA_30['Head'] == 53

    # Duplicated names in SMPL_ALL_54 resolve to SMPL_EXTRA_30 (the
    # LSP-style) slot, because composite construction uses
    # {**SMPL_24, **SMPL_EXTRA_30} (later wins). Cross-format
    # consumers depend on this exact resolution.
    assert SMPL_ALL_54['Pelvis_SMPL'] == 0
    assert SMPL_ALL_54['L_Hip_SMPL'] == 1
    assert SMPL_ALL_54['R_Hip_SMPL'] == 2
    assert SMPL_ALL_54['Pelvis'] == 49
    assert SMPL_ALL_54['L_Hip'] == 46
    assert SMPL_ALL_54['R_Hip'] == 45
    assert SMPL_ALL_54['Neck'] == 12
    assert SMPL_ALL_54['Neck_LSP'] == 47

    assert OPENPOSE_18['Nose'] == 0
    assert OPENPOSE_18['Neck'] == 1
    assert OPENPOSE_18['L_Ear'] == 17

    assert COCO_17['Nose'] == 0
    assert COCO_17['L_Hip'] == 11
    assert COCO_17['R_Hip'] == 12
    assert COCO_17['R_Ankle'] == 16

    assert COCO_FOOT_6['L_BigToe'] == 17
    assert COCO_FOOT_6['R_BigToe'] == 20
    assert COCO_FOOT_6['R_Heel'] == 22

    assert COCO_BODY_WITH_FOOT_23['Nose'] == 0
    assert COCO_BODY_WITH_FOOT_23['R_Ankle'] == 16
    assert COCO_BODY_WITH_FOOT_23['R_Heel'] == 22

    assert VITPOSE_25['Nose'] == 0
    assert VITPOSE_25['Mid_Hip'] == 8
    assert VITPOSE_25['R_Heel'] == 24

    assert MPI_INF_28['spine3_mpi_28'] == 0
    assert MPI_INF_28['Pelvis'] == 4
    assert MPI_INF_28['Head'] == 6
    assert MPI_INF_28['R_BigToe'] == 27

    assert H36M_32['Hip_H36M'] == 0
    assert H36M_32['Pelvis'] == 11
    assert H36M_32['Head'] == 15
    assert H36M_32['R_Hand_H36M'] == 31

    assert JTA_22['head_top'] == 0
    assert JTA_22['neck'] == 2
    assert JTA_22['left_ankle'] == 21


def test_index_transform_respects_known_smpl_to_coco_pins():
    # Cross-vocab guard: COCO_17 names that exist in SMPL_ALL_54 must
    # resolve to the LSP-style slots (not the kinematic ones). This
    # pins the load-bearing semantic for any get_index_transform-based
    # downstream pipeline.
    idx = get_index_transform(SMPL_ALL_54, COCO_17)
    assert len(idx) == 17
    # L_Hip is COCO_17 key 'L_Hip' -> SMPL_ALL_54 -> slot 46 (LSP).
    # R_Hip -> slot 45.
    coco_lhip_pos = list(COCO_17.keys()).index('L_Hip')
    coco_rhip_pos = list(COCO_17.keys()).index('R_Hip')
    assert idx[coco_lhip_pos] == 46, (idx[coco_lhip_pos], 46)
    assert idx[coco_rhip_pos] == 45, (idx[coco_rhip_pos], 45)
    # COCO_17 'Nose' lives at SMPL_ALL_54 slot 24.
    coco_nose_pos = list(COCO_17.keys()).index('Nose')
    assert idx[coco_nose_pos] == 24


def test_get_jta_22_with_smpl_names_branches():
    fmt_with = get_jta_22_with_smpl_names(include_hips=True)
    fmt_without = get_jta_22_with_smpl_names(include_hips=False)
    assert len(fmt_with) == 22
    assert len(fmt_without) == 22
    assert 'R_Hip_SMPL' in fmt_with and 'L_Hip_SMPL' in fmt_with
    assert 'R_Hip_SMPL' not in fmt_without and 'L_Hip_SMPL' not in fmt_without
    assert 'jta_unique_right_hip' in fmt_without
    assert 'jta_unique_left_hip' in fmt_without
    # Values are JTA-22 native positions (0..21), unique.
    for fmt in (fmt_with, fmt_without):
        values = sorted(fmt.values())
        assert values == list(range(22)), values


def smoke_test_joint_name_maps():
    test_atomic_vocabs_contiguous_from_zero()
    test_extension_index_ranges()
    test_composite_vocabs_equal_union()
    test_jta_22_native_ordering()
    test_known_name_index_pins()
    test_index_transform_respects_known_smpl_to_coco_pins()
    test_get_jta_22_with_smpl_names_branches()


if __name__ == '__main__':
    smoke_test_joint_name_maps()
    print('test_joint_name_maps: ok')
