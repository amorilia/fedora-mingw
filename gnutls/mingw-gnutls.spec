%define __strip %{_mingw_strip}
%define __objdump %{_mingw_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw_findrequires}
%define __find_provides %{_mingw_findprovides}

Name:           mingw-gnutls
Version:        2.4.2
Release:        1%{?dist}
Summary:        MinGW Windows GnuTLS TLS/SSL encryption library

License:        GPLv3+ and LGPLv2+
Group:          Development/Libraries
URL:            http://www.gnutls.org/
#Source0:        ftp://ftp.gnutls.org/pub/gnutls/gnutls-%{version}.tar.bz2
# XXX patent tainted SRP code removed.
Source0:        gnutls-%{version}-nosrp.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Patch0:         gnutls-certtool-build.patch
Patch1:         gnutls-2.4.0-nosrp.patch

BuildRequires:  mingw-filesystem >= 25
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-libgpg-error
BuildRequires:  mingw-libgcrypt
BuildRequires:  mingw-iconv
BuildRequires:  mingw-gettext
BuildRequires:  mingw-zlib
BuildRequires:  autoconf automake libtool

%description
MinGW Windows GnuTLS TLS/SSL encryption library.


%prep
%setup -q -n gnutls-%{version}
%patch0 -p1
%patch1 -p1

for i in auth_srp_rsa.c auth_srp_sb64.c auth_srp_passwd.c auth_srp.c gnutls_srp.c ext_srp.c; do
    touch lib/$i
done

%build
autoreconf
PATH="%{_mingw_bindir}:$PATH" \
%{_mingw_configure} --with-included-libtasn1 --disable-cxx \
           --disable-srp-authentication
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_mingw_datadir}/info/dir

rm $RPM_BUILD_ROOT%{_mingw_libdir}/libgnutls-extra.a
rm $RPM_BUILD_ROOT%{_mingw_libdir}/libgnutls-openssl.a
rm $RPM_BUILD_ROOT%{_mingw_libdir}/libgnutls.a

# Remove info and man pages which duplicate stuff in Fedora already.
rm -rf $RPM_BUILD_ROOT%{_mingw_infodir}
rm -rf $RPM_BUILD_ROOT%{_mingw_mandir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/certtool.exe
%{_mingw_bindir}/gnutls-cli-debug.exe
%{_mingw_bindir}/gnutls-cli.exe
%{_mingw_bindir}/gnutls-serv.exe
%{_mingw_bindir}/libgnutls-26.def
%{_mingw_bindir}/libgnutls-26.dll
%{_mingw_bindir}/libgnutls-config
%{_mingw_bindir}/libgnutls-extra-26.def
%{_mingw_bindir}/libgnutls-extra-26.dll
%{_mingw_bindir}/libgnutls-extra-config
%{_mingw_bindir}/libgnutls-openssl-26.def
%{_mingw_bindir}/libgnutls-openssl-26.dll
%{_mingw_bindir}/psktool.exe
%{_mingw_libdir}/libgnutls-extra.dll.a
%{_mingw_libdir}/libgnutls-extra.la
%{_mingw_libdir}/libgnutls-openssl.dll.a
%{_mingw_libdir}/libgnutls-openssl.la
%{_mingw_libdir}/libgnutls.dll.a
%{_mingw_libdir}/libgnutls.la
%{_mingw_libdir}/pkgconfig/gnutls-extra.pc
%{_mingw_libdir}/pkgconfig/gnutls.pc
%{_mingw_includedir}/gnutls/
%{_mingw_datadir}/aclocal/libgnutls-extra.m4
%{_mingw_datadir}/aclocal/libgnutls.m4
%{_mingw_datadir}/locale/*/LC_MESSAGES/gnutls.mo


%changelog
* Wed Sep 24 2008 Daniel P. Berrange <berrange@redhat.com> - 2.4.2-1
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
