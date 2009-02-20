%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-gsl
Version:        1.11
Release:        4%{?dist}
Summary:        MinGW Windows port of the GNU Scientific Library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.gnu.org/software/gsl/
Source0:        ftp://ftp.gnu.org/gnu/gsl/gsl-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Patch0:         gsl-1.10-lib64.patch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  pkgconfig
BuildRequires:  dos2unix

Requires:       pkgconfig


%description
The GNU Scientific Library (GSL) is a collection of routines for
numerical analysis, written in C.


%prep
%setup -q -n gsl-%{version}
%patch0 -p1 -b .lib64
iconv -f windows-1252 -t utf-8 THANKS > THANKS.aux
touch -r THANKS THANKS.aux
mv THANKS.aux THANKS


%build
# Native package has:
#   configure ... CFLAGS="$CFLAGS -fgnu89-inline"
# but that destroys the original CFLAGS setting.
%{_mingw32_configure}
make %{?_smp_mflags}

# These ltshwrapper files contain DOS line endings for
# unknown reason.  Bash chokes on them, so we have to convert
# them back to normal line endings.
dos2unix .libs/*_ltshwrapper


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove static libraries but DON'T remove *.dll.a files.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libgslcblas.a
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libgsl.a

# Remove info files and man pages which duplicate native package.
rm -r $RPM_BUILD_ROOT%{_mingw32_mandir}
rm -r $RPM_BUILD_ROOT%{_mingw32_infodir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYING
%{_mingw32_bindir}/libgslcblas-0.dll
%{_mingw32_bindir}/libgsl-0.dll
%{_mingw32_bindir}/gsl-config
%{_mingw32_bindir}/gsl-histogram.exe
%{_mingw32_bindir}/gsl-randist.exe
%{_mingw32_libdir}/libgslcblas.dll.a
%{_mingw32_libdir}/libgsl.dll.a
%{_mingw32_libdir}/libgslcblas.la
%{_mingw32_libdir}/libgsl.la
%{_mingw32_libdir}/pkgconfig/gsl.pc
%{_mingw32_datadir}/aclocal/gsl.m4
%{_mingw32_includedir}/gsl


%changelog
* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.11-4
- Rebuild for mingw32-gcc 4.4

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.11-3
- Include license.

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.11-2
- Use _smp_mflags.

* Fri Oct 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.11-1
- Initial RPM release.
