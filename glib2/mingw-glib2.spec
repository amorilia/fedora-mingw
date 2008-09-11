%define __strip %{_mingw_strip}
%define __objdump %{_mingw_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw_findrequires}
%define __find_provides %{_mingw_findprovides}

Name:           mingw-glib2
Version:        2.18.0
Release:        1%{?dist}
Summary:        MinGW Windows GLib2 library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.gtk.org
Source0:        http://download.gnome.org/sources/glib/2.18/glib-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Patch2:         gio-2.16-only-pass-uri-to-gio-apps.patch

BuildRequires:  mingw-filesystem >= 23
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-iconv
BuildRequires:  mingw-gettext


%description
MinGW Windows Glib2 library.


%prep
%setup -q -n glib-%{version}
%patch2 -p1


%build
%{_mingw_configure}
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT/%{_mingw_libdir}/charset.alias

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/glib-genmarshal.exe
%{_mingw_bindir}/glib-gettextize
%{_mingw_bindir}/glib-mkenums
%{_mingw_bindir}/gobject-query.exe
%{_mingw_bindir}/gspawn-win32-helper-console.exe
%{_mingw_bindir}/gspawn-win32-helper.exe
%{_mingw_bindir}/libgio-2.0-0.dll
%{_mingw_bindir}/libglib-2.0-0.dll
%{_mingw_bindir}/libgmodule-2.0-0.dll
%{_mingw_bindir}/libgobject-2.0-0.dll
%{_mingw_bindir}/libgthread-2.0-0.dll
%{_mingw_includedir}/glib-2.0/
%{_mingw_libdir}/gio-2.0.def
%{_mingw_libdir}/glib-2.0.def
%{_mingw_libdir}/glib-2.0/
%{_mingw_libdir}/gmodule-2.0.def
%{_mingw_libdir}/gobject-2.0.def
%{_mingw_libdir}/gthread-2.0.def
%{_mingw_libdir}/libgio-2.0.dll.a
%{_mingw_libdir}/libgio-2.0.la
%{_mingw_libdir}/libglib-2.0.dll.a
%{_mingw_libdir}/libglib-2.0.la
%{_mingw_libdir}/libgmodule-2.0.dll.a
%{_mingw_libdir}/libgmodule-2.0.la
%{_mingw_libdir}/libgobject-2.0.dll.a
%{_mingw_libdir}/libgobject-2.0.la
%{_mingw_libdir}/libgthread-2.0.dll.a
%{_mingw_libdir}/libgthread-2.0.la
%{_mingw_libdir}/pkgconfig/gio-2.0.pc
%{_mingw_libdir}/pkgconfig/gio-unix-2.0.pc
%{_mingw_libdir}/pkgconfig/glib-2.0.pc
%{_mingw_libdir}/pkgconfig/gmodule-2.0.pc
%{_mingw_libdir}/pkgconfig/gmodule-export-2.0.pc
%{_mingw_libdir}/pkgconfig/gmodule-no-export-2.0.pc
%{_mingw_libdir}/pkgconfig/gobject-2.0.pc
%{_mingw_libdir}/pkgconfig/gthread-2.0.pc
%{_mingw_datadir}/aclocal/glib-2.0.m4
%{_mingw_datadir}/aclocal/glib-gettext.m4
%{_mingw_datadir}/glib-2.0/
%{_mingw_datadir}/gtk-doc/html/gio/
%{_mingw_datadir}/gtk-doc/html/glib/
%{_mingw_datadir}/gtk-doc/html/gobject/
%{_mingw_datadir}/locale/*/LC_MESSAGES/glib20.mo
%{_mingw_mandir}/man1/glib-genmarshal.1*
%{_mingw_mandir}/man1/glib-gettextize.1*
%{_mingw_mandir}/man1/glib-mkenums.1*
%{_mingw_mandir}/man1/gobject-query.1*
%{_mingw_mandir}/man1/gtester-report.1*
%{_mingw_mandir}/man1/gtester.1*



%changelog
* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 2.18.0-1
- Initial RPM release
