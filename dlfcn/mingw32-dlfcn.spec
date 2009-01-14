%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

%define realname dlfcn-win32

%define alphatag r11

Name:          mingw32-dlfcn
Version:       0
Release:       0.3.%{alphatag}%{?dist}
Summary:       Implements a wrapper for dlfcn (dlopen dlclose dlsym dlerror)

License:       LGPLv2+
Group:         Development/Libraries
URL:           http://code.google.com/p/dlfcn-win32/
Source0:       http://dlfcn-win32.googlecode.com/files/%{realname}-%{alphatag}.tar.bz2
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch

BuildRequires: mingw32-filesystem >= 40
BuildRequires: mingw32-gcc
BuildRequires: mingw32-binutils
#BuildRequires: dos2unix

Patch1:        dlfcn_configure.patch


%description
This library implements a wrapper for dlfcn, as specified in POSIX and SUS,
around the dynamic link library functions found in the Windows API.


%prep
%setup -q -n %{realname}-%{alphatag}

%{__sed} -i 's/\r//' configure
%{__sed} -i 's/\r//' README
%{__sed} -i 's/\r//' COPYING

%patch1 -p1


%build
%{_mingw32_configure} \
  --incdir=%{_mingw32_includedir} \
  --cc=i686-pc-mingw32-gcc \
  --enable-shared=yes \
  --enable-static=no \
  --enable-strip=i686-pc-mingw32-strip
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc README COPYING
%{_mingw32_bindir}/libdl.dll
%{_mingw32_libdir}/libdl.dll.a
%{_mingw32_includedir}/dlfcn.h


%changelog
* Wed Jan 14 2009 Richard W.M. Jones <rjones@redhat.com> - 0-0.3.r11
- Use Version 0
  (https://www.redhat.com/archives/fedora-packaging/2009-January/msg00064.html)
- Revert use of dos2unix for now
  (https://www.redhat.com/archives/fedora-packaging/2009-January/msg00066.html)
- Use _smp_mflags.

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.2.r11
- Import into fedora-mingw temporary repository because there are packages
  which will depend on this.
- Fix the version/release according to packaging guidelines.
- Tidy up the spec file.
- Use dos2unix and keep the timestamps.

* Fri Jan 02 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - r11-1
- Initial RPM release. 
