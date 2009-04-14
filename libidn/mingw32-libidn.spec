%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

# Native Fedora package is ancient, 0.6.14, which doesn't even
# exist on the upstream servers any more.  I have gone for the
# latest version instead.

Name:           mingw32-libidn
Version:        1.9
Release:        5%{?dist}
Summary:        MinGW Windows Internationalized Domain Name support library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.gnu.org/software/libidn/
Source0:        http://josefsson.org/libidn/releases/libidn-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#Patch0:         libidn-0.6.14-aconf262.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 33
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-gettext
BuildRequires:  mingw32-iconv
BuildRequires:  pkgconfig, gettext
#BuildRequires:  libtool, automake, autoconf

Requires:       pkgconfig


%description
GNU Libidn is an implementation of the Stringprep, Punycode and
IDNA specifications defined by the IETF Internationalized Domain
Names (IDN) working group, used for internationalized domain
names.


%package static
Summary:        Static version of the MinGW Windows IDN library
Requires:       %{name} = %{version}-%{release}
Group:          Development/Libraries

%description static
Static version of the MinGW Windows IDN library.


%prep
%setup -q -n libidn-%{version}
#%patch0 -p1 -b .aconf262
#autoreconf


%build
%{_mingw32_configure} --disable-csharp --enable-static --enable-shared
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove documentation which duplicates native Fedora package.
rm -r $RPM_BUILD_ROOT%{_mingw32_datadir}/emacs
rm -r $RPM_BUILD_ROOT%{_mingw32_infodir}
rm -r $RPM_BUILD_ROOT%{_mingw32_mandir}/man*


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LIB
%{_mingw32_bindir}/idn.exe
%{_mingw32_bindir}/libidn-11.dll
%{_mingw32_libdir}/libidn.dll.a
%{_mingw32_libdir}/libidn.la
%{_mingw32_libdir}/pkgconfig/libidn.pc
%{_mingw32_includedir}/*.h
%{_mingw32_datadir}/locale/*/LC_MESSAGES/libidn.mo


%files static
%defattr(-,root,root,-)
%{_mingw32_libdir}/libidn.a

%changelog
* Fri Apr  3 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.9-5
- Added -static subpackage
- Fixed %%defattr line

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.9-4
- Rebuild for mingw32-gcc 4.4

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.14-3
- Include license file.

* Fri Jan 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.14-2
- Requires pkgconfig.

* Mon Nov 10 2008 Richard W.M. Jones <rjones@redhat.com> - 0.6.14-1
- Initial RPM release.
