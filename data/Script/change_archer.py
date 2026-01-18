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

'NPC: Bowman Job Instructor'
'Script: Bowman 2nd Job Advancement'

import math
import random

if self.userGetJob() == 300 and self.userGetLevel() >= 30:
    nBlack = self.inventoryGetItemCount(4031013)
    if self.inventoryGetItemCount(4031010) >= 1:
        if nBlack == 0:
            self.sayNext("Hmmm...it is definitely the letter from #b#p1012100##k...so you came all the way here to take the test and make the 2nd job advancement as the bowman. Alright, I'll explain the test to you. Don't sweat it much, though; it's not that complicated.")
            self.sayNext("I'll send you to a hidden map. You'll see monsters not normally seen in normal fields. They look the same like the regular ones, but with a totally different attitude. They neither boost your experience level nor provide you with item.")
            self.sayNext("You'll be able to acquire a marble called #b#t4031013##k while knocking down those monsters. It is a special marble made out of their sinister, evil minds. Collect 30 of those, then go talk to a colleague of mine in there. That's how you pass the test.")
            nRet = self.askYesNo("Once you go inside, you can't leave until you take care of your mission. If you die, your experience level will decrease...so you better really buckle up and get ready...well, do you want to go for it now?")
            if nRet == 0:
                self.sayNext("I don't think you are prepared for this. Find me when you ARE ready. There are neither portals nor stores inside, so you better get 100% ready for it.")
            elif nRet == 1:
                self.sayNext("Alright I'll let you in! Defeat the monsters inside, collect 30 Dark Marbles, and then talk to my colleague inside. Then he'll award you the proof of passing the test, #b#t4031012##k. Good luck.")
                aMap = [108000100, 108000101, 108000102]
                self.registerTransferField(aMap[math.floor(random.random() * len(aMap))], "")
        elif nBlack > 0:
            nRet = self.askYesNo("So you've given up in the middle of this before. Don't worry about it, because you can always retake the test. Now...do you want to go back in and try again?")
            if nRet == 0:
                self.sayNext("You don't seem too prepared for this. Find me when you ARE ready. There are neither portals or stores inside, so you better get 100% ready for it.")
            elif nRet == 1:
                self.sayNext("Alright! I'll let you in! Sorry to say this, but I have to take away all your marbles beforehand. Defeat the monsters inside, collect 30 Dark Marbles, then strike up a conversation with a colleague of mine inside. He'll give you the #b#t4031012##k, the proof that you've passed the test. Best of luck to you.")
                self.inventoryExchange(0, 4031013, -nBlack)
                aMap = [108000100, 108000101, 108000102]
                self.registerTransferField(aMap[math.floor(random.random() * len(aMap))], "")
    else:
        self.sayNext("Do you want to be a stronger bowman? Let me take care of that for you, then. You look definitely qualified for it. For now, go see #b#p1012100##k of Henesys first.")
elif self.userGetJob() == 300 and self.userGetLevel() < 30:
    self.sayNext("Do you want to be an even stronger bowman? Let me take care of that. However... you look pretty weak. It would be much better if you can train more, get stronger, and then come back.")
elif self.userGetJob() == 310 or self.userGetJob() == 320 or self.userGetJob() == 330:
    self.sayNext("Hmmm... it was you who passed my test! What do you think? Do you feel more powerful than before? Good! You now definitely have the look of a bowman...")
