# Copyright (c) 2009, Erik Karulf <erik@karulf.com>
# 
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# TODO:
# * Use mmap to sequentially scan through the file
# * docstrings
# * doctests

from cStringIO import StringIO
from mmap import mmap, ALLOCATIONGRANULARITY as BLOCKSIZE
from hashlib import md5, sha1, sha224, sha256, sha384, sha512
from zlib import adler32, crc32

CHECKSUM_FORMATS = {
    'adler32': adler32,
    'crc32'  : crc32,
    'md5'    : md5,
    'sha1'   : sha1,
    'sha224' : sha224,
    'sha256' : sha256,
    'sha384' : sha384,
    'sha512' : sha512,
}

def _calculate_checksum(format, data):
    if format in ('adler32', 'crc32'):
        # zlib-style functions
        func = CHECKSUM_FORMATS[format]
        value = None
        buf = data.read(BLOCKSIZE)
        while len(buf) > 0:
            if value is None:
                value = func(buf) & 0xffffffff
            else:
                value = func(buf, value) & 0xffffffff
            buf = data.read(BLOCKSIZE)
        return value
    else:
        # hashlib-style functions
        hash_class = CHECKSUM_FORMATS[format]
        h = hash_class()
        buf = data.read(BLOCKSIZE)
        while len(buf) > 0:
            h.update(buf)
            buf = data.read(BLOCKSIZE)
        return h.hexdigest()

def checksum(checksum_format, raw_data):
    format = checksum_format.lower()
    if format not in CHECKSUM_FORMATS:
        raise Exception('%s is not a valid checksum format.' % format)
    
    # Choose the optimal accessor
    data = None
    close = True
    if hasattr(raw_data, 'fileno'):
        # File object
        data = mmap(raw_data.fileno(), 0)   # Make the entire file available through mmap
    elif hasattr(raw_data, 'read'):
        # File-like object
        data = raw_data
        close = False
    else:
        # String-like object
        data = StringIO(raw_data)
    
    # Compute the hash
    try:
        value = _calculate_checksum(format, data)
    finally:
        if close:
            data.close()
    return value

