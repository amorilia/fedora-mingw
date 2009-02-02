%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

# For the curious:
# 0.9.5a soversion = 0
# 0.9.6  soversion = 1
# 0.9.6a soversion = 2
# 0.9.6c soversion = 3
# 0.9.7a soversion = 4
# 0.9.7ef soversion = 5
# 0.9.8ab soversion = 6
# 0.9.8g soversion = 7
# 0.9.8j + EAP-FAST soversion = 8
%define soversion 8

# Enable the tests.
# These only work some of the time, but fail randomly at other times
# (although I have had them complete a few times, so I don't think
# there is any actual problem with the binaries).
%define run_tests 0

# Number of threads to spawn when testing some threading fixes.
%define thread_test_threads %{?threads:%{threads}}%{!?threads:1}

Name:           mingw32-openssl
Version:        0.9.8j
Release:        2%{?dist}
Summary:        MinGW port of the OpenSSL toolkit

License:        OpenSSL
Group:          Development/Libraries
URL:            http://www.openssl.org/

# Use the hobble-openssl script to create the source file.
Source0:        openssl-%{version}-usa.tar.bz2

Source1:        hobble-openssl
Source2:        Makefile.certificate
Source6:        make-dummy-cert
Source8:        openssl-thread-test.c
Source9:        opensslconf-new.h
Source10:       opensslconf-new-warning.h

# Patches from Fedora native package.
# Build changes
Patch0:         openssl-0.9.8j-redhat.patch
Patch1:         openssl-0.9.8a-defaults.patch
Patch2:         openssl-0.9.8a-link-krb5.patch
Patch3:         openssl-0.9.8j-soversion.patch
Patch4:         openssl-0.9.8j-enginesdir.patch
Patch5:         openssl-0.9.8a-no-rpath.patch
Patch6:         openssl-0.9.8b-test-use-localhost.patch
Patch7:         openssl-0.9.8j-shlib-version.patch
# Bug fixes
Patch21:        openssl-0.9.8b-aliasing-bug.patch
Patch22:        openssl-0.9.8b-x509-name-cmp.patch
Patch23:        openssl-0.9.8g-default-paths.patch
Patch24:        openssl-0.9.8g-no-extssl.patch
# Functionality changes
Patch32:        openssl-0.9.8g-ia64.patch
Patch33:        openssl-0.9.8j-ca-dir.patch
Patch34:        openssl-0.9.6-x509.patch
Patch35:        openssl-0.9.8j-version-add-engines.patch
Patch38:        openssl-0.9.8a-reuse-cipher-change.patch
# Disabled this because it uses getaddrinfo which is lacking on Windows.
#Patch39:        openssl-0.9.8g-ipv6-apps.patch
Patch40:        openssl-0.9.8j-nocanister.patch
Patch41:        openssl-0.9.8j-use-fipscheck.patch
Patch42:        openssl-0.9.8j-fipscheck-hmac.patch
Patch43:        openssl-0.9.8j-evp-nonfips.patch
Patch44:        openssl-0.9.8j-kernel-fipsmode.patch
Patch45:        openssl-0.9.8j-env-nozlib.patch
Patch46:        openssl-0.9.8j-eap-fast.patch
Patch47:        openssl-0.9.8j-readme-warning.patch
Patch48:        openssl-0.9.8j-bad-mime.patch
Patch49:        openssl-0.9.8j-fips-no-pairwise.patch
# Backported fixes including security fixes

# MinGW-specific patches.
Patch100:       mingw32-openssl-0.9.8j-header-files.patch
Patch101:       mingw32-openssl-0.9.8j-configure.patch
Patch102:       mingw32-openssl-0.9.8j-shared.patch
Patch103:       mingw32-openssl-0.9.8g-global.patch
Patch104:       mingw32-openssl-0.9.8g-sfx.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 40
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw32-zlib
BuildRequires:  mingw32-pthreads

BuildRequires:  mktemp
#BuildRequires:  krb5-devel
BuildRequires:  perl
BuildRequires:  sed
BuildRequires:  /usr/bin/cmp
BuildRequires:  /usr/bin/rename

# XXX Not really sure about this one.  The build script uses
# /usr/bin/makedepend which comes from imake.
BuildRequires:  imake

