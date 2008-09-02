%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           mingw-gnutls
Version:        2.4.1
Release:        2%{?dist}
Summary:        MinGW Windows GnuTLS TLS/SSL encryption library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.gnu.org/software/gnutls/
Source0:        ftp://ftp.gnutls.org/pub/gnutls/gnutls-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-libgpg-error
BuildRequires:  mingw-libgcrypt

Requires:       mingw-runtime
Requires:       mingw-libgpg-error
Requires:       mingw-libgcrypt

%description
MinGW Windows GnuTLS TLS/SSL encryption library.


%prep
%setup -q -n gnutls-%{version}


%build
CFLAGS="-O2 -g -Wall -pipe" \
./configure \
  --build=%_build \
  --host=i686-pc-mingw32 \
  --prefix=%{_prefix}/i686-pc-mingw32/sys-root/mingw \
  --disable-cxx
# Disable C++ package until we have a C++ compiler (see mingw-gcc).

make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/certtool.exe
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/gnutls-cli-debug.exe
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/gnutls-cli.exe
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/gnutls-serv.exe
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libgnutls-26.def
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libgnutls-26.dll
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libgnutls-config
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libgnutls-extra-26.def
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libgnutls-extra-26.dll
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libgnutls-extra-config
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libgnutls-openssl-26.def
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libgnutls-openssl-26.dll
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/psktool.exe
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/srptool.exe
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgnutls-extra.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgnutls-extra.dll.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgnutls-extra.la
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgnutls-openssl.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgnutls-openssl.dll.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgnutls-openssl.la
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgnutls.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgnutls.dll.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgnutls.la
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/pkgconfig/gnutls-extra.pc
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/pkgconfig/gnutls.pc
%dir %{_prefix}/i686-pc-mingw32/sys-root/mingw/include/gnutls
%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/gnutls/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/aclocal/libgnutls-extra.m4
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/aclocal/libgnutls.m4
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/info/gnutls-*.png
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/info/gnutls.info*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/certtool.1*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/gnutls-cli-debug.1*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/gnutls-cli.1*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/gnutls-serv.1*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/psktool.1*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/srptool.1*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/gnutls_*.3*


%changelog
* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 2.4.1-2
- List files explicitly and use custom CFLAGS

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 2.4.1-1
- Initial RPM release, largely based on earlier work from several sources.
