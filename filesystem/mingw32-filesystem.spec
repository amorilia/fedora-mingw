%define debug_package %{nil}

Name:           mingw32-filesystem
Version:        27
Release:        1%{?dist}
Summary:        MinGW base filesystem and environment

Group:          Development/Libraries
License:        GPLv2+
URL:            http://hg.et.redhat.com/misc/fedora-mingw--devel/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Source0:        mingw32-COPYING
Source1:        mingw32-macros.mingw32
Source2:        mingw32.sh
Source3:        mingw32.csh
Source4:        mingw32-find-requires.sh
Source5:        mingw32-find-provides.sh

Requires:       setup
Requires:       rpm

# These are actually provided by Windows itself, or Wine.
Provides:       mingw32(gdi32.dll)
Provides:       mingw32(kernel32.dll)
Provides:       mingw32(ole32.dll)
Provides:       mingw32(mscoree.dll)
Provides:       mingw32(msvcrt.dll)
Provides:       mingw32(user32.dll)

Obsoletes:      mingw-filesystem = %{version}-%{release}
Provides:       mingw-filesystem < 26


%description
This package contains the base filesystem layout, RPM macros and
environment for all Fedora MinGW packages.

This environment is maintained by the Fedora MinGW SIG at:

  http://fedoraproject.org/wiki/SIGs/MinGW


%prep
%setup -q -c -T
cp %{SOURCE0} COPYING
sed 's/@VERSION@/%{version}/' < %{SOURCE4} > mingw32-find-requires.sh


%build
# nothing


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m 644 %{SOURCE2} %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.mingw32

mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32

# GCC requires these directories, even though they contain links
# to binaries which are also installed in /usr/bin etc.  These
# contain Fedora native binaries.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/lib

# The MinGW system root which will contain Windows native binaries
# and Windows-specific header files, pkgconfig, etc.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/include
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/sys
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/pkgconfig

mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/aclocal

# We don't normally package manual pages and info files, except
# where those are not supplied by a Fedora native package.  So we
# need to create the directories.
#
# Note that some packages try to install stuff in
#   /usr/i686-pc-mingw32/sys-root/mingw/man and
#   /usr/i686-pc-mingw32/sys-root/mingw/doc
# but those are both packaging bugs.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/doc
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/info
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man{1,2,3,4,5,6,7,8,l,n}

# NB. NOT _libdir
mkdir -p $RPM_BUILD_ROOT/usr/lib/rpm
install -m 0755 mingw32-find-requires.sh $RPM_BUILD_ROOT/usr/lib/rpm
install -m 0755 %{SOURCE5} $RPM_BUILD_ROOT/usr/lib/rpm


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING
%config(noreplace) %{_sysconfdir}/rpm/macros.mingw32
%config(noreplace) %{_sysconfdir}/profile.d/mingw32.sh
%config(noreplace) %{_sysconfdir}/profile.d/mingw32.csh
%{_prefix}/i686-pc-mingw32/
/usr/lib/rpm/mingw32-*


%changelog
* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 27-1
- Begin the grand renaming of mingw -> mingw32.
- Added mingw32(mscoree.dll).

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 25-1
- Add shared aclocal directory.

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 24-1
- Remove mingw-defs, since no longer used.
- Add _mingw_infodir.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 23-1
- Add macros for find-provides/requires scripts

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 22-1
- Windows provides OLE32.DLL.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 21-1
- Allow '.' in dll names for find-requires
- Windows provides GDI32.DLL.

* Fri Sep  5 2008 Richard W.M. Jones <rjones@redhat.com> - 20-1
- On 64 bit install in /usr/lib/rpm always.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 19-1
- 'user32.dll' is provided by Windows.
- Allow '-' in DLL names.
- More accurate detection of DLLs in requires/provides scripts.

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
