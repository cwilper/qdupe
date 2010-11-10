import hashlib
import os
import stat
import sys

def find_dupes(paths):
    print "Scanning for files..."
    map = {}
    for path in paths:
        _scan(path, map);

    total_files = 0
    total_size = 0
    num_dupes = 0
    wasted_bytes = 0
    print "Comparing %s sets of files..." % len(map.keys())
    print
    for size in map.keys():
        paths = map.get(size)
        total_files += len(paths)
        if len(paths) > 1:
            n = _compare(paths, size)
            num_dupes += n
            wasted_bytes += n * size
        total_size += size * len(paths)

    print "Found %s duplicates (%s bytes wasted)" % (num_dupes, wasted_bytes)
    print "Scanned %s files (%s bytes)" % (total_files, total_size)

def _scan(path, map):
    s = os.stat(path)
    mode = s[stat.ST_MODE]
    if stat.S_ISDIR(mode):
        for f in os.listdir(path):
            _scan(os.path.join(path, f), map)
    elif stat.S_ISREG(mode):
        size = s[stat.ST_SIZE]
        cpath = os.path.realpath(path)
        paths = map.get(size)
        if paths:
            paths.add(cpath)
        else:
            map[size] = set([cpath]);
    else:
        print 'Skipping non-regular file: %s' % path

def _compare(paths, size):
    # compare hashes of first 4k
    map = {}
    for path in paths:
        hash = _get_hash(path, 4096)
        matching_paths = map.get(hash)
        if matching_paths:
            matching_paths.add(path)
        else:
            map[hash] = set([path])
    num_dupes = 0
    for hash in map.keys():
        matching_paths = map.get(hash)
        if len(matching_paths) > 1:
            if (size > 4096):
                num_dupes += _compare_full(matching_paths, size)
            else:
                _report_dupes(size, hash, matching_paths)
                num_dupes += len(matching_paths) - 1
    return num_dupes

def _compare_full(paths, size):
    map = {}
    for path in paths:
        hash = _get_full_hash(path)
        matching_paths = map.get(hash)
        if matching_paths:
            matching_paths.add(path)
        else:
            map[hash] = set([path])
    num_dupes = 0
    for hash in map.keys():
        matching_paths = map.get(hash)
        if len(matching_paths) > 1:
            _report_dupes(size, hash, matching_paths)
            num_dupes += len(matching_paths) - 1
    return num_dupes

def _report_dupes(size, hash, paths):
    print "%s files, %s bytes, md5=%s" % (len(paths), size, hash)
    for path in paths:
        print "\t%s" % path
    print

def _get_hash(path, num_bytes):
    f = open(path, "rb")
    hash = hashlib.new("md5")
    data = f.read(num_bytes)
    hash.update(data)
    f.close()
    return hash.hexdigest()

def _get_full_hash(path):
    f = open(path, "rb")
    hash = hashlib.new("md5")
    while True:
        data = f.read(8192)
        if not data:
            break
        hash.update(data)
    f.close()
    return hash.hexdigest()
