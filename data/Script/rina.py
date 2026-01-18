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
NPC: Rina
Quest: Hungry Ronnie, Secret to Unagi Special
'''

val = self.questRecordGet(1005)
val2 = self.questRecordGet(1013)

if val == "start":
	# Check if player has the required items
	if self.inventoryItemCount(4000007) >= 50 and self.inventoryItemCount(4000017) >= 5:
		self.sayNext("Perfect! You brought me everything I need! Let me make the Unagi Special for you...")
		ret = self.inventoryExchange(0, 4000007, -50, 4000017, -5)
		if ret == True:
			self.questRecordSet(1005, "complete")
			# Give Unagi Special - would need proper quest item
			self.say("Here's the Unagi Special! Please give it to Ronnie. And remember, don't tell him what's in it!")
		else:
			self.say("You don't have enough space in your inventory. Please make some room and come back.")
	else:
		self.say("I need #b50 Curse Eye Tails#k and #b5 Pig's Heads#k to make the Unagi Special. Please bring me those items!")
elif val2 == "start":
	prompt = "This town is made by the group of bowmnen. If you want to become a bowman, please meet with #rAthena Pierce#k... She will help you. What? You don't know #rAthena Pierce#k? She saved our town long time ago from the monsters. Of course, it is safe now. She is the hero of our town."
	
	sel = self.askMenu(prompt + "\r\n\r\n#b#L0#Hungry Ronnie#l#k")
	if sel == 0:
		self.sayNext("So you came here as a favor for Ronnie? Hahaha... Hopefully Ronnie is not in trouble! Anyway, he wants the #bUnagi special#k, huh? It's easy to whip up, so why don't you just sit around and wait for a little bit as I make this dish...")
		self.sayNext("Oh shoot. I'm missing some #bCurse Eye Tails#k and #bPig's Heads#k! What? Of course they really go into this dish! Just, uh, please keep that a secret from Ronnie, okay?")
		ret = self.askYesNo("Anyway I don't have enough ingredients to make Unagi. Can you get them for me? #b50 Curse Eye Tails and 5 Pig's Heads#k and then I can make the #bUnagi Special#k.")
		if ret == True:
			self.questRecordSet(1005, "start")
else:
	self.say("This town is made by the group of bowmnen. If you want to become a bowman, please meet with #rAthena Pierce#k... She will help you. What? You don't know #rAthena Pierce#k? She saved our town long time ago from the monsters. Of course, it is safe now. She is the hero of our town.")