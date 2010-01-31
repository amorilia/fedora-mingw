%global __strip %{_mingw32_strip}
%global __objdump %{_mingw32_objdump}
%global _use_internal_dependency_generator 0
%global __find_requires %{_mingw32_findrequires}
%global __find_provides %{_mingw32_findprovides}

# Define this to run tests (requires Wine, and won't work
# inside mock or Koji).
%define run_tests 1

Name:		mingw32-example
Version:	1.0
Release:	1%{?dist}
Summary:	A library example, cross compiled for mingw32.

Group:		Development/Libraries
License:	LGPLv2+
#URL:		
Source0:	example-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
# cmake wants mingw32-gcc-c++
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  cmake
%if %run_tests
BuildRequires:  wine
%endif

%description
A library example.

%prep
%setup -q -n example-1.0


%build
%{_mingw32_cmake}
make %{?_smp_mflags}

%check
%if %run_tests
make %{?_smp_mflags} test
%endif

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
#%doc LICENSE
%{_mingw32_bindir}/libexample.dll
%{_mingw32_libdir}/libexample.dll.a
%{_mingw32_includedir}/example.h


%changelog
* Sun Jan 31 2010 Amorilia <amorilia@users.sourceforge.net> - 1.0-1
- Initial RPM release.
