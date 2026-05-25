'''
Master smoke-test runner. Imports each per-topic smoke_test_* function
and runs them sequentially.

Why the __file__ + sys.path trick: test_smoke/ is not a package (no
__init__.py on purpose, so pytest does not treat it as one). To let
this script import its siblings by name when run as `python
test_smoke/test_all_func.py` from any cwd, prepend the directory of
this file to sys.path before the imports.
'''

import os.path as osp
import sys


sys.path.insert(0, osp.dirname(osp.abspath(__file__)))

from test_joint_name_maps import smoke_test_joint_name_maps
from test_index_transform import smoke_test_index_transform
from test_skeleton_topology import smoke_test_skeleton_topology


def main():
    smoke_test_joint_name_maps()
    smoke_test_index_transform()
    smoke_test_skeleton_topology()
    print('test_all_func: all smoke tests passed')


if __name__ == '__main__':
    main()
