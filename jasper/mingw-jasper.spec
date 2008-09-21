%define __strip %{_mingw_strip}
%define __objdump %{_mingw_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw_findrequires}
%define __find_provides %{_mingw_findprovides}

Name:           mingw-jasper
Version:        1.900.1
Release:        3%{?dist}
Summary:        MinGW Windows Jasper library

License:        JasPer
URL:            http://www.ece.uvic.ca/~mdadams/jasper/
Source0:        http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-%{version}.zip
Patch1:         jasper-1.900.1-sleep.patch
Patch2:         jasper-1.900.1-mingw.patch
Patch3:         jasper-1.900.1-enable-shared.patch
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 23
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-libjpeg
BuildRequires:  autoconf automake libtool

%description
MinGW Windows Jasper library.


%prep
%setup -q -n jasper-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1


%build
autoreconf
%{_mingw_configure} --disable-opengl --enable-libjpeg
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install mandir=%{_mingw_mandir}

rm $RPM_BUILD_ROOT%{_mingw_libdir}/libjasper.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
# XXX dlls
%{_mingw_bindir}/i686-pc-mingw32-imgcmp.exe
%{_mingw_bindir}/i686-pc-mingw32-imginfo.exe
%{_mingw_bindir}/i686-pc-mingw32-jasper.exe
%{_mingw_bindir}/i686-pc-mingw32-tmrdemo.exe
%{_mingw_bindir}/libjasper-1.dll
%{_mingw_libdir}/libjasper.dll.a
%{_mingw_libdir}/libjasper.la
%{_mingw_includedir}/jasper/
%{_mingw_mandir}/man1/i686-pc-mingw32-imgcmp.1*
%{_mingw_mandir}/man1/i686-pc-mingw32-imginfo.1*
%{_mingw_mandir}/man1/i686-pc-mingw32-jasper.1*
%{_mingw_mandir}/man1/i686-pc-mingw32-jiv.1*


%changelog
* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 1.900.1-3
- Run autoreconf after changing configure.ac script and add BRs for autotools

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.900.1-2
- Enable DLLs.
- Remove static libraries.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.900.1-1
- Initial RPM release
