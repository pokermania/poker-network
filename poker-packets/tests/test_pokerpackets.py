#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, 2008, 2009 Loic Dachary <loic@dachary.org>
#
# This software's license gives you freedom; you can copy, convey,
# propagate, redistribute and/or modify this program under the terms of
# the GNU Affero General Public License (AGPL) as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version of the AGPL published by the FSF.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program in a file in the toplevel directory called
# "AGPLv3".  If not, see <http://www.gnu.org/licenses/>.
#
import unittest, sys, os
from os import path

TESTS_PATH = path.dirname(path.realpath(__file__))
sys.path.insert(0, path.join(TESTS_PATH, ".."))

from pokerpackets import networkpackets
import testpackets

class PokerPacketsTestCase(testpackets.PacketsTestBase):

    @staticmethod
    def polute(packet):
        if packet.type == networkpackets.PACKET_POKER_USER_INFO:
            packet.money = {5: (1,2,3), 10: (10,11,12)}
        else:
            testpackets.PacketsTestBase.polute(packet)
        
    def packUnpack(self, packet, field):
        packed = packet.pack()
        other_packet = networkpackets.PacketFactory[packet.type]()
        other_packet.unpack(packed)
        self.assertEqual(packed, other_packet.pack())
        self.assertEqual(packet.__dict__[field], other_packet.__dict__[field])
        info_packet = networkpackets.PacketFactory[packet.type]()
        info_packet.infoUnpack(packed);
        self.assertEqual(packed, info_packet.infoPack())
        
    #--------------------------------------------------------------    
    def test_all(self):
        verbose = int(os.environ.get('VERBOSE_T', '-1'))
        for type_index in networkpackets._TYPES:
            if networkpackets.PacketFactory.has_key(type_index):
                if verbose > 0:
                    print networkpackets.PacketNames[type_index]
                self.packetCheck(type = networkpackets.PacketFactory[type_index])

    #--------------------------------------------------------------    
    def test_PacketPokerPlayerArrive(self):
        packet = networkpackets.PacketPokerPlayerArrive(seat = 1)
        self.packUnpack(packet, 'seat')
        packet = networkpackets.PacketPokerPlayerArrive(blind = False)
        self.packUnpack(packet, 'blind')

    #--------------------------------------------------------------    
    def test_PacketPokerUserInfo(self):
        packet = networkpackets.PacketPokerUserInfo(money = {1: (2, 3, 4), 10: (20, 30, 40)})
        self.packUnpack(packet, 'money')
        self.assertTrue("(20, 30, 40)" in str(packet))

    #--------------------------------------------------------------    
    def test_PacketPokerPlayersList(self):
        packet = networkpackets.PacketPokerPlayersList(players = [('name', 10, 20)])
        self.packUnpack(packet, 'players')
        self.assertTrue("('name', 10, 20)" in str(packet))
        
    #--------------------------------------------------------------    
    def test_PacketPokerMoneyTransfert(self):
        packet = networkpackets.PacketPokerCashIn(
            url='url',
            name='name',
            bserial=10,
            value=20
        )
        self.packUnpack(packet, 'name')
        self.assertTrue("name = name" in str(packet))        

    #--------------------------------------------------------------    
    def test_verifyfactory(self):
        from pokerpackets.networkpackets import PacketNames, PacketFactory
        for packid in PacketNames.keys():
            self.assertTrue(PacketFactory.has_key(packid),"%d not found" % packid)
            self.assertEquals(PacketFactory[packid].type, packid)
        for packid in PacketFactory.keys():
            self.assertTrue(PacketNames.has_key(packid))
    #--------------------------------------------------------------    
    def test_PacketPokerTable(self):
        packet = networkpackets.PacketPokerTable(tourney_serial = 2)
        self.assertTrue("tourney_serial = 2" in str(packet))
    #--------------------------------------------------------------    
    def test_PacketPokerSetLocale(self):
        packet = networkpackets.PacketPokerSetLocale(serial = 42, locale = "fr_FR", game_id = 100)
        self.packUnpack(packet, 'game_id')
        self.assertTrue("100" in str(packet))

#--------------------------------------------------------------
def GetTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PokerPacketsTestCase))
    return suite
    
#--------------------------------------------------------------
def Run(verbose = 1):
    return unittest.TextTestRunner(verbosity=verbose).run(GetTestSuite())
    
#--------------------------------------------------------------
if __name__ == '__main__':
    if Run().wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
