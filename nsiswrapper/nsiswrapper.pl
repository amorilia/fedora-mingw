#!/usr/bin/perl -w
#
# NSISWrapper - a helper program for making Windows installers.
# Copyright (C) 2008 Red Hat Inc.
# Written by Richard W.M. Jones <rjones@redhat.com>,
# http://fedoraproject.org/wiki/MinGW
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

use strict;
use Getopt::Long;
use Pod::Usage;

=pod

=head1 NAME

nsiswrapper - Helper program for making NSIS Windows installers

=head1 SYNOPSIS

 nsiswrapper [options] [roots...]

 nsiswrapper myprogram.exe anotherprog.exe docs/ > script.nsis

 nsiswrapper --run myprogram.exe anotherprog.exe docs/

=head1 DESCRIPTION

nsiswrapper is a helper program for making it easier to create Windows
installers in a cross-compiler environment.  It still requires NSIS (a
Windows installer generator) but cuts out the tedium of writing the
NSIS command script, and can even invoke NSIS automatically to
generate a final Windows executable.

The general way to use it is to list out some files that you want
packaged.  For example:

  nsiswrapper myprogram.exe

This will search for C<myprogram.exe> and any libraries (C<*.dll>)
that it depends upon, and then it will print out an NSIS script.

If you want to have it run C<makensis> as well (to automatically
create a Windows installer) then do:

  nsiswrapper --run myprogram.exe

which will generate C<installer.exe> output file that contains
C<myprogram.exe> plus any dependencies.

You can list other files and directories that you want to have
contained in your installer.  For example:

  nsiswrapper myprogram.exe anotherprog.exe docs/*.html

There are many other command line options which control aspects of the
NSIS command script (and hence, the final installer), such as:

=over 4

=item *

The name of the final installer.

=item *

Desktop shortcuts and menu items.

=item *

License files.

=back

It's a good idea to examine the NSIS command script, to check that
nsiswrapper is including all the right dependencies.

=head1 OPTIONS

=over 4

=item B<--help>

Print brief help message and exit.

=item B<--man>

Print the full manual page for the command and exit.

=item B<--verbose>

Print verbose messages while running.  If this is not given then we
try to operate quietly.

=item B<--run>

Normally this program just prints out the NSIS installer command
script.  However if you supply this option, then we run C<makensis>
and attempt to generate an actual Windows installer.

=item B<--name "Name">

Set the long name of the installer.

If not set, the script tries to invent a suitable name based on the
first root file given on the command line.

See also B<--outfile>.

=item B<--outfile myinstaller.exe>

Set the output filename for the installer.

If not set, this defaults to C<installer.exe>.

This is the same as the C<OutFile> option to NSIS.

=item B<--installdir 'C:\foo'>

Set the default Windows installation directory.  If not set, this
program will choose a suitable default based on the name.

In any case, the end user can override this when they run the
installer.

Note that since this string will contain backslashes, you should
single-quote it to protect it from the shell.

This is the same as the C<InstallDir> option to NSIS.

=item B<--installdirregkey 'HKLM SOFTWARE\FOO'>

Set the name of the registry key used to save the installation
directory.  This has two purposes: Firstly it is used to automagically
remember the installation directory between installs.  Secondly your
program can use this as one method to find its own installation
directory (there are other ways to do this).

The default is C<HKLM SOFTWARE\Name> where C<Name> is derived from the
name of the installer.

Note that since this string will contain backslashes and spaces, you
should single-quote it to protect it from the shell.

This is the same as the C<InstallDirRegKey> option to NSIS.

=back

=cut

my $objdump;
my $help = '';
my $man = '';
my $verbose = '';
my %files;
my $name = '';
my $outfile = 'installer.exe';
my $installdir = '';
my $installdirregkey = '';

sub get_options
{
    my $result = GetOptions (
	"help|?" => \$help,
	"man" => \$man,
	"verbose" => \$verbose,
	"name=s" => \$name,
	"outfile=s" => \$outfile,
	"installdir=s" => \$installdir,
	"installdirregkey=s" => \$installdirregkey,
    );
    die "nsiswrapper: use --help for information about command line options\n"
	unless $result;

    pod2usage(1) if $help;
    pod2usage(-exitstatus => 0, -verbose => 2) if $man;

    # Add the roots to the list of files.
    die "nsiswrapper: no roots specified: use --help for more help\n"
	if @ARGV == 0;
    foreach (@ARGV) {
	my $exec = 0;
	$exec = 1 if m/\.exe$/i;

	$files{$_} = {
	    name => $_,
	    root => 1,
	    dir => -d $_,
	    exec => $exec,
	}
    }

    # Name not set?
    if (!$name) {
	# Massage the first root into a suitable package name.
	$_ = $ARGV[0];
	s{.*/}{};
	s{\.\w\w\w\w?$}{};
	$_ = ucfirst;
	$name = $_;
    }

    # InstallDir not set?
    if (!$installdir) {
	$_ = $name;
	s/\W/-/g;
	$installdir = "c:\\$_"
    }

    # InstallDirRegKey not set?
    if (!$installdirregkey) {
	$_ = $name;
	s/\W/-/g;
	$installdirregkey = "HKLM SOFTWARE\\$_"
    }
}

