%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-ocaml
Version:        3.11.0+beta1
Release:        1%{?dist}
Summary:        Objective Caml MinGW cross-compiler and programming environment

License:        QPL and (LGPLv2+ with exceptions)
Group:          Development/Libraries
URL:            http://caml.inria.fr/
Source0:        http://caml.inria.fr/pub/distrib/ocaml-3.11/ocaml-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils


%description
Objective Caml is a high-level, strongly-typed, functional and
object-oriented programming language from the ML family of languages.

This package is an OCaml cross-compiler which runs natively on Fedora
and produces Windows native executables.


%prep
%setup -q -n ocaml-%{version}


%build
# Remember that we're _not_ cross-compiling OCaml itself, we're trying
# to build a Fedora native OCaml compiler (ocamlopt) which just has
# the back-end part modified to generate Windows binaries.  So we
# build as normal on a Unix system, but we make sure that ocamlopt
# will use the Windows codegen and the MinGW assembler and linker.

CFLAGS="$RPM_OPT_FLAGS" \
./configure \
  -bindir %{_bindir} \
  -libdir %{_libdir}/ocaml \
  -x11lib %{_libdir} \
  -x11include %{_includedir} \
  -mandir %{_mandir}/man1

cp config/m-nt.h config/m.h

make world bootstrap opt opt.opt


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove static libraries but DON'T remove *.dll.a files.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libfoo.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/foo.dll
%{_mingw32_libdir}/foo.dll.a
# etc.


%changelog
* Fri Oct 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0+beta1-1
- Initial RPM release.
