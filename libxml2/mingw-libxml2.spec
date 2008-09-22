%define __strip %{_mingw_strip}
%define __objdump %{_mingw_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw_findrequires}
%define __find_provides %{_mingw_findprovides}

Name:           mingw-libxml2
Version:        2.7.1
Release:        1%{?dist}
Summary:        MinGW Windows libxml2 XML processing library

License:        MIT
Group:          Development/Libraries
URL:            http://xmlsoft.org/
Source0:        ftp://xmlsoft.org/libxml2/libxml2-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 23
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-zlib
BuildRequires:  mingw-gettext


%description
MinGW Windows libxml2 XML processing library.


%prep
%setup -q -n libxml2-%{version}


%build
LDFLAGS="-no-undefined" %{_mingw_configure} --without-python
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm $RPM_BUILD_ROOT%{_mingw_libdir}/libxml2.a

# Remove manpages which duplicate Fedora native.
rm -rf $RPM_BUILD_ROOT%{_mingw_mandir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/libxml2-2.dll
%{_mingw_bindir}/xml2-config
%{_mingw_bindir}/xmlcatalog.exe
%{_mingw_bindir}/xmllint.exe
%{_mingw_libdir}/libxml2.dll.a
%{_mingw_libdir}/libxml2.la
%{_mingw_libdir}/pkgconfig
%{_mingw_libdir}/pkgconfig/libxml-2.0.pc
%{_mingw_libdir}/xml2Conf.sh
%{_mingw_includedir}/libxml2
%{_mingw_datadir}/aclocal/*
%{_mingw_docdir}/libxml2-%{version}/
%{_mingw_datadir}/gtk-doc/html/libxml2/


%changelog
* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 2.7.1-1
- Update to 2.7.1 release

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 2.6.32-5
- Remove manpages which duplicate Fedora native.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 2.6.32-4
- Remove static libraries.
- List libdir files explicitly.

* Fri Sep  5 2008 Richard W.M. Jones <rjones@redhat.com> - 2.6.32-3
- Use RPM macros from mingw-filesystem.
- BuildArch is noarch.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 2.6.32-1
- Initial RPM release, largely based on earlier work from several sources.
