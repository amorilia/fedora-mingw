%include /usr/lib/rpm/mingw-defs

Name:           mingw-jasper
Version:        1.900.1
Release:        1%{?dist}
Summary:        MinGW Windows Jasper library

License: JasPer
URL:     http://www.ece.uvic.ca/~mdadams/jasper/
Source0: http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-%{version}.zip
Patch1: jasper-%{version}-sleep.patch
Patch2: jasper-%{version}-mingw.patch
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 19
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-libjpeg

%description
MinGW Windows Jasper library.


%prep
%setup -q -n jasper-%{version}
%patch1 -p1
%patch2 -p1

%build
%{_mingw_configure} --disable-opengl --enable-libjpeg
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install mandir=%{_mingw_mandir}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
# XXX dlls
%{_mingw_bindir}/i686-pc-mingw32-imgcmp.exe
%{_mingw_bindir}/i686-pc-mingw32-imginfo.exe
%{_mingw_bindir}/i686-pc-mingw32-jasper.exe
%{_mingw_bindir}/i686-pc-mingw32-tmrdemo.exe
%{_mingw_includedir}/jasper/
%{_mingw_libdir}/libjasper.a
%{_mingw_libdir}/libjasper.la
%{_mingw_mandir}/man1/i686-pc-mingw32-imgcmp.1*
%{_mingw_mandir}/man1/i686-pc-mingw32-imginfo.1*
%{_mingw_mandir}/man1/i686-pc-mingw32-jasper.1*
%{_mingw_mandir}/man1/i686-pc-mingw32-jiv.1*

%changelog
* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 2.18.0-1
- Initial RPM release
