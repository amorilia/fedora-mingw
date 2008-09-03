%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           mingw-gcc
Version:        4.3.2
Release:        3%{?dist}
Summary:        MinGW Windows cross-compiler (GCC) for C and C++

License:        GPLv2+
Group:          Development/Libraries
URL:            http://www.mingw.org/
Source0:        ftp://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-core-%{version}.tar.bz2
Source1:        ftp://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-g++-%{version}.tar.bz2
Patch1:         %{name}-build.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  texinfo
BuildRequires:  mingw-binutils
BuildRequires:  mingw-runtime
BuildRequires:  mingw-w32api
BuildRequires:  gmp-devel
BuildRequires:  mpfr-devel
BuildRequires:  libgomp

Requires:       mingw-binutils
Requires:       mingw-runtime
Requires:       mingw-w32api


%description
MinGW Windows cross-compiler (GCC) for C and C++.


%prep
%setup -q -c
%setup -q -D -T -a1
%patch1 -p1

%build
cd gcc-%{version}

mkdir -p build
cd build

#languages="c,c++"
languages="c"
# XXX C++ disabled for now because of a strange GCC bug.

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
  --target=i686-pc-mingw32 \
  --with-gnu-as --with-gnu-ld --verbose \
  --without-newlib \
  --disable-multilib \
  --with-system-zlib \
  --disable-nls --without-included-gettext \
  --disable-win32-registry \
  --enable-version-specific-runtime-libs \
  --with-sysroot=%{_prefix}/i686-pc-mingw32/sys-root \
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


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_prefix}/i686-pc-mingw32/lib/libiberty.a
%{_libdir}/gcc/i686-pc-mingw32
%{_libexecdir}/gcc/i686-pc-mingw32
%{_bindir}/i686-pc-mingw32-*
%{_mandir}/man1/i686-pc-mingw32-*


%changelog
* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.1-3
- Initial RPM release, largely based on earlier work from several sources.
