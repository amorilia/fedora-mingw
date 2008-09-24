%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-cairo
Version:        1.7.4
Release:        4%{?dist}
Summary:        MinGW Windows Cairo library

License:	LGPLv2 or MPLv1.1
URL:		http://cairographics.org
Source0:	http://cairographics.org/snapshots/cairo-%{version}.tar.gz
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-libxml2
BuildRequires:  mingw32-pixman
BuildRequires:  mingw32-freetype
BuildRequires:  mingw32-libpng
BuildRequires:  mingw32-fontconfig
BuildRequires:  pkgconfig

%description
MinGW Windows Cairo library.


%prep
%setup -q -n cairo-%{version}

%build
%{_mingw32_configure} --disable-xlib --disable-xcb --enable-win32 --enable-png --enable-freetype
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT%{_mingw32_libdir}/charset.alias

rm -f $RPM_BUILD_ROOT%{_mingw32_libdir}/libcairo.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libcairo-2.dll
%{_mingw32_includedir}/cairo/
%{_mingw32_libdir}/libcairo.dll.a
%{_mingw32_libdir}/libcairo.la
%{_mingw32_libdir}/pkgconfig/cairo-ft.pc
%{_mingw32_libdir}/pkgconfig/cairo-pdf.pc
%{_mingw32_libdir}/pkgconfig/cairo-png.pc
%{_mingw32_libdir}/pkgconfig/cairo-ps.pc
%{_mingw32_libdir}/pkgconfig/cairo-svg.pc
%{_mingw32_libdir}/pkgconfig/cairo-win32-font.pc
%{_mingw32_libdir}/pkgconfig/cairo-win32.pc
%{_mingw32_libdir}/pkgconfig/cairo.pc
%{_mingw32_datadir}/gtk-doc/html/cairo/


%changelog
* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.7.4-4
- Rename mingw -> mingw32.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 1.7.4-3
- Added dep on pkgconfig

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.7.4-2
- Remove static libraries.
- Fix source URL.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.7.4-1
- Initial RPM release
