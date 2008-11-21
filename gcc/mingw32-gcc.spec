%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           mingw32-gcc
Version:        4.3.2
Release:        11%{?dist}
Summary:        MinGW Windows cross-compiler (GCC) for C

License:        GPLv2+
Group:          Development/Languages
URL:            http://www.mingw.org/
Source0:        ftp://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-core-%{version}.tar.bz2
Source1:        ftp://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-g++-%{version}.tar.bz2
Patch1:         %{name}-build.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  texinfo
BuildRequires:  mingw32-filesystem >= 26
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-runtime
BuildRequires:  mingw32-w32api
BuildRequires:  gmp-devel
%if 0%{?fedora} >= 9
BuildRequires:  mpfr-devel
%endif
BuildRequires:  libgomp

Requires:       mingw32-filesystem >= 26
Requires:       mingw32-binutils
Requires:       mingw32-runtime
Requires:       mingw32-w32api
Requires:       mingw32-cpp


%description
MinGW Windows cross-compiler (GCC) for C


%package -n mingw32-cpp
Summary: MinGW Windows cross-C Preprocessor.
Group: Development/Languages

%description -n mingw32-cpp
MinGW Windows cross-C Preprocessor


%package c++
Summary: MinGW Windows cross-compiler for C++
Group: Development/Languages

%description c++
MinGW Windows cross-compiler for C++


%prep
%setup -q -c
%setup -q -D -T -a1
%patch1 -p1

%build
cd gcc-%{version}

mkdir -p build
cd build

languages="c,c++"

CC="%{__cc} ${RPM_OPT_FLAGS}" \
../configure \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --infodir=%{_infodir} \
  --datadir=%{_datadir} \
  --build=%_build --host=%_host \
  --target=%{_mingw32_target} \
  --with-gnu-as --with-gnu-ld --verbose \
  --without-newlib \
  --disable-multilib \
  --with-system-zlib \
  --disable-nls --without-included-gettext \
  --disable-win32-registry \
  --enable-version-specific-runtime-libs \
  --with-sysroot=%{_mingw32_sysroot} \
  --enable-languages="$languages" $optargs

make all


%install
rm -rf $RPM_BUILD_ROOT

cd gcc-%{version}
cd build
make DESTDIR=$RPM_BUILD_ROOT install

# These files conflict with existing installed files.
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty*
rm -f $RPM_BUILD_ROOT%{_mandir}/man7/*

mkdir -p $RPM_BUILD_ROOT/lib
ln -sf ..%{_prefix}/bin/i686-pc-mingw32-cpp \
  $RPM_BUILD_ROOT/lib/i686-pc-mingw32-cpp

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_bindir}/i686-pc-mingw32-gcc
%{_bindir}/i686-pc-mingw32-gcc-%{version}
%{_bindir}/i686-pc-mingw32-gccbug
%{_bindir}/i686-pc-mingw32-gcov
%{_prefix}/i686-pc-mingw32/lib/libiberty.a
%dir %{_libdir}/gcc/i686-pc-mingw32
%dir %{_libdir}/gcc/i686-pc-mingw32/%{version}
%{_libdir}/gcc/i686-pc-mingw32/%{version}/crtbegin.o
%{_libdir}/gcc/i686-pc-mingw32/%{version}/crtend.o
%{_libdir}/gcc/i686-pc-mingw32/%{version}/crtfastmath.o
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libgcc.a
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libgcov.a
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libssp.a
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libssp.la
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libssp_nonshared.a
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libssp_nonshared.la
%dir %{_libdir}/gcc/i686-pc-mingw32/%{version}/include
%dir %{_libdir}/gcc/i686-pc-mingw32/%{version}/include-fixed
%dir %{_libdir}/gcc/i686-pc-mingw32/%{version}/include/ssp
%{_libdir}/gcc/i686-pc-mingw32/%{version}/include-fixed/README
%{_libdir}/gcc/i686-pc-mingw32/%{version}/include-fixed/*.h
%{_libdir}/gcc/i686-pc-mingw32/%{version}/include/*.h
%{_libdir}/gcc/i686-pc-mingw32/%{version}/include/ssp/*.h
%dir %{_libdir}/gcc/i686-pc-mingw32/%{version}/install-tools
%{_libdir}/gcc/i686-pc-mingw32/%{version}/install-tools/*
%dir %{_libexecdir}/gcc/i686-pc-mingw32/%{version}/install-tools
%{_libexecdir}/gcc/i686-pc-mingw32/%{version}/install-tools/*
%{_mandir}/man1/i686-pc-mingw32-gcc.1*
%{_mandir}/man1/i686-pc-mingw32-gcov.1*


%files -n mingw32-cpp
%defattr(-,root,root)
/lib/i686-pc-mingw32-cpp
%{_bindir}/i686-pc-mingw32-cpp
%{_mandir}/man1/i686-pc-mingw32-cpp.1*
%dir %{_libdir}/gcc/i686-pc-mingw32
%dir %{_libdir}/gcc/i686-pc-mingw32/%{version}
%{_libexecdir}/gcc/i686-pc-mingw32/%{version}/cc1


%files c++
%defattr(-,root,root)
%{_bindir}/i686-pc-mingw32-g++
%{_bindir}/i686-pc-mingw32-c++
%{_mandir}/man1/i686-pc-mingw32-g++.1*
%{_libdir}/gcc/i686-pc-mingw32/%{version}/include/c++/
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libstdc++.a
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libstdc++.la
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libsupc++.a
%{_libdir}/gcc/i686-pc-mingw32/%{version}/libsupc++.la
%{_libexecdir}/gcc/i686-pc-mingw32/%{version}/cc1plus
%{_libexecdir}/gcc/i686-pc-mingw32/%{version}/collect2


%changelog
* Fri Nov 21 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-11
- Remove obsoletes for a long dead package.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-10
- Rebuild against mingw32-filesystem 37

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-9
- Rebuild against mingw32-filesystem 36

* Thu Oct 30 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-8
- Don't BR mpfr-devel for RHEL/EPEL-5 (Levente Farkas).

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-7
- Rename mingw -> mingw32.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-6
- Use RPM macros from mingw-filesystem.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-3
- Initial RPM release, largely based on earlier work from several sources.
