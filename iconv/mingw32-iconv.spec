%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:      mingw32-iconv
Version:   1.12
Release:   7%{?dist}
Summary:   GNU libraries and utilities for character set conversion

License:   GPLv2+ and LGPLv2+
Group:     Development/Libraries
URL:       http://www.gnu.org/software/libiconv/
Source0:   http://ftp.gnu.org/pub/gnu/libiconv/libiconv-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: mingw32-filesystem >= 23
BuildRequires: mingw32-gcc
BuildRequires: mingw32-binutils

# There's a quasi-circular dependency between mingw32-iconv and
# mingw32-gettext.  If gettext is installed when you build this then
# iconv will create *.mo files.  When this package is added to Fedora
# we can consider adding this circular dep:
#BuildRequires: mingw32-gettext


%description
MinGW Windows Iconv library


%prep
%setup -q -n libiconv-%{version}


%build
%{_mingw32_configure}
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# Remove documentation which duplicates what is already in
# Fedora native packages.
rm -rf $RPM_BUILD_ROOT%{_mingw32_docdir}/libiconv/
rm -rf $RPM_BUILD_ROOT%{_mingw32_mandir}

# If mingw32-gettext was installed during the build, remove the *.mo
# files.  If mingw32-gettext wasn't installed then there won't be any.
rm -rf $RPM_BUILD_ROOT%{_mingw32_datadir}/locale


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB
%{_mingw32_bindir}/iconv
%{_mingw32_bindir}/libcharset-1.dll
%{_mingw32_bindir}/libiconv-2.dll
%{_mingw32_includedir}/iconv.h
%{_mingw32_includedir}/libcharset.h
%{_mingw32_includedir}/localcharset.h
%{_mingw32_libdir}/charset.alias
%{_mingw32_libdir}/libcharset.a
%{_mingw32_libdir}/libcharset.dll.a
%{_mingw32_libdir}/libcharset.la
%{_mingw32_libdir}/libiconv.dll.a
%{_mingw32_libdir}/libiconv.la


%changelog
* Fri Dec 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.12-7
- Include the license files in doc section.
- Fix the changelog entry numbering.

* Mon Nov  3 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-5
- Changed the summary (Bruno Haible).
- Note about mingw32-gettext / Remove *.mo files.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-4
- Rename mingw -> mingw32.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-3
- Remove documentation which duplicates what is in Fedora native packages.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-2
- Use RPM macros from mingw-filesystem.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 0.17-1
- Initial RPM release, largely based on earlier work from several sources.
