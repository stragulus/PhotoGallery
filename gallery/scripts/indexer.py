#!/usr/bin/env python

import os
import sys
import sqlite3
import string
import random

from gallery.db import init_db, session
from gallery.db.models import Photo, Tag

# recursively scan path

def scan_dir(d, tags):
    files = os.listdir(d)

    for f in files:
        path = os.path.join(d, f)
        if f.startswith('.'):
            continue
        if os.path.isdir(path):
            scan_dir(path, tags + [ f ])

        if os.path.splitext(f.lower())[1] not in [ '.jpg', '.jpeg' ]:
            continue

        photo_tags = tags + [ os.path.splitext(f)[0] ]
        p = Photo(path)
        session.add(p)
        try:
            p.set_tags(set(photo_tags))
        except:
            print(photo_tags)
            raise
        session.flush()


if __name__ == "__main__":
    init_db()
    try:
        path = sys.argv[1]
    except:
        sys.stderr.write("Usage: indexer.py <path to dir with photos>\n")
        sys.exit(1)

    scan_dir(path, [])
