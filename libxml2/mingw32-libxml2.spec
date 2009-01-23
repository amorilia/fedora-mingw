%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-libxml2
Version:        2.7.2
Release:        5%{?dist}
Summary:        MinGW Windows libxml2 XML processing library

License:        MIT
Group:          Development/Libraries
URL:            http://xmlsoft.org/
Source0:        ftp://xmlsoft.org/libxml2/libxml2-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Not required for MinGW.
#Patch0:         libxml2-multilib.patch

# MinGW-specific patches.
Patch1000:      mingw32-libxml2-2.7.2-with-modules.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-zlib
BuildRequires:  mingw32-gettext

Requires:       pkgconfig


%description
MinGW Windows libxml2 XML processing library.


%prep
%setup -q -n libxml2-%{version}
%patch1000 -p1


%build
LDFLAGS="-no-undefined" \
%{_mingw32_configure} --without-python --with-modules --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# Remove manpages which duplicate Fedora native.
rm -rf $RPM_BUILD_ROOT%{_mingw32_mandir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libxml2-2.dll
%{_mingw32_bindir}/xml2-config
%{_mingw32_bindir}/xmlcatalog.exe
%{_mingw32_bindir}/xmllint.exe
%{_mingw32_libdir}/libxml2.dll.a
%{_mingw32_libdir}/libxml2.la
%{_mingw32_libdir}/pkgconfig
%{_mingw32_libdir}/pkgconfig/libxml-2.0.pc
%{_mingw32_libdir}/xml2Conf.sh
%{_mingw32_includedir}/libxml2
%{_mingw32_datadir}/aclocal/*
%{_mingw32_docdir}/libxml2-%{version}/
%{_mingw32_datadir}/gtk-doc/html/libxml2/


%changelog
* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 2.7.2-5
- Use _smp_mflags.
- Disable static libraries.

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 2.7.2-4
- Requires pkgconfig.

* Sat Oct 25 2008 Richard W.M. Jones <rjones@redhat.com> - 2.7.2-3
- Enable modules support for libxslt.

* Fri Oct 17 2008 Richard W.M. Jones <rjones@redhat.com> - 2.7.2-1
- Resynch to native Fedora package + patch.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.7.1-2
- Rename mingw -> mingw32.

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
