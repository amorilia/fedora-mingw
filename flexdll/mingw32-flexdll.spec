%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

%define debug_package %{nil}

# Running the tests requires Wine.
%define run_tests 0

Name:           mingw32-flexdll
Version:        0.11
Release:        7%{?dist}
Summary:        FlexDLL Windows DLL plugin API which is like dlopen

License:        zlib
Group:          Development/Libraries

URL:            http://alain.frisch.fr/flexdll.html
Source0:        http://alain.frisch.fr/flexdll/flexdll-%{version}.tar.gz
Source1:        flexlink.exe

# Patches for MinGW:
Patch1000:      mingw32-flexdll-0.11-mingw-cross.patch
Patch1001:      mingw32-flexdll-0.11-no-cygpath.patch
Patch1002:      mingw32-flexdll-0.11-no-directory.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  ocaml
BuildRequires:  dos2unix


%description
Under Windows, DLL (Dynamically-Linked Libraries) are generally used
to improve code modularity and sharing. A DLL can be loaded
automatically when the program is loaded (if it requires the DLL). The
program can also explicitly request Windows to load a DLL at any
moment during runtime, using the LoadLibrary function from the Win32
API.

This naturally suggests to use DLLs as a plugin mechanism. For
instance, a web server could load extensions modules stored in DLLs at
runtime. But Windows does not really make it easy to implement plugins
that way. The reason is that when you try to create a DLL from a set
of object files, the linker needs to resolve all the symbols, which
leads to the very problem solved by FlexDLL:

Windows DLL cannot refer to symbols defined in the main application or
in previously loaded DLLs.

Some usual solutions exist, but they are not very flexible. A notable
exception is the edll library (its homepage also describes the usual
solutions), which follows a rather drastic approach; indeed, edll
implements a new dynamic linker which can directly load object files
(without creating a Windows DLL).

FlexDLL is another solution to the same problem. Contrary to edll, it
relies on the native static and dynamic linkers. Also, it works both
with the Microsoft environment (MS linker, Visual Studio compilers)
and with Cygwin (GNU linker and compilers, in Cygwin or MinGW
mode). Actually, FlexDLL implements mostly the usual dlopen POSIX API,
without trying to be fully conformant though (e.g. it does not respect
the official priority ordering for symbol resolution). This should
make it easy to port applications developed for Unix.


%prep
%setup -q -n flexdll

%patch1000 -p1
%patch1001 -p1
%patch1002 -p1

for f in CHANGES LICENSE README; do
  chmod -x $f
  dos2unix $f
done


%build
make TOOLCHAIN=mingw MINCC=%{_mingw32_cc} CC=%{_mingw32_cc} \
  flexlink.exe build_mingw

strip flexlink.exe


%check
%if %{run_tests}
make -C test CC=%{_mingw32_cc} O=o CHAIN=mingw
%endif


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/flexdll

# Install everything in a libdir directory.  Some of the files
# have execute permissions which we can remove.
install -m 0644 \
  flexdll.h flexdll.c flexdll_initer.c default.manifest flexdll_*.o \
  $RPM_BUILD_ROOT%{_libdir}/flexdll
install -m 0755 flexlink.exe \
  $RPM_BUILD_ROOT%{_libdir}/flexdll

# Provide a wrapper script which sets FLEXDIR to point to the
# libdir directory.  Some programs call 'flexlink' and some call
# 'flexlink.exe' so provide both.
sed 's,@libdir@,%{_libdir},g' \
  < %{SOURCE1} > $RPM_BUILD_ROOT%{_bindir}/flexlink.exe
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/flexlink.exe
(cd $RPM_BUILD_ROOT%{_bindir} && ln flexlink.exe flexlink)


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc LICENSE README CHANGES
%{_bindir}/flexlink
%{_bindir}/flexlink.exe
%{_libdir}/flexdll


%changelog
* Sun Nov 16 2008 Richard W.M. Jones <rjones@redhat.com> - 0.11-7
- Apply no-directory patch.

* Sun Nov 16 2008 Richard W.M. Jones <rjones@redhat.com> - 0.11-6
- Permanently disable cygpath (avoids 'NUL' file being created).

* Fri Nov 14 2008 Richard W.M. Jones <rjones@redhat.com> - 0.11-4
- Initial RPM release.
