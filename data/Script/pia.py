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
NPC: Pia
Quest: Pia and the Blue Mushroom
'''

prompt = "Ah~! It is really getting to me!!! Blue Mushroom... Oh... Are you a stranger?"

sel = self.askMenu(prompt + "\r\n\r\n#b#L0#Pia and the Blue Mushroom#l#k")
if sel == 0:
	self.sayNext("You must be new around here. I'm Pia, and I need your help! I've been having nightmares about Blue Mushrooms lately. They're everywhere!")
	ret = self.askYesNo("Can you please hunt down some Blue Mushrooms for me? If you bring me #b15 Blue Mushroom Caps#k, I'll feel much better. Will you help me?")
	if ret == True:
		self.questRecordSet(1011, "start")
		self.say("Thank you! Please bring me 15 Blue Mushroom Caps. You can get them by defeating Blue Mushrooms in the forest nearby.")