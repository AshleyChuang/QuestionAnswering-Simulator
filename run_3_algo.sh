for i in $(seq 0 1 2)
do
	echo $i
	for j in $(seq 1 5)
		do
			echo $j
			java Main $i 2 $j 1 4 &
		done
done
