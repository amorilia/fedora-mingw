%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           mingw-libvirt
Version:        0.4.4
Release:        1%{?dist}
Summary:        MinGW Windows libvirt virtualization library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.libvirt.org/
Source0:        ftp://libvirt.org/libvirt/libvirt-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-libgpg-error
BuildRequires:  mingw-libgcrypt
BuildRequires:  mingw-gnutls
BuildRequires:  mingw-libxml2

Requires:       mingw-runtime
Requires:       mingw-libgpg-error
Requires:       mingw-libgcrypt
Requires:       mingw-gnutls
Requires:       mingw-libxml2

%description
MinGW Windows libvirt virtualization library.


%prep
%setup -q -n libvirt-%{version}


%build
# Make sure the true libxml path is available very early ...
CC="i686-pc-mingw32-gcc -I%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/libxml2" \
CFLAGS="$RPM_OPT_FLAGS -fno-stack-protector" \
./configure \
  --build=%_build \
  --host=i686-pc-mingw32 \
  --prefix=%{_prefix}/i686-pc-mingw32/sys-root/mingw \
  --without-xen --without-qemu --without-libvirtd \
  --without-sasl
# XXX Should include SASL, and maybe polkit?

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
* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.4-1
- Initial RPM release, largely based on earlier work from several sources.
