%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-libgsf
Version:        1.14.10
Release:        1%{?dist}
Summary:        MinGW Windows port of GNOME Structured File Library

License:        LGPLv2
Group:          Development/Libraries

URL:            http://www.gnome.org/projects/libgsf/
Source0:        ftp://ftp.gnome.org/pub/GNOME/sources/libgsf/1.14/libgsf-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-glib2
BuildRequires:  mingw32-libxml2
BuildRequires:  mingw32-bzip2 >= 1.0.5-4
BuildRequires:  mingw32-gettext
BuildRequires:  mingw32-iconv
BuildRequires:  mingw32-zlib
# We don't have bonobo in MinGW yet:
#BuildRequires:  mingw32-libbonobo
# We don't build Python packages yet:
#BuildRequires:  mingw32-pygtk2
# Seems like this is only needed for GNOME integration:
#BuildRequires:  mingw32-gnome-vfs2

BuildRequires:  autoconf, pkgconfig

Patch1000:      mingw32-libgsf-1.14.10-better-bz2-detection.patch
Patch1001:      mingw32-libgsf-1.14.10-glib-deprecated.patch


%description
A library for reading and writing structured files (eg MS OLE and Zip).

This is the MinGW Windows cross-compiled port of libgsf.


%prep
%setup -q -n libgsf-%{version}

%patch1000 -p1
%patch1001 -p1

autoconf


%build
%{_mingw32_configure} \
  --disable-gtk-doc --disable-static \
  --without-gnome-vfs --without-bonobo
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install

# Remove documentation which duplicates the Fedora native package.
rm -r $RPM_BUILD_ROOT%{_mingw32_datadir}/gtk-doc
rm -r $RPM_BUILD_ROOT%{_mingw32_mandir}/man1

# If native gconftool was installed then we will build the
# schemas.  However those are not useful under Windows because
# we don't have gconf itself.  Thus remove them if they were
# built.
rm -rf $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/gconf


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/gsf.exe
%{_mingw32_bindir}/gsf-office-thumbnailer.exe
%{_mingw32_bindir}/gsf-vba-dump.exe
%{_mingw32_bindir}/libgsf-1-114.dll
%{_mingw32_bindir}/libgsf-win32-1-114.dll
%{_mingw32_libdir}/libgsf-1.dll.a
%{_mingw32_libdir}/libgsf-1.la
%{_mingw32_libdir}/libgsf-win32-1.dll.a
%{_mingw32_libdir}/libgsf-win32-1.la
%{_mingw32_libdir}/pkgconfig/libgsf-1.pc
%{_mingw32_libdir}/pkgconfig/libgsf-win32-1.pc
%{_mingw32_includedir}/libgsf-1/
%{_mingw32_datadir}/locale/*/LC_MESSAGES/libgsf.mo


%changelog
* Sat Nov 22 2008 Richard W.M. Jones <rjones@redhat.com> - 1.14.10-1
- Initial RPM release.
