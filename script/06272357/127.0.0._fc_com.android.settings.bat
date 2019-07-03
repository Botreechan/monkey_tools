@echo off
echo Start collecting crash logs
title Crash
adb -s 127.0.0.1:7555 logcat -s AndroidRuntime > ./Result/06272357/127.0.0._crash.log