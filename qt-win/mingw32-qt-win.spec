%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-qt-win
Version:        4.4.3
Release:        1%{?dist}
Summary:        Qt for Windows

License:        GPLv2+
Group:          Development/Libraries

URL:            http://www.qtsoftware.com/
Source0:        ftp://ftp.trolltech.no/qt/source/qt-win-opensource-src-%{version}.zip
Source1:        qt-win-configure.sh

# Qt-win is supplied with a binary configure.exe.  Although we have source
# for this, (a) it can't be compiled on Linux, and (b) we cannot run
# the Windows binary during the build.  Instead we run the command by
# hand and create this diff to record what it did.
#
# The full configure command we ran is in qt-win-configure.sh.
Patch0:         qt-win-configure.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

# For the native qmake program.
BuildRequires:  qt-devel


%description
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


%prep
%setup -q -n qt-win-opensource-src-%{version}
%patch0 -p1


%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove static libraries but DON'T remove *.dll.a files.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libfoo.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc LICENSE
%{_mingw32_bindir}/foo.dll
%{_mingw32_libdir}/foo.dll.a
# etc.


%changelog
* Sun Feb  1 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.3-1
- Initial RPM release.
