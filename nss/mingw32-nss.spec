%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

# Version of NSPR that we depend on.
%define nspr_version 4.7

# Tests cause strange Wine failures ...
%define run_tests 0

Name:           mingw32-nss
Version:        3.12.2.0
Release:        6%{?dist}
Summary:        MinGW Windows port of NSS (Network Security Services)

License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

URL:            http://www.mozilla.org/projects/security/pki/nss/

# Extracted from the Fedora native package.  There is no upstream
# location for the tarballs.
Source0:        nss-%{version}-stripped.tar.bz2
Source1:        nss.pc.in
Source2:        nss-config.in
Source3:        blank-cert8.db
Source4:        blank-key3.db
Source5:        blank-secmod.db
Source8:        nss-prelink.conf
Source12:       nss-pem-20080124.tar.bz2

Source1000:     Cross.mk

Patch1:         nss-no-rpath.patch
Patch2:         nss-nolocalsql.patch
Patch5:         nss-pem-bug429175.patch
Patch6:         nss-enable-pem.patch

Patch1000:      nss-cross-compile.patch

BuildRequires:  mingw32-filesystem >= 33
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw32-nspr >= %{nspr_version}
BuildRequires:  mingw32-sqlite
BuildRequires:  mingw32-zlib

BuildRequires:  pkgconfig
BuildRequires:  perl

Requires:       pkgconfig


%description
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.


%prep
%setup -q -n nss-%{version}
%setup -q -T -D -n nss-%{version} -a 12

%patch1 -p0
%patch2 -p0
%patch5 -p0 -b .429175
%patch6 -p0 -b .libpem

%patch1000 -p0

# Notes on the naming:
# (1) "2.6" is the Linux version number which is appended to the name
#     also by NSS Makefiles.
# (2) OS_TARGET must be set to the basename (w/o 2.6).
cp %{SOURCE1000} mozilla/security/coreconf/FedoraCross2.6.mk

# This fixes a build failure in mock (not rpmbuild).
# This fix is not well-understood.
touch mozilla/security/nss/cmd/signtool/-lz
touch mozilla/security/nss/cmd/modutil/-lz


%build
# For cross-compilation, make sure pkg-config picks up the cross-compiled
# packages only.
PKG_CONFIG_LIBDIR="%{_mingw32_libdir}/pkgconfig"
export PKG_CONFIG_LIBDIR

NATIVE_CC=gcc
export NATIVE_CC
NATIVE_FLAGS="-DLINUX -Dlinux -D_POSIX_SOURCE -D_BSD_SOURCE -DHAVE_STRERROR"
export NATIVE_FLAGS

NS_USE_GCC=1
export NS_USE_GCC

OS_TARGET=FedoraCross
export OS_TARGET

# Enable compiler optimizations and disable debugging code
BUILD_OPT=1
export BUILD_OPT

# Generate symbolic info for debuggers
XCFLAGS="%{_mingw32_cflags}"
export XCFLAGS

export NSPR_INCLUDE_DIR=%{_mingw32_includedir}/nspr
export NSPR_LIB_DIR=%{_mingw32_bindir}

# Target is Win32 (32 bit):
#%ifarch x86_64 ppc64 ia64 s390x sparc64
#USE_64=1
#export USE_64
#%endif

# NSS_ENABLE_ECC=1
# export NSS_ENABLE_ECC

%{__make} -C ./mozilla/security/coreconf
%{__make} -C ./mozilla/security/dbm
%{__make} -C ./mozilla/security/nss

# enable the following line to force a test failure
# find ./mozilla -name \*.chk | xargs rm -f

%if %{run_tests}
# Run test suite.
# In order to support multiple concurrent executions of the test suite
# (caused by concurrent RPM builds) on a single host,
# we'll use a random port. Also, we want to clean up any stuck
# selfserv processes. If process name "selfserv" is used everywhere,
# we can't simply do a "killall selfserv", because it could disturb
# concurrent builds. Therefore we'll do a search and replace and use
# a different process name.
# Using xargs doesn't mix well with spaces in filenames, in order to
# avoid weird quoting we'll require that no spaces are being used.

SPACEISBAD=`find ./mozilla/security/nss/tests | grep -c ' '` ||:
if [ SPACEISBAD -ne 0 ]; then
  echo "error: filenames containing space are not supported (xargs)"
  exit 1