%if %{run_tests}
# Required both to build, and to run the tests.
# XXX This needs to be fixed - cross-compilation should not
# require running executables.
BuildRequires:  wine

# Required to run the tests.
BuildRequires:  xorg-x11-server-Xvfb
%endif

#Requires:       ca-certificates >= 2008-5
Requires:       pkgconfig


%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains Windows (MinGW) libraries and development tools.


%prep
%setup -q -n openssl-%{version}

%{SOURCE1} > /dev/null
%patch0 -p1 -b .redhat
%patch1 -p1 -b .defaults
# Fix link line for libssl (bug #111154).
%patch2 -p1 -b .krb5
%patch3 -p1 -b .soversion
%patch4 -p1 -b .enginesdir
%patch5 -p1 -b .no-rpath
%patch6 -p1 -b .use-localhost
%patch7 -p1 -b .shlib-version

%patch21 -p1 -b .aliasing-bug
%patch22 -p1 -b .name-cmp
%patch23 -p1 -b .default-paths
%patch24 -p1 -b .no-extssl

%patch32 -p1 -b .ia64
#patch33 is applied after make test
%patch34 -p1 -b .x509
%patch35 -p1 -b .version-add-engines
%patch38 -p1 -b .cipher-change
#%patch39 -p1 -b .ipv6-apps
%patch40 -p1 -b .nocanister
%patch41 -p1 -b .use-fipscheck
%patch42 -p1 -b .fipscheck-hmac
%patch43 -p1 -b .evp-nonfips
%patch44 -p1 -b .fipsmode
%patch45 -p1 -b .env-nozlib
%patch46 -p1 -b .eap-fast
%patch47 -p1 -b .warning
%patch48 -p1 -b .bad-mime
%patch49 -p1 -b .no-pairwise

%patch100 -p1 -b .mingw-header-files
%patch101 -p1 -b .mingw-configure
%patch102 -p1 -b .mingw-shared
%patch103 -p1 -b .mingw-global
%patch104 -p1 -b .mingw-sfx

# Modify the various perl scripts to reference perl in the right location.
perl util/perlpath.pl `dirname %{__perl}`

# Generate a table with the compile settings for my perusal.
touch Makefile
make TABLE PERL=%{__perl}

%build
# NB: 'no-hw' is vital.  MinGW cannot build the hardware drivers
# and if you don't have this you'll get an obscure link error.
%{_mingw32_env}; \
sed -i -e "s/MINGW32_CC/%{_mingw32_cc}/" -e "s/MINGW32_CFLAGS/%{_mingw32_cflags}/" -e "s/MINGW32_RANLIB/%{_mingw32_ranlib}/" Configure; \
./Configure \
  --prefix=%{_mingw32_prefix} \
  --openssldir=%{_mingw32_sysconfdir}/pki/tls \
  zlib enable-camellia enable-seed enable-tlsext enable-rfc3779 \
  no-idea no-mdc2 no-rc5 no-ec no-ecdh no-ecdsa no-hw shared \
  --enginesdir=%{_mingw32_libdir}/openssl/engines \
  mingw
#  --with-krb5-flavor=MIT
#  -I%{_mingw32_prefix}/kerberos/include -L%{_mingw32_prefix}/kerberos/%{_lib}
%{_mingw32_make} depend
%{_mingw32_make} all build-shared

# Generate hashes for the included certs.
%{_mingw32_make} rehash build-shared

%if %{run_tests}
#----------------------------------------------------------------------
# Run some tests.  I don't know why this isn't in a %-check section
# but this is how it is in the native RPM.

# This is a bit of a hack, but the test scripts look for 'openssl'
# by name.
pushd apps
ln -s openssl.exe openssl
popd

# This is useful for diagnosing Wine problems.
WINEDEBUG=+loaddll
export WINEDEBUG

# Make sure we can find the installed DLLs.
WINEDLLPATH=%{_mingw32_bindir}
export WINEDLLPATH

# The tests run Wine and require an X server (but don't really use
# it).  Therefore we create a virtual framebuffer for the duration of
# the tests.
# XXX There is no good way to choose a random, unused display.
# XXX Setting depth to 24 bits avoids bug 458219.
unset DISPLAY
display=:21
Xvfb $display -screen 0 1024x768x24 -ac -noreset & xpid=$!
trap "kill -TERM $xpid ||:" EXIT
sleep 3
DISPLAY=$display
export DISPLAY