# Check prerequisites.

sub check_prereqs
{
    my @paths = split (/:/, $ENV{PATH});

    if (! $objdump) {
	$objdump = check_path ("i686-pc-mingw32-objdump", @paths);
	if (! $objdump || ! -x $objdump) {
	    die "i686-pc-mingw32-objdump: program not found on \$PATH\n"
	}
    }
}

# Check for the existance of a file at the given paths (not
# necessarily executable).  Returns the pathname of the file or
# undefined if not found.

sub check_path
{
    local $_ = shift;
    my @paths = @_;

    my $found;
    foreach my $dir (@paths) {
	my $file = $dir . "/" . $_;
	if (-f $file) {
	    $found = $file;
	    last;
	}
    }
    $found
}

# Print configuration.

sub print_config
{
    print "Configuration:\n";
    print "\t\$PATH = $ENV{PATH}\n";
    print "\t\$objdump = $objdump\n";
    print "\t\$verbose = $verbose\n";
    print "\t\$name = \"$name\"\n";
    print "\t\$outfile = \"$outfile\"\n";
    print "\t\$installdir = \"$installdir\"\n";
    print "\t\$installdirregkey = \"$installdirregkey\"\n";
    my @roots = keys %files;
    print "\t\@roots = (", join (", ", @roots), ")\n";
    print "End of configuration.\n";
}

# Starting at the roots, get the dependencies.

sub do_dependencies
{
    my $gotem = 1;

    while ($gotem) {
	$gotem = 0;
	foreach (keys %files) {
	    my @deps = get_deps_for_file ($_);

	    # Add the deps as separate files.
	    foreach (@deps) {
		unless (exists $files{$_}) {
		    $files{$_} = {
			name => $_,
			root => 0,
			dir => 0,
			exec => 0,
		    };
		    $gotem = 1;
		}
	    }
	}
    }
}

my $path_warning = 0;

sub get_deps_for_file
{
    my $file = shift;
    my @paths = split (/:/, $ENV{PATH});

    # If we already fetched the dependencies for this file, just
    # return that list now.
    if (exists $files{$file}->{deps}) {
	return @{$files{$file}->{deps}}
    }

    my @deps = ();

    # We only know how to do this for *.exe and *.dll files.
    if (m/\.exe$/i || m/\.dll$/i) {
	my $cmd = "$objdump -p '$file' |
                   grep 'DLL Name:' |
                   grep -Eo '[-._[:alnum:]]+\.dll' |
                   sort -u"; # XXX quoting
	open DEPS, "$cmd |" or die "$cmd: $!";
	foreach (<DEPS>) {
	    chomp; $_ = lc;

	    # Ignore Windows system DLL deps.
	    next if is_windows_system_dll ($_);

	    # Does the file exist on the path?
	    my $found = check_path ($_, @paths);
	    if ($found) {
		push @deps, $found;
	    } else {
		warn "MISSING DEPENDENCY: $_ (for $file)\n";
		unless ($path_warning) {
		    warn "You may need to add the directory containing this file to your \$PATH\n";
		    $path_warning = 1;
		}
	    }
	}
	close DEPS;

	if ($verbose) {
	    if (@deps > 0) {
		print "dependencies found for binary $file:\n\t",
	          join ("\n\t", @deps), "\n";
	    } else {
		print "no dependencies found for $file\n"
	    }
	}

    }

    # Cache the list of dependencies so we can just return it
    # immediately next time.
    $files{$file}->{deps} = \@deps;
    return @deps;
}

