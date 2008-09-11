%define __strip %{_mingw_strip}
%define __objdump %{_mingw_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw_findrequires}
%define __find_provides %{_mingw_findprovides}

Name:           mingw-example
Version:        1.2.3
Release:        1%{?dist}
Summary:        

License:        LGPLv2+
Group:          Development/Libraries
URL:            
Source0:        
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 23
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
# Any additional BuildRequires.


%description
# description


%prep
%setup -q


%build
%{_mingw_configure}
make


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove static libraries but DON'T remove *.dll.a files.
rm $RPM_BUILD_ROOT%{mingw_libdir}/libfoo.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/foo.dll
%{_mingw_libdir}/foo.dll.a
# etc.


%changelog
* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-1
- Initial RPM release.
