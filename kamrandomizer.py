import random
import shutil
import copy
from math import ceil, floor
from os import path, remove
from time import sleep
from tkinter import Tk
from tkinter.filedialog import askopenfilename

"""
Ability Values:

00 - Nothing
01 - Fire
02 - Ice
03 - Burning
04 - Wheel
05 - Parasol
06 - Cutter
07 - Beam
08 - Stone
09 - Bomb
0A - Throw
0B - Sleep
0C - Cook
0D - Laser
0E - UFO
0F - Spark
10 - Tornado
11 - Hammer
12 - Sword
13 - Cupid
14 - Fighter
15 - Magic
16 - Smash
17 - Mini
18 - Crash
19 - Missile
1A - Master

The remaining values are either some sort of bug/crash, mix (like when you inhale two abilities at one), or duplicate.
"""

abilities = [
	"Nothing",
	"Fire",
	"Ice",
	"Burning",
	"Wheel",
	"Parasol",
	"Cutter",
	"Beam",
	"Stone",
	"Bomb",
	"Throw",
	"Sleep",
	"Cook",
	"Laser",
	"UFO",
	"Spark",
	"Tornado",
	"Hammer",
	"Sword",
	"Cupid",
	"Fighter",
	"Magic",
	"Smash",
	"Mini",
	"Crash",
	"Missile",
	"Master"
]

normalEnemies = {
	"Bang-Bang"				:	[[0x351AB6], 0x19],
	"Batty"					:	[[0x351A86], 0x00],
	"Big Waddle Dee"		:	[[0x3517E6], 0x00],
	"Blipper"				:	[[0x35167E], 0x00],
	"Bomber"				:	[[0x351A0E], 0x18],
	"Boxin"					:	[[0x3519C6], 0x14],
	"Bronto Burt"			:	[[0x351666], 0x00],
	"Chip"					:	[[0x35170E], 0x00],
	"Cookin"				:	[[0x3519DE], 0x0C],
	"Cupie"					:	[[0x35176E], 0x13],
	"Droppy"				:	[[0x351AFE, 0x3527D6], 0x00], # the second address is the one spawned by Wiz
	"Flamer"				:	[[0x351816], 0x03],
	"Foley"					:	[[0x35197E], 0x09],
	"Giant Rocky"			:	[[0x351A3E], 0x08],
	"Glunk"					:	[[0x351696], 0x00],
	# "Golem"					:	[[0x351966], 0x08], # mostly-unknown; this only covers the Golems spawned by King Golem; address search showed the same thing for all types of Golems
	"Haley"					:	[[0x35173E], 0x00],
	"Heavy Knight"			:	[[0x351A26], 0x12],
	"Hot Head"				:	[[0x35182E], 0x01],
	"Jack"					:	[[0x3517CE], 0x00],
	"Laser Ball"			:	[[0x351846], 0x0D],
	"Leap"					:	[[0x3517B6], 0x00],
	"Metal Guardian"		:	[[0x351A56], 0x0D],
	"Minny"					:	[[0x3519F6], 0x17],
	"Noddy"					:	[[0x35191E], 0x0B],
	# "Parasol Waddle Dee"	:	[[0x??????], 0x05], # unknown; address search showed it as Parasol object
	"Pengy"					:	[[0x35185E], 0x02],
	"Prank"					:	[[0x351B16], 0x00],
	"Rocky"					:	[[0x351876], 0x08],
	"Roly-Poly"				:	[[0x351756], 0x00],
	# "Shadow Kirby"			:	[[0x??????], 0x00], # unknown
	"Shooty"				:	[[0x351996], 0x00],
	"Sir Kibble"			:	[[0x35188E], 0x06],
	"Snapper"				:	[[0x352536], 0x12],
	"Snooter"				:	[[0x3516F6], 0x00],
	"Soarar"				:	[[0x351726], 0x00],
	"Sparky"				:	[[0x3518A6], 0x0F],
	"Squishy"				:	[[0x3516AE], 0x00], # Did you know there's only one of these in the entire game? And it's really well-hidden
	"Sword Knight"			:	[[0x3518BE], 0x12],
	"Twister"				:	[[0x3518EE], 0x10],
	"UFO"					:	[[0x3518D6], 0x0E],
	"Waddle Dee"			:	[[0x35164E, 0x351B76], 0x00], # the second address is the mini-boss version
	"Waddle Doo"			:	[[0x3517FE], 0x07],
	"Wheelie"				:	[[0x351906], 0x04]
}

