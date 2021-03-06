#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2006 - 2010 Loic Dachary <loic@dachary.org>
# Copyright (C) 2006 Mekensleep
#
# Mekensleep
# 26 rue des rosiers
# 75004 Paris
#       licensing@mekensleep.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Authors:
#  Pierre-Andre (05/2006)
#  Loic Dachary <loic@dachary.org>
#

import unittest, sys
from os import path

TESTS_PATH = path.dirname(path.realpath(__file__))
sys.path.insert(0, path.join(TESTS_PATH, ".."))

import random

from pokerengine import pokercards
from pokerengine import pokergame

RAND_MAX = 0x7fff

class PokerPlayerTestCase(unittest.TestCase):
    
    PokerPlayerAttributes = [
                                    'serial' ,\
                                    'name' , \
                                    'game' , \
                                    'fold' , \
                                    'remove_next_turn' , \
                                    'sit_out' , \
                                    'sit_out_next_turn' , \
                                    'sit_requested' , \
                                    'bot' , \
                                    'auto' , \
                                    'auto_blind_ante' , \
                                    'wait_for' , \
                                    'auto_muck' , \
                                    'auto_player_policy' ,\
                                    'auto_player_fold_next_turn' ,\
                                    'missed_blind' , \
                                    'missed_big_blind_count' , \
                                    'blind' , \
                                    'buy_in_payed' , \
                                    'ante' , \
                                    'all_in' , \
                                    'side_pot_index' , \
                                    'seat' , \
                                    'hand' , \
                                    'money' , \
                                    'rebuy' , \
                                    'bet' , \
                                    'dead' , \
                                    'talked_once' ,\
                                    'user_data',
                                    ]
                                
    # -----------------------------------------------------------------------------------------------------
    def setUp(self):
        self.player = pokergame.PokerPlayer(1, 'name', None)
    
    # -----------------------------------------------------------------------------------------------------    
    def tearDown(self):
        pass
        
    # -----------------------------------------------------------------------------------------------------    
    def testPokerPlayerGetSetUserData(self):
        """Test Poker Player : User data accessors"""
        
        self.failUnlessEqual(self.player.getUserData(), None)
        self.player.setUserData('UserData')
        self.failUnlessEqual(self.player.getUserData(), 'UserData')
        
    # -----------------------------------------------------------------------------------------------------    
    def testPokerPlayerIsAllIn(self):
        """Test Poker Player : Is all in"""
        
        self.failUnlessEqual(self.player.isAllIn(), False)
        self.player.all_in = True
        self.failUnlessEqual(self.player.isAllIn(), True)
        
    # -----------------------------------------------------------------------------------------------------    
    def testPokerPlayerIsFold(self):
        """Test Poker Player : Is fold"""
        
        self.failUnlessEqual(self.player.isFold(), False)
        self.failUnlessEqual(self.player.isNotFold(), True)
        self.player.fold = True
        self.failUnlessEqual(self.player.isFold(), True)
        self.failUnlessEqual(self.player.isNotFold(), False)
        
    # -----------------------------------------------------------------------------------------------------    
    def testPokerPlayerIsSit(self):
        """Test Poker Player : Is sit"""
        
        self.failUnlessEqual(self.player.isSit(), False)
        self.failUnlessEqual(self.player.isSitOut(), True)
        self.player.sit_out = False
        self.failUnlessEqual(self.player.isSit(), True)
        self.failUnlessEqual(self.player.isSitOut(), False)
        
    # -----------------------------------------------------------------------------------------------------    
    def testPokerPlayerIsConnected(self):
        """Test Poker Player : Is connected"""
        
        self.failUnlessEqual(self.player.isConnected(), True)
        self.failUnlessEqual(self.player.isDisconnected(), False)
        self.player.remove_next_turn = True
        self.failUnlessEqual(self.player.isConnected(), False)
        self.failUnlessEqual(self.player.isDisconnected(), True)
        
    # -----------------------------------------------------------------------------------------------------    
    def testPokerPlayerCopy(self):
        """Test Poker Player : Copy"""
        
        for attribute in PokerPlayerTestCase.PokerPlayerAttributes:
            setattr(self.player,attribute,random.randint(0,RAND_MAX))
            
        self.player.hand = pokercards.PokerCards()
            
        copy = self.player.copy()
        for attribute in PokerPlayerTestCase.PokerPlayerAttributes:
            try:
                self.failUnlessEqual(getattr(self.player,attribute), getattr(copy,attribute))
            except:
                self.fail('Exception during accessing attribute ' + attribute)
                
    # -----------------------------------------------------------------------------------------------------    
    def testPokerPlayerStringRepresentation(self):
        """Test Poker Player : String representation"""
        
        for attribute in PokerPlayerTestCase.PokerPlayerAttributes:
            setattr(self.player,attribute,random.randint(0,RAND_MAX))
            
        string = ''
        for attribute in PokerPlayerTestCase.PokerPlayerAttributes:
            if attribute == 'game': continue
            string += attribute + ' = ' + str(getattr(self.player,attribute)) + ', '

        # Skip the last comma and space character
        self.failUnlessEqual(string[:-2], str(self.player))
            
    # -----------------------------------------------------------------------------------------------------    
    def testBeginTurn(self):
        """Test Poker Player : Begin turn"""
        
        Attributes = {
                                'bet' : 0,
                                'dead' : 0,
                                'fold' : False,
                                'hand' : pokercards.PokerCards(),
                                'side_pot_index' : 0,
                                'all_in' : False,
                                'blind' : False,
                                'ante' : False
                            }
                                        
        for key in Attributes.keys():
            setattr(self.player,key,random.random())
            
        self.player.beginTurn()
        
        for key, value in Attributes.items():
            self.failUnlessEqual(getattr(self.player, key), value)
            
    # -----------------------------------------------------------------------------------------------------    
    def testIsInGame(self):
        """Test Poker Player : Is in game"""
        
        # Initially the player in in game because not all-in and not fold
        self.failIf(self.player.isAllIn())
        self.failIf(self.player.isFold())
        self.failUnless(self.player.isInGame())
        
        # Player is all in
        self.player.all_in = True
        self.failUnless(self.player.isAllIn())
        self.failIf(self.player.isInGame())
        self.player.all_in = False
        
        # Player is fold
        self.player.fold = True
        self.failUnless(self.player.isFold())
        self.failIf(self.player.isInGame())
        self.player.fold = False
        
    # -----------------------------------------------------------------------------------------------------    
    def testSitRequested(self):
        """Test Poker Player : Sit requested"""
        
        # Initially the player does not request  to sit
        self.failIf(self.player.isSitRequested())
        
        # Sit is now requested
        self.player.sit_requested = True
        self.failUnless(self.player.isSitRequested())
    
    # -----------------------------------------------------------------------------------------------------    
    def testIsBot(self):
        """Test Poker Player : Is bot"""
        
        # Initially the player is not a bot
        self.failIf(self.player.isBot())
        
        # The player is now a bot
        self.player.bot = True
        self.failUnless(self.player.isBot())
    
    # -----------------------------------------------------------------------------------------------------    
    def testIsAuto(self):
        """Test Poker Player : Is auto"""
        
        # Initially the player is not an automatic player
        self.failIf(self.player.isAuto())
        
        # The player is automatic
        self.player.auto = True
        self.failUnless(self.player.isAuto())
    
    # -----------------------------------------------------------------------------------------------------    
    def testIsAutoBlind(self):
        """Test Poker Player : Is auto blind"""
        
        # Initially the player does not in a automatic blind and ante mode
        self.failIf(self.player.isAutoBlindAnte())
        
        # Sit is now requested
        self.player.auto_blind_ante = True
        self.failUnless(self.player.isAutoBlindAnte())
    
    # -----------------------------------------------------------------------------------------------------    
    def testIsWaitForBlind(self):
        """Test Poker Player : Is wait for blind"""
        
        # Initially the player does not wait for blind
        self.failIf(self.player.isWaitForBlind())
        
        # The player is waiting the first round
        self.player.wait_for = 'first_round'
        self.failUnless(self.player.isWaitForBlind())
    
    # -----------------------------------------------------------------------------------------------------    
    def testIsMissedBlind(self):
        """Test Poker Player : Is missed blind"""
        
        # Initially blind is missed
        self.failIf(self.player.isMissedBlind())
        
        # A blind is missed
        self.player.missed_blind = 'big'
        self.failUnless(self.player.isMissedBlind())
        
        # No blind is missed
        self.player.missed_blind = 'n/a'
        self.failIf(self.player.isMissedBlind())
    
    # -----------------------------------------------------------------------------------------------------    
    def testIsBlind(self):
        """Test Poker Player : Is blind"""
        
        # Initially the player blind is late
        self.failUnlessEqual(self.player.blind, 'late')
        self.failUnless(self.player.isBlind())
        
        # The player not blind
        self.player.blind = None
        self.failIf(self.player.isBlind())
    
    # -----------------------------------------------------------------------------------------------------    
    def testIsBuyInPayed(self):
        """Test Poker Player : Is buy in payed"""
        
        # Initially the player nuy in is not payed
        self.failIf(self.player.isBuyInPayed())
        
        # The buy in is payed
        self.player.buy_in_payed = True
        self.failUnless(self.player.isBuyInPayed())
    
# -----------------------------------------------------------------------------------------------------
def GetTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PokerPlayerTestCase))
    # Comment out above and use line below this when you wish to run just
    # one test by itself (changing prefix as needed).
#    suite.addTest(unittest.makeSuite(PokerPlayerTestCase, prefix = "test2"))
    return suite
    
# -----------------------------------------------------------------------------------------------------
def GetTestedModule():
    return pokergame
  
# -----------------------------------------------------------------------------------------------------
def run():
    try:
        import xmlrunner
        runner = xmlrunner.XMLTestRunner(output='build/tests')
    except ImportError:
        runner = unittest.TextTestRunner()
    return runner.run(GetTestSuite())
    
# -----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    if run().wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)

# Interpreted by emacs
# Local Variables:
# compile-command: "( cd .. ; ./config.status tests/test-pokerplayer.py ) ; ( cd ../tests ; make TESTS='test-pokerplayer.py' check )"
# End:
