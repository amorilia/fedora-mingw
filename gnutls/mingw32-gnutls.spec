%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-gnutls
Version:        2.6.3
Release:        5%{?dist}
Summary:        MinGW Windows GnuTLS TLS/SSL encryption library

License:        GPLv3+ and LGPLv2+
Group:          Development/Libraries
URL:            http://www.gnutls.org/
#Source0:        ftp://ftp.gnutls.org/pub/gnutls/gnutls-%{version}.tar.bz2
# XXX patent tainted SRP code removed.
Source0:        gnutls-%{version}-nosrp.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Patch1:         gnutls-2.6.2-nosrp.patch

# MinGW-specific patches.
Patch1000:      mingw32-gnutls-2.6.3-certtool-build.patch

BuildRequires:  mingw32-filesystem >= 40
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-libgpg-error
BuildRequires:  mingw32-libgcrypt >= 1.2.2
BuildRequires:  mingw32-gettext
BuildRequires:  mingw32-iconv
BuildRequires:  mingw32-readline
BuildRequires:  mingw32-zlib

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

# Yes, really ...
BuildRequires:  pkgconfig

# For native /usr/bin/msgfmt etc.
BuildRequires:  gettext

Requires:       pkgconfig


%description
MinGW Windows GnuTLS TLS/SSL encryption library.


%prep
%setup -q -n gnutls-%{version}

%patch1 -p1 -b .nosrp

%patch1000 -p1 -b .mingw32

for i in auth_srp_rsa.c auth_srp_sb64.c auth_srp_passwd.c auth_srp.c gnutls_srp.c ext_srp.c; do
    touch lib/$i
done

%if 0%{?fedora} > 10
libtoolize --force --copy
aclocal
autoreconf
%endif


%build
PATH="%{_mingw32_bindir}:$PATH" \
%{_mingw32_configure} \
  --with-included-libtasn1 \
  --disable-srp-authentication \
  --disable-static
# %{?_smp_mflags} doesn't build correctly.
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_mingw32_datadir}/info/dir

# Remove info and man pages which duplicate stuff in Fedora already.
rm -rf $RPM_BUILD_ROOT%{_mingw32_infodir}
rm -rf $RPM_BUILD_ROOT%{_mingw32_mandir}

%find_lang gnutls


%clean
rm -rf $RPM_BUILD_ROOT


%files -f gnutls.lang
%defattr(-,root,root)
%doc COPYING COPYING.LIB
%{_mingw32_bindir}/certtool.exe
%{_mingw32_bindir}/gnutls-cli-debug.exe
%{_mingw32_bindir}/gnutls-cli.exe
%{_mingw32_bindir}/gnutls-serv.exe
%{_mingw32_bindir}/libgnutls-26.def
%{_mingw32_bindir}/libgnutls-26.dll
%{_mingw32_bindir}/libgnutls-config
%{_mingw32_bindir}/libgnutls-extra-26.def
%{_mingw32_bindir}/libgnutls-extra-26.dll
%{_mingw32_bindir}/libgnutls-extra-config
%{_mingw32_bindir}/libgnutls-openssl-26.def
%{_mingw32_bindir}/libgnutls-openssl-26.dll
%{_mingw32_bindir}/psktool.exe
%{_mingw32_libdir}/libgnutls-extra.dll.a
%{_mingw32_libdir}/libgnutls-extra.la
%{_mingw32_libdir}/libgnutls-openssl.dll.a
%{_mingw32_libdir}/libgnutls-openssl.la
%{_mingw32_libdir}/libgnutls.dll.a
%{_mingw32_libdir}/libgnutls.la
%{_mingw32_libdir}/pkgconfig/gnutls-extra.pc
%{_mingw32_libdir}/pkgconfig/gnutls.pc
%{_mingw32_includedir}/gnutls/
%{_mingw32_datadir}/aclocal/libgnutls-extra.m4
%{_mingw32_datadir}/aclocal/libgnutls.m4


%changelog
* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2.6.3-5
- Rebuild for mingw32-gcc 4.4

* Thu Feb 19 2009 Richard W.M. Jones <rjones@redhat.com> - 2.6.3-4
- +BR mingw32-gcc-c++

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 2.6.3-3
- Include license.

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 2.6.3-2
- Rebase to native Fedora version 2.6.3.
- Enable C++ library.
- Use find_lang macro.
- Don't build static library.
- Rebase MinGW patch to 2.6.3.
- +BR mingw32-dlfcn.
- +BR mingw32-readline.
- Force rebuild of libtool.

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 2.4.2-4
- Requires pkgconfig.

* Thu Nov 13 2008 Richard W.M. Jones <rjones@redhat.com> - 2.4.2-3
- fix chain verification issue CVE-2008-4989 (#470079)
- separate out the MinGW-specific patch from the others

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.4.2-2
- Rename mingw -> mingw32.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.4.2-1
- New native version.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 2.4.1-9
- Switch to source tar.bz2 with SRP stuff removed

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 2.4.1-8
- Remove duplicate manpages and info files.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 2.4.1-7
- Add BR on autoconf, automake and libtool

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 2.4.1-6
- Need to run autoreconf after patching src/Makefile.am.
- Remove static libs.

* Fri Sep  5 2008 Richard W.M. Jones <rjones@redhat.com> - 2.4.1-5
- Add patch to build certtool.exe because of missing dep of gnulib on intl.
- BuildArch is noarch.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 2.4.1-3
- Use mingw-filesystem RPM macros.
- Depends on mingw-iconv, mingw-gettext.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 2.4.1-2
- List files explicitly and use custom CFLAGS

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 2.4.1-1
- Initial RPM release, largely based on earlier work from several sources.