miniBosses = {
	"Batafire"		:	[[0x351BD6], 0x03],
	"Bombar"		:	[[0x351C36], 0x19],
	"Bonkers"		:	[[0x351BA6], 0x11],
	"Box Boxer"		:	[[0x351BEE], 0x14],
	"Boxy"			:	[[0x351C06], 0x15],
	"Master Hand"	:	[[0x351C1E], 0x16],
	"Mr. Frosty"	:	[[0x351B8E], 0x02],
	"Phan Phan"		:	[[0x351BBE], 0x0A]
}

objects = {
	"Batafire (Fireball)"			:	[[0x352566], 0x00],
	"Bombar (Bomb)"					:	[[0x3526FE], 0x09],
	"Bombar (Missile)"				:	[[0x352716], 0x19],
	"Bonkers (Large Rock)"			:	[[0x352626], 0x00],
	"Bonkers (Small Rock)"			:	[[0x35260E], 0x00],
	"Box Boxer (Energy Blast)"		:	[[0x35272E], 0x00],
	# "Boxy (Bomb)"					:	[[0x??????], 0x09], # unknown
	"Boxy (Present)"				:	[[0x3626CE], 0x00],
	"Dark Mind (Blue Star)"			:	[[0x35296E], 0x02],
	"Dark Mind (Bomb)"				:	[[0x351ACE], 0x18],
	"Dark Mind (Purple Star)"		:	[[0x352986], 0x0F],
	"Dark Mind (Red Star)"			:	[[0x352956], 0x01],
	"Enemy Star"					:	[[0x3525C6], 0x00], # the thing that's spawned by basically every boss/mini-boss
	"King Golem (Rock)"				:	[[0x3524D6], 0x00],
	"Master/Crazy Hand (Bullet)"	:	[[0x35290E], 0x03],
	# "Master/Crazy Hand (Star)"		:	[[0x??????], 0x08], # unknown; address search showed it as normal enemy star
	"Moley (Bomb)"					:	[[0x3528AE], 0x09],
	"Moley (Large Rock)"			:	[[0x3528C6], 0x08],
	"Moley (Oil Drum)"				:	[[0x3528DE], 0x03],
	"Moley (Screw)"					:	[[0x35287E], 0x00],
	"Moley (Small Rock)"			:	[[0x352866], 0x00],
	"Moley (Spiny)"					:	[[0x3528F6], 0x06],
	"Moley (Tire)"					:	[[0x352896], 0x04],
	"Mr. Frosty (Large Ice)"		:	[[0x3525F6], 0x00],
	"Mr. Frosty (Small Ice)"		:	[[0x3525DE], 0x00],
	"Parasol"						:	[[0x35257E], 0x05],
	"Phan Phan (Apple)"				:	[[0x35263E], 0x00],
	"Prank (Bomb)"					:	[[0x352686], 0x09],
	"Prank (Fireball)"				:	[[0x352656], 0x01],
	"Prank (Ice)"					:	[[0x35266E], 0x02],
	"Titan Head (Missile)"			:	[[0x35284E], 0x00],
	"Wiz (Balloon)"					:	[[0x352776], 0x00],
	"Wiz (Bomb)"					:	[[0x35278E], 0x09],
	"Wiz (Car)"						:	[[0x35275E], 0x04],
	"Wiz (Cloud)"					:	[[0x3527A6], 0x0F],
	"Wiz (Football)"				:	[[0x352746], 0x00],
	"Wiz (Poison Apple)"			:	[[0x3527BE], 0x0B]
}

