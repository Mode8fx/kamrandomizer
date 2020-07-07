#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 5.4
#  in conjunction with Tcl version 8.6
#    Jul 06, 2020 08:24:00 PM EDT  platform: Windows NT

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def set_Tk_var():
    global sourceRom
    sourceRom = tk.StringVar()
    global abilityDistributionType
    abilityDistributionType = tk.StringVar()
    global basicEnemyBehaviorType
    basicEnemyBehaviorType = tk.StringVar()
    global noneAbilityChanceEnemy
    noneAbilityChanceEnemy = tk.StringVar()
    global includeMiniBosses
    includeMiniBosses = tk.StringVar()
    global includeMinnyAndWheelie
    includeMinnyAndWheelie = tk.StringVar()
    global objectRandomizationType
    objectRandomizationType = tk.StringVar()
    global noneAbilityChanceObject
    noneAbilityChanceObject = tk.StringVar()
    global numSeeds
    numSeeds = tk.StringVar()
    global useSeed
    useSeed = tk.StringVar()
    global seedInput
    seedInput = tk.StringVar()
    global generateAbilityLog
    generateAbilityLog = tk.StringVar()
    global message
    message = tk.StringVar()
    message.set('')
    initVars()

def initVars():
    abilityDistributionType.set("Pure Random")
    basicEnemyBehaviorType.set("All Random")
    noneAbilityChanceEnemy.set("90")
    includeMiniBosses.set("1")
    includeMinnyAndWheelie.set("1")
    objectRandomizationType.set("Yes")
    noneAbilityChanceObject.set("90")
    numSeeds.set("1")
    useSeed.set("2")
    generateAbilityLog.set("1")

def setSourceRom():
    global sourceRom
    sourceRom.set(tk.filedialog.askopenfilename(filetypes=[("GBA ROM files", "*.gba")]))
    sys.stdout.flush()

def keepUpperCharsSeed(unused):
    global seedInput
    seedInput.set(''.join(ch.upper() for ch in seedInput.get() if ch.isalpha() or ch.isdigit()))
    seedInput.set(seedInput.get()[:10])

def keepNumsEnemies(unused):
    global noneAbilityChanceEnemy
    noneAbilityChanceEnemy.set(''.join(ch for ch in noneAbilityChanceEnemy.get() if ch.isdigit()))

def keepNumsObjects(unused):
    global noneAbilityChanceObject
    noneAbilityChanceObject.set(''.join(ch for ch in noneAbilityChanceObject.get() if ch.isdigit()))

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window(endProg=False):
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None
    if endProg:
        sys.exit()