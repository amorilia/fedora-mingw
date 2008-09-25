%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-pdcurses
Version:        3.4
Release:        1%{?dist}
Summary:        Curses library for MinGW

License:        Public Domain
Group:          Development/Libraries
URL:            http://pdcurses.sourceforge.net/
Source0:        http://dl.sourceforge.net/sourceforge/pdcurses/PDCurses-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Patch0:         mingw32-pdcurses-3.4-build.patch

BuildRequires:  mingw32-filesystem >= 26
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils


%description
PDCurses is a public domain curses library for DOS, OS/2, Win32, X11
and SDL, implementing most of the functions available in X/Open and
System V R4 curses. It supports many compilers for these
platforms. The X11 port lets you recompile existing text-mode curses
programs to produce native X11 applications.

Note that ncurses is not available for MinGW / Windows.  Applications
which need curses functionality can use this package, provided they
don't use any of the extensions specific to ncurses.


%prep
%setup -q -n PDCurses-%{version}
%patch0 -p1


%build
pushd win32
make -f mingwin32.mak \
  CC=%{_mingw32_cc} \
  LINK=%{_mingw32_cc} \
  WIDE=Y UTF8=Y DLL=Y
popd


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_includedir}

install win32/*.exe $RPM_BUILD_ROOT%{_mingw32_bindir}
install win32/pdcurses.dll $RPM_BUILD_ROOT%{_mingw32_bindir}/pdcurses.dll
install win32/pdcurses.a $RPM_BUILD_ROOT%{_mingw32_libdir}/pdcurses.dll.a
install curses.h panel.h term.h $RPM_BUILD_ROOT%{_mingw32_includedir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/pdcurses.dll
%{_mingw32_libdir}/pdcurses.dll.a
%{_mingw32_includedir}/curses.h
%{_mingw32_includedir}/panel.h
%{_mingw32_includedir}/term.h
%{_mingw32_bindir}/firework.exe
%{_mingw32_bindir}/newdemo.exe
%{_mingw32_bindir}/ptest.exe
%{_mingw32_bindir}/rain.exe
%{_mingw32_bindir}/testcurs.exe
%{_mingw32_bindir}/tuidemo.exe
%{_mingw32_bindir}/xmas.exe
%{_mingw32_bindir}/worm.exe


%changelog
* Thu Sep 25 2008 Richard Jones <rjones@redhat.com> - 3.4-1
- Initial RPM release.
