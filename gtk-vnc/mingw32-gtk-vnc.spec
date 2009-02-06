%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

%define _default_patch_fuzz 2

Name:           mingw32-gtk-vnc
Version:        0.3.8
Release:        2%{?dist}
Summary:        MinGW Windows port of VNC client GTK widget

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://sourceforge.net/projects/gtk-vnc
Source0:        http://downloads.sourceforge.net/gtk-vnc/gtk-vnc-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 46
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw32-cairo
BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-gettext
BuildRequires:  mingw32-iconv
BuildRequires:  mingw32-gnutls
BuildRequires:  mingw32-gtk2
BuildRequires:  pkgconfig

Requires:       pkgconfig


%description
gtk-vnc is a VNC viewer widget for GTK. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.


%prep
%setup -q -n gtk-vnc-%{version}


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
%doc COPYING.LIB
%{_mingw32_bindir}/gvncviewer.exe
%{_mingw32_bindir}/libgtk-vnc-1.0-0.dll
%{_mingw32_libdir}/libgtk-vnc-1.0.dll.a
%{_mingw32_libdir}/libgtk-vnc-1.0.la
%{_mingw32_libdir}/pkgconfig/gtk-vnc-1.0.pc
%{_mingw32_includedir}/gtk-vnc-1.0


%changelog
* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 0.3.8-2
- Needs mingw32-filesystem with the pkg-config library path fix.
- Added optional BRs suggested by auto-buildrequires.
- Include the license file.

* Tue Feb  3 2009 Michel Salim <salimma@fedoraproject.org> - 0.3.8-1
- Update to 0.3.8

* Fri Jan 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.3.8-0.4.20081030hg
- Requires pkgconfig.

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.3.8-0.3.20081030hg
- Use _smp_mflags.
- Disable static library.
- Rebuild libtool.

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
