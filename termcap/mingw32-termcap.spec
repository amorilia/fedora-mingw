# Note: Termcap was deprecated and removed from Fedora after F-8.  It
# has been replaced by ncurses.  However ncurses cannot be compiled on
# Windows so we have to supply termcap.  In addition, the last stand-
# alone Fedora termcap package was actually just /etc/termcap from
# ncurses.  So here we are using the GNU termcap library which is
# regretably GPL'd.

%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-termcap
Version:        1.3.1
Release:        1%{?dist}
Summary:        MinGW terminal feature database

License:        GPLv2+
Group:          Development/Libraries
URL:            ftp://ftp.gnu.org/gnu/termcap/
Source0:        ftp://ftp.gnu.org/gnu/termcap/termcap-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 28
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils


%description
This is the GNU termcap library -- a library of C functions that
enable programs to send control strings to terminals in a way
independent of the terminal type.  The GNU termcap library does not
place an arbitrary limit on the size of termcap entries, unlike most
other termcap libraries.

This package contains libraries and development tools for the MinGW
cross-compiled version.


%prep
%setup -q -n termcap-%{version}


%build
%{_mingw32_configure}
make

# Build a shared library.  No need for -fPIC on Windows.
%{_mingw32_cc} -shared -Wl,--out-implib,termcap.dll.a -o termcap.dll \
  termcap.o tparam.o version.o


%install
rm -rf $RPM_BUILD_ROOT

make install \
  prefix=$RPM_BUILD_ROOT%{_mingw32_prefix} \
  oldincludedir=

# Move the shared library to the correct locations.
mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
mv termcap.dll $RPM_BUILD_ROOT%{_mingw32_bindir}
mv termcap.dll.a $RPM_BUILD_ROOT%{_mingw32_libdir}

# Don't want the static library, thank you.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libtermcap.a

# Move the info files to the correct location.
mkdir -p $RPM_BUILD_ROOT%{_mingw32_infodir}
mv $RPM_BUILD_ROOT%{_mingw32_prefix}/info/* $RPM_BUILD_ROOT%{_mingw32_infodir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/termcap.dll
%{_mingw32_libdir}/termcap.dll.a
%{_mingw32_infodir}/*
%{_mingw32_includedir}/termcap.h


%changelog
* Thu Sep 25 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-1
- Initial RPM release.
