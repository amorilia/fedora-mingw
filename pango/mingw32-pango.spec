%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-pango
Version:        1.21.6
Release:        6%{?dist}
Summary:        MinGW Windows Pango library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.pango.org
Source0:        http://download.gnome.org/sources/pango/1.21/pango-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Native pango uses a %post script to generate this, but the
# pango-querymodules.exe binary is not something we can easily run on
# a Linux host. We could use wine but wine isn't happy in a mock
# environment. So we just include a pre-generated copy on basis that
# it won't ever change much.
#
# If you want to rebuild this, do:
# wine %{_mingw32_bindir}/pango-querymodules.exe > pango.modules
Source1:        pango.modules

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-iconv
BuildRequires:  mingw32-gettext
BuildRequires:  mingw32-cairo
BuildRequires:  mingw32-freetype
BuildRequires:  mingw32-fontconfig
BuildRequires:  mingw32-glib2
BuildRequires:  pkgconfig

%description
MinGW Windows Pango library.


%prep
%setup -q -n pango-%{version}

%build
# Need to run the correct version of glib-mkenums.
PATH=%{_mingw32_bindir}:$PATH \
%{_mingw32_configure}
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/pango/
cp %{SOURCE1} $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/pango/

rm -f $RPM_BUILD_ROOT/%{_mingw32_libdir}/charset.alias


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_mingw32_bindir}/libpango-1.0-0.dll
%{_mingw32_bindir}/libpangocairo-1.0-0.dll
%{_mingw32_bindir}/libpangoft2-1.0-0.dll
%{_mingw32_bindir}/libpangowin32-1.0-0.dll
%{_mingw32_bindir}/pango-querymodules.exe
%{_mingw32_includedir}/pango-1.0/
%{_mingw32_libdir}/libpango-1.0.dll.a
%{_mingw32_libdir}/libpango-1.0.la
%{_mingw32_libdir}/libpangocairo-1.0.dll.a
%{_mingw32_libdir}/libpangocairo-1.0.la
%{_mingw32_libdir}/libpangoft2-1.0.dll.a
%{_mingw32_libdir}/libpangoft2-1.0.la
%{_mingw32_libdir}/libpangowin32-1.0.dll.a
%{_mingw32_libdir}/libpangowin32-1.0.la
%{_mingw32_libdir}/pango-1.0.def
%{_mingw32_libdir}/pangocairo-1.0.def
%{_mingw32_libdir}/pangoft2-1.0.def
%{_mingw32_libdir}/pangowin32-1.0.def
%{_mingw32_libdir}/pango/
%{_mingw32_libdir}/pkgconfig/pango.pc
%{_mingw32_libdir}/pkgconfig/pangocairo.pc
%{_mingw32_libdir}/pkgconfig/pangoft2.pc
%{_mingw32_libdir}/pkgconfig/pangowin32.pc
%{_mingw32_datadir}/gtk-doc/html/pango/
%{_mingw32_mandir}/man1/pango-querymodules.1*
%{_mingw32_sysconfdir}/pango/


%changelog
* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.21.6-6
- Rename mingw -> mingw32.

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
