%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-virt-ctrl
Version:        1.0.3
Release:        2%{?dist}
Summary:        MinGW Windows port of virt-ctrl

License:        GPLv2+
Group:          Development/Libraries

URL:            http://et.redhat.com/~rjones/virt-ctrl/
Source0:        http://et.redhat.com/~rjones/virt-ctrl/files/virt-ctrl-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw32-ocaml >= 3.11.0

BuildRequires:  mingw32-ocaml-lablgtk >= 2.10.1
BuildRequires:  mingw32-gtk2
BuildRequires:  gnome-icon-theme
BuildRequires:  mingw32-ocaml-dbus >= 0.06
BuildRequires:  mingw32-ocaml-libvirt
BuildRequires:  mingw32-ocaml-xml-light
BuildRequires:  mingw32-ocaml-extlib

# gettext support is disabled temporarily.
## Tortuous list of BRs for gettext.
#BuildRequires:  ocaml-gettext-devel >= 0.3.0
#BuildRequires:  ocaml-fileutils-devel
#%ifnarch ppc64
#BuildRequires:  ocaml-camomile-data
#%endif


%description
Virt-ctrl is a graphical management app for virtual machines, modelled
after Virtual Machine Manager, but much more lightweight.


%prep
%setup -q -n virt-ctrl-%{version}


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
%{_mingw32_bindir}/virt-ctrl


%changelog
* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-2
- Rebuild for mingw32-gcc 4.4

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-1
- Initial RPM release.