%{_mingw32_make} LDCMD=%{_mingw32_cc} -C test apps tests

# Disable this thread test, because we don't have pthread on Windows.
%{_mingw32_cc} -o openssl-thread-test \
  -I./include \
  %-{_mingw32_cflags} \
  %-{SOURCE8} \
  -L. \
  -lssl -lcrypto \
  -lpthread -lz -ldl

## `krb5-config --cflags`
## `krb5-config --libs`
#
./openssl-thread-test --threads %{thread_test_threads}

#----------------------------------------------------------------------
%endif

# Patch33 must be patched after tests otherwise they will fail
patch -p1 -b -z .ca-dir < %{PATCH33}

# Add generation of HMAC checksum of the final stripped library
#%define __spec_install_post \
#    %{?__debug_package:%{__debug_install_post}} \
#    %{__arch_install_post} \
#    %{__os_install_post} \
#    fips/fips_standalone_sha1 $RPM_BUILD_ROOT/%{_lib}/libcrypto.so.%{version} >$RPM_BUILD_ROOT/%{_lib}/.libcrypto.so.%{version}.hmac \
#    ln -sf .libcrypto.so.%{version}.hmac $RPM_BUILD_ROOT/%{_lib}/.libcrypto.so.%{soversion}.hmac \
#%{nil}

if ! iconv -f UTF-8 -t ASCII//TRANSLIT CHANGES >/dev/null 2>&1 ; then
  iconv -f ISO-8859-1 -t UTF-8 -o CHANGES.utf8 CHANGES && \
    mv -f CHANGES.utf8 CHANGES
fi


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_mingw32_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_libdir}/openssl
mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_includedir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_mandir}
make INSTALL_PREFIX=$RPM_BUILD_ROOT install build-shared

# Install the actual DLLs.
install libcrypto-%{soversion}.dll $RPM_BUILD_ROOT%{_mingw32_bindir}
install libssl-%{soversion}.dll $RPM_BUILD_ROOT%{_mingw32_bindir}

# Remove static libraries but DON'T remove *.dll.a files.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libcrypto.a
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libssl.a

# I have no idea why it installs the manpages in /etc, but
# we remove them anyway.
rm -r $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/pki/tls/man

# Set permissions on lib*.dll.a so that strip works.
chmod 0755 $RPM_BUILD_ROOT%{_mingw32_libdir}/libcrypto.dll.a
chmod 0755 $RPM_BUILD_ROOT%{_mingw32_libdir}/libssl.dll.a

# Install a makefile for generating keys and self-signed certs, and a script
# for generating them on the fly.
mkdir -p $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/pki/tls/certs
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/pki/tls/certs/Makefile
install -m755 %{SOURCE6} $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/pki/tls/certs/make-dummy-cert

# Pick a CA script.
pushd  $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/pki/tls/misc
mv CA.sh CA
popd

mkdir -m700 $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/pki/CA
mkdir -m700 $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/pki/CA/private

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc LICENSE
%{_mingw32_bindir}/openssl.exe
%{_mingw32_bindir}/c_rehash
%{_mingw32_bindir}/libcrypto-%{soversion}.dll
%{_mingw32_bindir}/libssl-%{soversion}.dll
#{_mingw32_bindir}/.libcrypto*.hmac
%{_mingw32_libdir}/libcrypto.dll.a
%{_mingw32_libdir}/libssl.dll.a
%{_mingw32_libdir}/engines
%{_mingw32_libdir}/pkgconfig/*.pc
%{_mingw32_includedir}/openssl
%config(noreplace) %{_mingw32_sysconfdir}/pki


%changelog
* Mon Feb  2 2009 Levente Farkas <lfarkas@lfarkas.org> - 0.9.8j-2
- Various build fixes.

* Wed Jan 28 2009 Levente Farkas <lfarkas@lfarkas.org> - 0.9.8j-1
- update to new upstream version.

* Mon Dec 29 2008 Levente Farkas <lfarkas@lfarkas.org> - 0.9.8g-2
- minor cleanup.

* Tue Sep 30 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.8g-1
- Initial RPM release.
