%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-popt
Version:        1.13_cvs20081025
Release:        1%{?dist}
Summary:        MinGW Windows C library for parsing command line parameters

License:        MIT
Group:          Development/Libraries
URL:            http://www.rpm5.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

# Checked out from CVS on this date.
Source0:        popt-20081025.tar.gz

# Not needed - no multilib on MinGW.
#Source1:        http://people.redhat.com/jantill/fedora/png-mtime.py

# These don't apply to CVS.
#Patch0:         popt-1.13-multilib.patch
#Patch1:         popt-1.13-popt_fprintf.patch

# MinGW patches.
Patch1000:      popt-win.patch
Patch1001:      popt-gnulib.patch
Patch1002:      popt-autogen.patch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-gettext
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  python
BuildRequires:  autoconf, automake, libtool, gettext, perl


%description
Popt is a C library for parsing command line parameters. Popt was
heavily influenced by the getopt() and getopt_long() functions, but
it improves on them by allowing more powerful argument expansion.
Popt can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments. Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.


%prep
%setup -q -n popt

#%patch0 -p1 -b .multilib
#%patch1 -p1 -b .popt_fprintf

%patch1000 -p1 -b .win
%patch1001 -p1 -b .gnulib
%patch1002 -p1 -b .autogen

chmod 0755 configure


%build
%{_mingw32_configure}
make -C lib fnmatch.h
make
doxygen


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/popt.d

# Remove the static library.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libpopt.a

# Remove the man page since it duplicates content in the Fedora native pkg.
rm $RPM_BUILD_ROOT%{_mingw32_mandir}/man3/*

# This is broken under MinGW - we should have our own variant.
#%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libpopt-0.dll
%{_mingw32_libdir}/libpopt.dll.a
%{_mingw32_libdir}/libpopt.la
%{_mingw32_includedir}/popt.h
%{_mingw32_datadir}/locale/*/LC_MESSAGES/*.mo
%config(noreplace) %{_mingw32_sysconfdir}/popt.d


%changelog
* Sat Oct 25 2008 Richard W.M. Jones <rjones@redhat.com> - 1.13-1
- Initial RPM release.
