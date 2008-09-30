%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-openssl
Version:        0.9.8g
Release:        1%{?dist}
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
Patch0:         openssl-0.9.8g-redhat.patch
Patch1:         openssl-0.9.8a-defaults.patch
Patch2:         openssl-0.9.8a-link-krb5.patch
Patch3:         openssl-0.9.8g-soversion.patch
Patch4:         openssl-0.9.8a-enginesdir.patch
Patch5:         openssl-0.9.8a-no-rpath.patch
Patch6:         openssl-0.9.8b-test-use-localhost.patch
Patch7:         openssl-0.9.8g-shlib-version.patch
Patch21:        openssl-0.9.8b-aliasing-bug.patch
Patch22:        openssl-0.9.8b-x509-name-cmp.patch
Patch23:        openssl-0.9.8g-default-paths.patch
Patch24:        openssl-0.9.8g-no-extssl.patch
Patch32:        openssl-0.9.8g-ia64.patch
Patch33:        openssl-0.9.7f-ca-dir.patch
Patch34:        openssl-0.9.6-x509.patch
Patch35:        openssl-0.9.7-beta5-version-add-engines.patch
Patch38:        openssl-0.9.8a-reuse-cipher-change.patch
# Disabled this because it uses getaddrinfo which is lacking on Windows.
#Patch39:        openssl-0.9.8g-ipv6-apps.patch
Patch50:        openssl-0.9.8g-speed-bug.patch
Patch51:        openssl-0.9.8g-bn-mul-bug.patch
Patch52:        openssl-0.9.8g-cve-2008-0891.patch
Patch53:        openssl-0.9.8g-cve-2008-1671.patch

# MinGW-specific patches.
Patch100:       mingw32-openssl-0.9.8g-header-files.patch
Patch101:       mingw32-openssl-0.9.8g-configure.patch
Patch102:       mingw32-openssl-0.9.8g-shared.patch
Patch103:       mingw32-openssl-0.9.8g-global.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 26
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw32-zlib

BuildRequires:  mktemp
#BuildRequires:  krb5-devel
BuildRequires:  perl
BuildRequires:  sed
BuildRequires:  /usr/bin/cmp
BuildRequires:  /usr/bin/rename

# Required to run the tests.
BuildRequires:  wine
BuildRequires:  xorg-x11-server-Xvfb

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
%patch50 -p1 -b .speed-bug
%patch51 -p1 -b .bn-mul-bug
%patch52 -p0 -b .srvname-crash
%patch53 -p0 -b .srv-kex-crash

%patch100 -p1 -b .mingw-header-files
%patch101 -p1 -b .mingw-configure
%patch102 -p1 -b .mingw-shared
%patch103 -p1 -b .mingw-global

# Modify the various perl scripts to reference perl in the right location.
perl util/perlpath.pl `dirname %{__perl}`

# Generate a table with the compile settings for my perusal.
touch Makefile
make TABLE PERL=%{__perl}


%build

cat > gcc <<EOS
#!/bin/sh -
%{_bindir}/i686-pc-mingw32-gcc -m32 "$@"
EOS
export PATH=.:$PATH

# NB: 'no-hw' is vital.  MinGW cannot build the hardware drivers
# and if you don't have this you'll get an obscure link error.
./Configure \
  --openssldir=%{_mingw32_sysconfdir}/pki/tls \
  zlib enable-camellia enable-seed enable-tlsext enable-rfc3779 \
  no-idea no-mdc2 no-rc5 no-ec no-ecdh no-ecdsa no-hw shared \
  --enginesdir=%{_mingw32_libdir}/openssl/engines \
  mingw
#  --with-krb5-flavor=MIT
#  -I%{_mingw32_prefix}/kerberos/include -L%{_mingw32_prefix}/kerberos/%{_lib}
make depend
make all build-shared
make rehash build-shared

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
unset DISPLAY
display=:21
Xvfb $display -ac -noreset & xpid=$!
trap "kill -TERM $xpid ||:" EXIT
sleep 3
DISPLAY=$display
export DISPLAY

make LDCMD=%{_mingw32_cc} -C test apps tests

# Disable this thread test, because we don't have pthread on Windows.
#%-{_mingw32_cc} -o openssl-thread-test \
#  -I./include \
#  %-{_mingw32_cflags} \
#  %-{SOURCE8} \
#  -L. \
#  -lssl -lcrypto \
#  -lpthread -lz -ldl
#
## `krb5-config --cflags`
## `krb5-config --libs`
#
#./openssl-thread-test --threads %{thread_test_threads}

# Patch33 must be patched after tests otherwise they will fail
patch -p1 -b -z .ca-dir < %{PATCH33}

if ! iconv -f UTF-8 -t ASCII//TRANSLIT CHANGES >/dev/null 2>&1 ; then
  iconv -f ISO-8859-1 -t UTF-8 -o CHANGES.utf8 CHANGES && \
    mv -f CHANGES.utf8 CHANGES
fi


%install
rm -rf $RPM_BUILD_ROOT
exit 1
make DESTDIR=$RPM_BUILD_ROOT install

# Remove static libraries but DON'T remove *.dll.a files.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libfoo.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/foo.dll
%{_mingw32_libdir}/foo.dll.a
# etc.


%changelog
* Wed Sep 24 2008 Your Name <you@example.com> - 1.2.3-1
- Initial RPM release.
