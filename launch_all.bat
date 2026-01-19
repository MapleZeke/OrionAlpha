@echo off
title OrionAlpha - Unified Server
set CLASSPATH=.;target\OrionAlpha.jar
java -Xmx1200m -Dwzpath=data/ launcher.OrionLauncher --worlds=1
pause
