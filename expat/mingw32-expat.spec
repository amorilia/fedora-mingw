%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-expat
Version:        2.0.1
Release:        1%{?dist}
Summary:        MinGW Windows port of expat XML parser library

License:        MIT
Group:          Development/Libraries
URL:            http://www.libexpat.org/
Source0:        http://download.sourceforge.net/expat/expat-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 33
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  autoconf, automake, libtool


%description
This is expat, the C library for parsing XML, written by James Clark. Expat
is a stream oriented XML parser. This means that you register handlers with
the parser prior to starting the parse. These handlers are called when the
parser discovers the associated structures in the document being parsed. A
start tag is an example of the kind of structures for which you may
register handlers.


%prep
%setup -q -n expat-%{version}

rm -rf autom4te*.cache
cp `aclocal --print-ac-dir`/libtool.m4 conftools || exit 1
libtoolize --copy --force --automake && aclocal && autoheader && autoconf


%build
%{_mingw32_configure}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove static libraries but DON'T remove *.dll.a files.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libexpat.a

# Remove documentation which duplicates that found in the native package.
rm -r $RPM_BUILD_ROOT%{_mingw32_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libexpat-1.dll
%{_mingw32_bindir}/xmlwf
%{_mingw32_libdir}/libexpat.dll.a
%{_mingw32_libdir}/libexpat.la
%{_mingw32_includedir}/expat.h
%{_mingw32_includedir}/expat_external.h


%changelog
* Fri Oct 31 2008 Richard W.M. Jones <rjones@redhat.com> - 2.0.1-1
- Initial RPM release.