sub is_windows_system_dll
{
    local $_ = shift;

    $_ eq 'gdi32.dll' ||
	$_ eq 'kernel32.dll' ||
	$_ eq 'ole32.dll' ||
	$_ eq 'mscoree.dll' ||
	$_ eq 'msvcrt.dll' ||
	$_ eq 'user32.dll'
}

# Decide how we will name the output files.  This removes the
# common prefix from filenames, if it can determine one.

sub install_names
{
    my @names = keys %files;

    # Determine if all the names share a common prefix.
    my @namelens = map { length } @names;
    my $shortest = min (@namelens);

    my $prefixlen;
    for ($prefixlen = $shortest; $prefixlen >= 0; --$prefixlen) {
	my @ns = map { $_ = substr $_, 0, $prefixlen } @names;
	last if same (@ns);
    }

    if ($verbose) { print "prefix length = $prefixlen\n" }

    # Remove the prefix from each name and save the install directory
    # and install filename separately.
    foreach my $name (keys %files) {
	my $install_as = substr $name, $prefixlen;

	my ($install_dir, $install_name);

	if ($install_as =~ m{(.*)/(.*)}) {
	    $install_dir = $1;
	    $install_name = $2;
	} else {
	    $install_dir = ".";
	    $install_name = $install_as;
	}

	# Convert / in install_dir into backslashes.
	$install_dir =~ s{/}{\\}g;

	$files{$name}->{install_dir} = $install_dir;
	$files{$name}->{install_name} = $install_name;
    }
}

