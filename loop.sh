while true;
do
	python ping.py
	ret=$?
	if [ $ret -eq 0 ]; then
		break
	fi
	sleep 10s
done