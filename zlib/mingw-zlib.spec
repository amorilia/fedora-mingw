
%define __strip %{_mingw_strip}
%define __objdump %{_mingw_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw_findrequires}
%define __find_provides %{_mingw_findprovides}

Name:           mingw-zlib
Version:        1.2.3
Release:        6%{?dist}
Summary:        MinGW Windows zlib compression library

License:        zlib
Group:          Development/Libraries
URL:            http://www.zlib.net/
Source0:        http://www.zlib.net/zlib-%{version}.tar.gz
Patch1:         zlib-win32.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 23
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils

# For some reason mingw-find-provides doesn't get this.
Provides:       mingw(zlib1.dll)

%description
MinGW Windows zlib compression library.


%prep
%setup -q -n zlib-1.2.3
%patch1 -p1


%build
CC=%{_mingw_cc} \
CFLAGS="%{_mingw_cflags}" \
RANLIB=%{_mingw_ranlib} \
./configure

make -f win32/Makefile.gcc \
  CC=%{_mingw_cc} \
  AR=%{_mingw_ar} \
  RC=i686-pc-mingw32-windres \
  DLLWRAP=i686-pc-mingw32-dllwrap \
  STRIP=%{_mingw_strip} \
  all


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_mingw_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mingw_includedir}
mkdir -p $RPM_BUILD_ROOT%{_mingw_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mingw_mandir}/man3

make -f win32/Makefile.gcc \
     INCLUDE_PATH=$RPM_BUILD_ROOT%{_mingw_includedir} \
     LIBRARY_PATH=$RPM_BUILD_ROOT%{_mingw_libdir} \
     BINARY_PATH=$RPM_BUILD_ROOT%{_mingw_bindir} \
     install

# .dll.a file is misnamed for some reason - fix that.
mv $RPM_BUILD_ROOT%{_mingw_libdir}/libzdll.a \
   $RPM_BUILD_ROOT%{_mingw_libdir}/libz.dll.a

# Remove static library.
rm $RPM_BUILD_ROOT%{_mingw_libdir}/libz.a

%__install zlib.3 $RPM_BUILD_ROOT%{_mingw_mandir}/man3


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_includedir}/zconf.h
%{_mingw_includedir}/zlib.h
%{_mingw_libdir}/libz.dll.a
%{_mingw_bindir}/zlib1.dll
%{_mingw_mandir}/man3/zlib.3


%changelog
* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-6
- Remove static library.

* Fri Sep  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-5
- Fix misnamed file: zlibdll.a -> zlib.dll.a
- Explicitly provide mingw(zlib1.dll).

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-3
- Initial RPM release, largely based on earlier work from several sources.
