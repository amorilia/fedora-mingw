%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           mingw-libxml2
Version:        2.6.32
Release:        1%{?dist}
Summary:        MinGW Windows libxml2 XML processing library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.xmlsoft.org/
Source0:        ftp://xmlsoft.org/libxml2/libxml2-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils

Requires:       mingw-runtime

%description
MinGW Windows libxml2 XML processing library.


%prep
%setup -q -n libxml2-%{version}


%build
CFLAGS="$RPM_OPT_FLAGS -fno-stack-protector" \
./configure \
  --build=%_build \
  --host=i686-pc-mingw32 \
  --prefix=%{_prefix}/i686-pc-mingw32/sys-root/mingw \
  --without-python

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
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/doc/libxml2-%{version}/
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/gtk-doc/html/libxml2/
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/*


%changelog
* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 2.6.32-1
- Initial RPM release, largely based on earlier work from several sources.
