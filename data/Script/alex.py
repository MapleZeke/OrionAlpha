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
NPC: Alex
Quest: Alex's Request
'''

prompt = "It's been a months since I ran away from home, and frankly I'm sick of wandering around strange places now. But I feel weird about going home..."

sel = self.askMenu(prompt + "\r\n\r\n#b#L0#Alex's Request#l#k")
if sel == 0:
	self.sayNext("I ran away from home because my dad and I had a huge fight. I was young and stupid, and now I regret it. But I'm too scared to go back...")
	ret = self.askYesNo("I don't think my dad will just let me walk back in the door... Not without beating the bejeebus out of me. Can you find a way to calm him down? I need your help, man.")
	if ret == False:
		self.say("You can't do me a favor because I'm an immature kid who ran away from home, right? I understand, but I'm trying to... Ah, nevermind.")
	else:
		self.sayNext("Thank you! My dad lives in Perion. His name is... well, just ask around for 'Alex's father' and they'll point you in the right direction.")
		self.say("Please tell him that I'm sorry and that I want to come home. Maybe if you talk to him, he'll calm down and let me come back.")