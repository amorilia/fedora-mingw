%define binutils_version 2.18.50
%define mingw_binutils_version 20080109-2
%define mingw_binutils_rpmvers %{expand:%(echo %{mingw_binutils_version} | tr - _)} 

Name:           mingw-binutils
Version:        %{binutils_version}_%{mingw_binutils_rpmvers}
Release:        5%{?dist}
Summary:        MinGW Windows binutils

License:        GPLv2+ and LGPLv2+ and GPLv3+ and LGPLv3+
Group:          Development/Libraries
URL:            http://www.mingw.org/
Source0:        http://dl.sourceforge.net/sourceforge/mingw/binutils-%{binutils_version}-%{mingw_binutils_version}-src.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  texinfo


%description
MinGW Windows binutils (utilities like 'strip', 'as', 'ld') which
understand Windows executables and DLLs.


%prep
%setup -q -n binutils-%{binutils_version}


%build
mkdir -p build
cd build
CFLAGS="$RPM_OPT_FLAGS" \
../configure \
  --build=%_build --host=%_host \
  --target=i686-pc-mingw32 \
  --verbose --disable-nls \
  --without-included-gettext \
  --disable-win32-registry \
  --disable-werror \
  --with-sysroot=%{_prefix}/i686-pc-mingw32/sys-root \
  --prefix=%{_prefix} --bindir=%{_bindir} \
  --includedir=%{_includedir} --libdir=%{_libdir} \
  --mandir=%{_mandir} --infodir=%{_infodir}

make all


%install
rm -rf $RPM_BUILD_ROOT

cd build
make DESTDIR=$RPM_BUILD_ROOT install

# These files conflict with ordinary binutils.
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libiberty*


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mandir}/man1/*
%{_bindir}/i686-pc-mingw32-*
%{_prefix}/i686-pc-mingw32/bin/*
%{_prefix}/i686-pc-mingw32/lib/ldscripts


%changelog
* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.50_20080109_2-5
- Initial RPM release, largely based on earlier work from several sources.
