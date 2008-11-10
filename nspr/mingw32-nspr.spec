%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-nspr
Version:        4.7.2
Release:        1%{?dist}
Summary:        MinGW Windows port of the Netscape Portable Runtime (NSPR)

License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Development/Libraries
URL:            http://www.mozilla.org/projects/nspr/
Source0:        ftp://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v%{version}/src/nspr-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

#Source1:        nspr.pc.in
#Source2:        nspr-config-vars.in

#Patch1:         nspr-config-pc.patch

Patch1000:      mingw32-nspr-4.7.2-build.patch

BuildRequires:  mingw32-filesystem >= 33
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils


%description
NSPR provides platform independence for non-GUI operating system
facilities. These facilities include threads, thread synchronization,
normal file and network I/O, interval timing and calendar time, basic
memory management (malloc and free) and shared library linking.


%prep
%setup -q -n nspr-%{version}

pushd mozilla/nsprpub
%patch1000 -p0
popd


%build
pushd mozilla/nsprpub

# Configure for Windows cross-compiling.
%{_mingw32_configure} \
  --prefix=%{_mingw32_prefix} \
  --libdir=%{_mingw32_libdir} \
  --includedir=%{_mingw32_includedir}/nspr4 \
  --enable-optimize="$RPM_OPT_FLAGS" \
  --disable-debug \
  --enable-win32-target=WINNT \
  --enable-64bit=no

# Something in the configure script is added -m64 option,
# so remove it.
# Also remove stack-protector checks.
pushd config
mv autoconf.mk autoconf.mk.orig
sed -e 's/-m64//' -e 's/-fstack-protector//' \
  < autoconf.mk.orig > autoconf.mk
popd

# NSPR comes with its own "special" install program called nsinstall.
# This must be built as a native program.
make -C config CC=gcc CFLAGS="-DXP_UNIX=1"

# Now build the rest using the "special" nsinstall.
make \
  NSINSTALL=`pwd`/config/nsinstall \
  RANLIB=i686-pc-mingw32-ranlib \
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
install dist/lib/*.dll.a $RPM_BUILD_ROOT%{_mingw32_libdir}
cp -r dist/include/nspr $RPM_BUILD_ROOT%{_mingw32_includedir}/

popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libnspr4.dll
%{_mingw32_bindir}/libplc4.dll
%{_mingw32_bindir}/libplds4.dll
%{_mingw32_libdir}/libnspr4.dll.a
%{_mingw32_libdir}/libplc4.dll.a
%{_mingw32_includedir}/nspr


%changelog
* Mon Nov 10 2008 Richard W.M. Jones <rjones@redhat.com> - 4.7.2-1
- Initial RPM release.
