%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-jasper
Version:        1.900.1
Release:        6%{?dist}
Summary:        MinGW Windows Jasper library

License:        JasPer
URL:            http://www.ece.uvic.ca/~mdadams/jasper/
Source0:        http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-%{version}.zip
Patch1:         jasper-1.900.1-sleep.patch
Patch2:         jasper-1.900.1-mingw32.patch
Patch3:         jasper-1.900.1-enable-shared.patch
Patch4:         patch-libjasper-stepsizes-overflow.diff
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-libjpeg
BuildRequires:  autoconf automake libtool

%description
MinGW Windows Jasper library.


%prep
%setup -q -n jasper-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1


%build
autoreconf
%{_mingw32_configure} --disable-opengl --enable-libjpeg --disable-static
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install mandir=%{_mingw32_mandir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
# XXX dlls
%{_mingw32_bindir}/i686-pc-mingw32-imgcmp.exe
%{_mingw32_bindir}/i686-pc-mingw32-imginfo.exe
%{_mingw32_bindir}/i686-pc-mingw32-jasper.exe
%{_mingw32_bindir}/i686-pc-mingw32-tmrdemo.exe
%{_mingw32_bindir}/libjasper-1.dll
%{_mingw32_libdir}/libjasper.dll.a
%{_mingw32_libdir}/libjasper.la
%{_mingw32_includedir}/jasper/
%{_mingw32_mandir}/man1/i686-pc-mingw32-imgcmp.1*
%{_mingw32_mandir}/man1/i686-pc-mingw32-imginfo.1*
%{_mingw32_mandir}/man1/i686-pc-mingw32-jasper.1*
%{_mingw32_mandir}/man1/i686-pc-mingw32-jiv.1*


%changelog
* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.900.1-6
- Use _smp_mflags.
- Disable static libraries.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.900.1-5
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 1.900.1-4
- Add overflow patch from rawhide

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 1.900.1-3
- Run autoreconf after changing configure.ac script and add BRs for autotools

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.900.1-2
- Enable DLLs.
- Remove static libraries.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.900.1-1
- Initial RPM release
