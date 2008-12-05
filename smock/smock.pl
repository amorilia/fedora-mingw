#!/usr/bin/perl -w
#
# SMOCK - Simpler Mock
# by Dan Berrange and Richard W.M. Jones.
# Copyright (C) 2008 Red Hat Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

use strict;

use Getopt::Long;
use Pod::Usage;
use File::Temp qw(tempfile);

my @arches = ();
my @distros = ();
my $localrepo = $ENV{HOME} . "/public_html/smock/yum";
my $dryrun = 0;
my $chain = 0;
my $help = 0;
my $man = 0;

GetOptions (
    "arch=s" => \@arches,
    "distro=s" => \@distros,
    "localrepo=s" => \$localrepo,
    "dryrun" => \$dryrun,
    "chain" => \$chain,
    "help|?" => \$help,
    "man" => \$man
    ) or pod2usage (2);
pod2usage (1) if $help;
pod2usage (-exitstatus => 0, -verbose => 2) if $man;

=pod

=head1 NAME

 smock - Simpler mock

=head1 SYNOPSIS

 smock.pl --arch=i386 --arch=x86_64 --distro=fedora-10 list of SRPMs ...

=head1 DESCRIPTION

This is a wrapper around I<mock> which lets you build a whole group of
mutually dependent SRPMs in one go.

The smock command will work out the correct order in which to build
the SRPMs, and makes the result of previous RPM builds available as
dependencies for later builds.

Smock also works incrementally.  It won't rebuild RPMs which were
built already in a previous run, which means if a package fails to
build, you can just fix it and rerun the same smock command.  (In the
unlikely case that you want to force smock to rebuild RPMs then you
must bump the release number or delete the binary RPM from the
localrepo directory).

B<NOTE:> Please read the README file first.  You need to set up mock
and a web server before you can use this command.

=head1 OPTIONS

=over 4

=item B<--arch>

Specify the architecture(s) to build, eg. i386, x86_64.  You can
list this option several times to build several architectures.

=item B<--distro>

Specify the distribution(s) to build, eg. fedora-9, fedora-10.
You can list this option several times to build several distributions.

=item B<--localrepo>

Local repository.  Defaults to C<$HOME/public_html/smock/yum>

=item B<--dryrun>

Don't run any commands, just print the packages in the order
in which they must be built.

=item B<--chain>

Don't run any commands, just print the packages in the correct
format for chain building.  See:
L<http://fedoraproject.org/wiki/Koji/UsingKoji#Chained_builds>

=back

=cut

my @srpms = @ARGV;

if (0 == @arches) {
    die "smock: specify one or more architectures using --arch=<arch>\n"
}

if (0 == @distros) {
    die "smock: specify one or more distros using --distro=<distro>\n"
}

if (0 == @srpms) {
    die "smock: specify one or more SRPMs to build on the command line\n"
}

# Resolve the names, dependency list, etc. of the SRPMs that were
# specified.

sub get_one_line
{
    open PIPE, "$_[0] |" or die "$_[0]: $!";
    my $line = <PIPE>;
    chomp $line;
    close PIPE;
    return $line;
}

sub get_lines
{
    local $_;
    open PIPE, "$_[0] |" or die "$_[0]: $!";
    my @lines;
    foreach (<PIPE>) {
	chomp;
	push @lines, $_;
    }
    close PIPE;
    return @lines;
}

my %srpms = ();
foreach my $srpm (@srpms) {
    my $name = get_one_line "rpm -q --qf '%{name}' -p '$srpm'";
    my $version = get_one_line "rpm -q --qf '%{version}' -p '$srpm'";
    my $release = get_one_line "rpm -q --qf '%{release}' -p '$srpm'";

    my @buildrequires = get_lines "rpm -q --requires -p '$srpm' |
        grep -Eo '^[^[:space:]]+'";

    #print "Filename: $srpm\n";
    #print "  name          = $name\n";
    #print "  version       = $version\n";
    #print "  release       = $release\n";
    #print "  buildrequires = ", join (",", @buildrequires), "\n";

    $srpms{$name} = {
	name => $name,
	version => $version,
	release => $release,
	buildrequires => \@buildrequires,
	filename => $srpm
    }
}

# We don't care about buildrequires unless they refer to other
# packages that we are building.  So filter them on this condition.

sub is_member_of
{
    my $item = shift;

    foreach (@_) {
	return 1 if $item eq $_;
    }
    0;
}

sub dependency_in
{
    my $dep = shift;		# eg. dbus-devel

    while ($dep) {
	return $dep if is_member_of ($dep, @_);
	my $newdep = $dep;
	$newdep =~ s/-\w+$//;	# eg. dbus-devel -> dbus
	last if $newdep eq $dep;
	$dep = $newdep;
    }
    0;
}

