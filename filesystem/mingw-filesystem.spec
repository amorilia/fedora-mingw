%define debug_package %{nil}

Name:           mingw-filesystem
Version:        17
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
Source4:        mingw-find-requires.sh
Source5:        mingw-find-provides.sh
Source6:        mingw-defs

Requires:       setup
Requires:       rpm

# These are actually provided by Windows itself, or Wine.
Provides:       mingw(msvcrt.dll)
Provides:       mingw(kernel32.dll)


%description
This package contains the base filesystem layout, RPM macros and
environment for all Fedora MinGW packages.

This environment is maintained by the Fedora MinGW SIG at:

  http://fedoraproject.org/wiki/SIGs/MinGW


%prep
%setup -q -c -T
cp %{SOURCE0} COPYING
sed 's/@VERSION@/%{version}/' < %{SOURCE4} > mingw-find-requires.sh


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

mkdir -p $RPM_BUILD_ROOT%{_libdir}/rpm
install -m 0755 mingw-find-requires.sh $RPM_BUILD_ROOT%{_libdir}/rpm
install -m 0755 %{SOURCE5} $RPM_BUILD_ROOT%{_libdir}/rpm
install -m 0644 %{SOURCE6} $RPM_BUILD_ROOT%{_libdir}/rpm


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING
%config(noreplace) %{_sysconfdir}/rpm/macros.mingw
%config(noreplace) %{_sysconfdir}/profile.d/mingw.sh
%config(noreplace) %{_sysconfdir}/profile.d/mingw.csh
%{_prefix}/i686-pc-mingw32/
%{_libdir}/rpm/mingw-*


%changelog
* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 17-1
- Automatically add mingw-filesystem and mingw-runtime requires.
- Add --prefix to _mingw_configure macro.
- Three backslashes required on each continuation line in RPM macros.

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 14-1
- Fix path to mingw-find-requires/provides scripts.

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 12-1
- Put CFLAGS on a single line to avoid problems in some configure scripts.

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 10-1
- Provides certain base Windows DLLs (not literally).

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 9-1
- Include RPM dependency generators and definitions.

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 4-1
- Add _mingw_cc/cflags/etc. and _mingw_configure macros.

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3-1
- Add _mingw_host macro.

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 2-1
- Add _mingw_sysroot macro.
- Add _mingw_target macro.

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1-1
- Basic filesystem layout.
