%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-libjpeg
Version:        6b
Release:        5%{?dist}
Summary:        MinGW Windows Libjpeg library

License:        IJG
URL:            http://www.ijg.org/
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v%{version}.tar.gz
Source1:        configure.in

Patch1:         jpeg-c++.patch
Patch4:         libjpeg-cflags.patch
Patch5:         libjpeg-buf-oflo.patch
Patch6:         libjpeg-autoconf.patch

Patch100:       jpeg-mingw32.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-libpng
BuildRequires:  mingw32-zlib
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
%{_mingw32_configure} --enable-shared --enable-static
make libdir=%{_mingw32_libdir}


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_includedir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_prefix}/man/man1

make prefix=$RPM_BUILD_ROOT%{_mingw32_prefix} install

# Remove static library.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libjpeg.a

# Remove manual pages which duplicate Fedora native.
rm -rf $RPM_BUILD_ROOT%{_mingw32_prefix}/man


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/cjpeg
%{_mingw32_bindir}/djpeg
%{_mingw32_bindir}/jpegtran
%{_mingw32_bindir}/rdjpgcom
%{_mingw32_bindir}/wrjpgcom
%{_mingw32_bindir}/libjpeg-62.dll
%{_mingw32_includedir}/jconfig.h
%{_mingw32_includedir}/jerror.h
%{_mingw32_includedir}/jmorecfg.h
%{_mingw32_includedir}/jpeglib.h
%{_mingw32_libdir}/libjpeg.dll.a
%{_mingw32_libdir}/libjpeg.la


%changelog
* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 6b-5
- Rename mingw -> mingw32.

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
