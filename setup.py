#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pynleq2 is a python binding for NLEQ2.

NLEQ2 is part of the CodeLib collection of algortihms:
http://elib.zib.de/pub/elib/codelib/en/

Retrieved on 2015-10-20 13:25:

   /.../
   The ZIB-CodeLib software may be used for scientific and educational purposes
   free of charge. For commercial use of the software you must sign a license-
   agreement with the ZIB and pay a license-charge that depends on the
   referenced software package and the intended usage. Please read our sample
   license agreement for more details.

http://elib.zib.de/pub/elib/codelib/en/Lizenz.html

In order to indicate that you have read and accepted their license
you need to either:

- set the environment variable PYNLEQ2_NLEQ2_ROOT_URL to
  point to a repository which containing the source code of NLEQ2. e.g.
     $ export PYNLEQ2_NLEQ2_ROOT_URL=http://www.univeristy.edu/mirror/nleq2/

- Alternatively, extract the sources into the nleq2/ sub-directory manually.


The python interface (nleq2/nleq2.pyf) has been taken from the BSD licensed
PySCeS project (http://pysces.sourceforge.net/), see also LICENSE_pysces.txt
"""

import os, re
try:
    from numpy.distutils.core import setup, Extension
except Exception, ex:
    print "NumPy is required"
    os.sys.exit(os.EX_OK+1)

__version__ = '0.0.1.git'

sources = 'nleq2.pyf nleq2.f linalg_nleq2.f zibmon.f zibsec.f zibconst.f wnorm.f'.split()

# nleq2 version: 2.3.0.2
md5output = """
28ed88f1ae7bab8dc850348b5e734881  linalg_nleq2.f
73401c84c8e0d434fffa6f303ba813e0  nleq2.f
77189300200be5748152fa28dc236963  wnorm.f
5d912441fb6f55d10c8b98bbb9168195  zibconst.f
e2ac1a20fc6294cb3e0d7f65bbac53e6  zibmon.f
6520c958f2bd339b435a68541d5b910b  zibsec.f
"""
md5sums, sources = zip(*map(str.split, md5output[1:-1].split('\n')))


def md5_of_file(path, nblocks=128):
    from hashlib import md5
    md = md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(nblocks*md.block_size), b''):
            md.update(chunk)
    return md

def download(url, outpath):
    from urllib2 import urlopen
    try:
        f = urlopen(url)
        print("downloading " + url)
        with open(outpath, "wb") as fh:
            fh.write(f.read())
    except HTTPError, e:
        print("HTTP Error:", e.code, url)
    except URLError, e:
        print("URL Error:", e.reason, url)


for src, md5sum in zip(sources, md5sums):
    srcpath = os.path.join('nleq2', src)
    if not os.path.exists(srcpath):
        NLEQ2_URL = os.environ.get('PYNLEQ2_NLEQ2_ROOT_URL', None)
        if NLEQ2_URL:
            download(NLEQ2_URL+src, srcpath)
        else:
            fmtstr = "Could not find: %s (and $PYNLEQ2_NLEQ2_ROOT_URL not set)"
            raise ValueError(fmtstr % src)
    if md5_of_file(srcpath).hexdigest() != md5sum:
        raise ValueError("Mismatching MD5 sum for %s" % srcpath)

nleq2 = Extension('pynleq2.nleq2', [os.path.join('nleq2', f) for f in ('nleq2.pyf',) + sources])

setup(name="pynleq2",
      version = __version__,
      description = "Python binding for NLEQ2",
      author = "Björn Dahlgren",
      author_email = "bjodah@DELETEMEgmail.com",
      url = "http://github.com/bjodah/pynleq2",
      requires = ['numpy'],
      classifiers = [
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Fortran',
          'Programming Language :: Python'
      ],
      packages = ['pynleq2'],
      ext_modules = [nleq2]
)
