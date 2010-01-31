%define run_tests 1

Name:		example
Version:	1.0
Release:	1%{?dist}
Summary:	A library example.

Group:		Development/Libraries
License:	LGPLv2+
#URL:		
Source0:	example-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake

%description
A library example.

%prep
%setup -q


%build
%cmake .
make %{?_smp_mflags}

%check
%if %run_tests
LD_LIBRARY_PATH=. make %{?_smp_mflags} test
%endif

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
#%doc LICENSE
%{_libdir}/libexample.so
%{_includedir}/example.h


%changelog
* Sun Jan 31 2010 Amorilia <amorilia@users.sourceforge.net> - 1.0-1
- Initial RPM release.
