%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-libvirt
Version:        0.6.1
Release:        1%{?dist}%{?extra_release}
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
# Portable XDR <= 4.0.10 contains a serious endianness bug on Windows.
BuildRequires:  mingw32-portablexdr >= 4.0.11
BuildRequires:  mingw32-readline
BuildRequires:  mingw32-termcap >= 1.3.1-3
BuildRequires:  pkgconfig

# Need native version for msgfmt
BuildRequires:  gettext

BuildArch:      noarch

Requires:       pkgconfig


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
  --without-uml \
  --without-openvz \
  --without-libvirtd \
  --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -rf $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/libvirt
rm -rf $RPM_BUILD_ROOT%{_mingw32_datadir}/doc/*
rm -rf $RPM_BUILD_ROOT%{_mingw32_datadir}/gtk-doc/*

%find_lang libvirt


%clean
rm -rf $RPM_BUILD_ROOT


%files -f libvirt.lang
%defattr(-,root,root)
%doc COPYING.LIB
%{_mingw32_bindir}/libvirt-0.dll
%{_mingw32_bindir}/virsh.exe

%{_mingw32_libdir}/libvirt.dll.a
%{_mingw32_libdir}/libvirt.la
%{_mingw32_libdir}/pkgconfig/libvirt.pc

%dir %{_mingw32_datadir}/libvirt/
%dir %{_mingw32_datadir}/libvirt/schemas/
%{_mingw32_datadir}/libvirt/schemas/domain.rng
%{_mingw32_datadir}/libvirt/schemas/network.rng
%{_mingw32_datadir}/libvirt/schemas/storagepool.rng
%{_mingw32_datadir}/libvirt/schemas/storagevol.rng
%{_mingw32_datadir}/libvirt/schemas/nodedev.rng
%{_mingw32_datadir}/libvirt/schemas/capability.rng

%dir %{_mingw32_includedir}/libvirt
%{_mingw32_includedir}/libvirt/libvirt.h
%{_mingw32_includedir}/libvirt/virterror.h

%{_mingw32_mandir}/man1/virsh.1*


%changelog
* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 0.5.1-4
- Rebuild for mingw32-gcc 4.4

* Fri Jan 30 2009 Richard Jones <rjones@redhat.com> - 0.5.1-3
- Include license file.

* Fri Jan 30 2009 Richard Jones <rjones@redhat.com> - 0.5.1-2
- Requires pkgconfig.

* Fri Jan 23 2009 Richard Jones <rjones@redhat.com> - 0.5.1-1
- Rebase to Fedora native version 0.5.1.
- Use find_lang macro.
- Use _smp_mflags.
- Disable static libraries.

* Wed Nov 26 2008 Richard Jones <rjones@redhat.com> - 0.5.0-1
- New upstream version 0.5.0.

* Sat Nov 22 2008 Richard Jones <rjones@redhat.com> - 0.4.6-9
- Rebuild against new readline.

* Fri Oct 31 2008 Richard Jones <rjones@redhat.com> - 0.4.6-8
- Rebuild against latest termcap.

* Thu Oct 16 2008 Richard Jones <rjones@redhat.com> - 0.4.6-7
- Windows icon patch from
  https://www.redhat.com/archives/libvir-list/2008-October/msg00331.html

* Wed Oct 15 2008 Richard Jones <rjones@redhat.com> - 0.4.6-6
- Add patches from
  https://www.redhat.com/archives/libvir-list/2008-October/msg00328.html
- BR mingw32-portablexdr >= 4.0.11 to fix serious Windows endianness bug.

* Tue Oct 14 2008 Richard Jones <rjones@redhat.com> - 0.4.6-4
- +BR mingw32-readline.

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
