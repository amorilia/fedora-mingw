%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-freetype
Version:        2.3.7
Release:        5%{?dist}
Summary:        MinGW Windows Freetype library

License:        FTL or GPLv2+
URL:            http://www.freetype.org
Source:         http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.bz2
Source1:         http://download.savannah.gnu.org/releases/freetype/freetype-doc-%{version}.tar.bz2
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1:  freetype-2.1.10-enable-ft2-bci.patch
Patch2:  freetype-2.3.0-enable-spr.patch
Patch3:  freetype-2.2.1-enable-valid.patch
Patch4:  freetype-2.2.1-memcpy-fix.patch


BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 25
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-zlib

%description
MinGW Windows Freetype library.


%prep
%setup -q -n freetype-%{version} -b 1 -a 1

%build
%{_mingw32_configure}
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libfreetype.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/freetype-config
%{_mingw32_bindir}/libfreetype-6.dll
%{_mingw32_includedir}/freetype2
%{_mingw32_includedir}/ft2build.h
%{_mingw32_libdir}/libfreetype.dll.a
%{_mingw32_libdir}/libfreetype.la
%{_mingw32_libdir}/pkgconfig/freetype2.pc
%{_mingw32_datadir}/aclocal/freetype2.m4


%changelog
* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.3.7-5
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 2.3.7-4
- Import patches from rawhide  & add docs

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 2.3.7-3
- Depends on filesystem >= 25.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 2.3.7-2
- Fix source URL.
- Remove static libraries.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 2.3.7-1
- Initial RPM release
