#
# Tests
#

import os
import sys
import pyutils.fileio as fio


def test_create_dirtree(dir):
    dt = fio.DirectoryTree(dir)
    print('Number dirs: %d' % dt.dirctr)
    for k in dt.filedict.keys():
        fulldir = fio.join_path_list([dt.dirlist[i] for i in k])
        print('Key:', k, 'Path', fulldir)
        print('  Files:', dt.filedict[k])


def test_find_duplicates_in_tree(dir):
    dt = fio.DirectoryTree(dir)
    dups_name = fio.find_duplicate_attribute(dt, True)
    dups_size = fio.find_duplicate_attribute(dt, False)
    print('Names: ', dups_name)
    print('Sizes: ', dups_size)
    dups_bin = fio.find_duplicates(dt, dups_name)
    print('Binaries: ', dups_bin)

#
#

if __name__ == '__main__':
    dir1 = os.getcwd() if len(sys.argv) == 1 else sys.argv[1]
    flags = 0x02
    if flags & 0x01:
        test_create_dirtree(dir1)
    if flags & 0x02:
        test_find_duplicates_in_tree(dir1)
