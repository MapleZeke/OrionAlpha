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
NPC: Don Giovanni (Hair Salon Owner)
Script: Kerning City VIP Hair Stylist
'''

selectHair = self.askMenu("Hi! I'm Don Giovanni, the owner of this hair salon! If you have #b#t4050003##k, #b#t4050001##k, why don't you let me take care of the rest? Decide what you want to do with your hair...\r\n#b#L0# Change hairstyle (VIP coupon)#l\r\n#L1# Dye your hair (VIP coupon)#l")

if selectHair == 0:
    tHair = self.userGetHair() % 10
    
    if self.userGetGender() == 0:
        changeHair1 = 30030 + tHair
        changeHair2 = 30020 + tHair
        changeHair3 = 30000 + tHair
        changeHair4 = 30780 + tHair
        changeHair5 = 30130 + tHair
        changeHair6 = 30350 + tHair
        changeHair7 = 30190 + tHair
        changeHair8 = 30110 + tHair
        changeHair9 = 30180 + tHair
        changeHair10 = 30050 + tHair
        changeHair11 = 30040 + tHair
        changeHair12 = 30160 + tHair
        
        mHair = self.askAvatar("I can change your hairstyle to something totally new. Aren't you tired of your hair? I can give you a new cut with #b#t4050003##k. Choose the style you like.", 4050003, [changeHair1, changeHair2, changeHair3, changeHair4, changeHair5, changeHair6, changeHair7, changeHair8, changeHair9, changeHair10, changeHair11, changeHair12])
    elif self.userGetGender() == 1:
        changeHair1 = 31050 + tHair
        changeHair2 = 31040 + tHair
        changeHair3 = 31000 + tHair
        changeHair4 = 31760 + tHair
        changeHair5 = 31060 + tHair
        changeHair6 = 31090 + tHair
        changeHair7 = 31330 + tHair
        changeHair8 = 31020 + tHair
        changeHair9 = 31130 + tHair
        changeHair10 = 31120 + tHair
        changeHair11 = 31140 + tHair
        changeHair12 = 31010 + tHair
        
        mHair = self.askAvatar("I can change your hairstyle to something totally new. Aren't you tired of your hair? I can give you a new cut with #b#t4050003##k. Choose the style you like.", 4050003, [changeHair1, changeHair2, changeHair3, changeHair4, changeHair5, changeHair6, changeHair7, changeHair8, changeHair9, changeHair10, changeHair11, changeHair12])
    
    if mHair == 1:
        self.say("Alright, check out your new haircut. What do you think? Even I admit this is a work of art! HAHAHA. Come find me when you want a new haircut. I'll take care of the rest!")
    elif mHair == -1:
        self.say("Hmm... Looks like you don't have the right coupon... Too bad, I can't cut your hair without it. Sorry, pal.")
    elif mHair == -3:
        self.say("I'm sorry. Looks like we have a problem here at the salon. I don't think I can cut your hair right now. Come back later.")
    elif mHair == 0 or mHair == -2:
        self.say("I'm sorry. Looks like we have a small problem changing your hairstyle. Please come back in a bit.")

elif selectHair == 1:
    cHair = self.userGetHair()
    eHair = cHair - (cHair % 10)
    
    changeHair1 = eHair
    changeHair2 = eHair + 2
    changeHair3 = eHair + 3
    changeHair4 = eHair + 7
    changeHair5 = eHair + 5
    
    mHair = self.askAvatar("I can change your hair color to something totally new. Aren't you tired of your hair? I can dye your hair if you have #b#t4050001##k. Choose the color you like!", 4050001, [changeHair1, changeHair2, changeHair3, changeHair4, changeHair5])
    
    if mHair == 1:
        self.say("Alright, check out your new hair color. What do you think? Even I admit this is a work of art! HAHAHA. Come find me when you want a new haircut. I'll take care of the rest!")
    elif mHair == -1:
        self.say("Hmm... Looks like you don't have the right coupon... Too bad, I can't dye your hair without it. Sorry, pal.")
    elif mHair == -3:
        self.say("I'm sorry. Looks like we have a problem here at the salon. I don't think I can dye your hair right now. Come back later.")
    elif mHair == 0 or mHair == -2:
        self.say("I'm sorry. Looks like we have a small problem changing your color. Please come back in a bit.")