def main():
	global sourceRom
	global seedNum
	global currSeed
	global abilityDistributionType
	global basicEnemyBehaviorType
	global noneAbilityChanceBasicEnemy
	global noneAbilityChanceNonBasicEnemy
	global includeMiniBosses
	global randomizeMinnyAndWheelie
	global objectRandomizationType
	global noneAbilityChanceBasicObject
	global noneAbilityChanceNonBasicObject
	global generateAbilityLog

	print("\n")
	print("---------------------------------------------")
	print("| Welcome to the Amazing Mirror Randomizer! |")
	print("---------------------------------------------")
	sourceRom = ""
	while sourceRom == "":
		Tk().withdraw()
		sourceRom = askopenfilename(filetypes=[("GBA ROM files", "*.gba")])
	alreadyHaveSeed = makeChoice("Do you already have a seed?", ["Yes", "No"])
	seedInput = ""
	seedNum = 1
	if alreadyHaveSeed == 1:
		currSeed = verifySeed()
		generateAbilityLog = makeChoice("Generate a spoiler text file containing ability distribution?", [
			"Yes",
			"No"])
		numSeeds = 1
		generateSeed(currSeed)
	else:
		print("\nAnswer the following questions to generate a ROM.\n[R] means \"Recommended\".")
		sleep(1)
		abilityDistributionType = makeChoice("[1/6] How should abilities be distributed?", [
			"[R] Pure random (anything goes)",
			"By enemy grouping (enemies that gave matching abilities in the original game (like Sword Knight and Heavy Knight) will still give matching abilities)",
			"By ability frequency (for example, two enemies gave Ice in the original game, so two random enemies will give Ice here)"])
		if abilityDistributionType == 1:
			basicEnemyBehaviorType = makeChoice("[1a/6] How should enemies that do not give an ability be handled?", [
				"All enemies will give an ability",
				"[R] All enemies may or may not give an ability",
				"Basic enemies that did not originally give an ability (like Waddle Dee) may or may not give an ability; other enemies are still guaranteed to give an ability",
				"Unchanged (basic enemies will still not give an ability, and other enemies will)"])
		else:
			basicEnemyBehaviorType = 4
		if basicEnemyBehaviorType == 1:
			noneAbilityChanceBasicEnemy = 60
			noneAbilityChanceNonBasicEnemy = 60
		elif basicEnemyBehaviorType in [2, 3]:
			noneAbilityChanceEnemy = makeChoiceNumInput("[1b/6] For these enemies that may or may not give an ability, how likely is it that they do give an ability? (0\%-100\%) ([R] = 90)", 0, 100)
			noneAbilityChanceEnemy = min(ceil(noneAbilityChanceEnemy/1.67), 60) # this value rounds to increments of 1.67%; this is to reduce the length of the seed
			noneAbilityChanceBasicEnemy = noneAbilityChanceEnemy
			noneAbilityChanceNonBasicEnemy = noneAbilityChanceEnemy if basicEnemyBehaviorType == 2 else 30
		else:
			noneAbilityChanceBasicEnemy = 0
			noneAbilityChanceNonBasicEnemy = 60
		includeMiniBosses = makeChoice("[2/6] Include mini-bosses?", [
			"[R] Yes (randomize mini-boss abilities)",
			"No (do not change mini-bosses)"])
		randomizeMinnyAndWheelie = makeChoice("[3/6] Include Minny and Wheelie? (Not recommended; you need Mini and Wheel at certain parts of the game)", [
			"Yes (randomize Minny and Wheelie's abilities)",
			"[R] No (do not change their abilities)"])
		objectRandomizationType = makeChoice("[4/6] How would you like to randomize other objects (like inhalable enemy projectiles; basically everything except star blocks)?", [
			"Do not randomize objects",
			"Only randomize objects that already give abilities",
			"[R] Randomize all objects"])
		if objectRandomizationType in [1,2]:
			noneAbilityChanceObject = 30 # unused but needed for seed calculation
			noneAbilityChanceBasicObject = 0
			noneAbilityChanceNonBasicObject = 30
		else:
			noneAbilityChanceObject = makeChoiceNumInput("[4a/6] For objects that may or may not give an ability, how likely is it that they do give an ability? (0\%-100\%) ([R] = 90)", 0, 100)
			noneAbilityChanceObject = min(ceil(noneAbilityChanceObject/3.34), 30) # this value rounds to increments of 3.34%; this is to reduce the length of the seed
			noneAbilityChanceBasicObject = noneAbilityChanceObject
			noneAbilityChanceNonBasicObject = noneAbilityChanceObject
		generateAbilityLog = makeChoice("[5/6] Generate a spoiler text file containing ability distribution?", [
			"Yes",
			"No"])
		numSeeds = int(makeChoiceNumInput("[6/6] How many seeds do you want to generate with these settings? (up to 20)", 0, 100))

		settingsSeed = encodeSeed([abilityDistributionType-1, basicEnemyBehaviorType-1, noneAbilityChanceBasicEnemy, noneAbilityChanceNonBasicEnemy, includeMiniBosses-1, randomizeMinnyAndWheelie-1, objectRandomizationType-1, noneAbilityChanceObject], [2,3,60,60,1,1,2,30])[0]
		for i in range(numSeeds):
			maxVal = int("ZZZZZ", 36)
			genSeed = random.randint(0, maxVal)
			currSeed = (settingsSeed*(maxVal+1)) + genSeed
			generateSeed(currSeed)
	input("\nPress Enter to exit.")

