%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

%define py3kdate 20081210

%define unicode ucs4

%define pybasever 3.1
%define tools_dir %{_libdir}/python%{pybasever}/Tools
%define demo_dir %{_libdir}/python%{pybasever}/Demo
%define doc_tools_dir %{_libdir}/python%{pybasever}/Doc/tools

Name:           mingw32-python3
Version:        3.1
Release:        0.1.svn%{py3kdate}.%{?dist}
Summary:        MinGW Windows port of Python 3 programming language

License:        Python
Group:          Development/Libraries
URL:            http://www.python.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# Created by:
# svn co http://svn.python.org/projects/python/branches/py3k py3k
# tar --exclude .svn -zcf /tmp/py3k-%{py3kdate}.tar.gz py3k
Source0:        py3k-%{py3kdate}.tar.gz

# These are needed by ./configure when cross-compiling.
Source1000:     config.guess
Source1001:     config.sub

# The Python configure.in uses AC_STRUCT_ST_BLOCKS which wants a
# replacement fileblocks.c file if stat.st_blocks doesn't exist.
# We could use 'lib/fileblocks.c' from Gnulib (under GPL), but
# instead an empty file will do.  (Thanks Jim Meyering).
Source1002:     fileblocks.c

# Basic cross-compilation patch, mainly derived from
# http://bugs.python.org/issue1597850
Patch1000:      mingw32-python-3.1-cross-build.patch

# Windows has setlocale but not LC_CTYPE.
Patch1001:      mingw32-python-3.1-lc_ctype.patch

# Get posix module working.
Patch1002:      mingw32-python-3.1-posixmodule.patch

# Get miscellaneous modules working.
Patch1003:      mingw32-python-3.1-misc-modules.patch

# Get pwdmodule working (only barely functional on Windows).
Patch1004:      mingw32-python-3.1-pwdmodule.patch

BuildRequires:  mingw32-filesystem >= 40
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

# Only some of these deps have been ported to MinGW so far.  The
# rest are listed here as they appear in the native python spec,
# just so remember them.
BuildPrereq:    mingw32-readline
BuildPrereq:    mingw32-openssl
#BuildPrereq:    gmp-devel
#BuildPrereq:    ncurses-devel  <- doesn't exist for MinGW
BuildPrereq:    mingw32-pdcurses
BuildPrereq:    mingw32-gdbm
BuildPrereq:    mingw32-zlib
BuildPrereq:    mingw32-expat
#BuildPrereq:    libGL-devel
#BuildPrereq:    tk
#BuildPrereq:    tix
BuildPrereq:    mingw32-gcc-c++
#BuildPrereq:    libX11-devel <- no equivalent for MinGW
#BuildPrereq:    glibc-devel <- no equivalent for MinGW
#BuildPrereq:    tcl-devel
#BuildPrereq:    tk-devel
#BuildPrereq:    tix-devel
BuildPrereq:    mingw32-bzip2
BuildPrereq:    mingw32-sqlite
#BuildPrereq:    db4-devel >= 4.7

# Native dependencies.
BuildPrereq:    bzip2
BuildPrereq:    tar
BuildPrereq:    /usr/bin/find
BuildPrereq:    pkgconfig
BuildPrereq:    autoconf

# Will be required for cross-build.
#BuildRequires:  python = %{version}


%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing.

This packages is the MinGW port of the CPython interpreter,
development tools and libraries.


%prep
%setup -q -n py3k

%patch1000 -p0
%patch1001 -p0
%patch1002 -p0
%patch1003 -p0
%patch1004 -p0

cp %{SOURCE1000} .
cp %{SOURCE1001} .
cp %{SOURCE1002} Python/

autoreconf


%build
# Export these to avoid failing a cross-test in configure:
export ac_cv_file__dev_ptmx=no
export ac_cv_file__dev_ptc=no
export ac_cv_printf_zd_format=yes

%{_mingw32_configure} \
  --enable-unicode=%{unicode} \
  --enable-shared
#  --enable-ipv6

make OPT="%{_mingw32_cflags}"

exit 1

topdir=`pwd`
LD_LIBRARY_PATH=$topdir \
  $topdir/python \
    Tools/scripts/pathfix.py -i "%{_bindir}/env python%{pybasever}" .
# Rebuild with new python
# We need a link to a versioned python in the build directory
ln -s python python%{pybasever}
LD_LIBRARY_PATH=$topdir \
  PATH=$PATH:$topdir \
  make -s OPT="$CFLAGS"
# %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
exit 1
make DESTDIR=$RPM_BUILD_ROOT install

# Remove static libraries but DON'T remove *.dll.a files.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libfoo.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc XXX
%{_mingw32_bindir}/foo.dll
%{_mingw32_libdir}/foo.dll.a
# etc.


%changelog
* Fri Oct 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.5.2-1
- Initial RPM release.
