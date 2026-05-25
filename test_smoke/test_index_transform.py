'''
Smoke: get_index_transform behavior on typical and edge inputs.
'''

from hjlib_skeleton import (
    get_index_transform,
    SMPL_24,
    SMPL_ALL_54,
    COCO_17,
    COCO_BODY_WITH_FOOT_23,
)


def test_smpl54_to_coco17():
    # Every COCO_17 name except 'Nose' has a counterpart in SMPL_ALL_54
    # (Nose is present too, as SMPL_EXTRA_30 carries it). Therefore the
    # transform should return a list of 17 source indices, all within
    # the SMPL_ALL_54 value range.
    idx = get_index_transform(SMPL_ALL_54, COCO_17)
    assert len(idx) == 17, len(idx)
    for i in idx:
        assert 0 <= i < 54, i
    # The first target name is 'Nose', which lives at SMPL_ALL_54 index 24.
    assert idx[0] == SMPL_ALL_54['Nose'] == 24


def test_smpl54_to_body23_partial():
    # COCO_BODY_WITH_FOOT_23 introduces 6 foot-tip joints. SMPL_ALL_54
    # carries the same six (L_BigToe / L_SmallToe / L_Heel + R variants);
    # therefore all 23 should match.
    idx = get_index_transform(SMPL_ALL_54, COCO_BODY_WITH_FOOT_23)
    assert len(idx) == 23, len(idx)


def test_returns_target_ordering():
    # Iteration follows target_format key order; the resulting source
    # indices must be in that order, not source order.
    source = {'A': 10, 'B': 20, 'C': 30}
    target = {'C': 0, 'A': 1, 'B': 2}
    assert get_index_transform(source, target) == [30, 10, 20]


def test_missing_target_keys_skipped_silently():
    source = {'A': 10}
    target = {'A': 0, 'Z': 1}  # Z not in source
    assert get_index_transform(source, target) == [10]


def test_empty_inputs():
    assert get_index_transform({}, {}) == []
    assert get_index_transform({'A': 0}, {}) == []
    assert get_index_transform({}, {'A': 0}) == []


def test_no_overlap():
    assert get_index_transform({'A': 1}, {'B': 0}) == []


def test_smpl24_to_smpl24_identity_order():
    # Source == target: result equals each source's value in source's
    # own key-iteration order.
    idx = get_index_transform(SMPL_24, SMPL_24)
    assert idx == list(SMPL_24.values())


def smoke_test_index_transform():
    test_smpl54_to_coco17()
    test_smpl54_to_body23_partial()
    test_returns_target_ordering()
    test_missing_target_keys_skipped_silently()
    test_empty_inputs()
    test_no_overlap()
    test_smpl24_to_smpl24_identity_order()


if __name__ == '__main__':
    smoke_test_index_transform()
    print('test_index_transform: ok')
