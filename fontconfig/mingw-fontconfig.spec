%define __strip %{_mingw_strip}
%define __objdump %{_mingw_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw_findrequires}
%define __find_provides %{_mingw_findprovides}

Name:           mingw-fontconfig
Version:        2.6.0
Release:        2%{?dist}
Summary:        MinGW Windows Fontconfig library

License:        MIT
URL:            http://fontconfig.org
Source0:        http://fontconfig.org/release/fontconfig-%{version}.tar.gz
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 23
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-freetype
BuildRequires:  mingw-libxml2

%description
MinGW Windows Fontconfig library.


%prep
%setup -q -n fontconfig-%{version}

%build
%{_mingw_configure} --with-arch=i686
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT/%{_mingw_libdir}/charset.alias

# Remove static library.
rm $RPM_BUILD_ROOT%{_mingw_libdir}/libfontconfig.a

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/fc-cache.exe
%{_mingw_bindir}/fc-cat.exe
%{_mingw_bindir}/fc-list.exe
%{_mingw_bindir}/fc-match.exe
%{_mingw_bindir}/libfontconfig-1.dll
%{_mingw_libdir}/fontconfig.def
%{_mingw_libdir}/libfontconfig.dll.a
%{_mingw_libdir}/libfontconfig.la
%{_mingw_libdir}/pkgconfig/fontconfig.pc
%{_mingw_includedir}/fontconfig/
%{_mingw_sysconfdir}/fonts/
%{_mingw_mandir}/man1/fc-cache.1*
%{_mingw_mandir}/man1/fc-cat.1*
%{_mingw_mandir}/man1/fc-list.1*
%{_mingw_mandir}/man1/fc-match.1*
%{_mingw_mandir}/man3/Fc*.3*
%{_mingw_mandir}/man5/fonts-conf.5*
%{_mingw_datadir}/doc/fontconfig

%changelog
* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 2.6.0-2
- Remove static library.
- +BR mingw-libxml2.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 2.6.0-1
- Initial RPM release
