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
NPC: Luke (also used for Mike, who's NPC exists but isn't on any map yet)
Quest: Luke the Security Guy
'''

val = self.questRecordGet(1007)
if val == "start":
	# Check if player has all required items
	if self.inventoryItemCount(4000030) >= 100 and self.inventoryItemCount(4000042) >= 10 and self.inventoryItemCount(2020001) >= 1:
		self.sayNext("Wow! You got everything I need! Thank you so much! My mom is going to love this Snake Drink!")
		ret = self.inventoryExchange(0, 4000030, -100, 4000042, -10, 2020001, -1)
		if ret == True:
			self.questRecordSet(1007, "complete")
			self.userIncEXP(100, False)
			self.say("Thanks again! Here's a little something for your trouble. Now if you'll excuse me, I need to get back to napping... I mean, guarding!")
		else:
			self.say("Hmm, it seems you don't have enough space in your inventory. Please make some room and come back.")
	else:
		self.say("I need #b100 Jr. Necki Skins#k, #b10 Stirge Wings#k, and #b1 Salad#k. Please bring me all of those items!")
else:
	prompt = "Okay, who just woke me up?? I hate anyone that wakes me up from my nap ... huh? What am I doing? What do you think I'm doing? Of course I'm guarding the entrance!! This is the entrance to the #bVictoria Island : Center Dungeon#k. You have to be careful in there; the monsters you've faced don't even compare to the ones you're about to face in here. I suggest you don't go in there unless you can protect yourself. Okay, nap time!"
	
	sel = self.askMenu(prompt + "\r\n\r\n#b#L0#Luke the Security Guy#l#k")
	if sel == 0:
		ret = self.askYesNo("Being a good son, I annually make my mom an extra special, healthy, and tasty dish, but I don't have as much time this year because of my job. Can you get the ingredients I need for my dish?")
		if ret == False:
			self.say("Must be busy, eh? Can't blame you. I am, too. Let me know if you get any free time.")
		else:
			self.questRecordSet(1007, "start")
			self.say("Alright! This year I'm going to make my mom a tasty Snake Drink! Can you get me #b100 Jr. Necki Skins#k, #b10 Stirge Wings#k, and for the final touch, #b1 Salad#k please?")
