%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-ocaml-xml-light
Version:        2.2.cvs20070817
Release:        4%{?dist}
Summary:        MinGW Windows minimal XML parser and printer for OCaml

License:        LGPLv2+
Group:          Development/Libraries

URL:            http://tech.motion-twin.com/xmllight.html
Source0:        xml-light-%{version}.tar.gz

# Patches for MinGW:
Patch1000:      mingw32-ocaml-xml-light-2.2-build.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-ocaml >= 3.11.0-0.15.beta1


%description
Xml-Light is a minimal XML parser & printer for OCaml. It provides
functions to parse an XML document into an OCaml data structure, work
with it, and print it back to an XML document. It support also DTD
parsing and checking, and is entirely written in OCaml, hence it does
not require additional C library.


%prep
%setup -q -c -n %{name}-%{version}

%patch1000 -p0


%build
ulimit -s unlimited

make opt
sed -e 's/@VERSION@/%{VERSION}/' < META.in > META


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/xml-light

install xml-light.cmxa xml-light.a *.mli *.cmi *.cmx \
  $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/xml-light
install META $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/xml-light


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_libdir}/%{_mingw32_target}-ocaml/xml-light/


%changelog
* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-4
- Rebuild for mingw32-gcc 4.4

* Sun Nov 23 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2cvs20070817-3
- Rebuild against latest OCaml cross-compiler.

* Sun Nov 16 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2cvs20070817-2
- Force rebuild against latest OCaml compiler.

* Sat Nov 15 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2cvs20070817-1
- Initial RPM release.
