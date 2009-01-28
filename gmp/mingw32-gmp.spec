%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

# Define this to run tests (requires Wine, and won't work
# inside mock or Koji).
%define run_tests 0

Name:           mingw32-gmp
Version:        4.2.4
Release:        1%{?dist}
Summary:        Windows port of GNU arbitrary precision library

License:        LGPLv3+
Group:          Development/Libraries

URL:            http://gmplib.org/
Source0:        ftp://ftp.gnu.org/pub/gnu/gmp/gmp-%{version}.tar.bz2

# Present in the Fedora native package, but shouldn't be needed for
# Windows since we are only building on a single architecture.
#Source2:        gmp.h
#Source3:        gmp-mparam.h

# S390 patch is not applicable for Windows.
#Patch0:         gmp-4.0.1-s390.patch

# Fix broken sscanf test (sent upstream 2009-01-28).
Patch1000:      mingw32-gmp-4.2.4-sscanf-test.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 44
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils

BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-readline

BuildRequires:  flex

%if %run_tests
BuildRequires:  wine
%endif


%description
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands. GNU MP is fast because it uses fullwords as the basic
arithmetic type, it uses fast algorithms, it carefully optimizes
assembly code for many CPUs' most common inner loops, and it generally
emphasizes speed over simplicity/elegance in its operations.

Install the gmp package if you need a fast arbitrary precision
library.

This is the development package for Windows cross-compilation.


%prep
%setup -q -n gmp-%{version}

%patch1000 -p1


%build
%{_mingw32_configure} \
  --enable-mpbsd \
  --enable-cxx \
  --disable-static \
  --enable-shared
make %{?_smp_mflags}


%check
%if %run_tests
make %{?_smp_mflags} check
%endif


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
install -m 644 gmp-mparam.h ${RPM_BUILD_ROOT}%{_mingw32_includedir}

rm -rf $RPM_BUILD_ROOT%{_mingw32_infodir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYING.LIB README
%{_mingw32_bindir}/libgmp-3.dll
%{_mingw32_bindir}/libgmpxx-4.dll
%{_mingw32_bindir}/libmp-3.dll
%{_mingw32_libdir}/libgmp.dll.a
%{_mingw32_libdir}/libgmp.la
%{_mingw32_libdir}/libgmpxx.dll.a
%{_mingw32_libdir}/libgmpxx.la
%{_mingw32_libdir}/libmp.dll.a
%{_mingw32_libdir}/libmp.la
%{_mingw32_includedir}/*.h


%changelog
* Wed Jan 28 2009 Richard W.M. Jones <rjones@redhat.com> - 4.2.4-1
- Initial RPM release (on behalf of Ralf Corsepius).
