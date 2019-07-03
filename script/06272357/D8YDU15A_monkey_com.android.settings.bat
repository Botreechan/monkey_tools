@echo off
echo start  monkey test
title Monkey
adb -s D8YDU15A28004115 shell monkey -s 190627 -p com.android.settings --throttle 300 --ignore-crashes --ignore-native-crashes --ignore-security-exceptions --ignore-timeouts --monitor-native-crashes -v -v -v 500000 > ./Result/06272357/D8YDU15A_monkey.log