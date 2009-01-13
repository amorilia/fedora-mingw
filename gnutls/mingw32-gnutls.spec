%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-gnutls
Version:        2.4.2
Release:        4%{?dist}
Summary:        MinGW Windows GnuTLS TLS/SSL encryption library

License:        GPLv3+ and LGPLv2+
Group:          Development/Libraries
URL:            http://www.gnutls.org/
#Source0:        ftp://ftp.gnutls.org/pub/gnutls/gnutls-%{version}.tar.bz2
# XXX patent tainted SRP code removed.
Source0:        gnutls-%{version}-nosrp.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Patch1:         gnutls-2.4.0-nosrp.patch
Patch5:         gnutls-1.4.1-cve-2008-4989.patch

# MinGW-specific patches.
Patch1000:      gnutls-certtool-build.patch

BuildRequires:  mingw32-filesystem >= 25
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-libgpg-error
BuildRequires:  mingw32-libgcrypt
BuildRequires:  mingw32-iconv
BuildRequires:  mingw32-gettext
BuildRequires:  mingw32-zlib
BuildRequires:  autoconf automake libtool

Requires:       pkgconfig


%description
MinGW Windows GnuTLS TLS/SSL encryption library.


%prep
%setup -q -n gnutls-%{version}

%patch1 -p1 -b .nosrp
%patch5 -p1 -b .chain-verify

%patch1000 -p1 -b .mingw32

for i in auth_srp_rsa.c auth_srp_sb64.c auth_srp_passwd.c auth_srp.c gnutls_srp.c ext_srp.c; do
    touch lib/$i
done

%build
autoreconf
PATH="%{_mingw32_bindir}:$PATH" \
%{_mingw32_configure} --with-included-libtasn1 --disable-cxx \
           --disable-srp-authentication
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_mingw32_datadir}/info/dir

rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libgnutls-extra.a
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libgnutls-openssl.a
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libgnutls.a

# Remove info and man pages which duplicate stuff in Fedora already.
rm -rf $RPM_BUILD_ROOT%{_mingw32_infodir}
rm -rf $RPM_BUILD_ROOT%{_mingw32_mandir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
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
%{_mingw32_datadir}/locale/*/LC_MESSAGES/gnutls.mo


%changelog
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
