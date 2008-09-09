%include /usr/lib/rpm/mingw-defs

Name:           mingw-freetype
Version:        2.3.7
Release:        1%{?dist}
Summary:        MinGW Windows Freetype library

License: FTL or GPLv2+
URL: http://www.freetype.org
Source:  freetype-%{version}.tar.bz2
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 19
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-zlib

%description
MinGW Windows Freetype library.


%prep
%setup -q -n freetype-%{version}

%build
%{_mingw_configure}
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/freetype-config
%{_mingw_bindir}/libfreetype-6.dll
%{_mingw_includedir}/freetype2
%{_mingw_includedir}/ft2build.h
%{_mingw_libdir}/libfreetype.a
%{_mingw_libdir}/libfreetype.dll.a
%{_mingw_libdir}/libfreetype.la
%{_mingw_libdir}/pkgconfig/freetype2.pc
%{_mingw_datadir}/aclocal/freetype2.m4

%changelog
* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 2.3.7-1
- Initial RPM release
