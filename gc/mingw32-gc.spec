%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-gc
Version:        7.1
Release:        1%{?dist}
Summary:        MinGW Windows port of GC garbage collector for C and C++

License:        BSD
Group:          Development/Libraries
URL:            http://www.hpl.hp.com/personal/Hans_Boehm/gc/
Source0:        http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

# To be more backward-compatible abi-wise, TODO: upstream ml reference
Patch1:         gc-7.1-gcinit.patch
Patch3:         gc-7.1-sparc.patch
## upstream patches
# http://www.hpl.hp.com/hosted/linux/mail-archives/gc/2008-May/002206.html
Patch100:       gc-7.1-dont_add_byte.patch

# MinGW-specific patches.
Patch1000:      mingw32-gc-7.1-set-win32-threads.patch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils

# XXX Native package uses a separate libatomic_ops library.
# We don't have this for MinGW yet, so gc will use its own
# copy of this library during the build.

BuildRequires:  automake, libtool

Requires:       pkgconfig


%description
The Boehm-Demers-Weiser conservative garbage collector can be 
used as a garbage collecting replacement for C malloc or C++ new.


%prep
%setup -q -n gc-%{version}

# FIXME? -- Rex
%if 0%{?rhel} < 6 && 0%{?fedora} < 10
%patch1 -p1 -b .gcinit
%endif
%patch3 -p1 -b .sparc

%patch100 -p1 -b .dont_add_byte

%patch1000 -p1 -b .set_win32_threads

# refresh auto*/libtool to purge rpaths
rm -f libtool libtool.m4
libtoolize --force
autoreconf -i


%build
%{_mingw32_configure} \
  --disable-dependency-tracking \
  --disable-static \
  --enable-cplusplus \
  --enable-large-config \
  --enable-parallel-mark \
  --enable-threads=win32
make


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# The docs duplicate what is already in the native gc-devel
# package, except for README.win32 which is not in that
# package but useful for Windows developers.
mkdir -p $RPM_BUILD_ROOT%{_mingw32_docdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT%{_mingw32_datadir}/gc/README.win* \
  $RPM_BUILD_ROOT%{_mingw32_docdir}/%{name}-%{version}/
rm -r $RPM_BUILD_ROOT%{_mingw32_datadir}/gc


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libcord-1.dll
%{_mingw32_bindir}/libgc-1.dll
%{_mingw32_bindir}/libgccpp-1.dll
%{_mingw32_libdir}/libcord.dll.a
%{_mingw32_libdir}/libgc.dll.a
%{_mingw32_libdir}/libgccpp.dll.a
%{_mingw32_libdir}/libcord.la
%{_mingw32_libdir}/libgc.la
%{_mingw32_libdir}/libgccpp.la
%{_mingw32_libdir}/pkgconfig/bdw-gc.pc
%{_mingw32_docdir}/%{name}-%{version}
%{_mingw32_includedir}/gc.h
%{_mingw32_includedir}/gc_cpp.h
%{_mingw32_includedir}/gc/


%changelog
* Fri Oct 24 2008 Richard W.M. Jones <rjones@redhat.com> - 7.1-1
- Initial RPM release.
