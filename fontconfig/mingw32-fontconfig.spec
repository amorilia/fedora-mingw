%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-fontconfig
Version:        2.6.0
Release:        8%{?dist}
Summary:        MinGW Windows Fontconfig library

License:        MIT
URL:            http://fontconfig.org
Source0:        http://fontconfig.org/release/fontconfig-%{version}.tar.gz
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         mingw32-fontconfig-2.6.0-remove-logfile.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 40
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-expat
BuildRequires:  mingw32-freetype
BuildRequires:  mingw32-iconv
BuildRequires:  mingw32-libxml2
BuildRequires:  pkgconfig
BuildRequires:  docbook-utils
BuildRequires:  automake, autoconf, libtool

Requires:       pkgconfig


%description
MinGW Windows Fontconfig library.


%prep
%setup -q -n fontconfig-%{version}
%patch0 -p1
libtoolize --force --copy
autoreconf


%build
PATH="%{_mingw32_bindir}:$PATH" \
%{_mingw32_configure} --with-arch=i686
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT/%{_mingw32_libdir}/charset.alias

# Remove static library.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libfontconfig.a

# Remove duplicate manpages.
rm -rf $RPM_BUILD_ROOT%{_mingw32_mandir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYING
%{_mingw32_bindir}/fc-cache.exe
%{_mingw32_bindir}/fc-cat.exe
%{_mingw32_bindir}/fc-list.exe
%{_mingw32_bindir}/fc-match.exe
%{_mingw32_bindir}/libfontconfig-1.dll
%{_mingw32_libdir}/fontconfig.def
%{_mingw32_libdir}/libfontconfig.dll.a
%{_mingw32_libdir}/libfontconfig.la
%{_mingw32_libdir}/pkgconfig/fontconfig.pc
%{_mingw32_includedir}/fontconfig/
%{_mingw32_sysconfdir}/fonts/
%{_mingw32_datadir}/doc/fontconfig

%changelog
* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 2.6.0-8
- Include license.

* Fri Jan 30 2009 Richard W.M. Jones <rjones@redhat.com> - 2.6.0-7
- Requires pkgconfig.

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 2.6.0-6
- Use _smp_mflags.
- Rebuild libtool configuration.
- More BRs suggested by auto-buildrequires.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.6.0-5
- Rename mingw -> mingw32.

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
