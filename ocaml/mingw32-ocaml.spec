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

# This is installed as config/Makefile when we cross-compile.
Source1000:     Makefile-fedora-mingw.in

# XXX We should apply any Fedora native patches here.

# For patch description, see the top of each patch file.
# Start numbering at 1000 since these are MinGW-specific patches.
Patch1000:      mingw32-ocaml-3.11.0+beta1-combined-Makefile.patch
Patch1001:      mingw32-ocaml-3.11.0+beta1-disable-cmxs.patch
Patch1002:      mingw32-ocaml-3.11.0+beta1-filename-win32-dirsep.patch
Patch1003:      mingw32-ocaml-3.11.0+beta1-i386-profiling.patch
Patch1004:      mingw32-ocaml-3.11.0+beta1-no-stdlib-dir.patch
Patch1005:      mingw32-ocaml-3.11.0+beta1-win32-fixes.patch
Patch1006:      mingw32-ocaml-3.11.0+beta1-win32unix-path.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Is it noarch? (XXX)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-flexdll


%description
Objective Caml is a high-level, strongly-typed, functional and
object-oriented programming language from the ML family of languages.

This package is an OCaml cross-compiler which runs natively on Fedora
and produces Windows native executables.


%prep
%setup -q -n ocaml-%{version}

%patch1000 -p1
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1
%patch1006 -p0


%build
# Build native ocamlrun and ocamlc which contain the filename-win32-dirsep
# patch.
./configure \
  -no-tk \
  -bindir %{_bindir} \
  -libdir %{_libdir}/ocaml \
  -mandir %{_mandir}/man1
make world

# Now move the working ocamlrun, ocamlc into the boot/ directory,
# overwriting the binary versions which ship with the compiler with
# ones that contain the above filename-win32-dirsep patch.
make coreboot

# Now replace the compiler configuration (config/{s.h,m.h,Makefile})
# with ones as they would be on a 32 bit Windows system.
pushd config

# config/m.h can just be copied from config/m-nt.h which ships.
rm -f m.h
cp m-nt.h m.h

# config/s.h can just be copied from config/s-nt.h which ships.
rm -f s.h
cp s-nt.h s.h

# config/Makefile is a custom one which we supply.
rm -f Makefile
sed \
  -e 's,@prefix@,%{_prefix},g' \
  -e 's,@bindir@,%{_bindir},g' \
  -e 's,@libdir@,%{_libdir},g' \
  < %{SOURCE1000} > Makefile

popd

# We're going to build in otherlibs/win32unix and otherlibs/win32graph
# directories, but since they would normally only be built under
# Windows, they only have the Makefile.nt files.  Just symlink
# Makefile -> Makefile.nt for these cases.
for d in otherlibs/win32unix otherlibs/win32graph; do
  ln -s Makefile.nt $d/Makefile
done

# Now clean the temporary files from the previous build.  This
# will also cause asmcomp/arch.ml (etc) to be linked to the 32 bit
# i386 versions, essentially causing ocamlopt to use the Win/i386 code
# generator.
make partialclean

# Just rebuild some small bits that we need for the following
# 'make opt' to work.  Note that 'make all' fails here.
make -C byterun libcamlrun.a
make ocaml ocamlc
make -C stdlib
make -C tools ocamlmklib

# Build ocamlopt
make opt


%install
rm -rf $RPM_BUILD_ROOT

# Only want to install ocamlopt and libraries.
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/i686-pc-mingw32-ocaml
mkdir -p $RPM_BUILD_ROOT%{_libdir}/i686-pc-mingw32-ocaml/threads

make installopt \
  BINDIR=$RPM_BUILD_ROOT%{_bindir} \
  LIBDIR=$RPM_BUILD_ROOT%{_libdir}/i686-pc-mingw32-ocaml

# ocamlopt is a cross-compiler, so rename the binary.
# XXX This should probably use %{_mingw32_target} macro.
mv $RPM_BUILD_ROOT%{_bindir}/ocamlopt \
  $RPM_BUILD_ROOT%{_bindir}/i686-pc-mingw32-ocamlopt


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_bindir}/i686-pc-mingw32-ocamlopt
%{_libdir}/i686-pc-mingw32-ocaml/


%changelog
* Sat Nov 15 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0+beta1-1
- Initial RPM release.
