%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

# Define this to run tests (requires Wine, and won't work
# inside mock or Koji).
%define run_tests 0

Name:           mingw32-mpfr
Version:        2.3.2
Release:        2%{?dist}
Summary:        Windows port of multiple-precision floating-point computations

License:        LGPLv2+ and GPLv2+ and GFDL
Group:          Development/Libraries

URL:            http://www.mpfr.org/
Source0:        http://www.mpfr.org/mpfr-current/mpfr-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 40
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-gmp >= 4.2.1

# Native package requires these, but I can't see how they are used.
#BuildRequires:  autoconf
#BuildRequires:  libtool

Requires:       mingw32-gmp >= 4.2.1


%description
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and 
also has a well-defined semantics. It copies the good ideas from the 
ANSI/IEEE-754 standard for double-precision floating-point arithmetic 
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

This is the development package for Windows cross-compilation.


%prep
%setup -q -n mpfr-%{version}


%build
%{_mingw32_configure} \
  --disable-assert \
  --disable-static \
  --enable-shared
make %{?_smp_mflags}


%check
%if %run_tests
# Bloody Wine ...  'make check' doesn't work because Wine no longer
# looks on $PATH for libraries.  Instead we have to run the programs
# by hand from the .libs directory.
make %{?_smp_mflags} check
pushd .libs
for f in ../tests/.libs/*.exe; do
  srcdir=$(pwd)/../tests/ wine $f
done
popd
%endif


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# We don't want the documentation, since that is available
# in the native Fedora package.
rm -r $RPM_BUILD_ROOT%{_mingw32_infodir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB README
%{_mingw32_bindir}/libmpfr-1.dll
%{_mingw32_libdir}/libmpfr.dll.a
%{_mingw32_libdir}/libmpfr.la
%{_mingw32_includedir}/mpf2mpfr.h
%{_mingw32_includedir}/mpfr.h


%changelog
* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2.3.2-2
- Rebuild for mingw32-gcc 4.4

* Wed Jan 28 2009 Richard W.M. Jones <rjones@redhat.com> - 2.3.2-1
- Initial RPM release (on behalf of Ralf Corsepius).
