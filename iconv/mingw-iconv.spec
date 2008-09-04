%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:      mingw-iconv
Version:   1.12
Release:   1%{?dist}
Summary:   GNU libraries and utilities for producing multi-lingual messages

License:   GPLv2+ and LGPLv2+
Group:     Development/Libraries
URL:       http://www.gnu.org/software/iconv/
Source0:   http://ftp.gnu.org/pub/gnu/iconv/libiconv-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: mingw-gcc
BuildRequires: mingw-binutils

Requires:       mingw-runtime

%description
MinGW Windows Iconv library

%prep
%setup -q -n libiconv-%{version}

%build
CFLAGS="-O2 -g -Wall -pipe" \
./configure \
  --build=%_build \
  --host=i686-pc-mingw32 \
  --prefix=%{_prefix}/i686-pc-mingw32/sys-root/mingw

make

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/iconv
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libcharset-1.dll
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libiconv-2.dll
%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/iconv.h
%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/libcharset.h
%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/localcharset.h
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/charset.alias
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libcharset.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libcharset.dll.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libcharset.la
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libiconv.dll.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libiconv.la
%dir %{_prefix}/i686-pc-mingw32/sys-root/mingw/share/doc/libiconv/
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/doc/libiconv/*.html
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/iconv.1*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/iconv.3*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/iconv_close.3*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/iconv_open.3*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/iconvctl.3*


%changelog
* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 0.17-1
- Initial RPM release, largely based on earlier work from several sources.
