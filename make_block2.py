#!/usr/bin/env python3
"""
Make the block 2 tape (the game's ROM) for a public Game & Watch tape, from your own MAME set.

    python make_block2.py gnw_tbridge.zip [more.zip ...]
    python make_block2.py --as "Thief in Garden (TG-18)" trshutvoy.zip     (a game whose ROM is in
                                                    another game's ZIP; the name as in the table below)

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

# ROM file name in the MAME set, CRC32, game, tape name, chip
GAMES = [
    # Nintendo Game & Watch
    ('ac-01', 'ac94e6e4', 'Ball (AC-01)', '1980-Ball-AC-01', 'sm5a'),
    ('rc-04', '154ef27d', 'Fire (RC-04)', '1980-Fire-RC-04', 'sm5a'),
    ('fl-02', 'cc7a99e4', 'Flagman (FL-02)', '1980-Flagman-FL-02', 'sm5a'),
    ('ip-15', 'f6ed6f62', 'Judge (IP-05)', '1980-Judge-IP-05', 'sm5a'),
    ('mt-03', 'f8493177', 'Vermin (MT-03)', '1980-Vermin-MT-03', 'sm5a'),
    ('fp-24', '2806ab39', 'Chef (FP-24)', '1981-Chef-FP-24', 'sm5a'),
    ('mc-25', 'cb820c32', 'Egg (EG-26)', '1981-Egg-EG-26', 'sm5a'),
    ('fr-27', 'f4c53ef0', 'Fire (FR-27)', '1981-Fire-FR-27', 'sm5a'),
    ('cn-17', '6d251e2e', 'Helmet (CN-07)', '1981-Helmet-CN-07', 'sm5a'),
    ('ln-08', '9677681d', 'Lion (LN-08)', '1981-Lion-LN-08', 'sm5a'),
    ('mh-06', 'ae52c425', 'Manhole (MH-06)', '1981-Manhole-MH-06', 'sm5a'),
    ('mc-25', 'cb820c32', 'Mickey Mouse (MC-25)', '1981-Mickey Mouse-MC-25', 'sm5a'),
    ('oc-22', 'bd27781d', 'Octopus (OC-22)', '1981-Octopus-OC-22', 'sm5a'),
    ('pr-21', '392b545e', 'Parachute (PR-21)', '1981-Parachute-PR-21', 'sm5a'),
    ('pp-23', '49987769', 'Popeye (PP-23)', '1981-Popeye-PP-23', 'sm5a'),
    ('dk-52', '5180cbf8', 'Donkey Kong (DK-52)', '1982-Donkey Kong-DK-52', 'sm510'),
    ('dj-101', '8dcfb5d1', 'Donkey Kong Jr. (DJ-101)', '1982-Donkey Kong Jr.-DJ-101', 'sm510'),
    ('id-29', '5f6e8042', 'Fire Attack (ID-29)', '1982-Fire Attack-ID-29', 'sm510'),
    ('gh-54', '4df12b4d', 'Green House (GH-54)', '1982-Green House-GH-54', 'sm510'),
    ('dm-53_565', 'e21fc0f5', 'Mickey & Donald (DM-53)', '1982-Mickey & Donald-DM-53', 'sm510'),
    ('op-51', '31c288c9', 'Oil Panic (OP-51)', '1982-Oil Panic-OP-51', 'sm510'),
    ('sp-30', 'ba1d9504', 'Snoopy Tennis (SP-30)', '1982-Snoopy Tennis-SP-30', 'sm510'),
    ('tl-28', '284e7224', 'Turtle Bridge (TL-28)', '1982-Turtle Bridge-TL-28', 'sm510'),
    ('jr-55_560', '46aed0ae', 'Donkey Kong II (JR-55)', '1983-Donkey Kong II-JR-55', 'sm510'),
    ('tc-58', '1f88f6a2', 'Life Boat (TC-58)', '1983-Life Boat-TC-58', 'sm510'),
    ('nh-103', 'ec03acf7', 'Manhole (NH-103)', '1983-Manhole-NH-103', 'sm510'),
    ('mw-56', '385e59da', 'Mario Bros. (MW-56)', '1983-Mario Bros.-MW-56', 'sm510'),
    ('ml-102_577', 'c1128dea', "Mario's Cement Factory (ML-102)", "1983-Mario's Cement Factory-ML-102", 'sm510'),
    ('lp-57', '51a2c5c4', 'Rain Shower (LP-57)', '1983-Rain Shower-LP-57', 'sm510'),
    ('ud-202', '65e97963', 'Crab Grab (UD-202)', '1984-Crab Grab-UD-202', 'sm510'),
    ('bu-201', 'ae0d28e7', 'Spitball Sparky (BU-201)', '1984-Spitball Sparky-BU-201', 'sm510'),
    ('tf-104', '53cde918', 'Tropical Fish (TF-104)', '1985-Tropical Fish-TF-104', 'sm510'),
    ('mg-61', '79cd509c', 'Squish (MG-61)', '1986-Squish-MG-61', 'sm510'),
    # Konami
    ('584', '1d9022c8', 'Double Dribble (BH001)', '1989-Double Dribble-BH001', 'sm510'),
    ('598', '50870b35', 'Top Gun (BH003)', '1989-Top Gun-BH003', 'sm510'),
    # Tronica
    ('0126_228b', '3d319537', 'Space Mission (SM-11)', '1982-Space Mission-SM-11', 'sm5a'),
    ('0015_224b', 'f58a3832', 'Space Rescue (MG-9)', '1982-Space Rescue-MG-9', 'sm510'),
    ('0126_22yc', '3d319537', 'Spider (SG-21)', '1982-Spider-SG-21', 'sm5a'),
    ('0029_238c', '8977a1cf', 'Clever Chicken (CC-38V)', '1983-Clever Chicken-CC-38V', 'sm510'),
    ('0029_235d', '8977a1cf', "Diver's Adventure (DA-37)", "1983-Diver's Adventure-DA-37", 'sm510'),
    ('0019_238e', '8bd0eadd', 'Shuttle Voyage (MG-8)', '1983-Shuttle Voyage-MG-8', 'sm510'),
    ('0132_238a', 'db80f1ed', 'Super Goal Keeper (SK-10)', '1983-Super Goal Keeper-SK-10', 'sm5a'),
    ('0019_238e', '8bd0eadd', 'Thief in Garden (TG-18)', '1983-Thief in Garden-TG-18', 'sm510'),
    ('0015_236d', 'f58a3832', 'Thunder Ball (FR-23)', '1983-Thunder Ball-FR-23', 'sm510'),
    # Elektronika (USSR)
    ('im-02.bin', 'cb820c32', 'Nu, pogodi! (IM-02)', '1983-Nu, pogodi!-IM-02', 'sm5a'),
    ('im-10.bin', 'cb820c32', 'Hockey (IM-10)', '1988-Hockey-IM-10', 'sm5a'),
    ('im-03.bin', 'bd27781d', 'Tayny okeana (IM-03)', '1988-Tayny okeana-IM-03', 'sm5a'),
    ('im-19.bin', 'cb820c32', 'Biathlon (IM-19)', '1989-Biathlon-IM-19', 'sm5a'),
    ('im-09.bin', 'f4c53ef0', 'Kosmicheskiy most (IM-09)', '1989-Kosmicheskiy most-IM-09', 'sm5a'),
    ('im-32.bin', 'cb820c32', 'Kot-rybolov (IM-32)', '1989-Kot-rybolov-IM-32', 'sm5a'),
    ('im-33.bin', 'cb820c32', 'Kvaka-zadavaka (IM-33)', '1989-Kvaka-zadavaka-IM-33', 'sm5a'),
    ('im-16.bin', 'cb820c32', 'Okhota (IM-16)', '1989-Okhota-IM-16', 'sm5a'),
    ('im-13.bin', '553e2b09', 'Razvedchiki kosmosa (IM-13)', '1989-Razvedchiki kosmosa-IM-13', 'sm5a'),
    ('im-22.bin', 'cb820c32', 'Vesyolye futbolisty (IM-22)', '1989-Vesyolye futbolisty-IM-22', 'sm5a'),
    ('im-04.bin', '2806ab39', 'Vesyolyy povar (IM-04)', '1989-Vesyolyy povar-IM-04', 'sm5a'),
    ('im-23.bin', '3b6e726f', 'Autoslalom (IM-23)', '1990-Autoslalom-IM-23', 'sm5a'),
    ('im-53.bin', 'cb820c32', 'Ataka asteroidov (IM-53)', '1992-Ataka asteroidov-IM-53', 'sm5a'),
    ('im-55.bin', '006f82d0', 'Basketbol (IM-55)', '199x-Basketbol-IM-55', 'sm5a'),
    ('ecircus.bin', 'cb820c32', 'Circus (Elektronika)', '19xx-Circus-Elektronika', 'sm5a'),
    ('im-50.bin', 'cb820c32', 'Kosmicheskiy polyot (IM-50)', '19xx-Kosmicheskiy polyot-IM-50', 'sm5a'),
    ('im-51.bin', 'cb820c32', 'Morskaya ataka (IM-51)', '19xx-Morskaya ataka-IM-51', 'sm5a'),
    ('im-49.bin', 'cb820c32', 'Nochnye vorishki (IM-49)', '19xx-Nochnye vorishki-IM-49', 'sm5a'),
    # Nauchpribor (USSR)
    ('dbgb-06i.bin', '7e5bf42b', 'Altair (DBGB-06I)', '1991-Altair-DBGB-06I', 'sm5a'),
    # Tiger Electronics
    ('581', 'f6bd105f', "Castlevania II - Simon's Quest (7-781)", "1988-Castlevania II - Simon's Quest-7-781", 'sm510'),
    ('593', '2642f778', 'Double Dragon (7-780)', '1988-Double Dragon-7-780', 'sm510'),
    ('583', '598d8156', 'Gauntlet (7-778)', '1988-Gauntlet-7-778', 'sm510'),
    ('582', 'cee85bdd', 'Karnov (7-783)', '1988-Karnov-7-783', 'sm510'),
    ('597', '8b7acc97', 'Batman (7-799)', '1989-Batman-7-799', 'sm510'),
    ('m82', '278eafb0', 'Ninja Gaiden (7-787)', '1989-Ninja Gaiden-7-787', 'sm510'),
    ('595', 'b574d16f', 'Vindicators (7-786)', '1989-Vindicators-7-786', 'sm510'),
    ('m88', '1b3d15e7', 'Altered Beast (7-831)', '1990-Altered Beast-7-831', 'sm510'),
    ('m84', 'fe4d3618', 'Double Dragon II - The Revenge (7-798)', '1990-Double Dragon II - The Revenge-7-798', 'sm510'),
    ('m94', 'af183fbf', 'Golden Axe (7-817)', '1990-Golden Axe-7-817', 'sm510'),
    ('m96', '3704b60c', 'Robocop 2 (7-830)', '1990-Robocop 2-7-830', 'sm510'),
    ('m91', 'b207ac79', 'Space Harrier II (7-814)', '1990-Space Harrier II-7-814', 'sm510'),
    ('m92', '4b488e8f', 'Strider (7-815)', '1990-Strider-7-815', 'sm510'),
    ('mb3', '8fa4c55a', 'Battletoads (7-868)', '1991-Battletoads-7-868', 'sm510'),
    ('ma6', '8e2da0d9', 'Double Dragon 3 - The Rosetta Stone (7-858)', '1991-Double Dragon 3 - The Rosetta Stone-7-858', 'sm510'),
    ('mb7', '7eb1a6e2', 'Hook (7-869)', '1991-Hook-7-869', 'sm510'),
    ('ma4', '851ef37a', 'Mega Man 3 (7-834)', '1991-Mega Man 3-7-834', 'sm510'),
    ('ma8', '8470a539', 'Pit-Fighter (7-863)', '1991-Pit-Fighter-7-863', 'sm510'),
    ('583', '598d8156', 'Robin Hood (7-861)', '1991-Robin Hood-7-861', 'sm510'),
    ('ma5', '2624daed', 'Spider-Man (7-853)', '1991-Spider-Man-7-853', 'sm510'),
    ('ma2', '764b3757', 'Street Fighter 2010 - The Final Fight (7-837)', '1991-Street Fighter 2010 - The Final Fight-7-837', 'sm510'),
    ('mb0', '8433530c', 'Swamp Thing (7-851)', '1991-Swamp Thing-7-851', 'sm510'),
    ('mb5', 'f7f1d082', 'The Flash (7-859)', '1991-The Flash-7-859', 'sm510'),
    ('m96', '3704b60c', 'The Rocketeer (7-864)', '1991-The Rocketeer-7-864', 'sm510'),
    ('ma7', '6f3ff34f', 'X-Men (7-854)', '1991-X-Men-7-854', 'sm510'),
    ('mc3', '9c37a23c', 'Back to the Future (7-809)', '1992-Back to the Future-7-809', 'sm510'),
    ('mc7', 'eceda335', 'Home Alone (78-502)', '1992-Home Alone-78-502', 'sm510'),
    ('md7', 'ac8a21e9', 'Home Alone 2 - Lost in New York (78-506)', '1992-Home Alone 2 - Lost in New York-78-506', 'sm510'),
    ('md6', '00037018', 'Ninja Gaiden III (78-503)', '1992-Ninja Gaiden III-78-503', 'sm510'),
    ('mc6', '07b44e4c', 'Robocop 3 (78-514)', '1992-Robocop 3-78-514', 'sm510'),
    ('mc2', 'af33d432', 'The Addams Family (7-829)', '1992-The Addams Family-7-829', 'sm510'),
    ('me7', 'dcb16d98', "Wayne's World (78-523)", "1992-Wayne's World-78-523", 'sm510'),
    ('mf9', 'd95f54d5', 'Dennis the Menace (78-532)', '1993-Dennis the Menace-78-532', 'sm510'),
    ('mf4', 'f66faf73', 'Jurassic Park (78-524)', '1993-Jurassic Park-78-524', 'sm510'),
    ('mg6', 'f6375dc7', 'Mortal Kombat (78-553)', '1993-Mortal Kombat-78-553', 'sm510'),
    ('mg0', '5ef21421', 'Nightmare Before Christmas (78-537)', '1993-Nightmare Before Christmas-78-537', 'sm510'),
    ('me1', '73384e94', 'Street Fighter II (78-522)', '1993-Street Fighter II-78-522', 'sm510'),
    ('mf5', '264c8e82', 'Super Double Dragon (78-528)', '1993-Super Double Dragon-78-528', 'sm510'),
    ('me0', '29efae4a', 'The Incredible Crash Dummies (78-516)', '1993-The Incredible Crash Dummies-78-516', 'sm510'),
    ('mg2', '65c0f456', 'Transformers - Generation 2 (78-541)', '1993-Transformers - Generation 2-78-541', 'sm510'),
    ('md3', '11c2b09a', 'X-Men - Project X (78-504)', '1993-X-Men - Project X-78-504', 'sm510'),
    ('mj1', 'ccc196cf', 'Operation - Aliens (78-552)', '1994-Operation - Aliens-78-552', 'sm510'),
    ('mk0', 'dc7827a1', 'Skeleton Warriors - The Dark Crusade (78-569)', '1994-Skeleton Warriors - The Dark Crusade-78-569', 'sm510'),
    ('mj5', '09822d73', 'The Shadow (78-559)', '1994-The Shadow-78-559', 'sm510'),
    ('10_07', '63d0deaa', 'Apollo 13 (78-591)', '1995-Apollo 13-78-591', 'sm510'),
    ('mk3', '9993c382', 'Batman Forever - Double Dose of Doom (78-572)', '1995-Batman Forever - Double Dose of Doom-78-572', 'sm510'),
    ('mk5', '7beee5a7', 'Judge Dredd (78-581)', '1995-Judge Dredd-78-581', 'sm510'),
    ('10_06', 'fe053efb', '007 - GoldenEye (78-594)', '1996-007 - GoldenEye-78-594', 'sm510'),
    ('10_16', '77c2c2f7', 'Independence Day (78-624)', '1996-Independence Day-78-624', 'sm510'),
    ('10_18', 'aa796372', 'Kazaam (78-613)', '1996-Kazaam-78-613', 'sm510'),
    ('10_23', '6eaabfbd', 'Space Jam (78-621)', '1996-Space Jam-78-621', 'sm510'),
]
# each chip: its ROM size and where the emulator expects the ROM
# Games whose own MAME set is artwork only, because they share another game's ROM.
# Regenerated by tools/register_games.py.  set name -> (game, ROM set to download, that game).
CLONES = {
    'atakaast': ('Ataka asteroidov (IM-53)', 'gnw_mmouse', 'Mickey Mouse (MC-25)'),
    'biathlon': ('Biathlon (IM-19)', 'gnw_mmouse', 'Mickey Mouse (MC-25)'),
    'ecircus': ('Circus (Elektronika)', 'gnw_mmouse', 'Mickey Mouse (MC-25)'),
    'ehockey': ('Hockey (IM-10)', 'gnw_mmouse', 'Mickey Mouse (MC-25)'),
    'gnw_egg': ('Egg (EG-26)', 'gnw_mmouse', 'Mickey Mouse (MC-25)'),
    'kosmicmt': ('Kosmicheskiy most (IM-09)', 'gnw_fire', 'Fire (FR-27)'),
    'kosmicpt': ('Kosmicheskiy polyot (IM-50)', 'gnw_mmouse', 'Mickey Mouse (MC-25)'),
    'krybolov': ('Kot-rybolov (IM-32)', 'gnw_mmouse', 'Mickey Mouse (MC-25)'),
    'kvakazad': ('Kvaka-zadavaka (IM-33)', 'gnw_mmouse', 'Mickey Mouse (MC-25)'),
    'morataka': ('Morskaya ataka (IM-51)', 'gnw_mmouse', 'Mickey Mouse (MC-25)'),
    'nochnyev': ('Nochnye vorishki (IM-49)', 'gnw_mmouse', 'Mickey Mouse (MC-25)'),
    'nupogodi': ('Nu, pogodi! (IM-02)', 'gnw_mmouse', 'Mickey Mouse (MC-25)'),
    'okhota': ('Okhota (IM-16)', 'gnw_mmouse', 'Mickey Mouse (MC-25)'),
    'taynyoke': ('Tayny okeana (IM-03)', 'gnw_octopus', 'Octopus (OC-22)'),
    'tigarden': ('Thief in Garden (TG-18)', 'trshutvoy', 'Shuttle Voyage (MG-8)'),
    'trclchick': ('Clever Chicken (CC-38V)', 'trdivadv', "Diver's Adventure (DA-37)"),
    'trobhood': ('Robin Hood (7-861)', 'tgaunt', 'Gauntlet (7-778)'),
    'trockteer': ('The Rocketeer (7-864)', 'trobocop2', 'Robocop 2 (7-830)'),
    'trspider': ('Spider (SG-21)', 'trspacmis', 'Space Mission (SM-11)'),
    'trthuball': ('Thunder Ball (FR-23)', 'trsrescue', 'Space Rescue (MG-9)'),
    'vespovar': ('Vesyolyy povar (IM-04)', 'gnw_chef', 'Chef (FP-24)'),
    'vfutbol': ('Vesyolye futbolisty (IM-22)', 'gnw_mmouse', 'Mickey Mouse (MC-25)'),
}

CHIPS = {'sm510': (4096, 0x8000), 'sm5a': (0x740, 0x8000)}


def std_block(flag, payload, pause_ms):
    data = bytes([flag]) + payload
    c = 0
    for b in data:
        c ^= b
    data += bytes([c])
    return b'\x10' + struct.pack('<HH', pause_ms, len(data)) + data


def block2_tzx(rom, game, at):
    """A tape holding one CODE block: the ROM at `at`, named <MODEL-NO>-rom (from "Game Name (MODEL-NO)")."""
    name = (game.rsplit('(', 1)[1].rstrip(')') + '-rom').encode('ascii')[:10].ljust(10, b' ')
    header = bytes([3]) + name + struct.pack('<HHH', len(rom), at, 32768)
    return b'ZXTape!\x1a\x01\x14' + std_block(0x00, header, 500) + std_block(0xFF, rom, 1000)


class Problem(Exception):
    """A gentle, already-worded message for the person running the program."""


def say(lines):
    """Print a friendly message, set off by blank lines."""
    print()
    print('\n'.join(lines))
    print()


def crc_of(data):
    return '%08x' % (zlib.crc32(data) & 0xFFFFFFFF)


def find_rom(z, src, game=None):
    """(rom bytes, table entry) from an open ZIP.  `game` is the wanted "Game Name (MODEL-NO)"
    (any case) when a ROM is shared by two games.  Raises Problem with a ready-to-show message."""
    here = os.path.basename(src)
    members = [n for n in z.namelist() if not n.endswith('/')]
    inside = ', '.join(os.path.basename(n) for n in members) or '(nothing)'

    if game:
        picked = [g for g in GAMES if g[2].lower() == game.lower()]
        if not picked:
            import difflib
            near = difflib.get_close_matches(game, [g[2] for g in GAMES], n=3, cutoff=0.4)
            tail = (['Did you mean one of these?'] + ['    ' + m for m in near]) if near else \
                   ['The exact game names (with their model numbers) are listed in the README.']
            raise Problem(['I do not have a game called:  %s' % game,
                           'Type the name exactly as in the README, inside quotes, like this:',
                           '    python make_block2.py --as "Robin Hood (7-861)"  tgaunt.zip'] + tail)
        g = picked[0]
        for n in members:
            data = z.read(n)
            if crc_of(data) == g[1]:
                return data, g
        raise Problem(['I opened  %s  but the ROM for  %s  is not inside it.' % (here, g[2]),
                       'In this .zip I can see:  %s' % inside,
                       'Make sure you downloaded the right ROM set for that game (see the README).'])

    # no --as: exact match (file name + contents), then by contents, then by name (older version)
    for n in members:
        data = z.read(n)
        for g in GAMES:
            if g[0] == os.path.basename(n).lower() and g[1] == crc_of(data):
                return data, g
    by_crc = {}
    for g in GAMES:
        by_crc.setdefault(g[1], g)
    for n in members:
        data = z.read(n)
        g = by_crc.get(crc_of(data))
        if g:
            return data, g
    by_name = {g[0]: g for g in GAMES}
    for n in members:
        g = by_name.get(os.path.basename(n).lower())
        if g:
            data = z.read(n)
            if len(data) != CHIPS[g[4]][0]:
                raise Problem(['The file  %s  inside  %s  is not the right size' % (os.path.basename(n), here),
                               '(it is %d bytes; the ROM should be %d).' % (len(data), CHIPS[g[4]][0]),
                               'The .zip may be damaged — try downloading it again.'])
            print()
            print('Note: the ROM in this .zip is a slightly different version than expected.')
            print('      I have still made the tape.  If the game shows a red border and stops,')
            print('      you need the exact ROM set listed for it in the README.')
            return data, g

    for n in members:                   # an artwork-only set for a game that shares another's ROM?
        base = os.path.splitext(os.path.basename(n))[0].lower()
        if base in CLONES:
            cgame, parentset, pgame = CLONES[base]
            raise Problem(['%s  is only the artwork for  %s  -  there is no ROM inside it.' % (here, cgame),
                           '%s  uses the same ROM as  %s,' % (cgame, pgame),
                           'so download  %s.zip  and run this exact command:' % parentset,
                           '    python make_block2.py --as "%s"  %s.zip' % (cgame, parentset)])
    raise Problem(['I opened  %s  but could not find a Game & Watch ROM inside it.' % here,
                   'In this .zip I can see:  %s' % inside,
                   '',
                   'This might not be the right .zip.  Check its name against the list in the',
                   'README and download the one for the game you want.  (A few games share another',
                   'game\'s ROM and come as artwork only; for those, download the main game\'s set',
                   'and add  --as "Game Name (MODEL)".)'])


USAGE = [
    'make_block2.py  -  makes the ROM tape (block 2) for a Game & Watch game.',
    '',
    'What to do:',
    '  1.  Download the game\'s ROM set .zip  (the file names are listed in the README).',
    '  2.  Put it in the same folder as this program.',
    '  3.  Type this and press Enter:',
    '          python make_block2.py  gnw_mario.zip',
    '',
    '      (use the name of the .zip you downloaded).  On Windows you can type',
    '          python make_block2.py',
    '      then a space, then drag the .zip onto the window and press Enter.',
    '',
    'You can list several .zip files at once.',
    'For a game that shares another game\'s ROM, add  --as "Game Name (MODEL)".',
]


def one(src, want):
    """Make the tape for a single .zip; raise Problem on anything the user can fix."""
    if os.path.isdir(src):
        raise Problem(['%s  is a folder, not a .zip file.' % src,
                       'Point me at the .zip you downloaded, like:',
                       '    python make_block2.py  gnw_mario.zip'])
    if not os.path.exists(src):
        raise Problem(['I cannot find a file called:  %s' % src,
                       'Check the name is spelled exactly right (including the  .zip  at the end)',
                       'and that the file is in this folder.  Tip: on Windows, type',
                       '    python make_block2.py',
                       'then a space, then drag the .zip onto the window.'])
    try:
        z = zipfile.ZipFile(src)
    except zipfile.BadZipFile:
        raise Problem(['%s  is not a .zip file I can open.' % os.path.basename(src),
                       'It may be the wrong file, or the download did not finish.',
                       'Download the ROM set again and run this on the new .zip.'])
    with z:
        rom, (_, _, game, name, chip) = find_rom(z, src, want)
    out = os.path.join(os.path.dirname(os.path.abspath(src)), name + '-block2.tzx')
    with open(out, 'wb') as f:
        f.write(block2_tzx(rom, game, CHIPS[chip][1]))
    print()
    print('Done!  I made the ROM tape for  %s' % game)
    print('    ->  %s' % out)
    print('Load that game\'s public tape first; when it says "Now block 2: the ROM", play this tape.')


def main():
    args = sys.argv[1:]
    want = None
    if args[:1] == ['--as']:
        if len(args) < 2 or not args[1].strip():
            say(['After  --as  you need the game name in quotes, like:',
                 '    python make_block2.py --as "Robin Hood (7-861)"  tgaunt.zip'])
            sys.exit(1)
        want, args = args[1], args[2:]
    if not args:
        say(USAGE)
        sys.exit(1)

    failed = 0
    for src in args:
        try:
            one(src, want)
        except Problem as e:
            say(e.args[0])
            failed += 1
        except PermissionError:
            say(['I am not allowed to read or write near  %s.' % src,
                 'Try moving the .zip to your Desktop or Documents folder, then run it there.'])
            failed += 1
        except OSError as e:
            say(['Something went wrong with  %s:' % src, '    %s' % e,
                 'Try downloading the .zip again, or move it to a simple folder like your Desktop.'])
            failed += 1
    if failed:
        sys.exit(1)


if __name__ == '__main__':
    main()
