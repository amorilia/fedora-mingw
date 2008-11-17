%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-ocaml-curses
Version:        1.0.3
Release:        2%{?dist}
Summary:        MinGW Windows OCaml bindings for ncurses

License:        LGPLv2+
Group:          Development/Libraries

URL:            http://savannah.nongnu.org/projects/ocaml-tmk/
Source0:        http://download.savannah.gnu.org/releases/ocaml-tmk/ocaml-curses-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-ocaml >= 3.11.0+beta1-9
BuildRequires:  mingw32-ocaml-findlib
BuildRequires:  mingw32-pdcurses

# Upstream package doesn't come with a configure script so
# we have to rebuild it.
BuildRequires:  autoconf, automake, libtool

Requires:       mingw32-pdcurses


%description
OCaml bindings for curses.


%prep
%setup -q -n ocaml-curses-%{version}

autoreconf


%build
ulimit -s unlimited

%{_mingw32_configure}

make all opt \
  OCAMLC=%{_mingw32_target}-ocamlc \
  OCAMLOPT=%{_mingw32_target}-ocamlopt \
  OCAMLMKLIB=%{_mingw32_target}-ocamlmklib \
  OCAMLMKLIB_FLAGS="-L%{_mingw32_libdir}" \
  CLIBS="" \
  all opt

# Build the test program just to check that everything is OK.
%{_mingw32_target}-ocamlopt -I . \
  -o test.opt \
  curses.cmxa \
  test.ml \
  -cclib "-L%{_mingw32_libdir} pdcurses.dll.a"


%install
rm -rf $RPM_BUILD_ROOT

export OCAMLFIND_CONF=%{_sysconfdir}/%{_mingw32_target}-ocamlfind.conf
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml

mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
ocamlfind install curses META *.cmi *.cmx *.cmxa *.a *.mli


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_libdir}/%{_mingw32_target}-ocaml/curses/


%changelog
* Mon Nov 17 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-2
- Runtime requires PDCurses library.

* Mon Nov 17 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-1
- New upstream version 1.0.3 with proper support for Windows
  and PDCurses.

* Mon Nov 17 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1-4
- libmlcurses.a contained a copy of pdcurses.dll.a in error.

* Sun Nov 16 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1-3
- Use ocamlfind to install in the correct location.
- Install the META file.
- Fix the version number in changelog.

* Sun Nov 16 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1-2
- Initial release.
