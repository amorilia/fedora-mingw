%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-zlib
Version:        1.2.3
Release:        10%{?dist}
Summary:        MinGW Windows zlib compression library

License:        zlib
Group:          Development/Libraries
URL:            http://www.zlib.net/
Source0:        http://www.zlib.net/zlib-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# From Fedora native package, none is applicable to us.
#Patch3:        zlib-1.2.3-autotools.patch
#Patch4:        minizip-1.2.3-autotools.patch
#Patch5:        zlib-1.2.3-minizip.patch

# MinGW-specific patches.
Patch100:       zlib-win32.patch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils


%description
MinGW Windows zlib compression library.


%prep
%setup -q -n zlib-1.2.3

%patch100 -p1


%build
CC=%{_mingw32_cc} \
CFLAGS="%{_mingw32_cflags}" \
RANLIB=%{_mingw32_ranlib} \
./configure

make -f win32/Makefile.gcc \
  CC=%{_mingw32_cc} \
  AR=%{_mingw32_ar} \
  RC=i686-pc-mingw32-windres \
  DLLWRAP=i686-pc-mingw32-dllwrap \
  STRIP=%{_mingw32_strip} \
  all


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_includedir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_libdir}

make -f win32/Makefile.gcc \
     INCLUDE_PATH=$RPM_BUILD_ROOT%{_mingw32_includedir} \
     LIBRARY_PATH=$RPM_BUILD_ROOT%{_mingw32_libdir} \
     BINARY_PATH=$RPM_BUILD_ROOT%{_mingw32_bindir} \
     install

# .dll.a file is misnamed for some reason - fix that.
mv $RPM_BUILD_ROOT%{_mingw32_libdir}/libzdll.a \
   $RPM_BUILD_ROOT%{_mingw32_libdir}/libz.dll.a

# Remove static library.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libz.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_includedir}/zconf.h
%{_mingw32_includedir}/zlib.h
%{_mingw32_libdir}/libz.dll.a
%{_mingw32_bindir}/zlib1.dll


%changelog
* Thu Oct 16 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-10
- Consider native patches.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-9
- Rename mingw -> mingw32.

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-8
- Remove manpage.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-7
- Remove static library.

* Fri Sep  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-5
- Fix misnamed file: zlibdll.a -> zlib.dll.a
- Explicitly provide mingw(zlib1.dll).

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-3
- Initial RPM release, largely based on earlier work from several sources.
