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
NPC: Teo
Quest: Maya of Henesys (Maya and the Weird Medicine), Finding Sophia
'''

prompt = "I heard that Maya is sick again. Tragic..."

sel = self.askMenu(prompt + "\r\n\r\n#b#L0#Maya of Henesys#l#k")
if sel == 0:
	self.sayNext("You know about #bMaya of Henesys#k? She's been sick for quite some time now. I've been worried about her, but what can I do? I can't exactly cure her myself.")
	self.sayNext("If you happen to see her, please let her know that I hope she feels better soon. I'm sure she'd appreciate a visitor!")
	ret = self.askYesNo("Actually, on second thought, I have a favor to ask of you. Would you be willing to find #bSophia#k for me? She lives in Lith Harbor, and I need to get a message to her.")
	if ret == True:
		self.questRecordSet(1006, "start")
		self.say("Thank you so much! Please find Sophia in Lith Harbor and let her know that I need to speak with her. I really appreciate your help!")
