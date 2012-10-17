#!/usr/bin/env perl

my @lengths;
my @angles;
my @atoms;

while (<>) {
    
    if (/data_(\w+)/) {
        $name = $1;
    }
    elsif (/_cell_length_([abc]) (\d+\.\d+)/) {
        $lengths{$1} = $2;
    }
    elsif (/_cell_angle_([abg])\w+ (\d+\.\d+)/) {
        $angles{$1} = $2;
    }
    elsif (/_symmetry_group_IT_number (\d+)/) {
        $spacegrp = $1;
    }
    elsif (/^(\w+) \w+\d* (\d+\.\d+) (\d+\.\d+) (\d+\.\d+)/) {
        push @atoms, "$1 $2 $3 $4";
    }
}

printf "%38.6f %.6f %.6f\n", $lengths{"a"}, $lengths{"b"}, $lengths{"c"};
printf "%28.6f %.6f %.6f  SPGR = %d  OPT = 1\n", $angles{"a"}, $angles{"b"}, $angles{"g"}, $spacegrp;
printf " %d   0\n", ($#atoms + 1);
printf "     0 %-12s      : %s\n", $name, $name;
foreach my $i (0..$#atoms) {
    printf "%4d %s  0   0   0   0   0   0   0   0   0.000\n", ($i+1), $atoms[$i];
}
