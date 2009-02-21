%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

# NOTES, please read these carefully first:
#
# . We only build a few libraries at the moment, those listed in
#   %{subdirs} below.  We could build more without too much effort.
#
# . We should build our own qmake instead of relying on the one
#   from the native Fedora package.  The reason is so that we can
#   set the default include and library paths correctly.

%define subdirs src/corelib src/xml src/network src/gui src/winmain

Name:           mingw32-qt-win
Version:        4.5.0
Release:        0.2.rc1%{?dist}
Summary:        Qt for Windows

License:        GPLv2+
Group:          Development/Libraries

URL:            http://www.qtsoftware.com/
Source0:        ftp://ftp.trolltech.no/qt/source/qt-win-opensource-src-%{version}-rc1.zip

# To make the configure patch - see below.
Source1:        qt-win-configure.sh

# Override .qmake.cache
Source2:        qmake.cache.in

# Special cross-compilation qmake target.
Source3:        qmake.conf
Source4:        qplatformdefs.h

# Qt-win is supplied with a binary configure.exe.  Although we have source
# for this, (a) it can't be compiled on Linux, and (b) we cannot run
# the Windows binary during the build.  Instead we run the command by
# hand and create this diff to record what it did.
#
# Generate this patch using "qt-win-configure.sh".
Patch0:         qt-win-configure.patch

Patch11:        mingw32-qt-4.4.3-no-fpu-functions.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils

# For the native qmake, moc programs.
# Note that the precise same native version is required - eg. moc will
# not work unless it's the same version.
#BuildRequires:  qt-devel = %{version}  Stupid, can't write this ...
BuildRequires:  qt-devel

BuildRequires:  zip
BuildRequires:  dos2unix

# This is required because we want qmake, but also because we
# install the cross-compile qmake specs into a directory owned
# by this package.
Requires:       qt-devel


%description
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


%prep
%setup -q -n qt-win-opensource-src-%{version}-rc1

%patch0 -p1

%patch11 -p1

for f in LICENSE.GPL2 LICENSE.GPL3 GPL_EXCEPTION_ADDENDUM.TXT GPL_EXCEPTION.TXT OPENSOURCE-NOTICE.TXT README; do
  dos2unix --keepdate $f
done

# Override the .qmake.cache file.
rm .qmake.cache
sed -e s,@builddir@,$(pwd),g < %{SOURCE2} > .qmake.cache

# Cross-compilation qmake target.
mkdir mkspecs/fedora-win32-cross
cp %{SOURCE3} %{SOURCE4} mkspecs/fedora-win32-cross


%build
for d in %{subdirs}; do
  # Precompiled headers from a previous iteration of this loop
  # cause the compiler deep confusion, so make sure any are removed
  # _and_ the PCH directories are fresh and empty.
  rm -rf tmp/obj/release_shared/qt_pch.h.gch
  mkdir -p tmp/obj/release_shared/qt_pch.h.gch
  rm -rf tmp/obj/release_shared/qt_gui_pch.h.gch
  mkdir -p tmp/obj/release_shared/qt_gui_pch.h.gch

  # Now build in this directory.
  pushd $d
  qmake-qt4 -win32 *.pro
  make %{?_smp_mflags}
  popd
done


%install
rm -rf $RPM_BUILD_ROOT

for d in %{subdirs}; do
  # As above ... WTF is Qt doing confusing make and make install??
  rm -rf tmp/obj/release_shared/qt_pch.h.gch
  mkdir -p tmp/obj/release_shared/qt_pch.h.gch
  rm -rf tmp/obj/release_shared/qt_gui_pch.h.gch
  mkdir -p tmp/obj/release_shared/qt_gui_pch.h.gch

  pushd $d
  make %{?_smp_mflags} INSTALL_ROOT=$RPM_BUILD_ROOT install
  popd
done

# Qt ignores our carefully configured directories and just
# puts stuff in default directories.  Move them to the proper
# places ...
# (Actually this may be because we are using the native qmake)
mkdir -p $RPM_BUILD_ROOT%{_mingw32_includedir}
mv $RPM_BUILD_ROOT%{_includedir}/* $RPM_BUILD_ROOT%{_mingw32_includedir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_libdir}
mv $RPM_BUILD_ROOT%{_libdir}/*.dll $RPM_BUILD_ROOT%{_mingw32_bindir}
mv $RPM_BUILD_ROOT%{_libdir}/*.a $RPM_BUILD_ROOT%{_mingw32_libdir}
rm $RPM_BUILD_ROOT%{_libdir}/qt4/bin/*
rm $RPM_BUILD_ROOT%{_libdir}/*.prl

# Cross-compiler qmake specs.
mkdir -p $RPM_BUILD_ROOT%{_libdir}/qt4/mkspecs/fedora-win32-cross
cp %{SOURCE3} %{SOURCE4} \
  $RPM_BUILD_ROOT%{_libdir}/qt4/mkspecs/fedora-win32-cross


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc configure.output
%doc LICENSE.GPL2 LICENSE.GPL3 GPL_EXCEPTION_ADDENDUM.TXT GPL_EXCEPTION.TXT
%doc OPENSOURCE-NOTICE.TXT README
%{_mingw32_bindir}/QtCore4.dll
%{_mingw32_bindir}/QtGui4.dll
%{_mingw32_bindir}/QtNetwork4.dll
%{_mingw32_bindir}/QtXml4.dll
%{_mingw32_libdir}/libQtCore4.a
%{_mingw32_libdir}/libQtGui4.a
%{_mingw32_libdir}/libQtNetwork4.a
%{_mingw32_libdir}/libQtXml4.a
%{_mingw32_libdir}/libqtmain.a
%{_mingw32_includedir}/Qt/
%{_mingw32_includedir}/QtCore/
%{_mingw32_includedir}/QtGui/
%{_mingw32_includedir}/QtNetwork/
%{_mingw32_includedir}/QtXml/
%{_libdir}/qt4/mkspecs/fedora-win32-cross


%changelog
* Sat Feb 21 2009 Richard W.M. Jones <rjones@redhat.com> - 4.5.0-0.2.rc1
- Update to Qt 4.5.0-rc1.

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.3-4
- Rebuild for mingw32-gcc 4.4

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.3-3
- Fix required for older W32API in Fedora 10.

* Sun Feb  1 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.3-2
- Initial RPM release.
