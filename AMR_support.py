#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 5.4
#  in conjunction with Tcl version 8.6
#    Jul 06, 2020 08:24:00 PM EDT  platform: Windows NT

import sys
import binascii

try:
    import Tkinter as tk
    from Tkinter.filedialog import askopenfilename
    from Tkinter import font as tkFont
    from Tkinter.messagebox import showinfo, showerror
except ImportError:
    import tkinter as tk
    from tkinter.filedialog import askopenfilename
    from tkinter import font as tkFont
    from tkinter.messagebox import showinfo, showerror
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
    includeMinnyAndWheelie.set("2")
    objectRandomizationType.set("Yes")
    noneAbilityChanceObject.set("90")
    numSeeds.set("1")
    useSeed.set("2")
    generateAbilityLog.set("1")
    message.set("Welcome to the Amazing Mirror Randomizer! Move your mouse over a label to learn more about it.")

def setSourceRom():
    global sourceRom
    sourceRom.set(tk.filedialog.askopenfilename(filetypes=[("GBA ROM files", "*.gba")]))
    with open(sourceRom.get(), "rb") as inputFile:
        fileBytes = inputFile.read()
    currHash = "9F2A3048"
    fileHash = str(hex(binascii.crc32(fileBytes)))[2:].zfill(8).upper()
    if currHash != fileHash:
        showerror("Incorrect File", "Incorrect file; CRC32 does not match expected hash.\n\nExpected: "+currHash+"\nGot: "+fileHash)
        sourceRom.set("")

def keepUpperCharsSeed(unused):
    global seedInput
    seedInput.set(''.join(ch.upper() for ch in seedInput.get() if ch.isalpha() or ch.isdigit()))
    seedInput.set(seedInput.get()[:10])

def keepNumsEnemies(unused):
    global noneAbilityChanceEnemy
    noneAbilityChanceEnemy.set(''.join(ch for ch in noneAbilityChanceEnemy.get() if ch.isdigit()))
    temp = noneAbilityChanceEnemy.get()
    if len(temp) >= 3 and temp[:3] == "100":
        noneAbilityChanceEnemy.set("100")
    else:
        noneAbilityChanceEnemy.set(temp[:2])

def keepNumsObjects(unused):
    global noneAbilityChanceObject
    noneAbilityChanceObject.set(''.join(ch for ch in noneAbilityChanceObject.get() if ch.isdigit()))
    temp = noneAbilityChanceObject.get()
    if len(temp) >= 3 and temp[:3] == "100":
        noneAbilityChanceObject.set("100")
    else:
        noneAbilityChanceObject.set(temp[:2])

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