%define __strip %{_mingw_strip}
%define __objdump %{_mingw_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw_findrequires}
%define __find_provides %{_mingw_findprovides}

Name:           mingw-libvirt
Version:        0.4.5
Release:        4%{?dist}%{?extra_release}
Summary:        MinGW Windows libvirt virtualization library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://libvirt.org/
Source0:        ftp://libvirt.org/libvirt/libvirt-%{version}.tar.gz
Patch1:         libvirt-%{version}-no-emulator-segfault.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mingw-filesystem >= 23
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-libgpg-error
BuildRequires:  mingw-libgcrypt
BuildRequires:  mingw-gnutls
BuildRequires:  mingw-gettext
BuildRequires:  mingw-libxml2
BuildRequires:  mingw-portablexdr
BuildRequires:  pkgconfig
# Need native version for msgfmt
BuildRequires:  gettext

%description
MinGW Windows libvirt virtualization library.


%prep
%setup -q -n libvirt-%{version}
%patch1 -p1

%build
# XXX enable SASL in future
%{_mingw_configure} \
  --without-sasl \
  --without-avahi \
  --without-polkit \
  --without-python \
  --without-xen \
  --without-qemu \
  --without-lxc \
  --without-openvz \
  --without-libvirtd
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -rf $RPM_BUILD_ROOT/%{_mingw_sysconfdir}/libvirt
rm -rf $RPM_BUILD_ROOT/%{_mingw_datadir}/doc/*
rm -rf $RPM_BUILD_ROOT/%{_mingw_datadir}/gtk-doc/*

rm $RPM_BUILD_ROOT%{_mingw_libdir}/libvirt.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/libvirt-0.dll
%{_mingw_bindir}/virsh.exe

%{_mingw_libdir}/libvirt.dll.a
%{_mingw_libdir}/libvirt.la
%{_mingw_libdir}/pkgconfig/libvirt.pc

%{_mingw_datadir}/locale/*/LC_MESSAGES/libvirt.mo

%dir %{_mingw_includedir}/libvirt
%{_mingw_includedir}/libvirt/libvirt.h
%{_mingw_includedir}/libvirt/virterror.h

%{_mingw_mandir}/man1/virsh.1*


%changelog
* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.5-4%{?extra_release}
- Import crash fix from rawhide

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.5-3%{?extra_release}
- Add dep on gettext & pkgconfig

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-2
- Remove static lib.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.4-1
- Initial RPM release, largely based on earlier work from several sources.
