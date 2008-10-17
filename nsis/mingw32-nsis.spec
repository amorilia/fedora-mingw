%define sconsopts VERSION=%{version} PREFIX=%{_prefix} PREFIX_CONF=%{_sysconfdir} SKIPPLUGINS=System DEBUG_SYMBOLS=1 OPTS=1
%define _default_patch_fuzz 2

Name:           mingw32-nsis
Version:        2.39
Release:        5%{?dist}
Summary:        Nullsoft Scriptable Install System

License:        zlib and CPL
Group:          Development/Libraries
URL:            http://nsis.sourceforge.net/
Source0:        http://dl.sourceforge.net/sourceforge/nsis/nsis-%{version}-src.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Patches from Debian (mainly by Paul Wise).
Patch0:         nsis-2.39-debian-64bit-fixes.patch
Patch1:         nsis-2.39-debian-debug-opt.patch

# This patch is required for NSIS to find the correct cross-compiler.
Patch100:       nsis-2.39-mingw32-search.patch

BuildRequires:  mingw32-filesystem >= 20
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  python
BuildRequires:  scons >= 0.96.93

# We build with 'gcc -m32' and that fails on 64 bit platforms when we
# include <gnu/stubs.h>.  On x86-64, this is provided by
# glibc-devel.i386.  Depend on the file explicitly, since only recent
# versions of RPM let you require a package by architecture.
BuildRequires:  /usr/include/gnu/stubs-32.h

# We really need the 32 bit version of this library.  The 64 bit
# version will definitely not work.  XXX Need to do the right thing on
# non-x86 architectures.
BuildRequires:  /usr/lib/libwx_baseu-2.8.so


%description
NSIS, the Nullsoft Scriptable Install System, is a script-driven
Windows installation system.

This package includes native Fedora binaries of makensis (etc.) and
all plugins except for System.dll.  The System.dll plugin cannot be
built natively at this time since it includes inline Microsoft
assembler code.


%prep
%setup -q -n nsis-%{version}-src

%patch0 -p1
%patch1 -p1

%patch100 -p1


%build
scons %{sconsopts}


%install
rm -rf $RPM_BUILD_ROOT

mkdir $RPM_BUILD_ROOT
scons %{sconsopts} PREFIX_DEST=$RPM_BUILD_ROOT install

mv $RPM_BUILD_ROOT%{_docdir}/nsis $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/nsisconf.nsh
%{_includedir}/nsis
%doc %{_docdir}/%{name}-%{version}
%{_datadir}/nsis


%changelog
* Fri Oct 17 2008 Richard W.M. Jones <rjones@redhat.com> - 2.39-5
- Fix the Summary line.

* Wed Oct  8 2008 Richard W.M. Jones <rjones@redhat.com> - 2.39-4
- Initial RPM release.
