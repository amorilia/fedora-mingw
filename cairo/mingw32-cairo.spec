%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-cairo
Version:        1.8.0
Release:        6%{?dist}
Summary:        MinGW Windows Cairo library

License:        LGPLv2 or MPLv1.1
URL:            http://cairographics.org
Source0:        http://cairographics.org/snapshots/cairo-%{version}.tar.gz
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-libxml2
BuildRequires:  mingw32-pixman
BuildRequires:  mingw32-libpng
BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-iconv
BuildRequires:  mingw32-zlib
BuildRequires:  pkgconfig

# These are BRs for the base package, but are not needed on Win32
# because Cairo includes a separate Win32 font rendering back end
# (thanks to: Erik van Pienbroek).
#BuildRequires:  mingw32-fontconfig
#BuildRequires:  mingw32-freetype

Requires:       pkgconfig


%description
MinGW Windows Cairo library.


%prep
%setup -q -n cairo-%{version}


%build
%{_mingw32_configure} \
  --disable-xlib \
  --disable-xcb \
  --enable-win32 \
  --enable-png \
  --disable-static \
  --disable-ft
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT%{_mingw32_libdir}/charset.alias


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYING COPYING-LGPL-2.1 COPYING-MPL-1.1
%{_mingw32_bindir}/libcairo-2.dll
%{_mingw32_includedir}/cairo/
%{_mingw32_libdir}/libcairo.dll.a
%{_mingw32_libdir}/libcairo.la
%{_mingw32_libdir}/pkgconfig/cairo-pdf.pc
%{_mingw32_libdir}/pkgconfig/cairo-png.pc
%{_mingw32_libdir}/pkgconfig/cairo-ps.pc
%{_mingw32_libdir}/pkgconfig/cairo-svg.pc
%{_mingw32_libdir}/pkgconfig/cairo-win32-font.pc
%{_mingw32_libdir}/pkgconfig/cairo-win32.pc
%{_mingw32_libdir}/pkgconfig/cairo.pc
%{_mingw32_datadir}/gtk-doc/html/cairo/


%changelog
* Mon Jan 26 2009 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-6
- Requires pkgconfig (Erik van Pienbroek).

* Mon Jan 26 2009 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-5
- Don't need to remove extra pkgconfig file in install section.

* Mon Jan 26 2009 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-4
- Disable freetype in configure so it doesn't break if freetype
  or fontconfig are actually installed. (Erik van Pienbroek).

* Mon Jan 19 2009 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-3
- Include license file in documentation section.
- Disable building static library to save time.
- Remove BRs on mingw32-fontconfig and mingw32-freetype which are
  not needed on Win32.
- Use _smp_mflags.
- Added BRs mingw32-dlfcn, mingw32-iconv, mingw32-zlib.

* Wed Oct 29 2008 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-2
- Fix mixed spaces/tabs in specfile.

* Fri Oct 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-1
- New upstream version 1.8.0.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.7.4-4
- Rename mingw -> mingw32.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 1.7.4-3
- Added dep on pkgconfig

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.7.4-2
- Remove static libraries.
- Fix source URL.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.7.4-1
- Initial RPM release
