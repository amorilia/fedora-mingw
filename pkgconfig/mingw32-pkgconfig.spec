%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Summary: A tool for determining compilation options
Name: mingw32-pkgconfig
Version: 0.23
Release: 1%{?dist}
Epoch: 1
License: GPLv2+
URL: http://pkgconfig.freedesktop.org
Group: Development/Tools
Source:  http://www.freedesktop.org/software/pkgconfig/releases/pkg-config-%{version}.tar.gz
# https://bugs.freedesktop.org/show_bug.cgi?id=5703
Patch1:  pkgconfig-0.15.0-reqprov.patch
# don't call out to glib-config, since our glib-config is a pkg-config wrapper
Patch2:  pkg-config-0.21-compat-loop.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=16095
Patch3: pkg-config-lib64-excludes.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
# Any additional BuildRequires.
BuildRequires:  mingw32-glib2

%description
The pkgconfig tool determines compilation options. For each required
library, it reads the configuration file and outputs the necessary
compiler and linker flags.

%prep
%setup -n pkg-config-%{version} -q
%patch1 -p1 -b .reqprov
%patch2 -p1 -b .compat-loop
%patch3 -p0 -b .lib64

%build
%{_mingw32_configure} --disable-shared --with-pc-path=%{_mingw32_libdir}/pkgconfig:%{_mingw32_datadir}/pkgconfig
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_mingw32_libdir}/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_mingw32_datadir}/pkgconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS README NEWS COPYING
%{_mingw32_mandir}/man1/pkg-config.1
%{_mingw32_bindir}/pkg-config.exe
%{_mingw32_libdir}/pkgconfig
%{_mingw32_datadir}/pkgconfig
%{_mingw32_datadir}/aclocal/pkg.m4

%changelog
* Wed Oct 7 2009 Amorilia <amorilia@users.sourceforge.net> - 1:0.23-1
- Initial RPM release.
