%define __strip %{_mingw_strip}
%define __objdump %{_mingw_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw_findrequires}
%define __find_provides %{_mingw_findprovides}

Name:           mingw-cairo
Version:        1.7.4
Release:        3%{?dist}
Summary:        MinGW Windows Cairo library

License:	LGPLv2 or MPLv1.1
URL:		http://cairographics.org
Source0:	http://cairographics.org/snapshots/cairo-%{version}.tar.gz
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 23
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-libxml2
BuildRequires:  mingw-pixman
BuildRequires:  mingw-freetype
BuildRequires:  mingw-libpng
BuildRequires:  mingw-fontconfig
BuildRequires:  pkgconfig

%description
MinGW Windows Cairo library.


%prep
%setup -q -n cairo-%{version}

%build
%{_mingw_configure} --disable-xlib --disable-xcb --enable-win32 --enable-png --enable-freetype
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT%{_mingw_libdir}/charset.alias

rm -f $RPM_BUILD_ROOT%{_mingw_libdir}/libcairo.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/libcairo-2.dll
%{_mingw_includedir}/cairo/
%{_mingw_libdir}/libcairo.dll.a
%{_mingw_libdir}/libcairo.la
%{_mingw_libdir}/pkgconfig/cairo-ft.pc
%{_mingw_libdir}/pkgconfig/cairo-pdf.pc
%{_mingw_libdir}/pkgconfig/cairo-png.pc
%{_mingw_libdir}/pkgconfig/cairo-ps.pc
%{_mingw_libdir}/pkgconfig/cairo-svg.pc
%{_mingw_libdir}/pkgconfig/cairo-win32-font.pc
%{_mingw_libdir}/pkgconfig/cairo-win32.pc
%{_mingw_libdir}/pkgconfig/cairo.pc
%{_mingw_datadir}/gtk-doc/html/cairo/


%changelog
* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 1.7.4-3
- Added dep on pkgconfig

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.7.4-2
- Remove static libraries.
- Fix source URL.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.7.4-1
- Initial RPM release
