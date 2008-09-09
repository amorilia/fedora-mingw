%include /usr/lib/rpm/mingw-defs

Name:           mingw-fontconfig
Version:        2.6.0
Release:        1%{?dist}
Summary:        MinGW Windows Fontconfig library

License: MIT
URL: http://fontconfig.org
Source0: http://fontconfig.org/release/fontconfig-%{version}.tar.gz
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 19
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils

%description
MinGW Windows Fontconfig library.


%prep
%setup -q -n fontconfig-%{version}

%build
PKG_CONFIG_PATH=%{_mingw_libdir}/pkgconfig \
#{_mingw_configure} --with-arch=i686
  CC="%{_mingw_cc}" \
  CFLAGS="-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2  -fexceptions  --param=ssp-buffer-size=4" \
  ./configure \
    --build=%_build --host=%{_mingw_host} --target=%{_mingw_target} \
    --prefix=%{_mingw_prefix} --with-arch=i686
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT/%{_mingw_libdir}/charset.alias

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/fc-cache.exe
%{_mingw_bindir}/fc-cat.exe
%{_mingw_bindir}/fc-list.exe
%{_mingw_bindir}/fc-match.exe
%{_mingw_bindir}/libfontconfig-1.dll
%{_mingw_libdir}/fontconfig.def
%{_mingw_libdir}/libfontconfig.a
%{_mingw_libdir}/libfontconfig.dll.a
%{_mingw_libdir}/libfontconfig.la
%{_mingw_libdir}/pkgconfig/fontconfig.pc
%{_mingw_includedir}/fontconfig/
%{_mingw_sysconfdir}/fonts/
%{_mingw_mandir}/man1/fc-cache.1*
%{_mingw_mandir}/man1/fc-cat.1*
%{_mingw_mandir}/man1/fc-list.1*
%{_mingw_mandir}/man1/fc-match.1*
%{_mingw_mandir}/man3/Fc*.3*
%{_mingw_mandir}/man5/fonts-conf.5*
%{_mingw_datadir}/doc/fontconfig

%changelog
* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 2.18.0-1
- Initial RPM release
