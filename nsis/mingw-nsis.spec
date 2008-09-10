Name:           mingw-nsis
Version:        2.39
Release:        1%{?dist}
Summary:        MinGW Windows libxml2 XML processing library

License:        zlib and CPL
Group:          Development/Libraries
URL:            http://nsis.sourceforge.net/
Source0:        http://dl.sourceforge.net/sourceforge/nsis/nsis-%{version}-src.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         nsis-2.39-mingw-search.patch

BuildRequires:  mingw-filesystem >= 20
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  python
BuildRequires:  scons >= 0.96.93
BuildRequires:  wxGTK-devel


%description
NSIS, the Nullsoft Scriptable Install System, is a script-driven
Windows installation system.

This package includes native Fedora binaries of makensis (etc.)  There
are no native NSIS plugins available.  Complete Windows binaries and
plugins are in the mingw-nsis-win package, but you must run those
either on a Windows machine or under Wine.


%package win
Summary:        Windows binaries for %{name}
Requires:       %{name} = %{version}-%{release}
Group:          Development/Libraries

BuildArch:      noarch


%description win
This package includes complete Windows binaries and plugins for
%{name}.


%prep
%setup -q -n nsis-%{version}-src
%patch0 -p1


%build
scons \
  PREFIX=%{_prefix} PREFIX_CONF=%{_sysconfdir}


%install
rm -rf $RPM_BUILD_ROOT

mkdir $RPM_BUILD_ROOT
scons \
  PREFIX=%{_prefix} PREFIX_CONF=%{_sysconfdir} \
  PREFIX_DEST=$RPM_BUILD_ROOT \
  install

mv $RPM_BUILD_ROOT%{_docdir}/nsis $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

# It's not clear if we should move the Windows binaries
# to %{_mingw_sysroot} or leave them where they are.


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/nsisconf.nsh
%{_includedir}/nsis
%doc %{_docdir}/%{name}-%{version}

%files win
%defattr(-,root,root)
%{_datadir}/nsis


%changelog
* Fri Sep  5 2008 Richard W.M. Jones <rjones@redhat.com> - 2.39-1
- Initial RPM release.
