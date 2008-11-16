# Built-in strip corrupts binaries, so use the mingw32 strip instead:
%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}

%define debug_package %{nil}

%define otherlibraries win32unix str num dynlink bigarray systhreads win32graph

Name:           mingw32-ocaml
Version:        3.11.0+beta1
Release:        13%{?dist}
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
# Answer: yes and no.  In theory it should be, but because we install
# Windows binaries in %{_libdir}, the path is different if built on
# 32 and 64 bit platforms.  We should probably install the binaries
# in /usr/share.
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-flexdll

# These are required so we can use gcc -m32 and link to 32 bit X11:
BuildRequires:  /lib/libgcc_s.so.1
BuildRequires:  /usr/lib/crt1.o
BuildRequires:  /usr/lib/libX11.so

# While we still ship bytecode, this requires a /usr/bin/ocamlrun from
# the _identical_ native package.  We don't have that at the moment,
# which is why this is commented out.
#Requires:       ocaml-runtime = %{version}

# The built program will try to run the cross-compiler and flexdll, so
# these must be runtime requires.
Requires:       mingw32-gcc
Requires:       mingw32-binutils
Requires:       mingw32-flexdll

# i686-pc-mingw32-ocamlmklib tries to run ocamlopt which is probably a
# bug, but requires this (XXX).
Requires:       ocaml


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
# Don't run out of memory.
ulimit -s unlimited

# Build native ocamlrun and ocamlc which contain the
# filename-win32-dirsep patch.
#
# Note that we must build a 32 bit compiler, even on 64 bit build
# architectures, because this compiler will try to do strength
# reduction optimizations using its internal int type, and that must
# match Windows' int type.  (That's what -cc and -host are for).
./configure \
  -no-tk \
  -bindir %{_bindir} \
  -libdir %{_libdir}/ocaml \
  -mandir %{_mandir}/man1 \
  -cc "gcc -m32" -host i386-pc-linux -x11lib /usr/lib -verbose
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
  -e 's,@target@,%{_mingw32_target},g' \
  -e 's,@otherlibraries@,%{otherlibraries},g' \
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

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/threads
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/stublibs

# This is the equivalent of 'make install installopt', but
# we only want to install the parts which are really necessary
# for the cross-compiler.  eg. We don't need any of the native
# tools like ocamllex or ocamldoc.
%define makevars BINDIR=$RPM_BUILD_ROOT%{_bindir} LIBDIR=$RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml
make %{makevars} -C byterun install
make %{makevars} -C stdlib install
for i in %{otherlibraries}; do
  make %{makevars} -C otherlibs/$i install
done
make %{makevars} -C tools install
make %{makevars} installopt

install -m 0755 ocamlc $RPM_BUILD_ROOT%{_bindir}

cp config/Makefile \
   $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/Makefile.config

# For bytecode binaries, change the bang-path to point to the locally
# installed ocamlrun.
pushd $RPM_BUILD_ROOT%{_bindir}
for f in ocamlc ocamlcp ocamldep ocamlmklib ocamlopt ocamlprof; do
  mv $f $f.old
  echo '#!%{_bindir}/%{_mingw32_target}-ocamlrun' > $f
  tail -n +2 $f.old >> $f
  chmod +x $f
  rm $f.old
done
popd

# Rename all the binaries to target-binary.
pushd $RPM_BUILD_ROOT%{_bindir}
for f in ocamlc ocamlcp ocamldep ocamlmklib ocamlmktop ocamlopt ocamlprof ocamlrun; do
  mv $f %{_mingw32_target}-$f
done
popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_bindir}/%{_mingw32_target}-ocamlc
%{_bindir}/%{_mingw32_target}-ocamlcp
%{_bindir}/%{_mingw32_target}-ocamldep
%{_bindir}/%{_mingw32_target}-ocamlmklib
%{_bindir}/%{_mingw32_target}-ocamlmktop
%{_bindir}/%{_mingw32_target}-ocamlprof
%{_bindir}/%{_mingw32_target}-ocamlopt
%{_bindir}/%{_mingw32_target}-ocamlrun
%{_libdir}/%{_mingw32_target}-ocaml/


%changelog
* Sun Nov 16 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0+beta1-13
- Build the native compiler as 32 bits even on a 64 bit build
  architecture (because the target, Windows, is 32 bit).  The
  compiler does strength reduction and other optimizations
  internally so we must ensure it uses the same int type.
- Requires libX11-devel.i386 and libgcc.i386.
- Allow the normal dependency generators to run because this
  is a native package.
- Use mingw32 strip to avoid corrupting binaries.

* Sun Nov 16 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0+beta1-8
- Install ocamlc.

* Sat Nov 15 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0+beta1-7
- Further requirements.

* Sat Nov 15 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0+beta1-6
- Install tools, particularly ocamlmklib.

* Sat Nov 15 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0+beta1-5
- +Requires mingw32-flexdll and the cross-compiler.

* Sat Nov 15 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0+beta1-4
- Initial RPM release.
