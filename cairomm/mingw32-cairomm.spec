%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-cairomm
Version:        1.6.2
Release:        1%{?dist}
Summary:        MinGW Windows C++ API for the cairo graphics library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.cairographics.org
Source0:        http://www.cairographics.org/releases/cairomm-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-cairo


%description
Cairomm is the C++ API for the cairo graphics library. It offers all the power
of cairo with an interface familiar to C++ developers, including use of the 
Standard Template Library where it makes sense.


%prep
%setup -q -n cairomm-%{version}


%build
%{_mingw32_configure} --enable-static=no --enable-docs=no
make


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libcairomm-1.0-1.dll
%{_mingw32_libdir}/libcairomm-1.0.dll.a
%{_mingw32_libdir}/libcairomm-1.0.la
%{_mingw32_libdir}/pkgconfig/cairomm-1.0.pc
%{_mingw32_includedir}/cairomm-1.0


%changelog
* Fri Oct 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.6.2-1
- Initial RPM release.
