%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-curl
Version:        7.19.4
Release:        1%{?dist}
Summary:        MinGW Windows port of curl and libcurl

License:        MIT
Group:          Development/Libraries
URL:            http://curl.haxx.se/
Source0:        http://curl.haxx.se/download/curl-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

# Patches from native Fedora package.
Patch1:         curl-7.15.3-multilib.patch
Patch2:         curl-7.16.0-privlibs.patch
Patch3:         curl-7.17.1-badsocket.patch
Patch4:         curl-7.19.4-tool-leak.patch
Patch5:         curl-7.19.4-enable-aes.patch

# MinGW-specific patches.
Patch1000:      mingw-curl-7.18.2-getaddrinfo.patch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  pkgconfig
BuildRequires:  mingw32-gettext
BuildRequires:  mingw32-iconv
BuildRequires:  mingw32-zlib
BuildRequires:  mingw32-libidn
BuildRequires:  mingw32-libssh2

# See nss/README for the status of this package.
#BuildRequires:  mingw32-nss
# Temporarily we can use OpenSSL instead of NSS:
BuildRequires:  mingw32-openssl

# Not started porting this package yet.
#BuildRequires:  mingw32-openldap

# Not started porting this package yet.
#BuildRequires:  mingw32-krb5

Requires:       pkgconfig


%description
cURL is a tool for getting files from HTTP, FTP, FILE, LDAP, LDAPS,
DICT, TELNET and TFTP servers, using any of the supported protocols.
cURL is designed to work without user interaction or any kind of
interactivity. cURL offers many useful capabilities, like proxy
support, user authentication, FTP upload, HTTP post, and file transfer
resume.

This is the MinGW cross-compiled Windows library.


%package static
Summary:        Static version of the MinGW Windows Curl library
Requires:       %{name} = %{version}-%{release}
Group:          Development/Libraries

%description static
Static version of the MinGW Windows Curl library.


%prep
%setup -q -n curl-%{version}

%patch1 -p1 -b .multilib
%patch2 -p1 -b .privlibs
%patch3 -p1 -b .badsocket
%patch4 -p1 -b .toolleak
%patch5 -p1 -b .enableaes

%patch1000 -p1 -b .getaddrinfo


%build
%{_mingw32_configure} \
  --with-ssl --enable-ipv6 \
  --with-ca-bundle=%{_mingw32_sysconfdir}/pki/tls/certs/ca-bundle.crt \
  --with-libidn \
  --enable-static --with-libssh2 \
  --without-random

# It's not clear where to set the --with-ca-bundle path.  This is the
# default for CURLOPT_CAINFO.  If this doesn't exist, you'll get an
# error from all https transfers unless the program sets
# CURLOPT_CAINFO to point to the correct ca-bundle.crt file.

# --without-random disables random number collection (eg. from
# /dev/urandom).  There isn't an obvious alternative for Windows:
# Perhaps we can port EGD or use a library such as Yarrow.

# These are the original flags that we'll work towards as
# more of the dependencies get ported to Fedora MinGW.
#
#  --without-ssl --with-nss=%{_mingw32_prefix} --enable-ipv6
#  --with-ca-bundle=%{_mingw32_sysconfdir}/pki/tls/certs/ca-bundle.crt
#  --with-gssapi=%{_mingw32_prefix}/kerberos --with-libidn
#  --enable-ldaps --disable-static --with-libssh2

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove the man pages which duplicate documentation in the
# native Fedora package.
rm -r $RPM_BUILD_ROOT%{_mingw32_mandir}/man{1,3}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING
%{_mingw32_bindir}/curl-config
%{_mingw32_bindir}/curl.exe
%{_mingw32_bindir}/libcurl-4.dll
%{_mingw32_libdir}/libcurl.dll.a
%{_mingw32_libdir}/libcurl.la
%{_mingw32_libdir}/pkgconfig/libcurl.pc
%{_mingw32_includedir}/curl/


%files static
%defattr(-,root,root,-)
%{_mingw32_libdir}/libcurl.a

%changelog
* Fri Apr  3 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.19.4-1
- Update to version 7.19.4
- Fixed %%defattr line
- Added -static subpackage. Applications which want to use this
  static library need to add -DCURL_STATICLIB to the CFLAGS
- Merged the patches of the native .spec file (7.19.4-5)

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 7.18.2-6
- Rebuild for mingw32-gcc 4.4

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 7.18.2-5
- Include license.

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 7.18.2-4
- Rebuild against new OpenSSH (because of soname bump).

* Fri Jan 30 2009 Richard W.M. Jones <rjones@redhat.com> - 7.18.2-3
- Requires pkgconfig.

* Thu Nov 13 2008 Richard W.M. Jones <rjones@redhat.com> - 7.18.2-2
- Requires mingw32-filesystem >= 35.

* Thu Nov 13 2008 Richard W.M. Jones <rjones@redhat.com> - 7.18.2-1
- Initial RPM release.
