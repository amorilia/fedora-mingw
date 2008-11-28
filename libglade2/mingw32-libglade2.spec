%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-libglade2
Version:        2.6.3
Release:        1%{?dist}
Summary:        MinGW Windows Libglade2 library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.gnome.org
Source0:        http://download.gnome.org/sources/libglade/2.6/libglade-%{version}.tar.bz2
Patch1:         libglade-2.0.1-nowarning.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-gtk2
BuildRequires:  mingw32-fontconfig
BuildRequires:  mingw32-pango
BuildRequires:  mingw32-gettext
# Native one for msgfmt
BuildRequires:  gettext

%description
MinGW Windows Libglade2 library.


%prep
%setup -q -n libglade-%{version}
%patch1 -p1

%build
%{_mingw32_configure} --disable-gtk-doc
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libglade-2.0-0.dll
%{_mingw32_bindir}/libglade-convert
%{_mingw32_includedir}/libglade-2.0
%{_mingw32_libdir}/libglade-2.0.a
%{_mingw32_libdir}/libglade-2.0.dll.a
%{_mingw32_libdir}/libglade-2.0.la
%{_mingw32_libdir}/pkgconfig/libglade-2.0.pc

%{_mingw32_datadir}/gtk-doc/html/libglade
%dir %{_mingw32_datadir}/xml/libglade
%{_mingw32_datadir}/xml/libglade/glade-2.0.dtd


%changelog
* Fri Nov 28 2008 Daniel P. Berrange <berrange@redhat.com> - 2.6.3-1
- Initial build

