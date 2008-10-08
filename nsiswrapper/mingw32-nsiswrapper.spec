Name:           mingw32-nsiswrapper
Version:        1
Release:        1%{?dist}
Summary:        Helper program for making NSIS Windows installers

License:        GPLv2+
Group:          Development/Libraries
URL:            http://fedoraproject.org/wiki/MinGW
Source0:        nsiswrapper.pl
Source1:        README
Source2:        COPYING
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  perl

Requires:       mingw32-nsis


%description
NSISWrapper is a helper program for making Windows installers,
particularly when you are cross-compiling from Unix.

NSIS (a separate package) is a program for building Windows
installers.  This wrapper simply makes it easier to generate the
installer script that NSIS needs.


%prep
# empty


%build
# empty


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 %{SOURCE0} $RPM_BUILD_ROOT%{_bindir}/nsiswrapper

# Install documentation (manually).
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m 0644 %{SOURCE1} %{SOURCE2} \
  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

# Build the manpage from the source.
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
pod2man -c "NSIS" -r "%{name}-%{version}" %{SOURCE0} \
  > $RPM_BUILD_ROOT%{_mandir}/man1/nsiswrapper.1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}/COPYING
%doc %{_docdir}/%{name}-%{version}/README
%{_bindir}/nsiswrapper
%{_mandir}/man1/nsiswrapper.1*


%changelog
* Wed Oct  8 2008 Richard W.M. Jones <rjones@redhat.com> - 1-1
- Initial RPM release.
