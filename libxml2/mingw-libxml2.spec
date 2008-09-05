%include /usr/lib/rpm/mingw-defs

Name:           mingw-libxml2
Version:        2.6.32
Release:        3%{?dist}
Summary:        MinGW Windows libxml2 XML processing library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.xmlsoft.org/
Source0:        ftp://xmlsoft.org/libxml2/libxml2-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 19
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


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/libxml2-2.dll
%{_mingw_bindir}/xml2-config
%{_mingw_bindir}/xmlcatalog.exe
%{_mingw_bindir}/xmllint.exe
%{_mingw_libdir}/*
%{_mingw_includedir}/*
%{_mingw_datadir}/aclocal/*
%{_mingw_docdir}/libxml2-%{version}/
%{_mingw_datadir}/gtk-doc/html/libxml2/
%{_mingw_mandir}/man1/*
%{_mingw_mandir}/man3/*


%changelog
* Fri Sep  5 2008 Richard W.M. Jones <rjones@redhat.com> - 2.6.32-3
- Use RPM macros from mingw-filesystem.
- BuildArch is noarch.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 2.6.32-1
- Initial RPM release, largely based on earlier work from several sources.
