@echo off
echo off

@REM %1 = exe_path
@REM %2 = project_path
@REM %3 = bin_name

@REM _01_3L6_build_.bat
%1 %3 p %2 -q
rem _02_3L6_build_push_bin.bat
adb push %3 vendor/lib64/camera
rem _03_build_reboot camera server.bat
adb shell stop media
adb shell "ps | grep cameraserver"
@for /f "tokens=2" %%i in ('adb shell "ps | grep cameraserver"') do adb shell kill -9 %%i
adb shell "ps | grep mm-qcamera-daemon"
@for /f "tokens=2" %%i in ('adb shell "ps | grep mm-qcamera-daemon"') do adb shell kill -9 %%i
adb shell start media
adb shell "ps | grep cameraserver"
adb shell "ps | grep mm-qcamera-daemon"
adb shell "pkill -f camera"