fi
MYRAND=`perl -e 'print 9000 + int rand 1000'`; echo $MYRAND ||:
RANDSERV=selfserv_${MYRAND}; echo $RANDSERV ||:
DISTBINDIR=`ls -d ./mozilla/dist/*.OBJ/bin`; echo $DISTBINDIR ||:
pushd `pwd`
cd $DISTBINDIR
ln -s selfserv $RANDSERV
popd
# man perlrun, man perlrequick
# replace word-occurrences of selfserv with selfserv_$MYRAND
find ./mozilla/security/nss/tests -type f |\
  grep -v "\.db$" |grep -v "\.crl$" | grep -v "\.crt$" |\
  grep -vw CVS  |xargs grep -lw selfserv |\
  xargs -l perl -pi -e "s/\bselfserv\b/$RANDSERV/g" ||:

killall $RANDSERV || :

rm -rf ./mozilla/tests_results
cd ./mozilla/security/nss/tests/
# all.sh is the test suite script
HOST=localhost DOMSUF=localdomain PORT=$MYRAND ./all.sh
cd ../../../../

killall $RANDSERV || :

TEST_FAILURES=`grep -c FAILED ./mozilla/tests_results/security/localhost.1/output.log` || :
if [ $TEST_FAILURES -ne 0 ]; then
  echo "error: test suite returned failure(s)"
  exit 1
fi
echo "test suite completed"
%endif


%install
rm -rf $RPM_BUILD_ROOT

# There is no make install target so we'll do it ourselves.

%{__mkdir_p} $RPM_BUILD_ROOT/%{_mingw32_includedir}/nss3
%{__mkdir_p} $RPM_BUILD_ROOT/%{_mingw32_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_mingw32_libdir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_mingw32_libdir}/nss/unsupported-tools

# Set up our package file
%{__mkdir_p} $RPM_BUILD_ROOT/%{_mingw32_libdir}/pkgconfig
%{__cat} %{SOURCE1} | sed -e "s,%%libdir%%,%{_mingw32_libdir},g" \
                          -e "s,%%prefix%%,%{_mingw32_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_mingw32_prefix},g" \
                          -e "s,%%includedir%%,%{_mingw32_includedir}/nss3,g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSS_VERSION%%,%{version},g" > \
                          $RPM_BUILD_ROOT/%{_mingw32_libdir}/pkgconfig/nss.pc
NSS_VMAJOR=`cat mozilla/security/nss/lib/nss/nss.h | grep "#define.*NSS_VMAJOR" | awk '{print $3}'`
NSS_VMINOR=`cat mozilla/security/nss/lib/nss/nss.h | grep "#define.*NSS_VMINOR" | awk '{print $3}'`
NSS_VPATCH=`cat mozilla/security/nss/lib/nss/nss.h | grep "#define.*NSS_VPATCH" | awk '{print $3}'`

export NSS_VMAJOR 
export NSS_VMINOR 
export NSS_VPATCH

%{__mkdir_p} $RPM_BUILD_ROOT/%{_mingw32_bindir}
%{__cat} %{SOURCE2} | sed -e "s,@libdir@,%{_mingw32_libdir},g" \
                          -e "s,@prefix@,%{_mingw32_prefix},g" \
                          -e "s,@exec_prefix@,%{_mingw32_prefix},g" \
                          -e "s,@includedir@,%{_mingw32_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$NSS_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$NSS_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$NSS_VPATCH,g" \
                          > $RPM_BUILD_ROOT/%{_mingw32_bindir}/nss-config

chmod 755 $RPM_BUILD_ROOT/%{_mingw32_bindir}/nss-config

# Copy the binary libraries we want
for file in libsoftokn3.dll libfreebl3.dll libnss3.dll libnssutil3.dll \
            libssl3.dll libsmime3.dll libnssckbi.dll libnsspem.dll libnssdbm3.dll
do
  %{__install} -m 755 mozilla/dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_mingw32_bindir}
done

# These ghost files will be generated in the post step
# Make sure chk files can be found in both places
#for file in libsoftokn3.chk libfreebl3.chk
#do
#  touch $RPM_BUILD_ROOT/%{_lib}/$file
#  ln -s ../../%{_lib}/$file $RPM_BUILD_ROOT/%{_mingw32_libdir}/$file
#done

