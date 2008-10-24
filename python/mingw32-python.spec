%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

%{!?__python_ver:%define __python_ver EMPTY}
#define __python_ver 25
%define unicode ucs4

%define _default_patch_fuzz     2

%if "%{__python_ver}" != "EMPTY"
%define main_python 0
%define python python%{__python_ver}
%define tkinter tkinter%{__python_ver}
%else
%define main_python 1
%define python python
%define tkinter tkinter
%endif

%define pybasever 2.5
%define tools_dir %{_libdir}/python%{pybasever}/Tools
%define demo_dir %{_libdir}/python%{pybasever}/Demo
%define doc_tools_dir %{_libdir}/python%{pybasever}/Doc/tools

Name:           mingw32-python
Version:        2.5.2
Release:        1%{?dist}
Summary:        MinGW Windows port of Python programming language

License:        Python
Group:          Development/Libraries
URL:            http://www.python.org/
Source0:        http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 30
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
#BuildPrereq:    expat-devel
#BuildPrereq:    libGL-devel
#BuildPrereq:    tk
#BuildPrereq:    tix
BuildPrereq:    mingw32-gcc-c++
#BuildPrereq:    libX11-devel
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

# Required for cross-build.
BuildRequires:  python = %{version}

# Patches from native Fedora package.
Patch0: python-2.5-config.patch
Patch1: Python-2.2.1-pydocnogui.patch
Patch2: python-2.3.4-pydocnodoc.patch
Patch3: python-2.4.1-canonicalize.patch
Patch4: python-2.5-cflags.patch
Patch5: python-2.5.1-ctypes-exec-stack.patch
Patch6: python-2.5.1-plural-fix.patch
Patch7: python-2.5.1-sqlite-encoding.patch
Patch8: python-2.5-xmlrpclib-marshal-objects.patch
Patch9: python-2.5-tkinter.patch
Patch10: python-2.5.2-binutils-no-dep.patch
Patch11: python-2.5.1-codec-ascii-tolower.patch
Patch12: python-2.5.1-pysqlite.patch
Patch13: python-2.5.1-socketmodule-constants.patch
Patch14: python-2.5.1-socketmodule-constants2.patch
Patch15: python-2.5.1-listdir.patch
#Patch50: python-2.5-disable-egginfo.patch
Patch60: python-2.5.2-db47.patch
Patch101: python-2.3.4-lib64-regex.patch
Patch102: python-2.5-lib64.patch
Patch260: python-2.5.2-set_wakeup_fd4.patch
Patch999: python-2.5.CVE-2007-4965-int-overflow.patch
Patch998: python-2.5-CVE-2008-2316.patch

# MinGW-specific patches.
# See: http://bugs.python.org/issue1597850
Patch1000: mingw32-python-2.5.2-cross.patch


%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing.

This packages is the MinGW port of Python development tools and
libraries.


%prep
%setup -q -n Python-%{version}

%patch0 -p1 -b .rhconfig
%patch1 -p1 -b .no_gui
%patch2 -p1 -b .no-doc
%patch3 -p1 -b .canonicalize
%patch4 -p1 -b .cflags
%patch5 -p1 -b .ctypesexec
%patch6 -p1 -b .plural
%patch7 -p1
%patch8 -p1 -b .xmlrpc

# Try not disabling egg-infos, bz#414711
#patch50 -p1 -b .egginfo
%patch60 -p1 -b .db47

%if "%{_lib}" == "lib64"
%patch101 -p1 -b .lib64-regex
%patch102 -p1 -b .lib64
%endif

%patch10 -p1 -b .binutils-no-dep
%patch11 -p1 -b .ascii-tolower
%patch12 -p1 -b .pysqlite-2.3.3-minimal
%patch13 -p1 -b .socketmodule
%patch14 -p1 -b .socketmodule
%patch15 -p1 -b .socketmodule

%ifarch alpha ia64
# 64bit, but not lib64 arches need this too...
%patch101 -p1 -b .lib64-regex
%endif

%patch260 -p1 -b .set_wakeup_fd

%patch999 -p1 -b .cve2007-4965
%patch998 -p0 -b .cve2008-2316

%patch1000 -p1 -b .mingw32

# This shouldn't be necesarry, but is right now (2.2a3)
find -name "*~" |xargs rm -f


%build
export PKG_CONFIG_PATH="%{_mingw32_libdir}/pkgconfig"

# *_FOR_BUILD refer to the build compiler (for building intermediate
# tools), not the cross-compiler.
export CC_FOR_BUILD=gcc
export PYTHON_FOR_BUILD=/usr/bin/python

export CFLAGS="%{_mingw32_cflags} -D_GNU_SOURCE `pkg-config --cflags openssl`"
export LDFLAGS="`pkg-config --libs-only-L openssl`"
export CXXFLAGS="%{_mingw32_cflags} -m32 -D_GNU_SOURCE"
export OPT="%{_mingw32_cflags} -D_GNU_SOURCE"
export LINKCC="%{_mingw32_cc}"
export LDSHARED="%{_mingw32_cc}"
export BLDSHARED="%{_mingw32_cc}"

export CROSS_ROOT=%{_mingw32_prefix}

# Export these to avoid failing a cross-test in configure:
export ac_cv_file__dev_ptmx=no
export ac_cv_file__dev_ptc=no
export ac_cv_printf_zd_format=yes

# Automake is needed to get config.sub & config.guess.
automake --add-missing ||:
# Autoconf is needed because we patched configure.in.
autoconf

./configure \
  --build=%_build --host=%{_mingw32_host} --target=%{_mingw32_target} \
  --prefix=%{_mingw32_prefix} \
  --enable-unicode=%{unicode} \
  --enable-shared
#  --enable-ipv6

make OPT="$CFLAGS"
# %{?_smp_mflags}

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
%{_mingw32_bindir}/foo.dll
%{_mingw32_libdir}/foo.dll.a
# etc.


%changelog
* Fri Oct 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.5.2-1
- Initial RPM release.
