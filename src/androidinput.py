import glob
import os
import subprocess
import time

from src import config


# todo: to add check if few devices is connected, but chosen none

# Choose device
def chooseDevice():
    proc = subprocess.Popen(config.adb + 'devices -l', stdout=subprocess.PIPE, shell=True)
    # todo: parse output to provide change interface like '1: devId devName'
    deviceList = str.split(proc.stdout.read().decode("utf-8"), '\r\n')[1:-2]
    i = 0
    deviceIds = []
    for line in deviceList:   # printing device list
        print(str(i) + ': ' + line)
        deviceIds.append(line.split()[0])  # creating device ids list
        i += 1
    dev = input("Type device:")
    # If device is not selected, using adb without any parameters
    if dev == "":
        config.device = ""
        config.adb = "adb "
        print("using any device")
    # Else sending device id using parameter -s
    else:
        config.device = deviceIds[int(dev)]
        config.adb = "adb -s " + config.device + " "
        print("using device " + config.device)
    return


def apkList(num):
    # Sorting all apks in app dir from newest
    apks = sorted(glob.iglob(config.appDir + '*.apk'), key=os.path.getctime, reverse=True)
    # List of apks with creation time
    for i in range(num):
        print(str(i) + ": " + apks[i] + " : " + time.ctime(os.path.getctime(apks[i])))
    chooseApk = input("Which apk to install: ")
    return apks[int(chooseApk)]


def appInstall():
    # appPath = input ("Input app path:")
    # Looking for all *.apk files, sorting by time and choosing the latest
    appApk = max(glob.iglob(config.appDir + '*.apk'), key=os.path.getctime)
    print("The latest apk is " + appApk)
    print("Apk created: %s" % time.ctime(os.path.getctime(appApk)))  # apk creation time
    print("\n Installing...")
    proc = subprocess.Popen(config.adb + 'install ' + appApk, stdout=subprocess.PIPE, shell=True)
    print(proc.stdout.read().decode("utf-8"))
    # print ("Done at " + time.strftime("%H:%M:%S"))
    return


def appInstallChoosed():
    appApk = apkList(config.appHistory)
    print("Installing apk " + appApk)
    print("Apk created: %s" % time.ctime(os.path.getctime(appApk)))  # apk creation time
    print("\n Installing...")
    proc = subprocess.Popen(config.adb + 'install ' + appApk, stdout=subprocess.PIPE, shell=True)
    print(proc.stdout.read().decode("utf-8"))
    # print ("Done at " + time.strftime("%H:%M:%S"))
    return


def devUnlock(pin):
    """Unlock device by pin"""
    proc = subprocess.Popen(config.adb + 'shell input keyevent KEYCODE_POWER', stdout=subprocess.PIPE, shell=True)
    time.sleep(1)
    proc = subprocess.Popen(config.adb + 'shell input text "' + pin + '"', stdout=subprocess.PIPE, shell=True)
    time.sleep(1)
    proc = subprocess.Popen(config.adb + 'shell input keyevent KEYCODE_ENTER', stdout=subprocess.PIPE, shell=True)
    return


def takeScreenshot():
    # Output file
    outFile = config.scrDir + time.strftime("%Y-%m-%d-%H-%M-%S") + '.png'
    # Taking screenshot
    proc = subprocess.Popen(config.adb + 'shell screencap -p /sdcard/screen.png', stdout=subprocess.PIPE, shell=True)
    print(proc.stdout.read().decode("utf-8"))
    # Pulling screenshot from device
    proc = subprocess.Popen(config.adb + 'pull /sdcard/screen.png ' + outFile, stdout=subprocess.PIPE, shell=True)
    print(proc.stdout.read().decode("utf-8"))
    # Removing screenshot file from device
    oc = subprocess.Popen(config.adb + 'shell rm /sdcard/screen.png', stdout=subprocess.PIPE, shell=True)
    print('Saved: ' + outFile)
    # print ("Done at " + time.strftime("%H:%M:%S"))
    return


def takeVideo():
    # Output file
    outFile = config.scrDir + time.strftime("%Y-%m-%d-%H-%M-%S") + '.mp4'
    # begin to capture
    print('Capturing... Press Ctrl+C to stop')
    # open new window to capture
    with subprocess.Popen(config.adb + 'shell screenrecord --verbose /sdcard/video.mp4',
                          stdout=subprocess.PIPE) as proc:
        proc.wait(60 * 3)
        time.sleep(3)  # wait 3 sec to write file header
    # wait for signal to stop capturing
    print('Capturing done')
    # Pulling video from device
    with subprocess.Popen(config.adb + 'pull /sdcard/video.mp4 ' + outFile,
                          stdout=subprocess.PIPE, shell=True) as proc:
        proc.wait(30)
    # Removing video file from device
    proc = subprocess.Popen(config.adb + 'shell rm /sdcard/video.mp4', stdout=subprocess.PIPE, shell=True)
    print('Saved: ' + outFile)


def help():
    print('H - help, U - uninstall, I - install, IC - choose apk to install, ' +
          'C - clear, N - uNlock, CD - change device, D - current device, ' +
          'S - screenshot, V - video capture, E - to exit \n')
    return


def curDev():
    if config.adb == "adb ":
        print("Device is not selected")
    else:
        print("Current device is " + config.device)
    return


def clearData():
    confirm = input("Really clear? Y/N: ")
    if confirm == "Y" or confirm == "y":
        proc = subprocess.Popen(config.adb + 'shell pm clear ' + config.app, stdout=subprocess.PIPE, shell=True)
        print(proc.stdout.read().decode("utf-8"))
        # print ("Done at " + time.strftime("%H:%M:%S"))
    return


def uninstallApp():
    confirm = input("Really uninstall? Y/N: ")
    if confirm == "Y" or confirm == "y":
        proc = subprocess.Popen(config.adb + 'uninstall ' + config.app, stdout=subprocess.PIPE, shell=True)
        print(proc.stdout.read().decode("utf-8"))
        # print ("Done at " + time.strftime("%H:%M:%S"))
    return


# Run program
if __name__ == "__main__":
    help()

    # Choosing device
    chooseDevice()

    # Main loop
    while True:
        # text = input("::")
        # use devName instead id
        text = input(":" + config.device + "::")
        if text == "":
            continue
        elif text == "E":
            break
        elif text == "H":
            help()
        elif text == "U":
            uninstallApp()
        elif text == "I":
            appInstall()
        elif text == "IC":
            appInstallChoosed()
        elif text == "N":
            devUnlock('1111')
        elif text == "CD":
            chooseDevice()
        elif text == "C":
            clearData()
        elif text == "D":
            curDev()
        elif text == "S":
            takeScreenshot()
        elif text == "V":
            takeVideo()
        else:
            text = text.replace(' ', '%s')
            # print (text)
            proc = subprocess.Popen(config.adb + 'shell input text "' + text + '"', shell=True)
