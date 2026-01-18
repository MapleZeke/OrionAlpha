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
NPC: Blackbull
Quest: Fixing Blackbull's House
'''

# Check if player has the required items
if self.inventoryItemCount(4000001) >= 30 and self.inventoryItemCount(4000018) >= 50:
	self.sayNext("Oh! You brought me the materials I need! Thank you so much!")
	ret = self.inventoryExchange(0, 4000001, -30, 4000018, -50)
	if ret == True:
		self.userIncEXP(50, False)
		# Random reward: Steel Shield or Red Triangular Shield
		import random
		if random.randint(0, 1) == 0:
			self.inventoryExchange(0, 1092002, 1)  # Steel Shield
		else:
			self.inventoryExchange(0, 1092004, 1)  # Red Triangular Shield
		self.say("Here's a little something for your trouble. Thanks for helping me expand my house!")
	else:
		self.say("You don't have enough space in your inventory. Please make some room and come back.")
else:
	prompt = "Our family grew, and I'll have to fix the house to make it bigger, but I need materials to do so..."
	self.sayNext(prompt)
	ret = self.askYesNo("Can you help me gather the materials I need? I need #b30 Tree Branches#k from Stumps and #b50 Firewood#k from Axe Stumps. Will you help me?")
	if ret == True:
		self.say("Thank you! Please bring me 30 Tree Branches and 50 Firewood. I'll be waiting here!")