# Install the empty NSS db files
%{__mkdir_p} $RPM_BUILD_ROOT/%{_mingw32_sysconfdir}/pki/nssdb
%{__install} -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_mingw32_sysconfdir}/pki/nssdb/cert8.db
%{__install} -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_mingw32_sysconfdir}/pki/nssdb/key3.db
%{__install} -m 644 %{SOURCE5} $RPM_BUILD_ROOT/%{_mingw32_sysconfdir}/pki/nssdb/secmod.db
%{__mkdir_p} $RPM_BUILD_ROOT/%{_mingw32_sysconfdir}/prelink.conf.d
%{__install} -m 644 %{SOURCE8} $RPM_BUILD_ROOT/%{_mingw32_sysconfdir}/prelink.conf.d/nss-prelink.conf

# Copy the development libraries we want
for file in libcrmf.a libnssb.a libnssckfw.a
do
  %{__install} -m 644 mozilla/dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_mingw32_libdir}
done

# Copy the binaries we want
for file in certutil cmsutil crlutil modutil pk12util signtool signver ssltap
do
  %{__install} -m 755 mozilla/dist/*.OBJ/bin/$file $RPM_BUILD_ROOT/%{_mingw32_bindir}
done

# Copy the binaries we ship as unsupported
for file in atob btoa derdump ocspclnt pp selfserv shlibsign strsclnt symkeyutil tstclnt vfyserv vfychain
do
  %{__install} -m 755 mozilla/dist/*.OBJ/bin/$file $RPM_BUILD_ROOT/%{_mingw32_libdir}/nss/unsupported-tools
done

# Copy the include files we want
for file in mozilla/dist/public/nss/*.h
do
  %{__install} -m 644 $file $RPM_BUILD_ROOT/%{_mingw32_includedir}/nss3
done


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/nss-config
%{_mingw32_bindir}/certutil
%{_mingw32_bindir}/cmsutil
%{_mingw32_bindir}/crlutil
%{_mingw32_bindir}/modutil
%{_mingw32_bindir}/pk12util
%{_mingw32_bindir}/signtool
%{_mingw32_bindir}/signver
%{_mingw32_bindir}/ssltap
%{_mingw32_bindir}/libsoftokn3.dll
%{_mingw32_bindir}/libfreebl3.dll
%{_mingw32_bindir}/libnss3.dll
%{_mingw32_bindir}/libnssutil3.dll
%{_mingw32_bindir}/libssl3.dll
%{_mingw32_bindir}/libsmime3.dll
%{_mingw32_bindir}/libnssckbi.dll
%{_mingw32_bindir}/libnsspem.dll
%{_mingw32_bindir}/libnssdbm3.dll
%{_mingw32_sysconfdir}/pki/nssdb/cert8.db
%{_mingw32_sysconfdir}/pki/nssdb/key3.db
%{_mingw32_sysconfdir}/pki/nssdb/secmod.db
%{_mingw32_sysconfdir}/prelink.conf.d/nss-prelink.conf
%{_mingw32_includedir}/nss3/
%{_mingw32_libdir}/libcrmf.a
%{_mingw32_libdir}/libnssb.a
%{_mingw32_libdir}/libnssckfw.a
%{_mingw32_libdir}/nss/unsupported-tools/atob
%{_mingw32_libdir}/nss/unsupported-tools/btoa
%{_mingw32_libdir}/nss/unsupported-tools/derdump
%{_mingw32_libdir}/nss/unsupported-tools/ocspclnt
%{_mingw32_libdir}/nss/unsupported-tools/pp
%{_mingw32_libdir}/nss/unsupported-tools/selfserv
%{_mingw32_libdir}/nss/unsupported-tools/shlibsign
%{_mingw32_libdir}/nss/unsupported-tools/strsclnt
%{_mingw32_libdir}/nss/unsupported-tools/symkeyutil
%{_mingw32_libdir}/nss/unsupported-tools/tstclnt
%{_mingw32_libdir}/nss/unsupported-tools/vfychain
%{_mingw32_libdir}/nss/unsupported-tools/vfyserv
%{_mingw32_libdir}/pkgconfig/nss.pc


%changelog
* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 3.12.2.0-6
- Rebuild for mingw32-gcc 4.4

* Wed Feb 18 2009 Richard W.M. Jones <rjones@redhat.com> - 3.12.2.0-5
- Fix to build in mock.

* Tue Feb 17 2009 Richard W.M. Jones <rjones@redhat.com> - 3.12.2.0-4
- Now builds.

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 3.12.2.0-3
- Include license file.

* Fri Jan 30 2009 Richard W.M. Jones <rjones@redhat.com> - 3.12.2.0-2
- Initial RPM release.
