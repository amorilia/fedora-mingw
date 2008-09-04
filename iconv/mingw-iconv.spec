%include /usr/lib/rpm/mingw-defs

Name:      mingw-iconv
Version:   1.12
Release:   2%{?dist}
Summary:   GNU libraries and utilities for producing multi-lingual messages

License:   GPLv2+ and LGPLv2+
Group:     Development/Libraries
URL:       http://www.gnu.org/software/libiconv/
Source0:   http://ftp.gnu.org/pub/gnu/libiconv/libiconv-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: mingw-filesystem >= 19
BuildRequires: mingw-gcc
BuildRequires: mingw-binutils


%description
MinGW Windows Iconv library

%prep
%setup -q -n libiconv-%{version}

%build
%{_mingw_configure}
make

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_mingw_bindir}/iconv
%{_mingw_bindir}/libcharset-1.dll
%{_mingw_bindir}/libiconv-2.dll
%{_mingw_includedir}/iconv.h
%{_mingw_includedir}/libcharset.h
%{_mingw_includedir}/localcharset.h
%{_mingw_libdir}/charset.alias
%{_mingw_libdir}/libcharset.a
%{_mingw_libdir}/libcharset.dll.a
%{_mingw_libdir}/libcharset.la
%{_mingw_libdir}/libiconv.dll.a
%{_mingw_libdir}/libiconv.la
%{_mingw_docdir}/libiconv/
%{_mingw_mandir}/man1/iconv.1*
%{_mingw_mandir}/man3/iconv.3*
%{_mingw_mandir}/man3/iconv_close.3*
%{_mingw_mandir}/man3/iconv_open.3*
%{_mingw_mandir}/man3/iconvctl.3*


%changelog
* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-2
- Use RPM macros from mingw-filesystem.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 0.17-1
- Initial RPM release, largely based on earlier work from several sources.
