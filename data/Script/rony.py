'''
This file is part of OrionAlpha, a MapleStory Emulator Project.
Copyright (C) 2018 Eric Smith <notericsoft@gmail.com>
 
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

'''
Author: Eric
NPC: Ronnie
Quest: A Clue to the Secret Book, Hungry Ronnie
'''

val = self.questRecordGet(1012)
val2 = self.questRecordGet(1013)

if val2 == "start":
	# Check if player has all required items for Hungry Ronnie
	if self.inventoryItemCount(4000029) >= 50 and self.inventoryItemCount(2000003) >= 1:
		# Check for Unagi Special - this would need to be a quest item
		self.sayNext("Wow! You brought me food! Let me check... 50 Lupin's Bananas, Fresh Milk, and... where's the Unagi Special?")
		self.say("You need to get the Unagi Special from Rina in Henesys. She's the only one who knows how to make it!")
	else:
		self.say("I'm so hungry... Please bring me #b50 Lupin's Bananas#k, #bFresh Milk#k, and Rina's #bUnagi Special#k!")
elif val == "start":
	prompt = "Now what exactly is in this book that makes my dad take care of it so much? I want to know what's inside, but I don't think I'll understand it one bit..."
	
	sel = self.askMenu(prompt + "\r\n\r\n#b#L0#A Clue to the Secret Book#l#k")
	if sel == 0:
		self.sayNext("Who are you? You know my dad? Ah, you want this red book, huh? I see. My dad likes this book more than he likes me! This book... No, I can't give you this book! *Stomach growling* Ahhhh!")
		self.sayNext("No...I'm NOT hungry! Dang, all right. I'll give you the book. But not for free! I'm starving and I need food, so if you get me something to eat, the book is yours. I promise!")
		self.sayNext("I want #b50 Lupin's Bananas#k and Rina's #bUnagi Special#k, along with some #bFresh Milk#k. Rina is a friend of mine who lives in Henesys. Ask her for the Unagi Special and she'll make it for you.")
		ret = self.askYesNo("Oh yeah! The fairies from Ellinia probably have some #bFresh Milk#k. I always got mine from Ellinia. If you get hungry on your way back and eat my food, my dad's book is going to Curse Eye. So you better take care of that food!")
		if ret == True:
			self.questRecordSet(1013, "start")
else:
	self.say("I love this spot. It's so peaceful and quiet here, just me and my book...")
