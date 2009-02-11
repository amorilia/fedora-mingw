Name:           mingw32-crossreport
Version:        3
Release:        1%{?dist}
Summary:        Analysis tool to help cross-compilation to Windows

License:        GPLv2+
Group:          Development/Libraries
URL:            http://fedoraproject.org/wiki/MinGW
Source0:        crossreport.pl
Source1:        README
Source2:        COPYING
Source3:        crossreport.db
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  perl


%description
CrossReport is a tool to help you analyze the APIs used by a compiled
Linux program, in order to work out the effort required to
cross-compile that program for Windows, using the Fedora MinGW
cross-compiler.

The simplest way to use it is to point it at an existing Linux binary,
and then read the generated report.

What it does in more detail: It looks at the libraries and API calls
used by the Linux binary, and compares them to the libraries and API
calls that we currently support under the Fedora MinGW cross-compiler.
It then works out what is missing, and produces a report suggesting
the amount of work that needs to be done to port the program.  For
example, whether whole libraries need to be ported first, and/or how
to substitute individual calls to work on Windows.


%prep
# empty


%build
# empty


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 %{SOURCE0} $RPM_BUILD_ROOT%{_bindir}/mingw32-crossreport

# Install the database.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/crossreport
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/crossreport/

# Install documentation (manually).
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m 0644 %{SOURCE1} %{SOURCE2} \
  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

# Build the manpage from the source.
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
pod2man -c "CrossReport" -r "%{name}-%{version}" %{SOURCE0} \
  > $RPM_BUILD_ROOT%{_mandir}/man1/mingw32-crossreport.1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}/COPYING
%doc %{_docdir}/%{name}-%{version}/README
%{_bindir}/mingw32-crossreport
%{_mandir}/man1/mingw32-crossreport.1*
%{_datadir}/crossreport/


%changelog
* Wed Feb 11 2009 Richard W.M. Jones <rjones@redhat.com> - 3-1
- Initial RPM release.
