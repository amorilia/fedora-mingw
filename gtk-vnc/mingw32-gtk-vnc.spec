%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-gtk-vnc
Version:        0.3.7
Release:        2%{?dist}
Summary:        MinGW Windows port of VNC client GTK widget

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://gtk-vnc.sf.net/
Source0:        http://downloads.sourceforge.net/gtk-vnc/gtk-vnc-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1:         gtk-vnc-0.3.7-abs-ungrab.patch

# Dan's MinGW patch version 2, fixed so it can apply to the tarball.
Patch100:       gtk-vnc-0.3.7-mingw32-dan3.patch

# Extra files required by Gnulib.
Patch101:       gtk-vnc-0.3.7-mingw32-gnulib-files.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
# XXX


%description
# description


%prep
%setup -q -n gtk-vnc-%{version}

%patch1 -p1

%patch100 -p1
%patch101 -p1

autoreconf


%build
%{_mingw32_configure} --without-python --with-examples
make


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove static libraries but DON'T remove *.dll.a files.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libgtk-vnc-1.0.a

# automake gives gvncviewer a strange name ...
mv $RPM_BUILD_ROOT%{_mingw32_bindir}/i686-pc-mingw32-gvncviewer.exe \
   $RPM_BUILD_ROOT%{_mingw32_bindir}/gvncviewer.exe \


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/gvncviewer.exe
%{_mingw32_bindir}/libgtk-vnc-1.0-0.dll
%{_mingw32_libdir}/libgtk-vnc-1.0.dll.a
%{_mingw32_libdir}/libgtk-vnc-1.0.la
%{_mingw32_libdir}/pkgconfig/gtk-vnc-1.0.pc
%{_mingw32_includedir}/gtk-vnc-1.0


%changelog
* Thu Oct  9 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.7-2
- Initial RPM release.
