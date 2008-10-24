%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-glibmm24
Version:        2.18.1
Release:        2%{?dist}
Summary:        MinGW Windows C++ interface for GTK2 (a GUI library for X)

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://gtkmm.sourceforge.net/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/glibmm/2.18/glibmm-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-libsigc++20 >= 2.0.0
BuildRequires:  mingw32-glib2 >= 2.17.3
BuildRequires:  pkgconfig

Requires:       pkgconfig


%description
glibmm provides a C++ interface to the GTK+ GLib low-level core
library. Highlights include typesafe callbacks, widgets extensible via
inheritance and a comprehensive set of widget classes that can be
freely combined to quickly create complex user interfaces.


%prep
%setup -q -n glibmm-%{version}


%build
%{_mingw32_configure} --disable-static
make


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove docs, duplicate native package.
rm -r $RPM_BUILD_ROOT%{_mingw32_docdir}/glibmm-2.4
rm -r $RPM_BUILD_ROOT%{_mingw32_datadir}/devhelp


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libgiomm-2.4-1.dll
%{_mingw32_bindir}/libglibmm_generate_extra_defs-2.4-1.dll
%{_mingw32_bindir}/libglibmm-2.4-1.dll
%{_mingw32_libdir}/libgiomm-2.4.dll.a
%{_mingw32_libdir}/libgiomm-2.4.la
%{_mingw32_libdir}/libglibmm_generate_extra_defs-2.4.dll.a
%{_mingw32_libdir}/libglibmm_generate_extra_defs-2.4.la
%{_mingw32_libdir}/libglibmm-2.4.dll.a
%{_mingw32_libdir}/libglibmm-2.4.la
%{_mingw32_libdir}/giomm-2.4
%{_mingw32_libdir}/glibmm-2.4
%{_mingw32_includedir}/giomm-2.4
%{_mingw32_includedir}/glibmm-2.4
%{_mingw32_libdir}/pkgconfig/giomm-2.4.pc
%{_mingw32_libdir}/pkgconfig/glibmm-2.4.pc
%{_mingw32_datadir}/aclocal/glibmm_check_perl.m4


%changelog
* Fri Oct 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.1-2
- Initial RPM release.
