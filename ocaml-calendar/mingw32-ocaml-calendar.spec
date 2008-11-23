%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-ocaml-calendar
Version:        2.0.4
Release:        4%{?dist}
Summary:        MinGW Windows OCaml library for managing dates and times

License:        LGPLv2+
Group:          Development/Libraries

URL:            http://www.lri.fr/~signoles/prog.en.html#calendar
Source0:        http://www.lri.fr/~signoles/prog/calendar/calendar-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-ocaml >= 3.11.0-0.15.beta1
BuildRequires:  mingw32-ocaml-findlib >= 1.2.2-7


%description
Objective Caml library for managing dates and times.


%prep
%setup -q -n calendar-%{version}


%build
export OCAMLFIND_CONF=/etc/i686-pc-mingw32-ocamlfind.conf

%{_mingw32_configure} \
  --libdir=%{_libdir} \
  OCAMLC=i686-pc-mingw32-ocamlc \
  OCAMLCDOTOPT=i686-pc-mingw32-ocamlc \
  OCAMLOPT=i686-pc-mingw32-ocamlopt \
  OCAMLOPTDOTOPT=i686-pc-mingw32-ocamlopt \
  OCAMLDEP=i686-pc-mingw32-ocamldep
make


%install
rm -rf $RPM_BUILD_ROOT

export OCAMLFIND_CONF=/etc/i686-pc-mingw32-ocamlfind.conf
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml

mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_libdir}/%{_mingw32_target}-ocaml/calendar/


%changelog
* Sun Nov 23 2008 Richard W.M. Jones <rjones@redhat.com> - 2.0.4-4
- Rebuild with newly named mingw32-ocaml cross-compiler.

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 2.0.4-3
- Override ocamlc.opt, ocamlopt.opt in case a compatible native
  compiler is also installed.

* Sun Nov 16 2008 Richard W.M. Jones <rjones@redhat.com> - 2.0.4-2
- Force rebuild with latest OCaml compiler.

* Sun Nov 16 2008 Richard W.M. Jones <rjones@redhat.com> - 2.0.4-1
- Initial RPM release.
