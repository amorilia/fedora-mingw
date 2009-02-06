%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-nss
Version:        3.12.2.0
Release:        3%{?dist}
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

BuildRequires:  mingw32-filesystem >= 33
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
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


%build
# Enable compiler optimizations and disable debugging code
BUILD_OPT=1
export BUILD_OPT

# Generate symbolic info for debuggers
XCFLAGS=$RPM_OPT_FLAGS
export XCFLAGS

export NSPR_INCLUDE_DIR=%{_mingw32_includedir}/nspr
export NSPR_LIB_DIR=%{_mingw32_libdir}

PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=1

export PKG_CONFIG_ALLOW_SYSTEM_LIBS
export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS

NSPR_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nspr | sed 's/-I//'`
NSPR_LIB_DIR=`/usr/bin/pkg-config --libs-only-L nspr | sed 's/-L//'`

export NSPR_INCLUDE_DIR
export NSPR_LIB_DIR

%ifarch x86_64 ppc64 ia64 s390x sparc64
USE_64=1
export USE_64
%endif

# NSS_ENABLE_ECC=1
# export NSS_ENABLE_ECC

%{__make} -C ./mozilla/security/coreconf
%{__make} -C ./mozilla/security/dbm
%{__make} -C ./mozilla/security/nss

# Set up our package file
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
%{__cat} %{SOURCE1} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSS_VERSION%%,%{version},g" > \
                          $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/nss.pc
NSS_VMAJOR=`cat mozilla/security/nss/lib/nss/nss.h | grep "#define.*NSS_VMAJOR" 
| awk '{print $3}'`
NSS_VMINOR=`cat mozilla/security/nss/lib/nss/nss.h | grep "#define.*NSS_VMINOR" 
| awk '{print $3}'`
NSS_VPATCH=`cat mozilla/security/nss/lib/nss/nss.h | grep "#define.*NSS_VPATCH" 
| awk '{print $3}'`

export NSS_VMAJOR 
export NSS_VMINOR 
export NSS_VPATCH

%{__mkdir_p} $RPM_BUILD_ROOT/%{_bindir}
%{__cat} %{SOURCE2} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$NSS_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$NSS_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$NSS_VPATCH,g" \
                          > $RPM_BUILD_ROOT/%{_bindir}/nss-config

chmod 755 $RPM_BUILD_ROOT/%{_bindir}/nss-config
# enable the following line to force a test failure
# find ./mozilla -name \*.chk | xargs rm -f

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

TEST_FAILURES=`grep -c FAILED ./mozilla/tests_results/security/localhost.1/outpu
t.log` || :
if [ $TEST_FAILURES -ne 0 ]; then
  echo "error: test suite returned failure(s)"
  exit 1
fi
echo "test suite completed"


%install
rm -rf $RPM_BUILD_ROOT

# There is no make install target so we'll do it ourselves.

%{__mkdir_p} $RPM_BUILD_ROOT/%{_includedir}/nss3
%{__mkdir_p} $RPM_BUILD_ROOT/%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_lib}
%{__mkdir_p} $RPM_BUILD_ROOT/%{unsupported_tools_directory}

# Copy the binary libraries we want
for file in libsoftokn3.so libfreebl3.so libnss3.so libnssutil3.so \
            libssl3.so libsmime3.so libnssckbi.so libnsspem.so libnssdbm3.so
do
  %{__install} -m 755 mozilla/dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_lib}
  ln -sf ../../%{_lib}/$file $RPM_BUILD_ROOT/%{_libdir}/$file
done

# These ghost files will be generated in the post step
# Make sure chk files can be found in both places
for file in libsoftokn3.chk libfreebl3.chk
do
  touch $RPM_BUILD_ROOT/%{_lib}/$file
  ln -s ../../%{_lib}/$file $RPM_BUILD_ROOT/%{_libdir}/$file
done

# Install the empty NSS db files
%{__mkdir_p} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb
%{__install} -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/cert8.db
%{__install} -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/key3.db
%{__install} -m 644 %{SOURCE5} $RPM_BUILD_ROOT/%{_sysconfdir}/pki/nssdb/secmod.d
b
%{__mkdir_p} $RPM_BUILD_ROOT/%{_sysconfdir}/prelink.conf.d
%{__install} -m 644 %{SOURCE8} $RPM_BUILD_ROOT/%{_sysconfdir}/prelink.conf.d/nss
-prelink.conf

# Copy the development libraries we want
for file in libcrmf.a libnssb.a libnssckfw.a
do
  %{__install} -m 644 mozilla/dist/*.OBJ/lib/$file $RPM_BUILD_ROOT/%{_libdir}
done

# Copy the binaries we want
for file in certutil cmsutil crlutil modutil pk12util signtool signver ssltap
do
  %{__install} -m 755 mozilla/dist/*.OBJ/bin/$file $RPM_BUILD_ROOT/%{_bindir}
done

# Copy the binaries we ship as unsupported
for file in atob btoa derdump ocspclnt pp selfserv shlibsign strsclnt symkeyutil
 tstclnt vfyserv vfychain
do
  %{__install} -m 755 mozilla/dist/*.OBJ/bin/$file $RPM_BUILD_ROOT/%{unsupported
_tools_directory}
done

# Copy the include files we want
for file in mozilla/dist/public/nss/*.h
do
  %{__install} -m 644 $file $RPM_BUILD_ROOT/%{_includedir}/nss3
done


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc XXX
%{_mingw32_bindir}/foo.dll
%{_mingw32_libdir}/foo.dll.a
# etc.


%changelog
* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 3.12.2.0-3
- Include license file.

* Fri Jan 30 2009 Richard W.M. Jones <rjones@redhat.com> - 3.12.2.0-2
- Initial RPM release.
