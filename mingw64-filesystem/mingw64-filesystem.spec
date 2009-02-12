%define debug_package %{nil}

Name:           mingw64-filesystem
Version:        10
Release:        1%{?dist}
Summary:        MinGW base filesystem and environment

Group:          Development/Libraries
License:        GPLv2+
URL:            http://hg.et.redhat.com/misc/fedora-mingw--devel/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Source0:        COPYING
Source1:        macros.mingw64
Source2:        mingw64.sh
#Source3:        mingw64.csh
Source4:        mingw64-find-requires.sh
Source5:        mingw64-find-provides.sh
Source6:        mingw64-scripts.sh
Source7:        mingw64-rpmlint.config

Requires:       setup
Requires:       rpm
Requires:       rpmlint >= 0.85-2

BuildRequires:  rpmlint >= 0.85-2

# Note about 'Provides: mingw64(foo.dll)'
# ------------------------------------------------------------
#
# We want to be able to build & install mingw64 libraries without
# necessarily needing to install wine.  (And certainly not needing to
# install Windows!)  There is no requirement to have wine installed in
# order to use the mingw toolchain to develop software (ie. to
# compile more stuff on top of it), so why require that?
#
# So for expediency, this base package provides the "missing" DLLs
# from Windows.  Another way to do it would be to exclude these
# proprietary DLLs in our find-requires checking script - essentially
# it comes out the same either way.
#
#Provides:       mingw64(gdi32.dll)


%description
This package contains the base filesystem layout, RPM macros and
environment for all Fedora MinGW packages.

This environment is maintained by the Fedora MinGW SIG at:

  http://fedoraproject.org/wiki/SIGs/MinGW


%prep
%setup -q -c -T
cp %{SOURCE0} COPYING
sed 's/@VERSION@/%{version}/' < %{SOURCE4} > mingw64-find-requires.sh


%build
# nothing


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
install -m 755 %{SOURCE6} $RPM_BUILD_ROOT%{_libexecdir}/mingw64-scripts

mkdir -p $RPM_BUILD_ROOT%{_bindir}
pushd $RPM_BUILD_ROOT%{_bindir}
for i in mingw64-configure mingw64-make; do
  ln -s %{_libexecdir}/mingw64-scripts $i
done
popd

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
#install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.mingw64

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpmlint
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/rpmlint/

mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32

# These directories are used by GCC for cross-compilation.
# NOTE different contents from mingw32.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/lib

# The system root which will contain Windows native binaries
# and Windows-specific header files, pkgconfig, etc.
# NOTE different from mingw32.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/sys-root
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/sys-root/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/sys-root/include
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/sys-root/include/sys
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/sys-root/lib
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/sys-root/lib/pkgconfig

# GCC wants to look in include64/ directory for some reason.
pushd $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/sys-root
ln -s include include64
popd

# We don't normally package manual pages and info files, except
# where those are not supplied by a Fedora native package.  So we
# need to create the directories.
#
# Note that some packages try to install stuff in
#   /usr/x86_64-pc-mingw32/sys-root/man and
#   /usr/x86_64-pc-mingw32/sys-root/doc
# but those are both packaging bugs.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/sys-root/share
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/sys-root/share/doc
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/sys-root/share/info
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/sys-root/share/man
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/sys-root/share/man/man{1,2,3,4,5,6,7,8,l,n}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/sys-root/share/aclocal

pushd $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/sys-root
ln -s . mingw
popd


# NB. NOT _libdir
mkdir -p $RPM_BUILD_ROOT/usr/lib/rpm
install -m 0755 mingw64-find-requires.sh $RPM_BUILD_ROOT/usr/lib/rpm
install -m 0755 %{SOURCE5} $RPM_BUILD_ROOT/usr/lib/rpm


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING
%config(noreplace) %{_sysconfdir}/rpm/macros.mingw64
%config(noreplace) %{_sysconfdir}/profile.d/mingw64.sh
#%config(noreplace) %{_sysconfdir}/profile.d/mingw64.csh
%config(noreplace) %{_sysconfdir}/rpmlint/mingw64-rpmlint.config
%{_bindir}/mingw64-configure
%{_bindir}/mingw64-make
%{_libexecdir}/mingw64-scripts
%{_prefix}/x86_64-pc-mingw32/
/usr/lib/rpm/mingw64-*


%changelog
* Wed Feb 11 2009 Richard W.M. Jones <rjones@redhat.com> - 10-1
- Start mingw64 development.

* Sun Feb  1 2009 Richard W.M. Jones <rjones@redhat.com> - 46-1
- Unset PKG_CONFIG_PATH because /usr/lib/rpm/macros sets it (Erik van
  Pienbroek).

* Wed Jan 28 2009 Richard W.M. Jones <rjones@redhat.com> - 45-1
- Use PKG_CONFIG_LIBDIR instead of PKG_CONFIG_PATH so that native pkgconfig
  is never searched.

* Mon Jan 26 2009 Richard W.M. Jones <rjones@redhat.com> - 44-1
- Install rpmlint overrides file to suppress some rpmlint warnings.

* Sat Jan 24 2009 Richard W.M. Jones <rjones@redhat.com> - 43-6
- Don't claim C++ compiler exists if it's not installed, as this
  breaks autoconf and (in particular) libtool.

* Wed Jan 14 2009 Richard W.M. Jones <rjones@redhat.com> - 42-1
- Add pseudo-provides secur32.dll

* Wed Dec 17 2008 Levente Farkas <lfarkas@lfarkas.org> - 41-1
- Re-add mingw32-make

* Sat Dec  6 2008 Levente Farkas <lfarkas@lfarkas.org> - 40-2
- Rewrite mingw32-scripts to run in the current shell
- (Re-add mingw32-make) - Removed by RWMJ.
- Add mingw32-env to mingw32.sh

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 39-3
- Unify mingw32-filesystem packages from all three branches again, and test.
- Fix mingw32-scripts so it can handle extra parameters correctly.
- Remove mingw32-env & mingw32-make since neither of them actually work.

* Sun Nov 23 2008 Richard Jones <rjones@redhat.com> - 38-1
- Added mingw32(glut32.dll).

* Wed Nov 19 2008 Richard Jones <rjones@redhat.com> - 37-1
- Revert part of the 36-1 patch.  --build option to configure was wrong.

* Wed Nov 19 2008 Richard Jones <rjones@redhat.com> - 36-1
- Greatly improved macros (Levente Farkas).
- Added -mms-bitfields.

* Thu Nov 13 2008 Richard Jones <rjones@redhat.com> - 35-1
- Added mingw32(wldap32.dll) pseudo-provides.

* Wed Oct 29 2008 Richard Jones <rjones@redhat.com> - 34-1
- Set --prefix correctly.

* Wed Oct 29 2008 Richard Jones <rjones@redhat.com> - 33-1
- Remove mingw32.{sh,csh} which are unused.

* Mon Oct 27 2008 Richard Jones <rjones@redhat.com> - 32-1
- Add mingw32-configure script.

* Mon Oct 27 2008 Richard Jones <rjones@redhat.com> - 31-1
- Update the spec file with explanation of the 'Provides: mingw32(...)'
  lines for Windows system DLLs.

* Mon Oct  6 2008 Richard Jones <rjones@redhat.com> - 30-1
- Added _mingw32_cxx.

* Thu Sep 25 2008 Richard Jones <rjones@redhat.com> - 29-1
- Added _mingw32_as, _mingw32_dlltool, _mingw32_windres.

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
