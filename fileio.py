# File and directory management and manipulation, including synchronisation.
import sys
import os
import filecmp
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
    """
    Form path base/d while dealing correctly with multiple or absent backslashes etc.
    INPUTS:
        base - base path
        d - additional directory or file-name defined relative to base
    RETURNS: combined path
    """
    return os.path.normpath(os.path.join(base, d))

#
def join_path_list(pathlist):
    """
    Join list of paths (ordered base-most first) into a single combined path.
    """
    path = ''
    for p in pathlist:
        path = join_path(path, p)
    return path

#
def files_and_dirs(pathname, names=None):
    """
    Get the names of all files and directories in path-directory.
    INPUTS:
        pathname - path to directory of interest
        names - (optional) list of subset of names in directory
    RETURNS:
        files - list of names of files
        dirs - list of names of directories
    """
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

    def get_path(self, key):
        # Form full path from key
        return join_path_list([self.dirlist[i] for i in key])

    def get_filename(self, key, filenum):
        # Get local filename from key and file-index
        return self.filedict[key][filenum]

    def get_file_path(self, key, filenum):
        # Get full path-and-filename to specified file
        return join_path(self.get_path(key), self.filedict[key][filenum])

def find_duplicate_attribute(dirtree, isname):
    flist = []
    # List all files by (key, index, attribute)
    for k in dirtree.filedict.keys():
        if isname: # find duplicate names
            flist += [(k, i, f) for (i,f) in enumerate(dirtree.filedict[k])]
        else: # find duplicate sizes
            path = dirtree.get_path(k)
            getsize = lambda x: os.stat(join_path(path, x)).st_size
            flist += [(k, i, getsize(f)) for (i,f) in enumerate(dirtree.filedict[k])]
    # Sort files by attribute
    flist = sorted(flist, key=lambda x: x[-1])
    # Collect duplicate attributes
    i, dups = 0, list()
    while i < len(flist):
        j = i + 1
        while j < len(flist) and flist[i][-1] == flist[j][-1]:
            j += 1
        if j - i > 1:
            dups += [[(k, i) for (k,i,_) in flist[i:j]]]
        i = j
    return dups

# Find all files that have identical binaries
def find_duplicates(dirtree, dup_attrib):
    duplicates = list()
    for names in dup_attrib:
        # Within this set of matching-attribute files, there may be subgroups of identical binaries
        N = len(names)
        mark = [False] * N  # marker for already-grouped files
        fullname = [dirtree.get_file_path(*n) for n in names] # get set of full-path names
        for i in range(N):
            if mark[i]: continue  # i is already in a group, so move on
            mark[i] = True  # create new group
            group = [names[i]]
            for j in range(i+1, N): # seek to add files to group
                if mark[j]: continue # j is already in a group, move on
                if filecmp.cmp(fullname[i], fullname[j]):
                    mark[j] = True # binary match, add to group
                    group.append(names[j])
        if len(group) > 1:
            duplicates.append(group)
    return duplicates

# Graph-type data-structure of linked objects
class Neighbour:
    def __init__(self, lists):
        pass


# Return set of files that are (i) same name but different, and (ii) different name but identical binary.
def find_not_duplicates(dirtree):
    samename = find_duplicate_attribute(dirtree, True)
    samesize = find_duplicate_attribute(dirtree, False)
    identical, nameonly, namediff = list(), list(), list()
    # Need a graph data-structure to link things that are different to all the things that share a common attribute

# Find files that are: same, different, right-only, left-only
#   - for "different" want to show stats: (most recent, biggest, num of zeros, etc)
def compare_directories(d1, d2):
    pass

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
    dups_name = find_duplicate_attribute(dt, True)
    dups_size = find_duplicate_attribute(dt, False)
    print('Names: ', dups_name)
    print('Sizes: ', dups_size)
    dups_bin = find_duplicates(dt, dups_name)
    print('Binaries: ', dups_bin)

if __name__ == '__main__':
    dir1 = os.getcwd() if len(sys.argv) == 1 else sys.argv[1]
    flags = 0x02
    if flags & 0x01:
        test_create_dirtree(dir1)
    if flags & 0x02:
        test_find_duplicates_in_tree(dir1)