def generateSeed(seed):
	global normalEnemies
	global miniBosses
	global objects
	global myEnemies
	global myObjects
	global currSeed
	global seedNum
	global seedString
	global abilityDistributionType
	global basicEnemyBehaviorType
	global noneAbilityChanceBasicEnemy
	global noneAbilityChanceNonBasicEnemy
	global includeMiniBosses
	global randomizeMinnyAndWheelie
	global objectRandomizationType
	global noneAbilityChanceBasicObject
	global noneAbilityChanceNonBasicObject
	global generateAbilityLog

	seedString = str(dec_to_base(currSeed, 36)).upper().zfill(10)
	print("\nGenerating ROM #"+str(seedNum)+" with seed "+seedString+".")
	random.seed(currSeed)

	myEnemies = copy.deepcopy(normalEnemies)
	if includeMiniBosses:
		myEnemies.update(copy.deepcopy(miniBosses))
	myEnemies = shuffleDict(myEnemies)
	if not randomizeMinnyAndWheelie:
		del myEnemies["Minny"]
		del myEnemies["Wheelie"]
	if abilityDistributionType != 3:
		abilityArray = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19]
	else:
		abilityArray = []
		for key in myEnemies:
			currVal = myEnemies[key][1]
			abilityArray.append(currVal)
	if abilityDistributionType == 2:
		myEnemies = randomizeGroupByAbility(myEnemies, abilityArray)
	else:
		myEnemies = randomizeGroup(myEnemies, abilityArray, abilityDistributionType != 3, True)

	myObjects = shuffleDict(objects)
	if objectRandomizationType != 1:
		abilityArray = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19]
		myObjects = randomizeGroup(myObjects, abilityArray, True, False)

	generateRom()
	if generateAbilityLog:
		generateLog()
	seedNum += 1

def shuffleDict(oldDict):
	newKeys = list(oldDict.keys())
	random.shuffle(newKeys)
	newDict = dict()
	for key in newKeys:
		newDict.update(copy.deepcopy({key:oldDict[key]}))
	return newDict

def randomizeGroup(group, arr, allowDuplicates=True, isEnemy=True):
	for key in group:
		group[key] = randomizeAbilityWithArray(group[key], arr, isEnemy)
		if not allowDuplicates:
			# for i in range(len(arr)):
			# 	if arr[i] == group[key]:
			# 		del arr[i]
			# 		break
			arr.remove(group[key])
	return group

