%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-xerces-c
Version:        2.8.0
Release:        2%{?dist}
Summary:        Validating XML parser

License:        ASL 2.0
Group:          Development/Libraries

URL:            http://xml.apache.org/xerces-c/
Source0:        http://www.apache.org/dist/xerces/c/2/sources/xerces-c-src_2_8_0.tar.gz

# Patch allows dllwrap to be overridden.
Patch1000:      xerces-c-dllwrap.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils


%description
Xerces-C is a validating XML parser written in a portable subset of
C++. Xerces-C makes it easy to give your application the ability to
read and write XML data. A shared library is provided for parsing,
generating, manipulating, and validating XML documents. Xerces-C is
faithful to the XML 1.0 recommendation and associated standards (DOM
1.0, DOM 2.0. SAX 1.0, SAX 2.0, Namespaces).


%prep
%setup -q -n xerces-c-src_2_8_0

%patch1000 -p1

rm -rf doc/html/resources/.svn
find ./doc -type f -perm 755 -exec chmod 644 {} \;
find ./samples -type f -perm 755 -exec chmod 644 {} \;
%{__perl} -pi.orig -e 's|(PREFIX.)/lib\b|$1/%{_lib}|g' src/xercesc/configure */Makefile.in
rm doc/html/apiDocs/XMLRegisterCleanup_8hpp__incl.map
rm doc/html/apiDocs/XSConstants_8hpp__incl.map

# make rpmlint happy
sed -i 's/\r//' doc/charter.xml
iconv -f iso8859-1 -t utf-8 credits.txt > credits.utf8 && mv -f credits.{utf8,txt}
iconv -f iso8859-1 -t utf-8 doc/feedback.xml > doc/feedback.utf8 && mv -f doc/feedback.{utf8,xml}
iconv -f iso8859-1 -t utf-8 doc/migration.xml > doc/migration.utf8 && mv -f doc/migration.{utf8,xml}
iconv -f iso8859-1 -t utf-8 doc/releases_archive.xml > doc/releases_archive.utf8 && mv -f doc/releases_archive.{utf8,xml}


%build
export XERCESCROOT="$PWD"

# Let Makefiles be verbose
find -name 'Makefile.*' | while read f; do
        sed -i -e 's/$Q//g' \
        -e 's/{MAKE} -s/(MAKE)/g' \
        -e '/echo \"  (/d' \
        $f
done

# Remove conflicting flags from runConfigure
find -name runConfigure | while read f; do
        sed -i -e 's/-w -O -DNDEBUG/-DNDEBUG/g' $f
done

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

# not smp safe
%{__make} DLLWRAP=%{_mingw32_dllwrap}


%install
rm -rf $RPM_BUILD_ROOT

export XERCESCROOT="$PWD"
%{__make} install -C src/xercesc DESTDIR="$RPM_BUILD_ROOT"

# Move the DLLs into the bindir.
mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
mv $RPM_BUILD_ROOT%{_mingw32_libdir}/*.dll $RPM_BUILD_ROOT%{_mingw32_bindir}/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc LICENSE
%{_mingw32_includedir}/xercesc/
%{_mingw32_bindir}/libxerces-c.dll
%{_mingw32_bindir}/libxerces-c28.dll
%{_mingw32_bindir}/libxerces-c2_8_0.dll
%{_mingw32_bindir}/libxerces-depdom.dll
%{_mingw32_bindir}/libxerces-depdom28.dll
%{_mingw32_bindir}/libxerces-depdom2_8_0.dll


%changelog
* Wed Feb 18 2009 Richard W.M. Jones <rjones@redhat.com> - 2.8.0-2
- Initial RPM release.
