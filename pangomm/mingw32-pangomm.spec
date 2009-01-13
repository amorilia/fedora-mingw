%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

%define apiver 1.4

Name:           mingw32-pangomm
Version:        2.14.0
Release:        3%{?dist}
Summary:        MinGW Windows C++ interface for Pango

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://gtkmm.sourceforge.net/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/pangomm/2.14/pangomm-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         pangomm-2.14.0-devhelp.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-glibmm24 >= 2.14.1
BuildRequires:  mingw32-cairomm >= 1.2.2
BuildRequires:  mingw32-pango >= 1.21.4
BuildRequires:  doxygen
BuildRequires:  graphviz

Requires:       pkgconfig


%description
pangomm provides a C++ interface to the Pango library. Highlights
include typesafe callbacks, widgets extensible via inheritance and a
comprehensive set of widget classes that can be freely combined to
quickly create complex user interfaces.


%prep
%setup -q -n pangomm-%{version}
%patch0 -p1 -b .devhelp


%build
%{_mingw32_configure} --disable-static
make


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" install

rm -r $RPM_BUILD_ROOT%{_mingw32_libdir}/pangomm-%{apiver}

# Remove documentation.
rm -r $RPM_BUILD_ROOT%{_mingw32_docdir}/pangomm-%{apiver}
rm -r $RPM_BUILD_ROOT%{_mingw32_datadir}/devhelp


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libpangomm-%{apiver}-1.dll
%{_mingw32_libdir}/libpangomm-%{apiver}.la
%{_mingw32_libdir}/libpangomm-%{apiver}.dll.a
%{_mingw32_libdir}/pkgconfig/pangomm-%{apiver}.pc
%{_mingw32_includedir}/pangomm-%{apiver}


%changelog
* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 2.14.0-3
- Requires pkgconfig.

* Fri Oct 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.14.0-2
- Initial RPM release.
