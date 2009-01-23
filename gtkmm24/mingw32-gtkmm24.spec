%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-gtkmm24
Version:        2.14.1
Release:        3%{?dist}
Summary:        MinGW Windows C++ interface for GTK2 (a GUI library for X)

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://gtkmm.sourceforge.net/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/gtkmm/2.14/gtkmm-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-glibmm24 >= 2.18.0
BuildRequires:  mingw32-atk >= 1.9.0
BuildRequires:  mingw32-pango >= 1.5.2
BuildRequires:  mingw32-gtk2 >= 2.14.0
BuildRequires:  mingw32-cairomm >= 1.2.2
BuildRequires:  mingw32-pangomm >= 2.14.0

Requires:       pkgconfig


%description
gtkmm provides a C++ interface to the GTK+ GUI library. gtkmm2 wraps
GTK+ 2.  Highlights include typesafe callbacks, widgets extensible via
inheritance and a comprehensive set of widget classes that can be
freely combined to quickly create complex user interfaces.



%prep
%setup -q -n gtkmm-%{version}


%build
%{_mingw32_configure} --disable-static --enable-shared --disable-demos
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove documentation which duplicates that in the base package.
rm -r $RPM_BUILD_ROOT%{_mingw32_datadir}/devhelp
rm -r $RPM_BUILD_ROOT%{_mingw32_docdir}/*


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libatkmm-1.6-1.dll
%{_mingw32_bindir}/libgdkmm-2.4-1.dll
%{_mingw32_bindir}/libgtkmm-2.4-1.dll
%{_mingw32_libdir}/libatkmm-1.6.dll.a
%{_mingw32_libdir}/libatkmm-1.6.la
%{_mingw32_libdir}/libgdkmm-2.4.dll.a
%{_mingw32_libdir}/libgdkmm-2.4.la
%{_mingw32_libdir}/libgtkmm-2.4.dll.a
%{_mingw32_libdir}/libgtkmm-2.4.la
%{_mingw32_includedir}/atkmm-1.6
%{_mingw32_includedir}/gdkmm-2.4
%{_mingw32_includedir}/gtkmm-2.4
%{_mingw32_libdir}/gdkmm-2.4
%{_mingw32_libdir}/gtkmm-2.4
%{_mingw32_libdir}/pkgconfig/atkmm-1.6.pc
%{_mingw32_libdir}/pkgconfig/gdkmm-2.4.pc
%{_mingw32_libdir}/pkgconfig/gtkmm-2.4.pc


%changelog
* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 2.14.1-2
- Use _smp_mflags.

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 2.14.1-2
- Requires pkgconfig.

* Fri Oct 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.14.1-1
- Initial RPM release.