def randomizeGroupByAbility(group, arr):
	shuffledArray = arr[:]
	random.shuffle(shuffledArray)
	for key in group:
		group[key] = shuffledArray[group[key]]

def randomizeAbilityWithArray(entity, possibleAbilities, isEnemy=True):
	global abilityDistributionType
	global noneAbilityChanceBasicEnemy
	global noneAbilityChanceNonBasicEnemy
	global noneAbilityChanceBasicObject
	global noneAbilityChanceNonBasicObject

	if isEnemy:
		if abilityDistributionType == 1 and ((entity[1] == 0x00 and random.randint(1,60) > noneAbilityChanceBasicEnemy) or (entity[1] != 0x00 and random.randint(1,60) > noneAbilityChanceNonBasicEnemy)):
			entity[1] = 0x00
			return entity
	else:
		# objectRandomizationType checks are added so only one noneAbilityChanceObject variable has to be stored in the seed
		if (entity[1] == 0x00 and (objectRandomizationType == 2 or random.randint(1,30) > noneAbilityChanceBasicObject)) or (entity[1] != 0x00 and objectRandomizationType != 2 and random.randint(1,30) > noneAbilityChanceNonBasicObject):
			entity[1] = 0x00
			return entity
	originalAbility = entity[1]
	count = 0
	while entity[1] == originalAbility and count < 2: # unchanged abilites are possible but uncommon
		entity[1] = random.choice(possibleAbilities)
		count += 1
	return entity

def generateRom():
	global sourceRom
	global currSeed
	global seedString

	newRom = path.splitext(sourceRom)[0]+"-"+seedString+".gba"
	shutil.copyfile(sourceRom, newRom)
	try:
		file = open(newRom, "r+b")
		for key in myEnemies:
			for address in myEnemies[key][0]:
				file.seek(address)
				file.write(bytes([myEnemies[key][1]]))
		for key in myObjects:
			for address in myObjects[key][0]:
				file.seek(address)
				file.write(bytes([myObjects[key][1]]))
		file.close()
		print("Succesfully generated ROM with seed "+seedString)
	except:
		print("Something went wrong. Deleting generated ROM.")
		file.close()
		remove(newRom)

def generateLog():
	global sourceRom
	global myEnemies
	global myMiniBosses
	global myObjects
	global abilities

	newLog = path.splitext(sourceRom)[0]+"-"+seedString+".txt"
	file = open(newLog, "w")
	file.writelines("NORMAL ENEMIES:\n")
	for key in normalEnemies:
		if key in myEnemies:
			unchangedStr = " [unchanged]" if myEnemies[key][1] == normalEnemies[key][1] else ""
			file.writelines(key+" - "+abilities[myEnemies[key][1]]+unchangedStr+"\n")
		else:
			file.writelines(key+" - "+abilities[normalEnemies[key][1]]+" [unchanged]"+"\n")
	file.writelines("\nMINI-BOSSES:\n")
	for key in miniBosses:
		if key in myEnemies:
			unchangedStr = " [unchanged]" if myEnemies[key][1] == miniBosses[key][1] else ""
			file.writelines(key+" - "+abilities[myEnemies[key][1]]+unchangedStr+"\n")
		else:
			file.writelines(key+" - "+abilities[miniBosses[key][1]]+" [unchanged]"+"\n")
	file.writelines("\nOBJECTS:\n")
	for key in myObjects:
		if key in myObjects:
			unchangedStr = " [unchanged]" if myObjects[key][1] == objects[key][1] else ""
			file.writelines(key+" - "+abilities[myObjects[key][1]]+unchangedStr+"\n")
		else:
			file.writelines(key+" - "+abilities[objects[key][1]]+" [unchanged]"+"\n")
	file.close()

