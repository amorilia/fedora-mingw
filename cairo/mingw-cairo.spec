%include /usr/lib/rpm/mingw-defs

Name:           mingw-cairo
Version:        1.7.4
Release:        1%{?dist}
Summary:        MinGW Windows Cairo library

License:	LGPLv2 or MPLv1.1
URL:		http://cairographics.org
Source0:	http://cairographics.org/releases/cairo-%{version}.tar.gz
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 19
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-libxml2
BuildRequires:  mingw-pixman
BuildRequires:  mingw-freetype
BuildRequires:  mingw-libpng
BuildRequires:  mingw-fontconfig

%description
MinGW Windows Cairo library.


%prep
%setup -q -n cairo-%{version}

%build
%{_mingw_configure} --disable-xlib --disable-xcb --enable-win32 --enable-png --enable-freetype
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT/%{_mingw_libdir}/charset.alias

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/libcairo-2.dll
%{_mingw_includedir}/cairo/
%{_mingw_libdir}/libcairo.a
%{_mingw_libdir}/libcairo.dll.a
%{_mingw_libdir}/libcairo.la
%{_mingw_libdir}/pkgconfig/cairo-ft.pc
%{_mingw_libdir}/pkgconfig/cairo-pdf.pc
%{_mingw_libdir}/pkgconfig/cairo-png.pc
%{_mingw_libdir}/pkgconfig/cairo-ps.pc
%{_mingw_libdir}/pkgconfig/cairo-svg.pc
%{_mingw_libdir}/pkgconfig/cairo-win32-font.pc
%{_mingw_libdir}/pkgconfig/cairo-win32.pc
%{_mingw_libdir}/pkgconfig/cairo.pc
%{_mingw_datadir}/gtk-doc/html/cairo/


%changelog
* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.7.4-1
- Initial RPM release
