@ECHO OFF

SET NOW=%date:~3,2%%date:~0,16% %TIME%
:: delay in milliseconds
SET sleepAmount=300 
ECHO "Date: %NOW%"
ECHO "Starting bach.py test script"
:WHILE
	python bach.py
	IF %errorlevel% NEQ 1 GOTO SUCCESS
	ECHO "Failed to make chords."
	GOTO ENDIF
	:SUCCESS
	ECHO "Successfully made chords!"
	:ENDIF
	ECHO "Restarting in %sleepAmount% milliseconds."
	:: delay for sleepAmount milliseconds
	ping 127.0.0.1 -n 1 -w %sleepAmount% > nul 
GOTO WHILE