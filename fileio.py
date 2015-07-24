# File and directory management and manipulation, including synchronisation.
import sys
import os
#from pathlib import Path
import shutil

# TODO; We want:
# - list (recursively) directory: same, different, right-only, left-only
#   - for "different" want to show stats: (most recent, biggest, num of zeros, etc)
# - stats: percentages of dir-tree that are identical etc
# - check file timestamps: os.stat(fname).st_mtime
# - check files are identical
# - synchronise: copy files left-to-right, copy files right-to-left
# - check for existence of duplicate files in directory tree
#   - check for identical files with different names; and different files with same names (organised by st_mtime)

# See Python Cookbook (3rd Ed) - 13.7 and 13.9
# also, from functools import partial # see 5.8 of Python Cookbook (3rd Ed)

# To compare two files ---------------------
# import filecmp
# filecmp.cmp('undoc.rst', 'undoc.rst')

# Compare directories ----------------------
# from filecmp import dircmp
# def print_diff_files(dcmp):
#     for name in dcmp.diff_files:
#         print("diff_file %s found in %s and %s" % (name, dcmp.left,
#               dcmp.right))
#     for sub_dcmp in dcmp.subdirs.values():
#         print_diff_files(sub_dcmp)
#
# dcmp = dircmp('dir1', 'dir2')
# print_diff_files(dcmp)

#
def join_path(base, d):
    return os.path.normpath(os.path.join(base, d))

#
def join_path_list(pathlist):
    path = ''
    for p in pathlist:
        path = join_path(path, p)
    return path

#
def files_and_dirs(pathname, names=None):
    if not names:
        names = os.listdir(pathname)
    files, dirs = [], []
    for n in names:
        fullname = join_path(pathname, n)
        if os.path.isfile(fullname):
            files += [n]
        elif os.path.isdir(fullname):
            dirs += [n]
        else:
            print('Weird, name (%s) is neither file or directory ' % (n))
    return files, dirs

class DirectoryTree:
    def __init__(self, rootdir):
        self.dirctr = 0
        self.filedict = dict()
        path, d = os.path.split(rootdir)
        self.dirlist = list([path])
        self.__tree_recurse(path, d, 0, (0,))

    def __tree_recurse(self, path, d, depth, pathtuple):
        # Record local dir-name and index-tuple to full-path
        self.dirlist += [d]
        self.dirctr += 1
        filekey = tuple(list(pathtuple) + [self.dirctr])
        # Get files and directories from current path
        fulldir = join_path(path, d)
        flist, dlist = files_and_dirs(fulldir)
        self.filedict[filekey] = flist # store files, indexed by full-path code
        # Recurse over dictionaries
        for dchild in dlist:
            self.__tree_recurse(fulldir, dchild, depth+1, filekey)

def search_sorted_duplicates(flist, icomp):
    i, dups = 0, list()
    while i < len(flist):
        j = i + 1
        while j < len(flist) and flist[i][icomp] == flist[j][icomp]:
            j += 1
        if j - i > 1:
            dups += [(flist[i][0], [f[-1] for f in flist[i:j]])]
        i = j
    return dups

def find_duplicate_names_in_tree(dirtree):
    flist = []
    for k in dirtree.filedict.keys():
        flist += [(f, k) for f in dirtree.filedict[k]]
    flist.sort()
    return search_sorted_duplicates(flist, 0)

def find_duplicate_size_in_tree(dirtree):
    flist = []
    for k in dirtree.filedict.keys():
        path = join_path_list([dirtree.dirlist[i] for i in k]) # form full path
        flist += [(f, os.stat(join_path(path,f)).st_size, k) for f in dirtree.filedict[k]]
    flist = sorted(flist, key=lambda x: x[1])
    return search_sorted_duplicates(flist, 1)

#
# Tests
#

def test_create_dirtree(dir):
    dt = DirectoryTree(dir)
    print('Number dirs: %d' % dt.dirctr)
    for k in dt.filedict.keys():
        fulldir = join_path_list([dt.dirlist[i] for i in k])
        print('Key:', k, 'Path', fulldir)
        print('  Files:', dt.filedict[k])

def test_find_duplicates_in_tree(dir):
    dt = DirectoryTree(dir)
    dups_name = find_duplicate_names_in_tree(dt)
    dups_size = find_duplicate_size_in_tree(dt)
    print('Names: ', dups_name)
    print('Sizes: ', dups_size)

if __name__ == '__main__':
    dir1 = os.getcwd() if len(sys.argv) == 1 else sys.argv[1]
    flags = 0x02
    if flags & 0x01:
        test_create_dirtree(dir1)
    if flags & 0x02:
        test_find_duplicates_in_tree(dir1)