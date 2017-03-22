#!/usr/bin/env python

from __future__ import print_function

import itertools
import subprocess
import os


def loc(owner, repo):
    report = subprocess.check_output(["loc", os.path.join("mirror", owner, repo)])
    lines = report.decode("utf-8").splitlines()
    _, files, _, _, _, sloc = lines[-2].split()
    return int(files), int(sloc)


if __name__ == "__main__":
    print("url", "primary language", "files", "sloc", sep="\t")

    for line in itertools.islice(open("showcases.tsv"), 1, None):
        url, lang, stars, forks = line.split("\t")
        _, _, _, owner, repo = url.split("/")
        files, sloc = loc(owner, repo)
        print(url, lang, files, sloc, sep="\t")
