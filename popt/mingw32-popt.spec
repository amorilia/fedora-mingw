%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

# popt 1.13 doesn't work for cross-compilation, but the CVS version
# contains significant fixes which get some of the way there.  (We
# patch it further, and have sent those fixes upstream).  This is the
# date of the CVS version that we use as a base:
%define cvsdate 20081025

Name:           mingw32-popt
Version:        1.14
Release:        0.3.cvs%{cvsdate}%{?dist}
Summary:        MinGW Windows C library for parsing command line parameters

License:        MIT
Group:          Development/Libraries
URL:            http://www.rpm5.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

# Checked out from CVS on this date.
Source0:        popt-%{cvsdate}.tar.gz

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
%{_mingw32_configure} --disable-static
make -C lib fnmatch.h
make %{?_smp_mflags}
doxygen


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/popt.d

# Remove the man page since it duplicates content in the Fedora native pkg.
rm $RPM_BUILD_ROOT%{_mingw32_mandir}/man3/*

%find_lang popt


%clean
rm -rf $RPM_BUILD_ROOT


%files -f popt.lang
%defattr(-,root,root)
%doc COPYING
%{_mingw32_bindir}/libpopt-0.dll
%{_mingw32_libdir}/libpopt.dll.a
%{_mingw32_libdir}/libpopt.la
%{_mingw32_includedir}/popt.h
%config(noreplace) %{_mingw32_sysconfdir}/popt.d


%changelog
* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.14-0.3.cvs20081025
- Rebuild for mingw32-gcc 4.4

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.14-0.2.cvs20081025
- Include license file.

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.14-0.1.cvs20081025
- The version should be 1.14 because this is a pre-release (from CVS).
- Disable static libraries.
- Build using _smp_mflags.
- Use find_lang.

* Sat Oct 25 2008 Richard W.M. Jones <rjones@redhat.com> - 1.13-1
- Initial RPM release.
