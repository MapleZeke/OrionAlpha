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
NPC: Biggs
Quest: Bigg's Collection of Items
'''

prompt = "I can't stay in this town forever. Someone rescue me!"
self.sayNext(prompt)
ret = self.askYesNo("I'm Biggs, and I collect various items. If you bring me certain items, I can reward you for your efforts. Are you interested in helping me?")
if ret == True:
	self.say("Great! Come back when you have some items I might be interested in. I'll let you know what I need.")
