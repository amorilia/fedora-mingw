%define gcc_major 4
%define gcc_minor 2
%define apple_build 5566

Name:           darwinx-gcc
Version:        %{gcc_major}.%{gcc_minor}
Release:        0.%{apple_build}.1%{?dist}
Summary:        Darwin (Mac OS X) GCC cross-compiler

License:        GPLv2+
Group:          Development/Libraries

URL:            http://www.opensource.apple.com/darwinsource/
Source0:        http://www.opensource.apple.com/darwinsource/tarballs/other/gcc_%{gcc_major}%{gcc_minor}-%{apple_build}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  darwinx-filesystem >= 1
BuildRequires:  darwinx-odcctools
BuildRequires:  darwinx-headers


%description
This is a GCC-based cross-compiler which creates Darwin (Mac OS X)
programs.  This is a port of Apple's GCC %{gcc_major}.%{gcc_minor} from Xcode
(build %{apple_build}).


%prep
%setup -q -n gcc_%{gcc_major}%{gcc_minor}-%{apple_build}


%build

languages="c,c++,objc,obj-c++"

for arch in powerpc i386; do
  mkdir build-${arch}
  pushd build-${arch}

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
    --target=${arch}-apple-darwin8 \
    --verbose \
    --without-newlib \
    --disable-multilib \
    --with-system-zlib \
    --disable-nls --without-included-gettext \
    --disable-win32-registry \
    --enable-languages="$languages" $optargs

#    --with-sysroot=%{_prefix}/$arch-apple-darwin8

  make %{?_smp_mflags}

  popd
done

exit 1


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove static libraries but DON'T remove *.dll.a files.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libfoo.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc LICENSE
%{_mingw32_bindir}/foo.dll
%{_mingw32_libdir}/foo.dll.a
# etc.


%changelog
* Fri Jan 23 2009 Your Name <you@example.com> - 1.2.3-1
- Initial RPM release.
