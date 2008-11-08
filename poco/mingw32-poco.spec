%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-poco
Version:        1.3.3p1
Release:        1%{?dist}
Summary:        MinGW Windows C++ libraries for network-centric applications

License:        Boost
Group:          Development/Libraries
URL:            http://pocoproject.org/
Source0:        http://prdownloads.sourceforge.net/poco/poco-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1001:      poco-01-buildsystem.patch
Patch1002:      poco-02-makefiles.patch
Patch1003:      poco-03-memcpy.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 33
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-openssl


%description
POCO, the C++ Portable Components, is a collection of open source C++
class libraries that simplify and accelerate the development of
network-centric, portable applications in C++. The libraries integrate
perfectly with the C++ Standard Library and fill many of the
functional gaps left open by it. Their modular and efficient design
and implementation makes the C++ Portable Components extremely well
suited for embedded development, an area where the C++ programming
language is becoming increasingly popular, due to its suitability for
both low-level (device I/O, interrupt handlers, etc.) and high-level
object-oriented development. Of course, POCO is also ready for
enterprise-level challenges.

The POCO libraries free developers from re-inventing the wheel, and
allow them to spend their time on more worthwhile areas, such as
getting things done quickly and working on the features that make
their application unique.


%prep
%setup -q -n poco-%{version}

cp build/config/MinGW build/config/MinGW-cross
%patch1001 -p0
%patch1002 -p0
%patch1003 -p0


%build
./configure --config=MinGW-cross --prefix=%{_mingw32_prefix}
make %{?_smp_flags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# *.dll files should be installed in %{_mingw32_bindir}.
mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
mv $RPM_BUILD_ROOT%{_mingw32_libdir}/*.dll $RPM_BUILD_ROOT%{_mingw32_bindir}/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
# XXX I think the '*d.dll' libraries are debug versions and
# possibly they should be moved to a subpackage?
%{_mingw32_bindir}/libPocoFoundationd.dll
%{_mingw32_bindir}/libPocoFoundation.dll
%{_mingw32_bindir}/libPocoNetd.dll
%{_mingw32_bindir}/libPocoNet.dll
%{_mingw32_bindir}/libPocoUtild.dll
%{_mingw32_bindir}/libPocoUtil.dll
%{_mingw32_bindir}/libPocoXMLd.dll
%{_mingw32_bindir}/libPocoXML.dll
%{_mingw32_libdir}/libPocoFoundationd.dll.a
%{_mingw32_libdir}/libPocoFoundation.dll.a
%{_mingw32_libdir}/libPocoNetd.dll.a
%{_mingw32_libdir}/libPocoNet.dll.a
%{_mingw32_libdir}/libPocoUtild.dll.a
%{_mingw32_libdir}/libPocoUtil.dll.a
%{_mingw32_libdir}/libPocoXMLd.dll.a
%{_mingw32_libdir}/libPocoXML.dll.a
%{_mingw32_includedir}/Poco


%changelog
* Sat Nov  8 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.3p1-1
- Initial RPM release.
