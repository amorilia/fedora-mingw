%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-ocaml-extlib
Version:        1.5.1
Release:        3%{?dist}
Summary:        MinGW Windows port of OCaml ExtLib

License:        LGPLv2+ with exceptions
Group:          Development/Libraries

URL:            http://code.google.com/p/ocaml-extlib/
Source0:        http://ocaml-extlib.googlecode.com/files/extlib-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-ocaml >= 3.11.0-0.15.beta1


%description
ExtLib is a project aiming at providing a complete - yet small -
standard library for the OCaml programming language. The purpose of
this library is to add new functions to OCaml Standard Library
modules, to modify some functions in order to get better performances
or more safety (tail-recursive) but also to provide new modules which
should be useful for the average OCaml programmer.


%prep
%setup -q -n extlib-%{version}

# Files in the archive have spurious +x mode.
chmod 0644 *

# and DOS line endings.
for f in *.ml *.mli README.txt LICENSE; do \
  %{__sed} -i 's/\r//' $f;
done


%build
# Extlib build system is on crack and unusable for cross-compiling.
# We ignore it completely and do the build steps by hand.  This
# list of modules should match the list in 'install.ml'.
%define modules enum bitSet dynArray extArray extHashtbl extList extString global IO option pMap std uChar uTF8 base64 unzip refList optParse dllist

i686-pc-mingw32-ocamlopt -c \
  $(for f in %{modules}; do echo $f.mli; done)
i686-pc-mingw32-ocamlopt -c \
  $(for f in %{modules}; do echo $f.ml; done)
i686-pc-mingw32-ocamlopt -a -o extLib.cmxa \
  $(for f in %{modules}; do echo $f.cmx; done)


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/extlib

install $(for f in %{modules}; do echo $f.mli $f.cmx $f.cmi; done) \
  $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/extlib
install extLib.cmxa extLib.a \
  $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/extlib
install META.txt \
  $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/extlib/META


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_libdir}/%{_mingw32_target}-ocaml/extlib


%changelog
* Sun Nov 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-3
- Rebuild with latest OCaml cross-compiler.

* Sun Nov 16 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-2
- Force rebuild against latest OCaml compiler.

* Sat Nov 15 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-1
- Initial RPM release.