my @names = sort keys %srpms;
foreach my $name (@names) {
    my @buildrequires = @{$srpms{$name}->{buildrequires}};
    @buildrequires = grep { $_ = dependency_in ($_, @names) } @buildrequires;
    $srpms{$name}{buildrequires} = \@buildrequires;
}

# Now sort the SRPMs into the correct order for building

my ($fh, $filename) = tempfile ();

foreach my $name (@names) {
    my @buildrequires = @{$srpms{$name}->{buildrequires}};
    foreach (@buildrequires) {
	print $fh "$_ $name\n"
    }
}
close $fh;

my @buildorder = get_lines "tsort $filename";

# With --chain flag we print the packages in groups for chain building.

if ($chain) {
    my %group = ();
    my $name;

    print 'make chain-build CHAIN="';

    foreach $name (@buildorder) {
	my @br = @{$srpms{$name}->{buildrequires}};

	# If a BR occurs within the current group, then start the next group.
	my $occurs = 0;
	foreach (@br) {
	    if (exists $group{$_}) {
		$occurs = 1;
		last;
	    }
	}

	if ($occurs) {
	    %group = ();
	    print ": ";
	}

	$group{$name} = 1;
	print "$name ";
    }
    print "\"\n";

    exit 0
}

# With --dryrun flag we just print the packages in build order then exit.

if ($dryrun) {
    foreach (@buildorder) {
	print "$_\n";
    }

    exit 0
}

# Now we can build each SRPM.

sub my_mkdir
{
    local $_ = $_[0];

    if (! -d $_) {
	mkdir ($_, 0755) or die "mkdir $_: $!"
    }
}

sub createrepo
{
    my $arch = shift;
    my $distro = shift;

    my_mkdir "$localrepo/$distro";
    my_mkdir "$localrepo/$distro/src";
    my_mkdir "$localrepo/$distro/src/SRPMS";
    system ("cd $localrepo/$distro/src && rm -rf repodata && createrepo -q .") == 0
	or die "createrepo failed: $?\n";

    my_mkdir "$localrepo/$distro/$arch";
    my_mkdir "$localrepo/$distro/$arch/RPMS";
    my_mkdir "$localrepo/$distro/$arch/logs";

    system ("cd $localrepo/$distro/$arch && rm -rf repodata && createrepo -q --exclude 'logs/*rpm' .") == 0
	or die "createrepo failed: $?\n";
}

if (! -d "$localrepo/scratch") {
    mkdir "$localrepo/scratch"
	or die "mkdir $localrepo/scratch: $!\nIf you haven't set up a local repository yet, you must read the README file.\n";
}

system "rm -f $localrepo/scratch/*";

# NB: Need to do the arch/distro in the outer loop to work
# around the caching bug in mock/yum.
foreach my $arch (@arches) {
    foreach my $distro (@distros) {
	foreach my $name (@buildorder) {
	    my $version = $srpms{$name}->{version};
	    my $release = $srpms{$name}->{release};
	    my $srpm_filename = $srpms{$name}->{filename};

	    $release =~ s/\.fc?\d+$//; # "1.fc9" -> "1"

	    # Does the built (binary) package exist already?
	    my $pattern = "$localrepo/$distro/$arch/RPMS/$name-$version-$release.*.rpm";
	    #print "pattern = $pattern\n";
	    my @binaries = glob $pattern;

	    if (@binaries == 0)
	    {
		# Rebuild the package.
		print "*** building $name-$version-$release $arch $distro ***\n";

		createrepo ($arch, $distro);
		system ("mock -r $distro-$arch --resultdir $localrepo/scratch $srpm_filename") == 0
		    or die "Build failed, return code $?\nLeaving the logs in $localrepo/scratch\n";

		# Build was a success so move the final RPMs into the
		# mock repo for next time.
		system ("mv $localrepo/scratch/*.src.rpm $localrepo/$distro/src/SRPMS") == 0 or die "mv";
		system ("mv $localrepo/scratch/*.rpm $localrepo/$distro/$arch/RPMS") == 0 or die "mv";
		my_mkdir "$localrepo/$distro/$arch/logs/$name-$version-$release";
		system ("mv $localrepo/scratch/*.log $localrepo/$distro/$arch/logs/$name-$version-$release/") == 0 or die "mv";

		createrepo ($arch, $distro);
	    }
	    else
	    {
		print "skipping $name-$version-$release $arch $distro\n";
	    }
	}
    }
}
