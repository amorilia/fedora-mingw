%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-pixman
Version:        0.13.2
Release:        2%{?dist}
Summary:        MinGW Windows Pixman library

License:        MIT
URL:            http://xorg.freedesktop.org/
Group:          Development/Libraries

Source0:        http://xorg.freedesktop.org/archive/individual/lib/pixman-%{version}.tar.gz
Source1:        make-pixman-snapshot.sh

Patch0:         pixman-0.13.2-license.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-dlfcn

Requires:       pkgconfig

%description
MinGW Windows Pixman library.


%prep
%setup -q -n pixman-%{version}
%patch0 -p1


%build
# Uses GTK for its testsuite, so disable this otherwise
# we have a chicken & egg problem on mingw
%{_mingw32_configure} --disable-gtk --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc LICENSE
%{_mingw32_bindir}/libpixman-1-0.dll
%{_mingw32_includedir}/pixman-1
%{_mingw32_libdir}/libpixman-1.dll.a
%{_mingw32_libdir}/libpixman-1.la
%{_mingw32_libdir}/pkgconfig/pixman-1.pc


%changelog
* Thu Jan 15 2009 Richard W.M. Jones <rjones@redhat.com> - 0.13.2-2
- Include LICENSE file (freedesktop bug 19582).

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 0.13.2-1
- Resynch with Fedora package (0.13.2).
- Disable static library for speed.
- Use _smp_mflags.
- Requires pkgconfig.
- Depends on dlfcn.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 0.12.0-2
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 0.12.0-1
- Update to 0.12.0 release

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 0.11.10-2
- Remove static library.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 0.11.10-1
- Initial RPM release
