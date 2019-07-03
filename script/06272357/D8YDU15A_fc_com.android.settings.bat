@echo off
echo Start collecting crash logs
title Crash
adb -s D8YDU15A28004115 logcat -s AndroidRuntime > ./Result/06272357/D8YDU15A_crash.log