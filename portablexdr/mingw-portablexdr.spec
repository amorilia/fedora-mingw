%include /usr/lib/rpm/mingw-defs

Name:           mingw-portablexdr
Version:        4.0.10
Release:        3%{?dist}
Summary:        MinGW Windows PortableXDR XDR / RPC library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://et.redhat.com/~rjones/portablexdr/
Source0:        http://et.redhat.com/~rjones/portablexdr/portablexdr-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 19
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils


%description
MinGW Windows PortableXDR XDR / RPC library.


%prep
%setup -q -n portablexdr-%{version}


%build
%{_mingw_configure}
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/libportablexdr-0.dll
%{_mingw_libdir}/libportablexdr.a
%{_mingw_libdir}/libportablexdr.dll.a
%{_mingw_libdir}/libportablexdr.la
%{_mingw_includedir}/rpc


%changelog
* Fri Sep  5 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.10-3
- Use RPM macros from mingw-filesystem.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 4.0.10-2
- List files explicitly and set custom CFLAGS

* Tue Jul  8 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.10-1
- New upstream release 4.0.10.
- No need to manually install header files in this version.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.9-2
- Initial RPM release, largely based on earlier work from several sources.
