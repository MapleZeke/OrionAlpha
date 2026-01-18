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
NPC: Sen
Quest: Nina's Brother Sen
'''

val = self.questRecordGet(1002)
if val == "start":
	self.say("Who are you? What do you want from me? Oh, my sister sent you? She wants to give me a gift?")
	self.sayNext("Yeah, well, I could use some #bOranges#k. I heard they taste great, and I want to have one! Tell her that!")
	ret = self.askYesNo("You want me to go tell her now?")
	if ret == False:
		self.say("Awww... You aren't going to tell her?")
	else:
		self.say("You know where my sister is, right? I mean, you just talked to her...")
		self.questRecordSet(1003, "start")
else:
	self.say("There is nothing to eat in here. My poor tummy...")