#!/usr/bin/python
from time import sleep

from flash.retrieve import run as flashRetrieve
from flash.deploy import run as flashDeploy
from uploads.deploy import run as uploadsDeploy
from wifi.deploy import run as wifiDeploy
from main.deploy import run as mainDeploy

def runFlash():

    print("Checking Micropython image retrieved")
    flashRetrieve()

    print("Deploying Micropython image")
    flashDeploy()

    sleep(10) # give board and serial connection time to reset


def runInstall():

    print("Deploying Scripts")
    uploadsDeploy()

    print("Configuring Default Wifi Access Point")
    wifiDeploy()

    print("Deploying App")
    mainDeploy()

def run():
    runFlash()
    runInstall()
    print('All features deployed. Now unplug and replug board to ensure it resets \a\a\a')


if __name__ == "__main__":
    run()
