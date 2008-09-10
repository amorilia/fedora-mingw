%include /usr/lib/rpm/mingw-defs

Name:           mingw-pango
Version:        1.21.6
Release:        1%{?dist}
Summary:        MinGW Windows Pango library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.pango.org
Source0:        http://download.gnome.org/sources/pango/1.21/pango-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 19
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-iconv
BuildRequires:  mingw-gettext
BuildRequires:  mingw-cairo
BuildRequires:  mingw-freetype
BuildRequires:  mingw-fontconfig

%description
MinGW Windows Pango library.


%prep
%setup -q -n pango-%{version}

%build
PKG_CONFIG_PATH=%{_mingw_libdir}/pkgconfig \
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

%changelog
* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.21.6-1
- Initial RPM release
