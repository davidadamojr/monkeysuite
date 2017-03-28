#!/bin/bash

# get process for package name

PACKAGENAME=$1

PATH="$HOME/local/bin:$HOME/Android/Sdk/tools:$HOME/Android/Sdk/build-tools/23.0.1:$HOME/Android/Sdk/platform-tools:$PATH"
ANDROID_HOME="$HOME/Android/Sdk"
JAVA_HOME="/usr/lib/jvm/java-8-oracle"

adb shell pidof -s $PACKAGENAME


