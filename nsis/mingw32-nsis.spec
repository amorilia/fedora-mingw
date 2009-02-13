%define sconsopts VERSION=%{version} PREFIX=%{_prefix} PREFIX_CONF=%{_sysconfdir} SKIPPLUGINS=System DEBUG_SYMBOLS=1 OPTS=1
%define _default_patch_fuzz 2

Name:           mingw32-nsis
Version:        2.43
Release:        1%{?dist}
Summary:        Nullsoft Scriptable Install System

License:        zlib and CPL
Group:          Development/Libraries
URL:            http://nsis.sourceforge.net/
Source0:        http://dl.sourceforge.net/sourceforge/nsis/nsis-%{version}-src.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Patches from Debian (mainly by Paul Wise).
Patch0:         nsis-2.42-debian-64bit-fixes.patch
Patch1:         nsis-2.43-debian-debug-opt.patch

BuildRequires:  mingw32-filesystem >= 40
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  python
BuildRequires:  scons
BuildRequires:  wxGTK-devel

# since nsis a 32 bit only apps
ExclusiveArch:  i386 ppc

%description
NSIS, the Nullsoft Scriptable Install System, is a script-driven
Windows installation system.

This package includes native Fedora binaries of makensis (etc.) and
all plugins except for System.dll.  The System.dll plugin cannot be
built natively at this time since it includes inline Microsoft
assembler code.


%prep
%setup -q -n nsis-%{version}-src

%patch0 -p1 -b .64bit
%patch1 -p1 -b .debug


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
%doc %{_docdir}/%{name}-%{version}
%config(noreplace) %{_sysconfdir}/nsisconf.nsh
%{_bindir}/*
#{_includedir}/nsis
%{_datadir}/nsis


%changelog
* Fri Feb 13 2009 Levente Farkas <lfarkas@lfarkas.org> - 2.43-1
- update to the latest upstream

* Wed Jan 14 2009 Levente Farkas <lfarkas@lfarkas.org> - 2.42-1
- update to the latest upstream
- a few small changes

* Fri Oct 17 2008 Richard W.M. Jones <rjones@redhat.com> - 2.39-5
- Fix the Summary line.

* Wed Oct  8 2008 Richard W.M. Jones <rjones@redhat.com> - 2.39-4
- Initial RPM release.
