#!/usr/bin/env zsh

directories=($@)

# setup a pipe to hold the file paths
pathfifo=`mktemp -u -t paths`
mkfifo $pathfifo

# setup a pipe to hold the results
tablefifo=`mktemp -u -t table`
mkfifo $tablefifo

# setup pipe to hold file being parse
outfifo=`mktemp -u -t outfile`
mkfifo $outfifo


# parse each file in turn
while read path; do
    ext = ${path:e}
    if [[ "$ext" == "data" ]]; then
      cat $path >&$outfile
    elif [[ "$ext" == "gz" ]]; then
      gunzip -c $path >&$outfile
    else
      continue
    fi
    fwk=$(awk '/Framework name:/ {print $3}' <&$outfile)
    T=$(awk '/External temperature/ {printf "%.2f", $3}' <&$outfile)
    # using perl for awk portability concerns
    mol=$(perl -n -e '/Component 0 +\[(\w+)\] +\(Adsorbate/ && print $1' <&$outfile)
    W=($(awk '/\['"$mol"'\] Average Widom/ {printf "%.4e %.4e",$4,$6}' <&$outfile))
    KH=($(awk '/\['"$mol"'\] Average Henry/ {printf "%.4e %.4e",$5,$7}' <&$outfile))
    RT=$((0.0083145*$T))
    dH=($(awk '/\['"$mol"'\] Average +<U_/ {printf "%.3f %.2e\n",($9-'"$RT"'),$11}' <&$outfile))
    echo "$fwk $T $mol ${W[@]} ${KH[@]} ${dH[@]}" 
done <$pathfifo >$tablefifo

exec {paths}<> $pathfifo
exec {table}<> $tablefifo
exec {outfile}<> $outfifo

# find paths to files to parse
for dir in $directories; do
  find "$dir" -name "*.data" -or -name "output.0.log.gz" >>&$paths
done

#<(echo "material T molecule <W> <W>_err KH KH_err delta_H delta_H_err" \
#            echo "- K - - - mol/(kg*Pa) mol/(kg*Pa) kJ/mol kJ/mol")

# Print a formatted table to stdout
column -t  <&$table

#unhook the file descriptors
exec {paths}<>&-
exec {table}<>&-

# destroy the pipes
rm $pathfifo $pathfifo $pathfifo

exit 0

