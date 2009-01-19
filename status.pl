#!/usr/bin/perl -wT

# Produce a status page for all current and pending Fedora MinGW packages.
# By Richard W.M. Jones <rjones@redhat.com>
#
# Requires:
# . All Fedora MinGW packages have to be checked out
#   under $HOME/d/fedora.
# . All pending packages to be available in
#   $HOME/d/fedora-mingw--devel.
#
# The output is normally placed here:
# http://annexia.org/fedora_mingw
#
# Checks that the package build-requires mingw32-* in order to know if
# it's an MinGW-related package.
#
# Only recognizes the Fedora/EPEL branches listed below and ignores
# anything else.  There are no MinGW packages in RHEL at this time.
#
# XXX This script is a bit crap.  Instead of using lame specfile
# parsing, this should be generated from the SRPMs.

use strict;

use POSIX qw(strftime);
use CGI qw/:standard/;

my $home = $ENV{HOME};
if ($home =~ m/(.*)/) { $home = $1; }

my $fedora = $home . "/d/fedora";
my $pending = $home . "/d/fedora-mingw--devel";

chdir $pending or die "$pending: $!\n";

my %branches = (
    "EL-5" => {
	name => "EPEL 5",
	url => "http://fedoraproject.org/wiki/EPEL",
	title => "Packages for Red Hat Enterprise Linux 5",
	sortorder => 2,
	class => "epelbg",
    },
    "F-10" => {
	name => "Fedora 10",
	url => "http://fedoraproject.org/",
	sortorder => 10,
	class => "fedorabg",
    },
    "devel" => {
	name => "Devel",
	url => "http://fedoraproject.org/wiki/Releases/Rawhide",
	title => "Fedora 11 in development a.k.a. Rawhide",
	sortorder => 99,
	class => "develbg",
    },
    "pending" => {
	name => "Pending",
	url => "https://bugzilla.redhat.com/buglist.cgi?version=rawhide&component=Package+Review&target_milestone=&bug_status=NEW&bug_status=ASSIGNED&bug_status=NEEDINFO&bug_status=MODIFIED&short_desc_type=allwordssubstr&short_desc=mingw32&long_desc_type=allwordssubstr&long_desc=",
	sortorder => 100,
	class => "pendingbg",
    },
);

# List of packages to ignore in pending.
my %ignore_pending = ();
open IGNORE, "IGNORE" or die "IGNORE: $!\n";
while (<IGNORE>) {
    next if /^\#/ || /^$/;
    m/(.*)/; # untaint
    $ignore_pending{"mingw32-$1"} = 1;
}
close IGNORE;

# List of packages to ignore in Fedora checkout,
# because they confuse this script.
my %ignore_fedora = (
    "cyrus-sasl" => 1,
    "kernel" => 1,
    "msmtp" => 1,
    "openldap" => 1,
    "pixman" => 1,
    "python" => 1,
    "xenwatch" => 1,
);

# List of packages.
my %packages;

# Count of packages by branch.
my %count;

