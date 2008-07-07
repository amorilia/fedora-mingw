%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           mingw-libgpg-error
Version:        1.6
Release:        1%{?dist}
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
CFLAGS="$RPM_OPT_FLAGS" \
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
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/aclocal/gpg-error.m4
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/common-lisp/source/gpg-error/*


%changelog
* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 1.6-1
- Initial RPM release, largely based on earlier work from several sources.
