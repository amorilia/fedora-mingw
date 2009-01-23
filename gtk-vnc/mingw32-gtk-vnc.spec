%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

%define _default_patch_fuzz 2

Name:           mingw32-gtk-vnc
Version:        0.3.8
Release:        0.3.20081030hg%{?dist}
Summary:        MinGW Windows port of VNC client GTK widget

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://gtk-vnc.sf.net/
Source0:        gtk-vnc-0.3.8-20081030.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Patches submitted upstream 2008-10-28/29/30:
Patch100:       gtk-vnc-00-win32.patch
Patch101:       gtk-vnc-01-recv.patch
Patch102:       gtk-vnc-02-ioctl.patch
Patch103:       gtk-vnc-03-wsastartup.patch
#Patch104:       gtk-vnc-hgignore.patch
Patch105:       gtk-vnc-ldflags-confusion.patch
Patch106:       gtk-vnc-dan-fd-fix.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-gtk2
BuildRequires:  mingw32-gnutls
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig


%description
gtk-vnc is a VNC viewer widget for GTK. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.


%prep
%setup -q -n gtk-vnc-0.3.7

%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
#%patch104 -p1
%patch105 -p1
%patch106 -p1

autoreconf


%build
%{_mingw32_configure} --without-python --with-examples --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

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
* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.3.8-0.3.20081030hg
- Use _smp_mflags.
- Disable static library.

* Thu Oct 30 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.8-0.2.20081030hg
- Add Dan's fd/socket fix for Windows.

* Thu Oct 30 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.8-0.1.20081030hg
- Upgrade to current version in Mercurial (pre-release of 0.3.8).
- More MinGW patches.

* Fri Oct 10 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.7-3
- Missing BRs discovered by mock.
- Added description section.

* Thu Oct  9 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.7-2
- Initial RPM release.
