%include        /usr/lib/rpm/mingw-defs

Name:           mingw-libvirt
Version:        0.4.5
Release:        2%{?dist}%{?extra_release}
Summary:        MinGW Windows libvirt virtualization library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.libvirt.org/
Source0:        ftp://libvirt.org/libvirt/libvirt-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mingw-filesystem >= 19
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-libgpg-error
BuildRequires:  mingw-libgcrypt
BuildRequires:  mingw-gnutls
BuildRequires:  mingw-gettext
BuildRequires:  mingw-libxml2
BuildRequires:  mingw-portablexdr


%description
MinGW Windows libvirt virtualization library.


%prep
%setup -q -n libvirt-%{version}


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
* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-2
- Remove static lib.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.4-1
- Initial RPM release, largely based on earlier work from several sources.
