#!/bin/bash

# retrieve adb logs with level WARNING and above

LOGFILEPATH=$1
PROCESSID=$2

PATH="$HOME/local/bin:$HOME/Android/Sdk/tools:$HOME/Android/Sdk/build-tools/23.0.1:$HOME/Android/Sdk/platform-tools:$PATH"
ANDROID_HOME="$HOME/Android/Sdk"
JAVA_HOME="/usr/lib/jvm/java-8-oracle"

if [ "$PROCESSID" = "-1" ]
then
    adb logcat -d *:W > $LOGFILEPATH
else
    adb logcat -d *:W | grep $PROCESSID > $LOGFILEPATH
fi


