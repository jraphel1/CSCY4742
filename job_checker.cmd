@echo off
set JOB_ID=ftjob-5IUApOOiHS6nxTPZxeYUQBx1
:loop
echo Checking job status for %JOB_ID%...
openai api fine_tunes.follow -i %JOB_ID%
timeout /t 30 >nul
goto loop