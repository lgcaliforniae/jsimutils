#!/usr/bin/env zsh

directories=($@)

(echo "material T molecule <W> <W>_err KH KH_err delta_H delta_H_err"
echo "- K - - - mol/(kg*Pa) mol/(kg*Pa) kJ/mol kJ/mol"

for dir in ${directories[@]}; do
  for f in `find "$dir" -name "*.data" -or -name "output.0.log.gz"`; do
    if [[ ${f:e} == "gz" ]]; then
      gunzip -c $f > tmp
      f=tmp
    fi
    fwk=$(awk '/Framework name:/ {print $3}' $f)
    T=$(awk '/External temperature/ {printf "%.2f", $3}' $f)
    # using perl for awk portability concerns
    mol=$(perl -n -e '/Component 0 +\[(\w+)\] +\(Adsorbate/ && print $1' < $f)
    W=($(awk '/\['"$mol"'\] Average Widom/ {printf "%.4e %.4e",$4,$6}' $f))
    KH=($(awk '/\['"$mol"'\] Average Henry/ {printf "%.4e %.4e",$5,$7}' $f))
    RT=$((0.0083145*$T))
    dH=($(awk '/\['"$mol"'\] Average +<U_/ {printf "%.3f %.2e\n",($9-'"$RT"'),$11}' $f))
    echo "$fwk $T $mol ${W[@]} ${KH[@]} ${dH[@]}"
  done
done )| column -t

exit 0

