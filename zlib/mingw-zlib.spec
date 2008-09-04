%include /usr/lib/rpm/mingw-defs

Name:           mingw-zlib
Version:        1.2.3
Release:        3%{?dist}
Summary:        MinGW Windows zlib compression library

License:        zlib
Group:          Development/Libraries
URL:            http://www.zlib.net/
Source0:        http://www.zlib.net/zlib-%{version}.tar.gz
Patch1:         zlib-win32.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 12
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils

Requires:       mingw-filesystem >= 12
Requires:       mingw-runtime

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
     install

# DLL needs to do in the bin directory.
mv $RPM_BUILD_ROOT%{_mingw_libdir}/libz.dll $RPM_BUILD_ROOT%{_mingw_bindir}

%__install zlib.3 $RPM_BUILD_ROOT%{_mingw_mandir}/man3


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_includedir}/zconf.h
%{_mingw_includedir}/zlib.h
%{_mingw_libdir}/libz.a
%{_mingw_libdir}/libzdll.a
%{_mingw_bindir}/libz.dll
%{_mingw_mandir}/man3/zlib.3


%changelog
* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-3
- Initial RPM release, largely based on earlier work from several sources.
