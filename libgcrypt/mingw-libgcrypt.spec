%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           mingw-libgcrypt
Version:        1.4.1
Release:        1%{?dist}
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
CFLAGS="$RPM_OPT_FLAGS -fno-stack-protector" \
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
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/aclocal/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/info/*


%changelog
* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-1
- Initial RPM release, largely based on earlier work from several sources.
