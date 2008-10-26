%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-libxslt
Version:        1.1.24
Release:        2%{?dist}
Summary:        MinGW Windows Library providing the Gnome XSLT engine

License:        MIT
Group:          Development/Libraries
URL:            http://xmlsoft.org/XSLT/
Source0:        ftp://xmlsoft.org/XSLT/libxslt-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Patch0:         multilib.patch
Patch1:         libexslt-rc4.patch

Patch1000:      mingw32-libxslt-1.1.24-win32-shared.patch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-libgcrypt
BuildRequires:  mingw32-libxml2 >= 2.7.2-3
BuildRequires:  pkgconfig
BuildRequires:  autoconf, automake, libtool

Requires:       mingw32-libxml2 >= 2.7.2-3
Requires:       pkgconfig


%description
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. To use it you need to have a version of libxml2 >= 2.6.27
installed. The xsltproc command is a command line interface to the XSLT engine


%prep
%setup -q -n libxslt-%{version}
%patch0 -p1
%patch1 -p0

%patch1000 -p1


%build
PATH=%{_mingw32_bindir}:$PATH \
%{_mingw32_configure} --without-python --enable-shared
make
gzip -9 ChangeLog


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove static libraries but DON'T remove *.dll.a files.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libexslt.a
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libxslt.a

# Remove doc and man which duplicate stuff already in Fedora native package.
rm -r $RPM_BUILD_ROOT%{_mingw32_docdir}
rm -r $RPM_BUILD_ROOT%{_mingw32_mandir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/xslt-config
%{_mingw32_bindir}/xsltproc.exe
%{_mingw32_includedir}/libexslt
%{_mingw32_includedir}/libxslt
#%{_mingw32_bindir}/libexslt.dll
#%{_mingw32_libdir}/libexslt.dll.a
%{_mingw32_libdir}/libexslt.la
%{_mingw32_bindir}/libxslt-1.dll
%{_mingw32_libdir}/libxslt.dll.a
%{_mingw32_libdir}/libxslt.la
%{_mingw32_libdir}/pkgconfig/libexslt.pc
%{_mingw32_libdir}/pkgconfig/libxslt.pc
%{_mingw32_libdir}/xsltConf.sh
%{_mingw32_datadir}/aclocal/libxslt.m4


%changelog
* Sat Oct 25 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.24-2
- Initial RPM release.
