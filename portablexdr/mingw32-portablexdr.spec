%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-portablexdr
Version:        4.0.11
Release:        2%{?dist}
Summary:        MinGW Windows PortableXDR XDR / RPC library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://et.redhat.com/~rjones/portablexdr/
Source0:        http://et.redhat.com/~rjones/portablexdr/portablexdr-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils


%description
MinGW Windows PortableXDR XDR / RPC library.


%prep
%setup -q -n portablexdr-%{version}


%build
%{_mingw32_configure} --disable-static
make %{?_smp_flags}


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libportablexdr-0.dll
%{_mingw32_libdir}/libportablexdr.dll.a
%{_mingw32_libdir}/libportablexdr.la
%{_mingw32_includedir}/rpc


%changelog
* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 4.0.11-2
- Disable static libraries.
- Use _smp_flags.

* Wed Oct 15 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.11-1
- New upstream version 4.0.11.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.10-5
- Rename mingw -> mingw32.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.10-4
- Remove static library.

* Fri Sep  5 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.10-3
- Use RPM macros from mingw-filesystem.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 4.0.10-2
- List files explicitly and set custom CFLAGS

* Tue Jul  8 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.10-1
- New upstream release 4.0.10.
- No need to manually install header files in this version.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.9-2
- Initial RPM release, largely based on earlier work from several sources.
