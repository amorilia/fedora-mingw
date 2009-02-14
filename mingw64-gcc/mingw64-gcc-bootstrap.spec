# This is the bootstrap GCC which is required for bootstrapping
# mingw64-runtime.

%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

%define upstream_version 4.4-20090206

Name:           mingw64-gcc-bootstrap
Version:        4.4.0
Release:        0.20090206.7%{?dist}
Summary:        MinGW Windows cross-compiler (GCC) for C

License:        GPLv2+
Group:          Development/Languages
URL:            http://www.mingw.org/
Source0:        ftp://ftp.mirrorservice.org/sites/sourceware.org/pub/gcc/snapshots/4.4-20090206/gcc-core-4.4-20090206.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  texinfo
BuildRequires:  mingw64-filesystem >= 6
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-headers
BuildRequires:  gmp-devel
%if 0%{?fedora} >= 9
BuildRequires:  mpfr-devel
%endif
BuildRequires:  libgomp
BuildRequires:  flex

# NB: Explicit mingw64-filesystem dependency is REQUIRED here.
Requires:       mingw64-filesystem >= 6
Requires:       mingw64-binutils
Requires:       mingw64-headers
Requires:       mingw64-cpp-bootstrap


%description
MinGW Windows cross-compiler (GCC) for C


%package -n mingw64-cpp-bootstrap
Summary: MinGW Windows cross-C Preprocessor.
Group: Development/Languages


%description -n mingw64-cpp-bootstrap
MinGW Windows cross-C Preprocessor


%prep
%setup -q -c


%build
cd gcc-%{upstream_version}

mkdir -p build
cd build

languages="c"

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
  --target=%{_mingw64_target} \
  --with-gnu-as --with-gnu-ld --verbose \
  --without-newlib \
  --disable-multilib \
  --with-system-zlib \
  --disable-nls --without-included-gettext \
  --disable-win32-registry \
  --enable-version-specific-runtime-libs \
  --with-sysroot=%{_mingw64_sysroot} \
  --enable-languages="$languages" $optargs

make %{?_smp_mflags} all-gcc


%install
rm -rf $RPM_BUILD_ROOT

cd gcc-%{upstream_version}
cd build
make DESTDIR=$RPM_BUILD_ROOT install-gcc

# These files conflict with existing installed files.
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -f $RPM_BUILD_ROOT%{_mandir}/man7/*

mkdir -p $RPM_BUILD_ROOT/lib
ln -sf ..%{_prefix}/bin/x86_64-pc-mingw32-cpp \
  $RPM_BUILD_ROOT/lib/x86_64-pc-mingw32-cpp

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_bindir}/x86_64-pc-mingw32-gcc
%{_bindir}/x86_64-pc-mingw32-gcc-%{version}
%{_bindir}/x86_64-pc-mingw32-gccbug
%{_bindir}/x86_64-pc-mingw32-gcov
%dir %{_libdir}/gcc/x86_64-pc-mingw32
%dir %{_libdir}/gcc/x86_64-pc-mingw32/%{version}
%dir %{_libdir}/gcc/x86_64-pc-mingw32/%{version}/include
%dir %{_libdir}/gcc/x86_64-pc-mingw32/%{version}/include-fixed
%{_libdir}/gcc/x86_64-pc-mingw32/%{version}/include-fixed/README
%{_libdir}/gcc/x86_64-pc-mingw32/%{version}/include-fixed/*.h
%{_libdir}/gcc/x86_64-pc-mingw32/%{version}/include/*.h
%dir %{_libdir}/gcc/x86_64-pc-mingw32/%{version}/install-tools
%{_libdir}/gcc/x86_64-pc-mingw32/%{version}/install-tools/*
%dir %{_libexecdir}/gcc/x86_64-pc-mingw32/%{version}/install-tools
%{_libexecdir}/gcc/x86_64-pc-mingw32/%{version}/install-tools/*
%{_mandir}/man1/x86_64-pc-mingw32-gcc.1*
%{_mandir}/man1/x86_64-pc-mingw32-gcov.1*


%files -n mingw64-cpp-bootstrap
%defattr(-,root,root)
/lib/x86_64-pc-mingw32-cpp
%{_bindir}/x86_64-pc-mingw32-cpp
%{_mandir}/man1/x86_64-pc-mingw32-cpp.1*
%dir %{_libdir}/gcc/x86_64-pc-mingw32
%dir %{_libdir}/gcc/x86_64-pc-mingw32/%{version}
%{_libexecdir}/gcc/x86_64-pc-mingw32/%{version}/cc1
%{_libexecdir}/gcc/x86_64-pc-mingw32/%{version}/collect2


%changelog
* Wed Feb 11 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-0.20090206.7
- Started mingw64 development.

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-12
- Rebuild against latest filesystem package.

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
