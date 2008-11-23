%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-ocaml-csv
Version:        1.1.7
Release:        3%{?dist}
Summary:        MinGW Windows OCaml library for reading and writing CSV files

License:        LGPLv2+
Group:          Development/Libraries

URL:            http://merjis.com/developers/csv
Source0:        http://merjis.com/_file/ocaml-csv-%{version}.tar.gz

# Patches from native Fedora package:
Patch0:         csv-extlib.patch
Patch1:         csv-install.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-ocaml >= 3.11.0-0.15.beta1
BuildRequires:  mingw32-ocaml-extlib


%description
This OCaml library can read and write CSV files, including all
extensions used by Excel - eg. quotes, newlines, 8 bit characters in
fields, quote-0 etc.

The library comes with a handy command line tool called csvtool for
handling CSV files from shell scripts.


%prep
%setup -q -n ocaml-csv-%{version}

%patch0 -p0
%patch1 -p1


%build
ulimit -s unlimited

%{_mingw32_target}-ocamlopt -I +extlib extLib.cmxa -c csv.mli
%{_mingw32_target}-ocamlopt -I +extlib extLib.cmxa -c csv.ml
%{_mingw32_target}-ocamlopt -a -o csv.cmxa csv.cmx
%{_mingw32_target}-ocamlopt -I +extlib extLib.cmxa csv.cmxa csvtool.ml \
  -o csvtool.exe


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/csv
mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}

install csv.cmxa *.a *.mli *.cmi *.cmx \
  $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/csv
install META $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/csv

install csvtool.exe $RPM_BUILD_ROOT%{_mingw32_bindir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/csvtool.exe
%{_libdir}/%{_mingw32_target}-ocaml/csv


%changelog
* Sun Nov 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-3
- Rebuild with latest OCaml cross-compiler.

* Sun Nov 16 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-2
- Force rebuild with latest OCaml compiler.

* Sat Nov 15 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-1
- Initial RPM release.
