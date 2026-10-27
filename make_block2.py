#!/usr/bin/env python3
"""
Make the block 2 tape (the game's 4 KB ROM) for a public Game & Watch tape, from your own MAME set.

    python make_block2.py gnw_tbridge.zip [more.zip ...]

Each ZIP is a MAME Game & Watch set: the ROM image plus LCD artwork (e.g. gnw_tbridge.zip holds tl-28
and gnw_tbridge.svg).  Only the ROM is taken; everything else in the ZIP is ignored.  The game is
recognised by the ROM's CRC32 (or, failing that, its file name), and the tape is written next to the ZIP
as <year>-<Game Name>-<MODEL-NO>-block2.tzx.

Load the public tape of the same game first; when it prints "Now block 2: the ROM", play this one.

Python 3 standard library only.
"""
import os
import struct
import sys
import zipfile
import zlib

# ROM file name in the MAME set, CRC32, tape key, tape name
GAMES = [
    ('ud-202', '65e97963', 'ud202', '1984-Crab Grab-UD-202'),
    ('dk-52', '5180cbf8', 'dk52', '1982-Donkey Kong-DK-52'),
    ('jr-55_560', '46aed0ae', 'jr55', '1983-Donkey Kong II-JR-55'),
    ('dj-101', '8dcfb5d1', 'dj101', '1982-Donkey Kong Jr.-DJ-101'),
    ('id-29', '5f6e8042', 'id29', '1982-Fire Attack-ID-29'),
    ('gh-54', '4df12b4d', 'gh54', '1982-Green House-GH-54'),
    ('tc-58', '1f88f6a2', 'tc58', '1983-Life Boat-TC-58'),
    ('nh-103', 'ec03acf7', 'nh103', '1983-Manhole-NH-103'),
    ('mw-56', '385e59da', 'mw56', '1983-Mario Bros.-MW-56'),
    ('ml-102_577', 'c1128dea', 'ml102', "1983-Mario's Cement Factory-ML-102"),
    ('dm-53_565', 'e21fc0f5', 'dm53', '1982-Mickey & Donald-DM-53'),
    ('op-51', '31c288c9', 'op51', '1982-Oil Panic-OP-51'),
    ('lp-57', '51a2c5c4', 'lp57', '1983-Rain Shower-LP-57'),
    ('sp-30', 'ba1d9504', 'sp30', '1982-Snoopy Tennis-SP-30'),
    ('bu-201', 'ae0d28e7', 'bu201', '1984-Spitball Sparky-BU-201'),
    ('mg-61', '79cd509c', 'mg61', '1986-Squish-MG-61'),
    ('tf-104', '53cde918', 'tf104', '1985-Tropical Fish-TF-104'),
    ('tl-28', '284e7224', 'tl28', '1982-Turtle Bridge-TL-28'),
]
ROM_AT = 0x8000                 # where the emulator expects the ROM


def std_block(flag, payload, pause_ms):
    data = bytes([flag]) + payload
    c = 0
    for b in data:
        c ^= b
    data += bytes([c])
    return b'\x10' + struct.pack('<HH', pause_ms, len(data)) + data


def block2_tzx(rom, key):
    """A tape holding one CODE block: the ROM at 8000h, named <key>-rom."""
    name = (key + '-rom').encode('ascii')[:10].ljust(10, b' ')
    header = bytes([3]) + name + struct.pack('<HHH', len(rom), ROM_AT, 32768)
    return b'ZXTape!\x1a\x01\x14' + std_block(0x00, header, 500) + std_block(0xFF, rom, 1000)


def find_rom(z):
    """(rom bytes, table entry) from an open ZIP."""
    members = [n for n in z.namelist() if not n.endswith('/')]
    by_crc = {g[1]: g for g in GAMES}
    by_name = {g[0]: g for g in GAMES}
    for n in members:
        data = z.read(n)
        if len(data) == 4096 and '%08x' % (zlib.crc32(data) & 0xFFFFFFFF) in by_crc:
            return data, by_crc['%08x' % (zlib.crc32(data) & 0xFFFFFFFF)]
    for n in members:
        g = by_name.get(os.path.basename(n).lower())
        if g:
            data = z.read(n)
            if len(data) != 4096:
                raise SystemExit('%s is %d bytes, expected 4096' % (n, len(data)))
            print('WARNING: %s has CRC32 %08x, expected %s: a different revision; the emulator checks the '
                  'ROM and will stop with a red border if it is not the one it was built for'
                  % (n, zlib.crc32(data) & 0xFFFFFFFF, g[1]))
            return data, g
    raise SystemExit('no known Game & Watch ROM in this ZIP (members: %s)' % ', '.join(members))


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    for src in sys.argv[1:]:
        with zipfile.ZipFile(src) as z:
            rom, (_, _, key, name) = find_rom(z)
        out = os.path.join(os.path.dirname(os.path.abspath(src)), name + '-block2.tzx')
        with open(out, 'wb') as f:
            f.write(block2_tzx(rom, key))
        print('%s -> %s' % (src, out))


if __name__ == '__main__':
    main()
