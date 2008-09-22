%define __strip %{_mingw_strip}
%define __objdump %{_mingw_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw_findrequires}
%define __find_provides %{_mingw_findprovides}

Name:           mingw-gtk2
Version:        2.14.2
Release:        1%{?dist}
Summary:        MinGW Windows Gtk2 library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.gtk.org
Source0:        http://download.gnome.org/sources/gtk+/2.14/gtk+-%{version}.tar.bz2
Patch1:         gtk+-2.11.1-set-invisible-char-to-bullet.patch
Patch2:         gail-leaks.patch
Patch3:         info-leak.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 23
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-iconv
BuildRequires:  mingw-gettext
BuildRequires:  mingw-glib2
BuildRequires:  mingw-cairo
BuildRequires:  mingw-jasper
BuildRequires:  mingw-libpng
BuildRequires:  mingw-libjpeg
BuildRequires:  mingw-pango
BuildRequires:  mingw-atk
BuildRequires:  pkgconfig
# Native one for msgfmt
BuildRequires:  gettext
# Native one for glib-genmarsjal
BuildRequires:  glib2-devel
# Native one for gtk-update-icon-cache
BuildRequires:  gtk2
# Native one for gdk-pixbuf-csource
BuildRequires:  gtk2-devel

Requires(post): wine


%description
MinGW Windows Gtk2 library.


%prep
%setup -q -n gtk+-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
# Need to run the correct version of glib-mkenums.
PATH=%{_mingw_bindir}:$PATH

%{_mingw_configure}
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT/%{_mingw_libdir}/charset.alias

# Remove manpages which duplicate those in Fedora native.
rm -rf $RPM_BUILD_ROOT%{_mingw_mandir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
wine %{_mingw_bindir}/gdk-pixbuf-query-loaders.exe \
  > %{_mingw_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders

%preun
rm -f %{_mingw_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders


%files
%defattr(-,root,root)
%{_mingw_datadir}/gtk-doc/html/gail-libgail-util
%{_mingw_datadir}/gtk-doc/html/gdk-pixbuf
%{_mingw_datadir}/gtk-doc/html/gdk
%{_mingw_datadir}/gtk-doc/html/gtk
%{_mingw_datadir}/locale/*/LC_MESSAGES/gtk20-properties.mo
%{_mingw_datadir}/locale/*/LC_MESSAGES/gtk20.mo
%{_mingw_datadir}/themes/*
%{_mingw_bindir}/gdk-pixbuf-csource.exe
%{_mingw_bindir}/gdk-pixbuf-query-loaders.exe
%{_mingw_bindir}/gtk-builder-convert
%{_mingw_bindir}/gtk-demo.exe
%{_mingw_bindir}/gtk-query-immodules-2.0.exe
%{_mingw_bindir}/gtk-update-icon-cache.exe
%{_mingw_bindir}/libgailutil-18.dll
%{_mingw_bindir}/libgdk-win32-2.0-0.dll
%{_mingw_bindir}/libgdk_pixbuf-2.0-0.dll
%{_mingw_bindir}/libgtk-win32-2.0-0.dll
%{_mingw_libdir}/gtk-2.0/
%{_mingw_libdir}/libgailutil.dll.a
%{_mingw_libdir}/libgailutil.la
%{_mingw_libdir}/libgdk-win32-2.0.dll.a
%{_mingw_libdir}/libgdk-win32-2.0.la
%{_mingw_libdir}/libgdk_pixbuf-2.0.dll.a
%{_mingw_libdir}/libgdk_pixbuf-2.0.la
%{_mingw_libdir}/libgtk-win32-2.0.dll.a
%{_mingw_libdir}/libgtk-win32-2.0.la
%{_mingw_libdir}/gdk_pixbuf-2.0.def
%{_mingw_libdir}/gdk-win32-2.0.def
%{_mingw_libdir}/gtk-win32-2.0.def
%{_mingw_libdir}/pkgconfig/gail.pc
%{_mingw_libdir}/pkgconfig/gdk-2.0.pc
%{_mingw_libdir}/pkgconfig/gdk-win32-2.0.pc
%{_mingw_libdir}/pkgconfig/gdk-pixbuf-2.0.pc
%{_mingw_libdir}/pkgconfig/gtk+-2.0.pc
%{_mingw_libdir}/pkgconfig/gtk+-win32-2.0.pc
%{_mingw_includedir}/gtk-2.0/
%{_mingw_includedir}/gail-1.0/
%{_mingw_sysconfdir}/gtk-2.0/
%{_mingw_datadir}/aclocal/gtk-2.0.m4
%{_mingw_datadir}/gtk-2.0/


%changelog
* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 2.14.2-1
- Update to 2.14.2 release

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 2.14.0-5
- Remove manpages duplicating those in Fedora native packages.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 2.14.0-4
- Added dep on pkgconfig, gettext and glib2 (native)

* Thu Sep 11 2008 Richard W.M. Jones <rjones@redhat.com> - 2.14.0-3
- post/preun scripts to update the gdk-pixbuf.loaders list.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 2.14.0-2
- Jasper DLLs now fixed.
- Fix source URL.
- Run the correct glib-mkenums.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 2.14.0-1
- Initial RPM release
