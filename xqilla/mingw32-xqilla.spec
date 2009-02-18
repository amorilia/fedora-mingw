%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-xqilla
Version:        2.1.3
Release:        1%{?dist}
Summary:        XQilla is an XQuery and XPath 2.0 library, built on top of Xerces-C

License:        ASL 2.0
Group:          Development/Libraries

URL:            http://xqilla.sourceforge.net/HomePage
Source0:        http://downloads.sourceforge.net/xqilla/XQilla-%{version}.tar.gz
Source1:        http://www.apache.org/dist/xerces/c/2/sources/xerces-c-src_2_8_0.tar.gz

Patch1:         xqilla-xercesc-libdir.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils

BuildRequires:  mingw32-xerces-c >= 2.8.0
BuildRequires:  autoconf, automake, libtool
BuildRequires:  doxygen, graphviz

%define xercesc_dir xerces-c-src_2_8_0
%define xercesc_build_root %{_builddir}/%{xercesc_dir}


%description
XQilla is an XQuery and XPath 2.0 implementation written in C++ and based
on Xerces-C. It implements the DOM 3 XPath API, as well as having it's own
more powerful API. It conforms to the W3C proposed recomendation of XQuery
and XPath 2.0.


%prep
%setup -q -b 1 -n XQilla-%{version}
%patch1


%build
rm -f aclocal.m4
aclocal
libtoolize --force --copy
automake --add-missing --copy --force
autoconf

%{_mingw32_configure} \
  --disable-static \
  --disable-rpath \
  --with-xerces=%{xercesc_build_root}
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
%{_mingw32_bindir}/foo.dll
%{_mingw32_libdir}/foo.dll.a


%changelog
* Wed Feb 18 2009 Richard W.M. Jones <rjones@redhat.com> - 2.1.3-1
- Initial RPM release.
