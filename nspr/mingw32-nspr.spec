%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-nspr
Version:        4.7.2
Release:        6%{?dist}
Summary:        MinGW Windows port of the Netscape Portable Runtime (NSPR)

License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Development/Libraries
URL:            http://www.mozilla.org/projects/nspr/
Source0:        ftp://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v%{version}/src/nspr-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Source1:        nspr.pc.in
Source2:        nspr-config-vars.in

Patch1:         nspr-config-pc.patch

BuildRequires:  mingw32-filesystem >= 33
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

Requires:       pkgconfig


%description
NSPR provides platform independence for non-GUI operating system
facilities. These facilities include threads, thread synchronization,
normal file and network I/O, interval timing and calendar time, basic
memory management (malloc and free) and shared library linking.


%prep
%setup -q -n nspr-%{version}

cp ./mozilla/nsprpub/config/nspr-config.in \
   ./mozilla/nsprpub/config/nspr-config-pc.in
%patch1 -p0

cp %{SOURCE2} ./mozilla/nsprpub/config/


%build
pushd mozilla/nsprpub

# Configure for Windows cross-compiling.
%{_mingw32_configure} \
  --includedir=%{_mingw32_includedir}/nspr4 \
  --enable-optimize="%{_mingw32_cflags}" \
  --disable-debug \
  --enable-win32-target=WINNT \
  --enable-64bit=no

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
rm -rf $RPM_BUILD_ROOT

pushd mozilla/nsprpub

# 'make install' doesn't appear to work, so do it by hand.
mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_includedir}
install dist/bin/*.dll $RPM_BUILD_ROOT%{_mingw32_bindir}
install dist/lib/*.a $RPM_BUILD_ROOT%{_mingw32_libdir}
cp -rL dist/include/nspr $RPM_BUILD_ROOT%{_mingw32_includedir}/

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
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libnspr4.dll
%{_mingw32_bindir}/libplc4.dll
%{_mingw32_bindir}/libplds4.dll
%{_mingw32_libdir}/libnspr4.a
%{_mingw32_libdir}/libplc4.a
%{_mingw32_libdir}/libnspr4_s.a
%{_mingw32_libdir}/libplc4_s.a
%{_mingw32_libdir}/libplds4.a
%{_mingw32_libdir}/libplds4_s.a
%{_mingw32_libdir}/pkgconfig/nspr.pc
%{_mingw32_includedir}/nspr


%changelog
* Wed Feb 18 2009 Richard W.M. Jones <rjones@redhat.com> - 4.7.2-6
- Fix build inside mock.

* Tue Feb 17 2009 Richard W.M. Jones <rjones@redhat.com> - 4.7.2-4
- 'cp -L' to install header files, not symlinks to header files.

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 4.7.2-3
- Requires pkgconfig.

* Mon Nov 10 2008 Richard W.M. Jones <rjones@redhat.com> - 4.7.2-2
- Initial RPM release.
