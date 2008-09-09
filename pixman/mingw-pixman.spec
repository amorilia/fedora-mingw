%include /usr/lib/rpm/mingw-defs

Name:           mingw-pixman
Version:        0.11.10
Release:        1%{?dist}
Summary:        MinGW Windows Pixman library

License:        MIT
URL:            http://xorg.freedesktop.org
Source0:        http://xorg.freedesktop.org/archive/individual/lib/pixman-%{version}.tar.gz
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 19
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils

%description
MinGW Windows Pixman library.


%prep
%setup -q -n pixman-%{version}

%build
# Uses GTK for its testsuite, so disable this otherwise
# we have a chicken & egg problem on mingw
%{_mingw_configure} --disable-gtk
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/libpixman-1-0.dll
%{_mingw_includedir}/pixman-1
%{_mingw_libdir}/libpixman-1.a
%{_mingw_libdir}/libpixman-1.dll.a
%{_mingw_libdir}/libpixman-1.la
%{_mingw_libdir}/pkgconfig/pixman-1.pc

%changelog
* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 2.18.0-1
- Initial RPM release
