'''
Cross-format joint index lookup.

Given two joint-name vocabularies (e.g. SMPL_ALL_54, COCO_17), build the
list of source indices to pick so that the resulting array follows the
target ordering for every joint name that both formats share.

Names that exist only in the target are silently skipped. The returned
list length is therefore <= len(target_format); callers that need a
length check should assert on the result.
'''


def get_index_transform(
    source_format: dict[str, int],
    target_format: dict[str, int],
) -> list[int]:
    '''
    Build the source-index list whose i-th entry is the source index of
    the i-th cross-matched target joint name.

    Iteration order follows `target_format` (Python dict insertion
    order). Joints present only in `target_format` are silently skipped.

    @param source_format Joint-name -> source-index mapping.
    @param target_format Joint-name -> target-index mapping (only its
                         keys + iteration order are used).
    @return List of source indices, length = number of names shared by
            both vocabularies.
    '''
    index: list[int] = []
    for joint_name in target_format:
        if joint_name in source_format:
            index.append(source_format[joint_name])
    return index
