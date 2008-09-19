#!/usr/bin/python

import sys
from tempfile import mkdtemp
from os import mkdir, system
import rpm


def compare_header(refspec, altspec):
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
        print "WARNING: different version: '%s': '%s' != '%s': '%s'" % (refname, refver, altname, altver)

    if refver != altver:
        print "WARNING: different license: '%s': '%s' != '%s': '%s'" % (refname, reflic, altname, altlic)

    if refver != altver:
        print "WARNING: different URL: '%s': '%s' != '%s': '%s'" % (refname, refurl, altname, alturl)

def compare_sources(refspec, altspec):
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
            print "WARNING: missing source: '%s'" % s[1]
    for s in altsrc:
        if not s[1] in refsrcname:
            print "WARNING: extra source: '%s'" % s[1]

    for s1 in refsrc:
        for s2 in altsrc:
            if s1[1] != s2[1]:
                continue
            if s1[0] != s2[0]:
                print "WARNING: different base URI for source '%s': '%s' != '%s'" % (s1[1], s1[0], s2[0])


def compare_patches(refspec, altspec):
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
            print "WARNING missing patch '%s'" % p

    for p in altpatch:
        if not p in refpatch:
            print "WARNING extra patch '%s'" % p

scratchdir = mkdtemp("rpm-source-compare")

if len(sys.argv) != 3:
    print "syntax: %s REFERENCE-SPEC ALTERNATE-SPEC" % sys.argv[0]
    sys.exit(1)

refspecfile = sys.argv[1]
altspecfile = sys.argv[2]

ts = rpm.ts()

refspec = ts.parseSpec(refspecfile)
altspec = ts.parseSpec(altspecfile)

compare_header(refspec, altspec)
compare_sources(refspec, altspec)
compare_patches(refspec, altspec)

