NOW=$(date +"%m-%d-%Y %T")
sleepAmount=0.3
echo "Date: $NOW"
echo "Starting bach.py test script"
while true
do
	if python bach.py; then
		echo "Successfully made chords!"
	else
		echo "Failed to make chords."
	fi
	echo "Restarting in $sleepAmount seconds."
	sleep $sleepAmount
done