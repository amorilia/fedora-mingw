%define __strip %{_mingw_strip}
%define __objdump %{_mingw_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw_findrequires}
%define __find_provides %{_mingw_findprovides}

Name:           mingw-libjpeg
Version:        6b
Release:        4%{?dist}
Summary:        MinGW Windows Libjpeg library

License:        IJG
URL:            http://www.ijg.org/
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v%{version}.tar.bz2
Source1:        configure.in

Patch1:         jpeg-c++.patch
Patch4:         libjpeg-cflags.patch
Patch5:         libjpeg-buf-oflo.patch
Patch6:         libjpeg-autoconf.patch

Patch100:       jpeg-mingw.patch

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 23
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-libpng
BuildRequires:  mingw-zlib
BuildRequires:  autoconf, libtool

%description
MinGW Windows Libjpeg library.


%prep
%setup -q -n jpeg-6b

%patch1 -p1 -b .c++
%patch4 -p1 -b .cflags
%patch5 -p1 -b .oflo
%patch6 -p1

%patch100 -p1

# For long-obsolete reasons, libjpeg 6b doesn't ship with a configure.in.
# We need to re-autoconf though, in order to update libtool support,
# so supply configure.in.
cp %{SOURCE1} configure.in

# libjpeg 6b includes a horribly obsolete version of libtool.
# Blow it away and replace with build system's version.
rm -f config.guess config.sub ltmain.sh ltconfig aclocal.m4
cp /usr/share/aclocal/libtool.m4 aclocal.m4
libtoolize
autoconf

%build
%{_mingw_configure} --enable-shared --enable-static
make libdir=%{_mingw_libdir}


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_mingw_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mingw_includedir}
mkdir -p $RPM_BUILD_ROOT%{_mingw_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mingw_prefix}/man/man1

make prefix=$RPM_BUILD_ROOT%{_mingw_prefix} install

# Remove static library.
rm $RPM_BUILD_ROOT%{_mingw_libdir}/libjpeg.a

# Remove manual pages which duplicate Fedora native.
rm -rf $RPM_BUILD_ROOT%{_mingw_prefix}/man


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/cjpeg
%{_mingw_bindir}/djpeg
%{_mingw_bindir}/jpegtran
%{_mingw_bindir}/rdjpgcom
%{_mingw_bindir}/wrjpgcom
%{_mingw_bindir}/libjpeg-62.dll
%{_mingw_includedir}/jconfig.h
%{_mingw_includedir}/jerror.h
%{_mingw_includedir}/jmorecfg.h
%{_mingw_includedir}/jpeglib.h
%{_mingw_libdir}/libjpeg.dll.a
%{_mingw_libdir}/libjpeg.la


%changelog
* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 6b-4
- Switch to tar.bz2 source, and rename configure.in

* Sun Sep 21 2008 Daniel P. Berrange <berrange@redhat.com> - 6b-3
- Fix URL.
- Remove manpages which duplicate Fedora native.

* Wed Sep 10 2008 Daniel P. Berrange <berrange@redhat.com> - 6b-2
- Rename configure.in with a prefix.
- Remove static library.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 6b-1
- Initial RPM release
