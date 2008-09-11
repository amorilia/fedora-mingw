%define __strip %{_mingw_strip}
%define __objdump %{_mingw_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw_findrequires}
%define __find_provides %{_mingw_findprovides}

Name:           mingw-gnutls
Version:        2.4.1
Release:        7%{?dist}
Summary:        MinGW Windows GnuTLS TLS/SSL encryption library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.gnu.org/software/gnutls/
Source0:        ftp://ftp.gnutls.org/pub/gnutls/gnutls-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Patch0:         gnutls-certtool-build.patch

BuildRequires:  mingw-filesystem >= 23
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


%build
autoreconf
PATH="%{_mingw_bindir}:$PATH" \
%{_mingw_configure} --with-included-libtasn1 --disable-cxx
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_mingw_datadir}/info/dir

rm $RPM_BUILD_ROOT%{_mingw_libdir}/libgnutls-extra.a
rm $RPM_BUILD_ROOT%{_mingw_libdir}/libgnutls-openssl.a
rm $RPM_BUILD_ROOT%{_mingw_libdir}/libgnutls.a


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
%{_mingw_bindir}/srptool.exe
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
%{_mingw_datadir}/info/gnutls-*.png
%{_mingw_datadir}/info/gnutls.info*
%{_mingw_mandir}/man1/certtool.1*
%{_mingw_mandir}/man1/gnutls-cli-debug.1*
%{_mingw_mandir}/man1/gnutls-cli.1*
%{_mingw_mandir}/man1/gnutls-serv.1*
%{_mingw_mandir}/man1/psktool.1*
%{_mingw_mandir}/man1/srptool.1*
%{_mingw_mandir}/man3/gnutls_*.3*
%{_mingw_datadir}/locale/*/LC_MESSAGES/gnutls.mo


%changelog
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