# Collect the package names & status from the specfiles.
sub collect {
    my $specfile;

    # Fedora and EPEL packages.
    foreach $specfile (<$fedora/*/*/*.spec>) {
	if ($specfile =~ m{/([^/]+)/([^/]+)\.spec$}) {
	    my $specfile_name = $2;
	    my $branch = $1;
	    if (exists $branches{$branch} &&
		!exists $ignore_fedora{$specfile_name}) {
		collect_specfile ($specfile, $branch);
	    }
	}
    }

    # Pending packages in review.
    foreach $specfile (<$pending/*/*.spec>) {
	collect_specfile ($specfile, "pending");
    }
}

sub collect_specfile {
    my $specfile = shift;
    my $branch = shift;

    # Read the specfile and parse the bits we understand.
    my ($name, $version, $summary, $description, $url, $is_mingw,
	@rpmdefines);
    @rpmdefines = (["nil", ""]);

    open SPEC, "$specfile" or die "$specfile: $!";
    while (<SPEC>) {
	if (/^Name:\s*(\S+)/) {
	    $name = $1;
	    $name = rpmsubst ($name, 1, @rpmdefines) if $name =~ /%{/;
	    $is_mingw = 1 if $name =~ /mingw32/;
	} elsif (/^Version:\s*(\S+)/) {
	    $version = $1;
	    $version = rpmsubst ($version, 1, @rpmdefines) if $version =~ /%{/;
	} elsif (!$url && /^URL:\s*(\S+)/) {
	    $url = $1;
	    $url = rpmsubst ($url, 1, @rpmdefines) if $url =~ /%{/;
	} elsif (!$summary && /^Summary:\s*(.*)/) {
	    $summary = $1;
	    #$is_mingw = 1 if $summary =~ /mingw32/i;
	} elsif (/^(Build)?Requires:.*mingw32/) {
	    $is_mingw = 1
	} elsif (!$description && /^%description/) {
	    $description = "";
	    while (<SPEC>) {
		last if /^%/;
		$description .= $_;
	    }
	    $description = rpmsubst ($description, 1, @rpmdefines)
		if $description =~ /%{/;
	    #$is_mingw = 1 if $description =~ /mingw/i;
        }

	# Handle simple RPM defines.
        elsif (/^%define\s+([A-Za-z_]+)\s+(.*)/) {
	    my $name = $1;
	    my $val = $2;
	    if (only_simple_substs ($val)) {
		$val = rpmsubst ($val, 0, @rpmdefines);
		push @rpmdefines, [ $name, $val ];
	    }
	}
    }

    # Check it's a MinGW package.  If name/summary/description contains
    # 'mingw' or it Requires/BuildRequires some mingw32-* package then we
    # assume it's related.
    if (!$is_mingw) {
	warn "warning: $name ($branch) ignored, not a MinGW package\n";
	return;
    }

    # Ignore certain packages appearing in pending branch.
    if ($branch eq "pending") {
	if (exists $ignore_pending{$name}) {
	    return;
	}

	# Also ignore packages marked NOT-FOR-FEDORA in pending.
	my $dirname = $specfile;
	$dirname =~ s{/[^/]+$}{};
	if (-f "$dirname/NOT-FOR-FEDORA") {
	    return;
	}
    }

    #print "$name $version $url\n";

    # If the package is in "pending" then there shouldn't be a
    # Fedora package also.
    if ($branch eq "pending" && exists $packages{$name}) {
	die "error: pending $name is also in Fedora repo\n"
    }

    # Add the package.
    $packages{$name} = {} unless exists $packages{$name};
    if (exists $packages{$name}{$branch}) {
	die "$name ($branch) package already seen\n";
    }
    $packages{$name}{$branch} = {
	name => $name,
	branch => $branch,
	version => $version,
	url => $url,
	summary => $summary,
	description => $description,
    }
}

sub only_simple_substs {
    local $_ = shift;

    s/%{[A-Za-z_]+}//g;
    s/%\([A-Za-z_]+\)//g;
    ! (m/%{/ || m/%\(/)
}

# Simple RPM '%define' substitutions.
sub rpmsubst {
    local $_ = shift;
    my $fail = shift;

    my $pair;
    foreach $pair (@_) {
	my $var = $pair->[0];
	my $val = $pair->[1];

	s/%{$var}/$val/ge;
	s/%\($var\)/$val/ge;
    }

    if ($fail && (m/%{/ || m/%\(/)) {
	die "rpmsubst: string contains undefined substitutions: $_\n";
    }

    $_;
}

sub branchsortorder {
    $branches{$a}{sortorder} <=> $branches{$b}{sortorder}
}

sub nbsp {
    local $_ = shift;
    s/\s+/&nbsp;/g;
    $_
}

sub output_header {
    print "Status of packages in Fedora, EPEL and RHEL, last updated on ";
    print strftime("%Y-%m-%d",gmtime);
    print ".\n\n";
    print "<html>\n";
    print "<table class=\"top_table fedoratbl\">\n";
    print "<tr><th>Name</th>\n";
    foreach (sort branchsortorder (keys %branches)) {
	my $name = $branches{$_}{name};
	my $url = $branches{$_}{url};
	my $class = $branches{$_}{class};

	print "<th class=\"$class\">";
	if (exists $branches{$_}{title}) {
	    my $title = escapeHTML ($branches{$_}{title});
	    print "<a title=\"$title\" href=\"$url\">",
	      nbsp(escapeHTML($name)),
	      "</a>";
	} else {
	    print "<a href=\"$url\">",
	      nbsp(escapeHTML($name)),
	      "</a>";
	}
	print "</th>\n";
    }
    print "</tr>\n";

    # Count the packages in each branch.
    %count = ();
    foreach (keys %branches) {
	$count{$_} = 0
    }
}

sub output_package {
    my $name = shift;

    # Get the URL, summary and description from devel
    # or pending (if possible).
    my ($url, $summary, $description);
    if (exists $packages{$name}{devel}) {
	$url = $packages{$name}{devel}{url};
	$summary = $packages{$name}{devel}{summary};
	$description = $packages{$name}{devel}{description};
    } elsif (exists $packages{$name}{pending}) {
	$url = $packages{$name}{pending}{url};
	$summary = $packages{$name}{pending}{summary};
	$description = $packages{$name}{pending}{description};
    }

    print "<tr><td>";
    if (defined $url) {
	if (defined $summary && defined $description) {
	    print "<a title=\"",
	      escapeHTML($description),
	      "\" href=\"$url\">",
	      escapeHTML($name),
	      "</a><br/><small>",
	      escapeHTML($summary),
	      "</small>";
	} else {
	    print "<a href=\"$url\">", escapeHTML($name), "</a>";
	}
    } else {
	print (escapeHTML($name));
    }
    print "</td>\n";

    my $branch;
    foreach $branch (sort branchsortorder (keys %branches)) {
	my $brclass = $branches{$branch}{class};

	if (exists $packages{$name}{$branch}) {
	    $count{$branch}++;

	    my %r = %{$packages{$name}{$branch}};

	    my $class = "released";
	    $class = "pending" if $branch eq "pending";
	    $class = "devel" if $branch eq "devel";
	    $class = "filesystem" if $name eq "mingw32-filesystem";

	    print "<td class=\"$brclass $class\">$r{version}</td>\n";
	} else {
	    # No package in this branch.
	    print "<td class=\"$brclass\">&nbsp;</td>\n"
	}
    }

    print "</tr>\n";
}

sub output_trailer {
    # Summary of packages in each branch.
    print "<tr><td>Totals</td>";
    my $branch;
    foreach $branch (sort branchsortorder (keys %branches)) {
	print "<td>$count{$branch}</td>";
    }
    print "</tr>\n";

    print "</table>\n";
    print "</html>\n";
}

# Define a standard package name order.
sub pkgnameorder {
    # "mingw32-*" packages always sort first.
    return -1 if $a =~ /^mingw32/ && $b !~ /^mingw32/;
    return 1 if $a !~ /^mingw32/ && $b =~ /^mingw32/;

    return (lc($a) cmp lc($b))
}

sub main {
    # Collect all the specfiles, into %packages hash.
    collect ();

    # Get the package names.
    my @names = sort pkgnameorder (keys %packages);

    # Generate the output.
    output_header ();
    foreach (@names) {
	output_package ($_);
    }
    output_trailer ();
}

main ()
