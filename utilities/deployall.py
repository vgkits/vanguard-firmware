#!/usr/bin/python
from time import sleep

from flash.retrieve import run as flashRetrieve
from flash.deploy import run as flashDeploy
from imports.deploy import run as importsDeploy
from replserver.deploy import run as replserverDeploy
from main.deploy import run as mainDeploy

def runFlash():

    print("Checking Micropython image retrieved")
    flashRetrieve()

    print("Deploying Micropython image")
    flashDeploy()

    sleep(4) # give board and serial connection time to reset


def runInstall():

    print("Deploying Modules")
    importsDeploy()

    print("Deploying REPLServer")
    replserverDeploy()

    print("Deploying App")
    mainDeploy()

def run():
    runFlash()
    runInstall()
    print('All modules, replserver boot and application main files deployed. Now unplug the cockle to ensure it resets \a\a\a')


if __name__ == "__main__":
    run()
