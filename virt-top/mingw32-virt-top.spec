%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-virt-top
Version:        1.0.3
Release:        3%{?dist}
Summary:        MinGW Windows port of top(1) for virtualization stats

License:        GPLv2+
Group:          Development/Libraries

URL:            http://et.redhat.com/~rjones/virt-top/
Source0:        http://et.redhat.com/~rjones/virt-top/files/virt-top-%{version}.tar.gz

# Patches from native Fedora package:
Patch0:         virt-top-1.0.3-bogus-zh_CN-plurals.patch

# Patches for MinGW.
Patch1000:      virt-top-1.0.3-link-pdcurses.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw32-ocaml
BuildRequires:  mingw32-flexdll >= 0.11-7
#BuildRequires:  ocaml-ocamldoc
BuildRequires:  mingw32-ocaml-findlib
BuildRequires:  mingw32-ocaml-curses >= 1.0.3-4
BuildRequires:  mingw32-ocaml-extlib
BuildRequires:  mingw32-ocaml-xml-light
BuildRequires:  mingw32-ocaml-csv
BuildRequires:  mingw32-ocaml-calendar
BuildRequires:  mingw32-ocaml-libvirt >= 0.4.4.2-2

# gettext support is disabled temporarily.
## Tortuous list of BRs for gettext.
#BuildRequires:  ocaml-gettext-devel >= 0.3.0
#BuildRequires:  ocaml-fileutils-devel
#%ifnarch ppc64
#BuildRequires:  ocaml-camomile-data
#%endif

# Non-OCaml BRs.
BuildRequires:  libvirt-devel
BuildRequires:  perl
BuildRequires:  gawk

BuildRequires:  autoconf, automake, libtool


%description
virt-top is a 'top(1)'-like utility for showing stats of virtualized
domains.  Many keys and command line options are the same as for
ordinary 'top'.

It uses libvirt so it is capable of showing stats across a variety of
different virtualization systems.


%prep
%setup -q -n virt-top-%{version}

%patch0 -p1
%patch1000 -p1

chmod -x COPYING

autoreconf


%build
# Workaround for non-tail-recursion in flexdll.
ulimit -s unlimited

export OCAMLFIND_CONF=%{_sysconfdir}/%{_mingw32_target}-ocamlfind.conf
export OCAMLC=%{_mingw32_target}-ocamlc
%{_mingw32_configure}
make opt


%install
rm -rf $RPM_BUILD_ROOT

export OCAMLFIND_CONF=%{_sysconfdir}/%{_mingw32_target}-ocamlfind.conf

make DESTDIR=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/virt-top


%changelog
* Sat Jan 24 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-3
- PDcurses library was renamed to libpdcurses.dll

* Mon Nov 17 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-2
- Initial RPM release.
