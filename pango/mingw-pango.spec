%define __strip %{_mingw_strip}
%define __objdump %{_mingw_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw_findrequires}
%define __find_provides %{_mingw_findprovides}

Name:           mingw-pango
Version:        1.21.6
Release:        5%{?dist}
Summary:        MinGW Windows Pango library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.pango.org
Source0:        http://download.gnome.org/sources/pango/1.21/pango-%{version}.tar.bz2
# Native pango uses a %post script to generate this, but the pango-querymodules.exe
# binary is not something we can easily run on a Linux host. We could use wine by
# wine isn't happy in a mock environment. So we just include a pre-generated copy
# on basis that it won't ever change much
Source1:        pango.modules
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 23
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-iconv
BuildRequires:  mingw-gettext
BuildRequires:  mingw-cairo
BuildRequires:  mingw-freetype
BuildRequires:  mingw-fontconfig
BuildRequires:  mingw-glib2
BuildRequires:  pkgconfig

%description
MinGW Windows Pango library.


%prep
%setup -q -n pango-%{version}

%build
# Need to run the correct version of glib-mkenums.
PATH=%{_mingw_bindir}:$PATH \
%{_mingw_configure}
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT%{_mingw_sysconfdir}/pango/
cp %{SOURCE1} $RPM_BUILD_ROOT%{_mingw_sysconfdir}/pango/

rm -f $RPM_BUILD_ROOT/%{_mingw_libdir}/charset.alias


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_mingw_bindir}/libpango-1.0-0.dll
%{_mingw_bindir}/libpangocairo-1.0-0.dll
%{_mingw_bindir}/libpangoft2-1.0-0.dll
%{_mingw_bindir}/libpangowin32-1.0-0.dll
%{_mingw_bindir}/pango-querymodules.exe
%{_mingw_includedir}/pango-1.0/
%{_mingw_libdir}/libpango-1.0.dll.a
%{_mingw_libdir}/libpango-1.0.la
%{_mingw_libdir}/libpangocairo-1.0.dll.a
%{_mingw_libdir}/libpangocairo-1.0.la
%{_mingw_libdir}/libpangoft2-1.0.dll.a
%{_mingw_libdir}/libpangoft2-1.0.la
%{_mingw_libdir}/libpangowin32-1.0.dll.a
%{_mingw_libdir}/libpangowin32-1.0.la
%{_mingw_libdir}/pango-1.0.def
%{_mingw_libdir}/pangocairo-1.0.def
%{_mingw_libdir}/pangoft2-1.0.def
%{_mingw_libdir}/pangowin32-1.0.def
%{_mingw_libdir}/pango/
%{_mingw_libdir}/pkgconfig/pango.pc
%{_mingw_libdir}/pkgconfig/pangocairo.pc
%{_mingw_libdir}/pkgconfig/pangoft2.pc
%{_mingw_libdir}/pkgconfig/pangowin32.pc
%{_mingw_datadir}/gtk-doc/html/pango/
%{_mingw_mandir}/man1/pango-querymodules.1*
%{_mingw_sysconfdir}/pango/


%changelog
* Tue Sep 23 2008 Daniel P. Berrange <berrange@redhat.com> - 1.21.6-5
- Remove use of wine in %post

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 1.21.6-4
- Add dep on pkgconfig

* Thu Sep 11 2008 Richard W.M. Jones <rjones@redhat.com> - 1.21.6-3
- post/preun scripts to update the pango.modules list.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.21.6-2
- Run the correct glib-mkenums.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.21.6-1
- Initial RPM release
