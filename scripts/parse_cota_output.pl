#!/usr/bin/env perl


my @components;
my $n_ucs = 1;
my @loadings;

# state values: 
# 0 - initialization
# 1 - running
# 2 - completed
my $job_state = 0; 

# end flag
# 0 - before final loadings
# 1 - after final loadings
my $endflag = 0;

# read flag
# 0 - average abs. loading for component i has NOT been read
# 1 - average abs. loading for component i HAS been read
my $read = 0;

while (<STDIN>) {
    if (/External temperature: +(\d+\.\d+)/) 
    {
        $temperature = sprintf("%.2f", $1);
    }
    
    elsif (/External Pressure: +(\d+\.\d+)/)
    {
        $pressure = sprintf("%.5e", $1);
    }
    
    elsif (/Component +(\d+) +\[(\S+)\] \((Adsorbate|Cation)/) 
    {
        $current_comp = $1;
        push @components, {"name" => $2, "type" => $3, "parfug" => 0.0, "molfrac" => 0.0, "compress" => 1.0, "mass" => 0.0};
    }
    
    elsif (/MolFraction: +(\d+\.\d+)/)
    {
        $components[$current_comp]{"molfrac"} = sprintf("%.5f", $1);
    }

    elsif (/Compressibility: +(\d+\.\d+)/)
    {
        $components[$current_comp]{"compress"} = sprintf("%.5f", $1);
    }

    elsif (/Partial fugacity: +(\d+\.\d+)/)
    {
        $components[$current_comp]{"parfug"} = sprintf("%.5e", $1);
    }
    
    elsif (/Mass: +(\d+\.\d+) +\[a\.u\.\]/) 
    {
        $components[$current_comp]{"mass"} = $1;
    }
    
    elsif (/Framework name: +(\S+)/)
    {
        $fwk_name = $1;
    }
    
    elsif (/Framework Mass: +(\d+\.\d+)/) 
    {
        $fwk_mass = $1;
    }
 
    elsif (/Number of unitcells \[[abc]\]: +(\d+)/)
    {
        $n_ucs *= $1;
    }    

    elsif (/Component +(\d+) +: +(\d+) molecules/) 
    {
        if ( $components[$1]{"type"} == "Cation" )
        {
            $fwk_mass += ($components[$1]{"mass"} * $2)/$n_ucs;
        }
    }
    
    elsif (/Starting simulation/)
    {
        $job_state = 1;
    }

    elsif (/Finishing simulation/)
    {
        $job_state = 2;
    }

    elsif (/Number of molecules:/ && $job_state == 2)
    {
        $endflag = 1;
    }

    elsif (/Component +(\d+) +\[.*\]/ && $endflag == 1)
    {
        $current_comp = $1;
        push @loadings, {"avg" => 0.0, "err" => 0.0};
        $read = 0;
    } 

    elsif (/Average +(\d+\.\d+) +\+\/\- +(\d+\.\d+)/ && $endflag == 1 && $read == 0) 
    {
        $loadings[$current_comp]{"avg"} = sprintf("%.5e", $1);
        $loadings[$current_comp]{"err"} = sprintf("%.5e", $2);
        $read = 1;
    }
}

my $loading_to_kg = 1000/$fwk_mass;

if ($job_state == 0) 
{
    print "init only!\n";
}

elsif ($job_state == 1 || $job_state == 2)
{
    for ($i=0; $i<=$#components; $i++)
    {
        $c = $components[$i];
        open FILE, ">>$fwk_name\-$temperature\_K\-$c->{name}-$c->{type}.csv" or die $!;

        if ($job_state == 2)
        {
            $uc = sprintf("%.5e", $loadings[$i]->{"avg"}/$n_ucs);
            $uce = sprintf("%.5e", $loadings[$i]->{"err"}/$n_ucs);
            $kg = sprintf("%.5e", $loading_to_kg*($loadings[$i]->{"avg"}));
            $kge = sprintf("%.5e", $loading_to_kg*($loadings[$i]->{"err"}));
            print FILE "$pressure,$c->{molfrac},$c->{compress},$c->{parfug},$uc,$uce,$kg,$kge\n";
        }

        else 
        {
            print FILE "$pressure,$c->{molfrac},$c->{compress},$c->{parfug},incomplete\n";
        }
            
        close FILE;
    }
}

