%define debug_package %{nil}

Name:           mingw-filesystem
Version:        1
Release:        1%{?dist}
Summary:        MinGW base filesystem and environment

Group:          Development/Libraries
License:        GPLv2+
URL:            http://hg.et.redhat.com/misc/fedora-mingw--devel/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Source0:        mingw-COPYING
Source1:        mingw-macros.mingw
Source2:        mingw.sh
Source3:        mingw.csh

Requires:       setup
Requires:       rpm


%description
This package contains the base filesystem layout, RPM macros and
environment for all Fedora MinGW packages.

This environment is maintained by the Fedora MinGW SIG at:

  http://fedoraproject.org/wiki/SIGs/MinGW


%prep
%setup -q -c -T
cp %{SOURCE0} COPYING


%build
# nothing


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m 644 %{SOURCE2} %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.mingw

mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32

# GCC requires these directories, even though they contain links
# to binaries which are also installed in /usr/bin etc.  These
# contain Fedora native binaries.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/lib

# The MinGW system root which will contain Windows native binaries
# and Windows-specific header files, man pages, pkgconfig, etc.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/doc
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/include
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/sys
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/doc
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man{1,2,3,4,5,6,7,8,l,n}

# Note that some packages try to install in
# /usr/i686-pc-mingw32/sys-root/mingw/man and
# /usr/i686-pc-mingw32/sys-root/mingw/doc
# but these are both packaging bugs.


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING
%config(noreplace) %{_sysconfdir}/rpm/macros.mingw
%config(noreplace) %{_sysconfdir}/profile.d/mingw.sh
%config(noreplace) %{_sysconfdir}/profile.d/mingw.csh
%{_prefix}/i686-pc-mingw32/


%changelog
* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1-1
- Basic filesystem layout.
