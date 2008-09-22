#!/usr/bin/python

import sys
from tempfile import mkdtemp
from os import mkdir, system
import os.path
import rpm


def compare_header(refspec, altspec):
    warnings = []

    refhdr = refspec.packages()[0].header()
    althdr = altspec.packages()[0].header()

    refname = refhdr[rpm.RPMTAG_NAME]
    altname = althdr[rpm.RPMTAG_NAME]

    refver = refhdr[rpm.RPMTAG_VERSION]
    altver = althdr[rpm.RPMTAG_VERSION]

    reflic = refhdr[rpm.RPMTAG_LICENSE]
    altlic = althdr[rpm.RPMTAG_LICENSE]

    refurl = refhdr[rpm.RPMTAG_URL]
    alturl = althdr[rpm.RPMTAG_URL]

    if refver != altver:
        warnings.append("different version: '%s': '%s' != '%s': '%s'" % (refname, refver, altname, altver))

    if reflic != altlic:
        warnings.append("different license: '%s': '%s' != '%s': '%s'" % (refname, reflic, altname, altlic))

    if refurl != alturl:
        warnings.append("different URL: '%s': '%s' != '%s': '%s'" % (refname, refurl, altname, alturl))

    return warnings

def compare_sources(refspec, altspec):
    warnings = []
    refsrc = []
    altsrc = []
    refsrcname = []
    altsrcname = []
    for src in refspec.sources():
        if src[2] == rpm.RPMBUILD_ISSOURCE:
            uri = src[0]
            offset = uri.rfind("/")
            if offset != -1:
                baseuri = uri[0:offset]
                srcname = uri[offset+1:]
            else:
                baseuri = ""
                srcname = uri
            refsrc.append([baseuri, srcname])
            refsrcname.append(srcname)

    for src in altspec.sources():
        if src[2] == rpm.RPMBUILD_ISSOURCE:
            uri = src[0]
            offset = uri.rfind("/")
            if offset != -1:
                baseuri = uri[0:offset]
                srcname = uri[offset+1:]
            else:
                baseuri = ""
                srcname = uri
            altsrc.append([baseuri, srcname])
            altsrcname.append(srcname)


    for s in refsrc:
        if not s[1] in altsrcname:
            warnings.append("missing source: '%s'" % s[1])
    for s in altsrc:
        if not s[1] in refsrcname:
            warnings.append("extra source: '%s'" % s[1])

    for s1 in refsrc:
        for s2 in altsrc:
            if s1[1] != s2[1]:
                continue
            if s1[0] != s2[0]:
                warnings.append("different base URI for source '%s': '%s' != '%s'" % (s1[1], s1[0], s2[0]))

    return warnings


def compare_patches(refspec, altspec):
    warnings = []
    refpatch = []
    altpatch = []
    for src in refspec.sources():
        if src[2] == rpm.RPMBUILD_ISPATCH:
            refpatch.append(src[0])
    for src in altspec.sources():
        if src[2] == rpm.RPMBUILD_ISPATCH:
            altpatch.append(src[0])

    for p in refpatch:
        if not p in altpatch:
            warnings.append("missing patch '%s'" % p)

    for p in altpatch:
        if not p in refpatch:
            warnings.append("extra patch '%s'" % p)

    return warnings


def compare_specs(refspec, altspec):
    warnings = []

    for w in compare_header(refspec, altspec):
        warnings.append(w)
    for w in compare_sources(refspec, altspec):
        warnings.append(w)
    for w in compare_patches(refspec, altspec):
        warnings.append(w)

    return warnings

def load_suppressions(file):
    if not os.path.exists(file):
        return []

    supp = []
    s = open(suppressionfile)
    try:
        while 1:
            line = s.readline()
            if not line:
                break;

            line = line[0:-1]
            supp.append(line)
    finally:
        s.close()

    return supp



scratchdir = mkdtemp("rpm-source-compare")

if len(sys.argv) != 4:
    print "syntax: %s REFERENCE-SPEC ALTERNATE-SPEC SUPPRESSIONS" % sys.argv[0]
    sys.exit(1)

refspecfile = sys.argv[1]
altspecfile = sys.argv[2]
suppressionfile = sys.argv[3]

ts = rpm.ts()

refspec = ts.parseSpec(refspecfile)
altspec = ts.parseSpec(altspecfile)
suppressions = load_suppressions(suppressionfile)


warnings = []
for w in compare_specs(refspec, altspec):
    if not w in suppressions:
        warnings.append(w)

if len(warnings) == 0:
    print "PASS"
else:
    for w in warnings:
        print "WARNING %s" % w
