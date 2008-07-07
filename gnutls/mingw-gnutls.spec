%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           mingw-gnutls
Version:        2.4.1
Release:        1%{?dist}
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
CFLAGS="$RPM_OPT_FLAGS -fno-stack-protector" \
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
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/aclocal/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/info/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/*


%changelog
* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 2.4.1-1
- Initial RPM release, largely based on earlier work from several sources.
