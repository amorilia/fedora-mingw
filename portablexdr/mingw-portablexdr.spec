%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           mingw-portablexdr
Version:        4.0.10
Release:        1%{?dist}
Summary:        MinGW Windows PortableXDR XDR / RPC library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://et.redhat.com/~rjones/portablexdr/
Source0:        http://et.redhat.com/~rjones/portablexdr/portablexdr-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils

Requires:       mingw-runtime

%description
MinGW Windows PortableXDR XDR / RPC library.


%prep
%setup -q -n portablexdr-%{version}


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
%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/rpc


%changelog
* Tue Jul  8 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.10-1
- New upstream release 4.0.10.
- No need to manually install header files in this version.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.9-2
- Initial RPM release, largely based on earlier work from several sources.