sub max
{
    my $max = $_[0];
    for (@_[1..$#_]) {
	$max = $_ if $_ > $max;
    }
    $max
}

sub min
{
    my $min = $_[0];
    for (@_[1..$#_]) {
	$min = $_ if $_ < $min;
    }
    $min
}

sub same
{
    my  $s = $_[0];
    for (@_[1..$#_]) {
	return 0 if $_ ne $s;
    }
    1;
}

# Print the list of files.

sub print_files
{
    print "Files:\n";
    foreach (sort keys %files) {
	print "\t$_";
	if ($files{$_}->{root}) {
	    print " [root]";
	}
	if ($files{$_}->{dir}) {
	    print " [dir]";
	}
	print STDOUT ("\n\t  => ",
	       $files{$_}->{install_dir}, " \\ ", $files{$_}->{install_name},
	       "\n");
    }
    print "End of files.\n";
}

# Write the NSIS script.

sub write_script
{
    my $io = shift;

    print $io <<EOT;
#!Nsis Installer Command Script
#
# This is an NSIS Installer Command Script generated automatically
# by the Fedora nsiswrapper program.  For more information see:
#
#   http://fedoraproject.org/wiki/MinGW
#
# To build an installer from the script you would normally do:
#
#   makensis this_script
#
# which will generate the output file '$outfile' which is a Windows
# installer containing your program.

Name "$name"
OutFile "$outfile"
InstallDir "$installdir"
InstallDirRegKey $installdirregkey "Install_Dir"

ShowInstDetails hide
ShowUninstDetails hide

# Uncomment this to enable BZip2 compression, which results in
# slightly smaller files but uses more memory at install time.
#SetCompressor bzip2

XPStyle on

Page components
Page directory
Page instfiles

ComponentText "Select which optional components you want to install."

DirText "Please select the installation folder."

Section "$name"
  SectionIn RO
EOT

    # Set the output files.
    my $olddir;
    foreach (sort keys %files) {
	if (!$olddir || $files{$_}->{install_dir} ne $olddir) {
	    # Moved into a new install directory.
	    my $dir = $files{$_}->{install_dir};
	    print $io "\n  SetOutPath \"\$INSTDIR\\$dir\"\n";
	    $olddir = $dir;
	}

	# If it's a directory, we copy it recursively, otherwise
	# just copy the single file.
	if ($files{$_}->{dir}) {
	    print $io "  File /r \"$_\"\n";
	} else {
	    print $io "  File \"$_\"\n";
	}
    }

    print $io <<EOT;
SectionEnd

Section "Start Menu Shortcuts"
  CreateDirectory "\$SMPROGRAMS\\$name"
  CreateShortCut "\$SMPROGRAMS\\$name\\Uninstall $name.lnk" "\$INSTDIR\\Uninstall $name.exe" "" "\$INSTDIR\\Uninstall $name.exe" 0
EOT

    # Start menu entries for each executable.
    foreach (sort keys %files) {
	if ($files{$_}->{exec}) {
	    my $install_dir = $files{$_}->{install_dir};
	    my $install_name = $files{$_}->{install_name};
	    print $io "  CreateShortCut \"\$SMPROGRAMS\\$name\\$install_name.lnk\" \"\$INSTDIR\\$install_dir\\$install_name\" \"\" \"\$INSTDIR\\$install_dir\\$install_name\" 0\n";
	}
    }

    print $io <<EOT;
SectionEnd

Section "Desktop Icons"
EOT

    # Desktop icons for each executable.
    foreach (sort keys %files) {
	if ($files{$_}->{exec}) {
	    my $install_dir = $files{$_}->{install_dir};
	    my $install_name = $files{$_}->{install_name};
	    print $io "  CreateShortCut \"\$DESKTOP\\$install_name.lnk\" \"\$INSTDIR\\$install_dir\\$install_name\" \"\" \"\$INSTDIR\\$install_dir\\$install_name\" 0\n";
	}
    }

    print $io <<EOT;
SectionEnd

Section "Uninstall"
EOT

    # Remove desktop icons and menu shortcuts.
    foreach (reverse sort keys %files) {
	if ($files{$_}->{exec}) {
	    my $install_name = $files{$_}->{install_name};
	    print $io "  Delete /rebootok \"\$DESKTOP\\$install_name.lnk\"\n";
	    print $io "  Delete /rebootok \"\$SMPROGRAMS\\$name\\$install_name.lnk\"\n";
	}
    }
    print $io "  Delete /rebootok \"\$SMPROGRAMS\\$name\\Uninstall $name.lnk\"\n\n";

    # Remove remaining files.
    $olddir = '';
    foreach (reverse sort keys %files) {
	if (!$olddir || $files{$_}->{install_dir} ne $olddir) {
	    # Moved into a new install directory, so delete the previous one.
	    print $io "  RMDir \"\$INSTDIR\\$olddir\"\n\n"
		if $olddir;
	    $olddir = $files{$_}->{install_dir};
	}

	# If it's a directory, we delete it recursively, otherwise
	# just delete the single file.
	my $install_dir = $files{$_}->{install_dir};
	my $install_name = $files{$_}->{install_name};
	if ($files{$_}->{dir}) {
	    print $io "  RMDir /r \"\$INSTDIR\\$install_dir\"\n\n";
	    $olddir = ''; # Don't double-delete directory.
	} else {
	    print $io "  Delete /rebootok \"\$INSTDIR\\$install_dir\\$install_name\"\n";
	}
    }

    print $io "  RMDir \"\$INSTDIR\\$olddir\"\n" if $olddir;

    print $io <<EOT;
  RMDir "\$INSTDIR"
SectionEnd

Section -post
  WriteUninstaller "\$INSTDIR\\Uninstall $name.exe"
SectionEnd
EOT

}

# Main program.

sub main
{
    get_options ();
    check_prereqs ();
    print_config () if $verbose;
    do_dependencies ();
    install_names ();
    print_files () if $verbose;
    write_script (\*STDOUT);
}

main ()
