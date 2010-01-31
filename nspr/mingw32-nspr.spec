%global __strip %{_mingw32_strip}
%global __objdump %{_mingw32_objdump}
%global _use_internal_dependency_generator 0
%global __find_requires %{_mingw32_findrequires}
%global __find_provides %{_mingw32_findprovides}

Summary:        MinGW Windows port of the Netscape Portable Runtime (NSPR)
Name:           mingw32-nspr
Version:        4.8
Release:        2%{?dist}
License:        MPLv1.1 or GPLv2+ or LGPLv2+
URL:            http://www.mozilla.org/projects/nspr/
Group:          System Environment/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildArch:      noarch

# Sources available at ftp://ftp.mozilla.org/pub/mozilla.org/nspr/releases/
# When CVS tag based snapshots are being used, refer to CVS documentation on
# mozilla.org and check out subdirectory mozilla/nsprpub.
Source0:        nspr-%{version}.tar.bz2
Source1:        nspr.pc.in
Source2:        nspr-config-vars.in

Patch1:         nspr-config-pc.patch
Patch1000:      mingw32-nspr-4.7.2-build.patch
Patch1001:      mingw32-nspr-4.7.2-extra-build.patch
Patch1002:      nspr-configure-fedora-cross.patch

BuildRequires:  mingw32-filesystem >= 33
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
# XXX not sure if this is really required
BuildRequires:  mingw32-dlfcn

Requires:       pkgconfig

%description
NSPR provides platform independence for non-GUI operating system
facilities. These facilities include threads, thread synchronization,
normal file and network I/O, interval timing and calendar time, basic
memory management (malloc and free) and shared library linking.

# static package not created at the moment
#%package static
#Summary: Static version of the MinGW Windows NSPR library
#Requires: %{name} = %{version}-%{release}
#Group: Development/Libraries
#
#%description static
#Static version of the MinGW Windows NSPR library.

%prep
%setup -q -n nspr-%{version}

# Original nspr-config is not suitable for our distribution,
# because on different platforms it contains different dynamic content.
# Therefore we produce an adjusted copy of nspr-config that will be 
# identical on all platforms.
# However, we need to use original nspr-config to produce some variables
# that go into nspr.pc for pkg-config.

cp ./mozilla/nsprpub/config/nspr-config.in ./mozilla/nsprpub/config/nspr-config-pc.in
%patch1 -p0
pushd ./mozilla/nsprpub
%patch1000 -p0
%patch1001 -p0
%patch1002 -p4
popd

cp %{SOURCE2} ./mozilla/nsprpub/config/

%build
pushd mozilla/nsprpub

# Configure for Windows cross-compiling.
%{_mingw32_configure} \
  --includedir=%{_mingw32_includedir}/nspr4 \
  --enable-win32-target=WINNT \
  --enable-64bit=no \
  --enable-optimize="%{_mingw32_cflags}" \
  --disable-debug

# NSPR comes with its own "special" install program called nsinstall.
# This must be built as a native program.
make -C config CC=gcc CFLAGS="-DXP_UNIX=1"

# Now build the rest using the "special" nsinstall.
make \
  NSINSTALL=$(pwd)/config/nsinstall \
  RANLIB=i686-pc-mingw32-ranlib \
  RC=i686-pc-mingw32-windres \
  %{?_smp_mflags}

popd


%install

%{__rm} -Rf $RPM_BUILD_ROOT

pushd mozilla/nsprpub

# 'make install' doesn't appear to work, so do it by hand.
mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_includedir}
install dist/bin/*.dll $RPM_BUILD_ROOT%{_mingw32_bindir}
install dist/lib/*.a $RPM_BUILD_ROOT%{_mingw32_libdir}
cp -rL dist/include/nspr $RPM_BUILD_ROOT%{_mingw32_includedir}/nspr4
install -m 755 ./config/nspr-config $RPM_BUILD_ROOT%{_mingw32_bindir}

# Write an nspr pkgconfig file.

NSPR_LIBS=`./config/nspr-config --libs`
NSPR_CFLAGS=`./config/nspr-config --cflags`
NSPR_VERSION=`./config/nspr-config --version`
%{__mkdir_p} $RPM_BUILD_ROOT/%{_mingw32_libdir}/pkgconfig

cat ./config/nspr-config-vars > \
                     $RPM_BUILD_ROOT/%{_mingw32_libdir}/pkgconfig/nspr.pc

cat %{SOURCE1} | sed -e "s,%%libdir%%,%{_mingw32_libdir},g" \
                     -e "s,%%prefix%%,%{_mingw32_prefix},g" \
                     -e "s,%%exec_prefix%%,%{_mingw32_prefix},g" \
                     -e "s,%%includedir%%,%{_mingw32_includedir}/nspr4,g" \
                     -e "s,%%NSPR_VERSION%%,$NSPR_VERSION,g" \
                     -e "s,%%FULL_NSPR_LIBS%%,$NSPR_LIBS,g" \
                     -e "s,%%FULL_NSPR_CFLAGS%%,$NSPR_CFLAGS,g" >> \
                     $RPM_BUILD_ROOT/%{_mingw32_libdir}/pkgconfig/nspr.pc

popd


%clean
%{__rm} -Rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_mingw32_bindir}/libnspr4.dll
%{_mingw32_bindir}/libplc4.dll
%{_mingw32_bindir}/libplds4.dll
%{_mingw32_libdir}/libnspr4.dll.a
%{_mingw32_libdir}/libplc4.dll.a
%{_mingw32_libdir}/libplds4.dll.a
# not generated for some reason
#%{_mingw32_bindir}/libnspr4.la
#%{_mingw32_bindir}/libplc4.la
#%{_mingw32_bindir}/libplds4.la
%{_mingw32_includedir}/nspr4/
%{_mingw32_libdir}/pkgconfig/nspr.pc
%{_mingw32_bindir}/nspr-config

# static package not created at the moment
#%files static
#%defattr(-,root,root,-)
#%{_mingw32_libdir}/libnspr4.a
#%{_mingw32_libdir}/libplc4.a
#%{_mingw32_libdir}/libplds4.a
#%{_mingw32_libdir}/libnspr4_s.a
#%{_mingw32_libdir}/libplc4_s.a
#%{_mingw32_libdir}/libplds4_s.a

%changelog
* Sun Jan 31 2010 Amorilia <amorilia@users.sourceforge.net> - 4.8-2
- Another fix for build inside mock.

* Fri Oct 9 2009 Amorilia <amorilia@users.sourceforge.net> - 4.8-1
- Update to 4.8
- Fix for libplds4.dll.a import library

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 4.7.2-7
- Rebuild for mingw32-gcc 4.4

* Wed Feb 18 2009 Richard W.M. Jones <rjones@redhat.com> - 4.7.2-6
- Fix build inside mock.

* Tue Feb 17 2009 Richard W.M. Jones <rjones@redhat.com> - 4.7.2-4
- 'cp -L' to install header files, not symlinks to header files.

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 4.7.2-3
- Requires pkgconfig.

* Mon Nov 10 2008 Richard W.M. Jones <rjones@redhat.com> - 4.7.2-2
- Initial RPM release.
