from clientpackets import *

def packetToExport(ptype):
    packet = PacketFactory[ptype]
    pname = PacketNames[ptype]
    return {
        'name': pname,
        'fields': packet.info[2:]
    }

def exportPackets():
    exp = [(ptype, packetToExport(ptype)) for ptype in PacketFactory.iterkeys()]
    return exp


if __name__ == '__main__':
    import json
    encoder = json.JSONEncoder(separators=(',',':'))
    exp = exportPackets()
    print '{%s}' % ',\n'.join('"%d": %s' % (p[0], encoder.encode(p[1])) for p in exp)