@echo off
echo Start collecting memory logs
title Memory
:memory
adb -s D8YDU15A28004115 shell dumpsys meminfo com.android.settings | findstr TOTAL: > ./Result/06272357/D8YDU15A_memory.log
ping -n 30 127.0.0.1>nul
goto memory