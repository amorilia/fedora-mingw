%define sconsopts VERSION=%{version} PREFIX=%{_prefix} PREFIX_CONF=%{_sysconfdir} SKIPPLUGINS=System DEBUG_SYMBOLS=1 OPTS=1

Name:           mingw32-nsis
Version:        2.39
Release:        1%{?dist}
Summary:        MinGW Windows libxml2 XML processing library

License:        zlib and CPL
Group:          Development/Libraries
URL:            http://nsis.sourceforge.net/
Source0:        http://dl.sourceforge.net/sourceforge/nsis/nsis-%{version}-src.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Patches from Debian (mainly by Paul Wise).
Patch0:         nsis-2.39-debian-64bit-fixes.patch
Patch1:         nsis-2.39-debian-debug-opt.patch

# This patch is required for NSIS to find the correct cross-compiler.
Patch2:         nsis-2.39-mingw32-search.patch

BuildRequires:  mingw32-filesystem >= 20
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  python
BuildRequires:  scons >= 0.96.93
BuildRequires:  wxGTK-devel


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
%patch2 -p1


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


%changelog
* Mon Sep 22 2008 Richard W.M. Jones <rjones@redhat.com> - 2.39-1
- Initial RPM release.
