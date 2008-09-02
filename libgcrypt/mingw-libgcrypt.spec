%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           mingw-libgcrypt
Version:        1.4.1
Release:        2%{?dist}
Summary:        MinGW Windows gcrypt encryption library

License:        LGPLv2+
Group:          Development/Libraries
URL:            ftp://ftp.gnupg.org/gcrypt/libgcrypt/
Source0:        ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-libgpg-error

Requires:       mingw-runtime
Requires:       mingw-libgpg-error

%description
MinGW Windows gcrypt encryption library.


%prep
%setup -q -n libgcrypt-%{version}


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
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/dumpsexp.exe
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libgcrypt-11.dll
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libgcrypt-config
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgcrypt.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgcrypt.def
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgcrypt.dll.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgcrypt.la
%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/gcrypt-module.h
%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/gcrypt.h
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/aclocal/libgcrypt.m4
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/info/gcrypt.info

%changelog
* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 1.4.1-2
- List files explicitly and use custom CFLAGS

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-1
- Initial RPM release, largely based on earlier work from several sources.
