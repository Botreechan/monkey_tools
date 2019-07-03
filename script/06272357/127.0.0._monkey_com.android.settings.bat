@echo off
echo start  monkey test
title Monkey
adb -s 127.0.0.1:7555 shell monkey -s 190627 -p com.android.settings --throttle 300 --ignore-crashes --ignore-native-crashes --ignore-security-exceptions --ignore-timeouts --monitor-native-crashes -v -v -v 500000 > ./Result/06272357/127.0.0._monkey.log