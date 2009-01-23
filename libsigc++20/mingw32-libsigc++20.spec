%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-libsigc++20
Version:        2.2.2
Release:        3%{?dist}
Summary:        MinGW Windows port of the typesafe signal framework for C++

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://libsigc.sourceforge.net/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/libsigc++/2.2/libsigc++-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils

BuildRequires:  m4

Requires:       pkgconfig


%description
This library implements a full callback system for use in widget
libraries, abstract interfaces, and general programming. Originally
part of the Gtk-- widget set, %name is now a separate library to
provide for more general use. It is the most complete library of its
kind with the ability to connect an abstract callback to a class
method, function, or function object. It contains adaptor classes for
connection of dissimilar callbacks and has an ease of use unmatched by
other C++ callback libraries.

Package GTK-- (gtkmm), which is a C++ binding to the GTK+ library,
starting with version 1.1.2, uses %name.


%prep
%setup -q -n libsigc++-%{version}


%build
%{_mingw32_configure} --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Docs duplicate native package.
rm -r $RPM_BUILD_ROOT%{_mingw32_docdir}/libsigc-2.0

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libsigc-2.0-0.dll
%{_mingw32_libdir}/libsigc-2.0.dll.a
%{_mingw32_libdir}/libsigc-2.0.la
%{_mingw32_libdir}/pkgconfig/sigc++-2.0.pc
%{_mingw32_includedir}/sigc++-2.0
# WTF? This contains a header file ...
%{_mingw32_libdir}/sigc++-2.0


%changelog
* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 2.2.2-3
- Use _smp_mflags.

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 2.2.2-2
- Requires pkgconfig.

* Fri Oct 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.2-1
- Initial RPM release.
