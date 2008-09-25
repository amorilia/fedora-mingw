%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-libvirt
Version:        0.4.6
Release:        3%{?dist}%{?extra_release}
Summary:        MinGW Windows libvirt virtualization library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://libvirt.org/
Source0:        ftp://libvirt.org/libvirt/libvirt-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-libgpg-error
BuildRequires:  mingw32-libgcrypt
BuildRequires:  mingw32-gnutls
BuildRequires:  mingw32-gettext
BuildRequires:  mingw32-libxml2
BuildRequires:  mingw32-portablexdr
BuildRequires:  pkgconfig
# Need native version for msgfmt
BuildRequires:  gettext

BuildArch:      noarch


%description
MinGW Windows libvirt virtualization library.


%prep
%setup -q -n libvirt-%{version}


%build
# XXX enable SASL in future
%{_mingw32_configure} \
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

rm -rf $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/libvirt
rm -rf $RPM_BUILD_ROOT%{_mingw32_datadir}/doc/*
rm -rf $RPM_BUILD_ROOT%{_mingw32_datadir}/gtk-doc/*

rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libvirt.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libvirt-0.dll
%{_mingw32_bindir}/virsh.exe

%{_mingw32_libdir}/libvirt.dll.a
%{_mingw32_libdir}/libvirt.la
%{_mingw32_libdir}/pkgconfig/libvirt.pc

%{_mingw32_datadir}/locale/*/LC_MESSAGES/libvirt.mo

%dir %{_mingw32_includedir}/libvirt
%{_mingw32_includedir}/libvirt/libvirt.h
%{_mingw32_includedir}/libvirt/virterror.h

%{_mingw32_mandir}/man1/virsh.1*


%changelog
* Thu Sep 25 2008 Richard Jones <rjones@redhat.com> - 0.4.6-3
- BuildArch should be noarch

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.6-2
- Whitespace removal.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.6-1
- New upstream release 0.4.6.
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.5-4%{?extra_release}
- Import crash fix from rawhide

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.5-3%{?extra_release}
- Add dep on gettext & pkgconfig

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-2
- Remove static lib.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.4-1
- Initial RPM release, largely based on earlier work from several sources.
