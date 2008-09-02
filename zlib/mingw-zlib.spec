%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           mingw-zlib
Version:        1.2.3
Release:        1%{?dist}
Summary:        MinGW Windows zlib compression library

License:        zlib
Group:          Development/Libraries
URL:            http://www.zlib.net/
Source0:        http://www.zlib.net/zlib-%{version}.tar.gz
Patch1:         zlib-win32.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils

Requires:       mingw-runtime

%description
MinGW Windows zlib compression library.


%prep
%setup -q -n zlib-1.2.3
%patch1 -p1

%build
CFLAGS="-O2 -g -pipe -Wall" \
CC=i686-pc-mingw32-gcc RANLIB=i686-pc-mingw32-ranlib ./configure

make -f win32/Makefile.gcc \
  CC=i686-pc-mingw32-gcc \
  AR=i686-pc-mingw32-ar \
  RC=i686-pc-mingw32-windres \
  DLLWRAP=i686-pc-mingw32-dllwrap \
  STRIP=i686-pc-mingw32-strip \
  all

%install
rm -rf $RPM_BUILD_ROOT

make -f win32/Makefile.gcc \
     INCLUDE_PATH=$RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/include \
     LIBRARY_PATH=$RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib \
     install

mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3
%__install zlib.3  $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/zconf.h
%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/zlib.h
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libz.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libzdll.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libz.dll
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/zlib.3


%changelog
* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.50_20080109_2-5
- Initial RPM release, largely based on earlier work from several sources.
