%define __strip %{_mingw_strip}
%define __objdump %{_mingw_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw_findrequires}
%define __find_provides %{_mingw_findprovides}

Name:           mingw-fontconfig
Version:        2.6.0
Release:        4%{?dist}
Summary:        MinGW Windows Fontconfig library

License:        MIT
URL:            http://fontconfig.org
Source0:        http://fontconfig.org/release/fontconfig-%{version}.tar.gz
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         mingw-fontconfig-2.6.0-remove-logfile.patch

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 23
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-freetype
BuildRequires:  mingw-libxml2
BuildRequires:  pkgconfig
BuildRequires:  docbook-utils
BuildRequires:  autoconf automake libtool


%description
MinGW Windows Fontconfig library.


%prep
%setup -q -n fontconfig-%{version}
%patch0 -p1
autoreconf


%build
PATH="%{_mingw_bindir}:$PATH" \
%{_mingw_configure} --with-arch=i686
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT/%{_mingw_libdir}/charset.alias

# Remove static library.
rm $RPM_BUILD_ROOT%{_mingw_libdir}/libfontconfig.a

# Remove duplicate manpages.
rm -rf $RPM_BUILD_ROOT%{_mingw_mandir}


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
%{_mingw_datadir}/doc/fontconfig

%changelog
* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 2.6.0-4
- Remove duplicate manpages.
- Patch to delete logfile left when building (unused) manpages.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 2.6.0-3
- Add mingw_bindir to $PATH for freetype-config script

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 2.6.0-2
- Remove static library.
- +BR mingw-libxml2.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 2.6.0-1
- Initial RPM release