def makeChoice(question, choices, allowMultiple=False):
	numChoices = len(choices)
	if numChoices == 0:
		print("Warning: A question was asked with no valid answers. Returning None.")
		return None
	if numChoices == 1:
		print("A question was asked with only one valid answer. Returning this answer.")
		return choices[0]
	print("\n"+question)
	for i in range(numChoices):
		print(str(i+1)+": "+choices[i])
	cInput = input().split(" ")
	if not allowMultiple:
		try:
			assert len(cInput) == 1
			choice = int(cInput[0])
			assert choice > 0 and choice <= numChoices
			return choice
		except:
			print("Invalid input.")
			return makeChoice(question, choices, allowMultiple)
	else:
		try:
			choices = [int(c) for c in cInput]
			for choice in choices:
				assert choice > 0 and choice <= numChoices
			return choices
		except:
			print("Invalid input.")
			return makeChoice(question, choices, allowMultiple)

def makeChoiceNumInput(question, minVal, maxVal):
	while True:
		print("\n"+question)
		try:
			var = float(input())
			assert minVal <= var <= maxVal
			return var
		except:
			print("Invalid input.")

# taken from https://www.codespeedy.com/inter-convert-decimal-and-any-base-using-python/
def dec_to_base(num,base):  #Maximum base - 36
    base_num = ""
    while num>0:
        dig = int(num%base)
        if dig<10:
            base_num += str(dig)
        else:
            base_num += chr(ord('A')+dig-10)  #Using uppercase letters
        num //= base
    base_num = base_num[::-1]  #To reverse the string
    return base_num

def encodeSeed(varArray, maxValueArray, base=10):
	seed = 0
	baseShift = 0
	for i in range(len(varArray)):
		seed += varArray[i]<<baseShift
		baseShift += maxValueArray[i].bit_length()
	return seed, dec_to_base(seed, base)

def decodeSeed(seed, maxValueArray, seedBase=10):
	if type(seed) is str:
		seed = int(seed, seedBase)
	baseShift = 0
	varArray = []
	for i in range(len(maxValueArray)):
		bitLength = maxValueArray[i].bit_length()
		varArray.append((seed>>baseShift) & ((2**bitLength)-1))
		baseShift += bitLength
	return varArray

def verifySeed():
	global abilityDistributionType
	global basicEnemyBehaviorType
	global noneAbilityChanceBasicEnemy
	global noneAbilityChanceNonBasicEnemy
	global includeMiniBosses
	global randomizeMinnyAndWheelie
	global objectRandomizationType
	global noneAbilityChanceBasicObject
	global noneAbilityChanceNonBasicObject

	while True:
		print("\nPlease type the seed and press Enter.")
		seedInput = input().upper().strip()
		try:
			assert(len(seedInput) == 10)
			abilityDistributionType, basicEnemyBehaviorType, noneAbilityChanceBasicEnemy, noneAbilityChanceNonBasicEnemy, includeMiniBosses, randomizeMinnyAndWheelie, objectRandomizationType, noneAbilityChanceObject = decodeSeed(seedInput[:5], [2,3,60,60,1,1,2,30], 36)
			abilityDistributionType += 1
			basicEnemyBehaviorType += 1
			includeMiniBosses += 1
			randomizeMinnyAndWheelie += 1
			objectRandomizationType += 1
			assert 1 <= abilityDistributionType <= 3
			assert 1 <= basicEnemyBehaviorType <= 4
			assert 0 <= noneAbilityChanceBasicEnemy <= 60
			assert 0 <= noneAbilityChanceNonBasicEnemy <= 60
			assert 1 <= includeMiniBosses <= 2
			assert 1 <= randomizeMinnyAndWheelie <= 2
			assert 1 <= objectRandomizationType <= 3
			assert 0 <= noneAbilityChanceObject <= 30
			noneAbilityChanceBasicObject = noneAbilityChanceObject
			noneAbilityChanceNonBasicObject = noneAbilityChanceObject
			return int(seedInput, 36)
		except:
			print("Invalid seed.")

if __name__ == '__main__':
	main()