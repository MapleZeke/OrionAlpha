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
NPC: Andre (Hair Salon Assistant)
Script: Kerning City General Hair Stylist
'''

selectHair = self.askMenu("I'm Andres, Don's assistant. Everyone calls me Andre. If you have a #b#t4050002##k or #b#t4050001##k, let me change your hairstyle...\r\n#b#L0# Haircut (regular coupon)#l\r\n#L2# Dye your hair (regular coupon)#l")

if selectHair == 0:
    nRet1 = self.askYesNo("If you use a regular coupon, your hair will change RANDOMLY with the chance of getting a new style you didn't even think was possible. Will you use #b#t4050002##k and really change your style?")
    
    if nRet1 == 0:
        self.say("I see... Think about it a bit more, and come find me if you want.")
    elif nRet1 == 1:
        tHair = self.userGetHair() % 10
        
        if self.userGetGender() == 0:
            changeHair1 = 30000 + tHair
            changeHair2 = 30020 + tHair
            changeHair3 = 30030 + tHair
            changeHair4 = 30040 + tHair
            changeHair5 = 30050 + tHair
            changeHair6 = 30110 + tHair
            changeHair7 = 30130 + tHair
            changeHair8 = 30160 + tHair
            changeHair9 = 30180 + tHair
            changeHair10 = 30190 + tHair
            changeHair11 = 30350 + tHair
            changeHair12 = 30610 + tHair
            changeHair13 = 30440 + tHair
            changeHair14 = 30400 + tHair
            
            mHair = self.makeRandAvatar(4050002, [changeHair1, changeHair2, changeHair3, changeHair4, changeHair5, changeHair6, changeHair7, changeHair8, changeHair9, changeHair10, changeHair11, changeHair12, changeHair13, changeHair14])
        elif self.userGetGender() == 1:
            changeHair1 = 31000 + tHair
            changeHair2 = 31010 + tHair
            changeHair3 = 31020 + tHair
            changeHair4 = 31040 + tHair
            changeHair5 = 31050 + tHair
            changeHair6 = 31060 + tHair
            changeHair7 = 31090 + tHair
            changeHair8 = 31120 + tHair
            changeHair9 = 31130 + tHair
            changeHair10 = 31140 + tHair
            changeHair11 = 31330 + tHair
            changeHair12 = 31700 + tHair
            changeHair13 = 31620 + tHair
            changeHair14 = 31610 + tHair
            
            mHair = self.makeRandAvatar(4050002, [changeHair1, changeHair2, changeHair3, changeHair4, changeHair5, changeHair6, changeHair7, changeHair8, changeHair9, changeHair10, changeHair11, changeHair12, changeHair13, changeHair14])
        
        if mHair == 1:
            self.say("Here's the mirror. Your new cut! What do you think? I know it's not the trendiest, but it looks really cool to me! Come back when you need a new change!")
        elif mHair == -1:
            self.say("Hmm... Are you sure you have the right coupon? Sorry, but no haircut without it.")
        elif mHair == -3:
            self.say("I'm sorry. Looks like we have a problem here at the salon. I don't think I can cut your hair right now. Come back later.")
        elif mHair == 0 or mHair == -2:
            self.say("I'm sorry. Looks like we have a small problem changing your hairstyle. Please come back in a bit.")

elif selectHair == 2:
    nRet1 = self.askYesNo("If you use a regular coupon, your hair will change randomly. Do you still want to use #b#t4050001##k and dye your hair?")
    
    if nRet1 == 0:
        self.say("I see... Think about it a bit more, and come find me if you want.")
    elif nRet1 == 1:
        cHair = self.userGetHair()
        eHair = cHair - (cHair % 10)
        
        changeHair1 = eHair
        changeHair2 = eHair + 2
        changeHair3 = eHair + 3
        changeHair4 = eHair + 7
        changeHair5 = eHair + 5
        
        mHair = self.makeRandAvatar(4050001, [changeHair1, changeHair2, changeHair3, changeHair4, changeHair5])
        
        if mHair == 1:
            self.say("Here's the mirror. Your new cut! What do you think? I know it's not the trendiest, but it looks really cool to me! Come back when you need a new change!")
        elif mHair == -1:
            self.say("Hmm... Are you sure you have the right coupon? Sorry, but no haircut without it.")
        elif mHair == -3:
            self.say("I'm sorry. Looks like we have a problem here at the salon. I don't think I can dye your hair right now. Come back later.")
        elif mHair == 0 or mHair == -2:
            self.say("I'm sorry. Looks like we have a small problem changing your color. Please come back in a bit.")