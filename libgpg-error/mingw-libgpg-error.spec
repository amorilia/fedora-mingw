%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           mingw-libgpg-error
Version:        1.6
Release:        2%{?dist}
Summary:        MinGW Windows GnuPGP error library

License:        LGPLv2+
Group:          Development/Libraries
URL:            ftp://ftp.gnupg.org/GnuPG/libgpg-error
Source0:        ftp://ftp.gnupg.org/GnuPG/libgpg-error/libgpg-error-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils

Requires:       mingw-runtime

%description
MinGW Windows GnuPGP error library.


%prep
%setup -q -n libgpg-error-%{version}


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
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/gpg-error-config
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/gpg-error.exe
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libgpg-error-0.dll
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgpg-error.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgpg-error.dll.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgpg-error.la
%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/gpg-error.h
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/aclocal/gpg-error.m4
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/common-lisp/source/gpg-error/*

%changelog
* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 1.6-2
- List files explicitly and use custom CFLAGS

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 1.6-1
- Initial RPM release, largely based on earlier work from several sources.
