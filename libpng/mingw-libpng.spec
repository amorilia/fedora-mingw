%define __strip %{_mingw_strip}
%define __objdump %{_mingw_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw_findrequires}
%define __find_provides %{_mingw_findprovides}

Name:           mingw-libpng
Version:        1.2.31
Release:        3%{?dist}
Summary:        MinGW Windows Libpng library

License:        zlib
URL:            http://www.libpng.org/pub/png/
Source0:        ftp://ftp.simplesystems.org/pub/png/src/libpng-%{version}.tar.bz2
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 23
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-zlib

%description
MinGW Windows Libpng library.


%prep
%setup -q -n libpng-%{version}

%build
%{_mingw_configure}
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm $RPM_BUILD_ROOT%{_mingw_libdir}/libpng.a

# No need to distribute manpages which appear in the Fedora
# native packages already.
rm -rf $RPM_BUILD_ROOT%{_mingw_mandir}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/libpng-3.dll
%{_mingw_bindir}/libpng-config
%{_mingw_bindir}/libpng12-0.dll
%{_mingw_bindir}/libpng12-config
%{_mingw_includedir}/libpng12
%{_mingw_includedir}/png.h
%{_mingw_includedir}/pngconf.h
%{_mingw_libdir}/libpng.dll.a
%{_mingw_libdir}/libpng.la
%{_mingw_libdir}/libpng12.a
%{_mingw_libdir}/libpng12.dll.a
%{_mingw_libdir}/libpng12.la
%{_mingw_libdir}/pkgconfig/libpng.pc
%{_mingw_libdir}/pkgconfig/libpng12.pc


%changelog
* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.31-3
- Don't duplicate Fedora native manpages.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.31-2
- Remove static library.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.2.31-1
- Initial RPM release
