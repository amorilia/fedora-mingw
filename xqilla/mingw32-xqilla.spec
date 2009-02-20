%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-xqilla
Version:        2.2.0
Release:        2%{?dist}
Summary:        XQilla is an XQuery and XPath 2.0 library, built on top of Xerces-C

License:        ASL 2.0
Group:          Development/Libraries

URL:            http://xqilla.sourceforge.net/HomePage
Source0:        http://downloads.sourceforge.net/xqilla/XQilla-%{version}.tar.gz
Source1:        http://www.apache.org/dist/xerces/c/2/sources/xerces-c-src_2_8_0.tar.gz

# Patch from Xerces-C.
Patch1000:      xerces-c-dllwrap.patch

# Use ifdef WIN32 instead of MSVC-specific tests.
Patch1001:      xqilla-xmark-test-win32.patch

# XQC (the C API) does not work.  The library part compiles OK but for
# reasons unknown the symbols never get added to the libxqilla.dll.a
# implib.  The patch disables those sample programs.
Patch1002:      xqilla-no-xqc-tests.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils

BuildRequires:  mingw32-xerces-c >= 2.8.0
BuildRequires:  flex
BuildRequires:  autoconf, automake, libtool
BuildRequires:  doxygen, graphviz


%description
XQilla is an XQuery and XPath 2.0 implementation written in C++ and based
on Xerces-C. It implements the DOM 3 XPath API, as well as having it's own
more powerful API. It conforms to the W3C proposed recomendation of XQuery
and XPath 2.0.


%prep
%setup -q -a 1 -n XQilla-%{version}

pushd xerces-c-src_2_8_0
%patch1000 -p1
popd

%patch1001 -p1
%patch1002 -p1


%build
# XQilla requires a _built_ copy of Xerces-C.  Thus we have to build
# one first, copying much of the code from 'mingw32-xerces-c.spec'.
# Native Fedora package instead patches the configure script to look
# at the installed copy.
pushd xerces-c-src_2_8_0
export XERCESCROOT="$PWD"
cd $XERCESCROOT/src/xercesc
CXXFLAGS="%{_mingw32_cflags}" \
CFLAGS="%{_mingw32_cflags}" \
./runConfigure \
  -pmingw-msys \
  -c%{_mingw32_cc} \
  -x%{_mingw32_cxx} \
  -minmem \
  -nwinsock \
  -tWin32 \
  -b32 \
  -P %{_mingw32_prefix} \
  -C --libdir="%{_mingw32_libdir}" -C --host=%{_mingw32_host}
%{__make} DLLWRAP=%{_mingw32_dllwrap}
popd

rm -f aclocal.m4
aclocal
libtoolize --force --copy
automake --add-missing --copy --force
autoconf

MINGW32_CFLAGS="%{_mingw32_cflags} -DXQILLA_APIS" \
MINGW32_CXXFLAGS="%{_mingw32_cflags} -DXQILLA_APIS" \
%{_mingw32_configure} \
  --disable-static \
  --disable-rpath \
  --with-xerces=$(pwd)/xerces-c-src_2_8_0
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

export CPPROG="cp -p"
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f '{}' ';'
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
cp -pr ChangeLog LICENSE $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
cp -pr docs/dom3-api docs/simple-api \
        $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
for file in `find $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}`; do\
        if ! [ -s "$file" ]; then rm -f "$file"; fi;
done


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc LICENSE
%{_mingw32_bindir}/i686-pc-mingw32-xqilla.exe
%{_mingw32_bindir}/libxqilla-5.dll
%{_mingw32_libdir}/libxqilla.dll.a
%{_mingw32_includedir}/xqc.h
%{_mingw32_includedir}/xqilla/


%changelog
* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2.2.0-2
- Rebuild for mingw32-gcc 4.4

* Wed Feb 18 2009 Richard W.M. Jones <rjones@redhat.com> - 2.2.0-1
- Initial RPM release.
