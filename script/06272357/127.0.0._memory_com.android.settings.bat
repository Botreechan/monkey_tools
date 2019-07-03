@echo off
echo Start collecting memory logs
title Memory
:memory
adb -s 127.0.0.1:7555 shell dumpsys meminfo com.android.settings | findstr TOTAL: > ./Result/06272357/127.0.0._memory.log
ping -n 30 127.0.0.1>nul
goto memory