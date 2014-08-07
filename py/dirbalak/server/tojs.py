from realtimewebui.tojs import *
from realtimewebui import tojs
import time

_MAXIMUM_EVENTS_BACKLOG = 50


def appendEvent(eventListID, text):
    tojs.appendAndCycle(
        "events/%s" % eventListID, dict(time=time.time(), text=text), maximumSize=_MAXIMUM_EVENTS_BACKLOG)


def addToProjectsList(asDict):
    tojs.subsetDefault("projectsList", asDict['gitURL'], asDict)


def addToBuildHostsList(ipAddress):
    tojs.subset("buildHostsList", ipAddress, True)


def removeFromBuildHostsList(ipAddress):
    tojs.subunset("buildHostsList", ipAddress)
