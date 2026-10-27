# Game & Watch on the ZX Spectrum 48K

https://github.com/user-attachments/assets/6002bfec-042c-406d-9c05-a8ce425c4b6c

*Mario Bros. (MW-56) running on a ZX Spectrum 48K.*

**Nintendo Game & Watch LCD handhelds on the ZX Spectrum 48K**: a cycle-accurate Sharp SM510 emulator
written in Z80 assembly, with ready-to-load TZX tapes for 18 Game & Watch models and Munchy, an original
Pac-Man-style Game & Watch game with a clock and alarm. Runs on real Spectrums and in emulators.

Each tape here contains a loader and block 1. Block 1 holds the emulator (a Sharp SM510 emulator in
Z80, plus a Spectrum host) and the screen graphics drawn for the Spectrum. The game program itself, the
4 KB ROM of the original handheld, is not included. You supply it as a second tape, made from your own
MAME set.

## Making the ROM tape

    python make_block2.py gnw_tbridge.zip

This takes a MAME Game & Watch set: the ZIP holding the ROM image and its LCD artwork. Only the ROM is
used. The tool writes `<year>-<Game Name>-<MODEL-NO>-block2.tzx` next to the ZIP. You can give it several
ZIPs at once. It needs only Python 3.

## Loading

1. `LOAD ""` and play the public tape of the game. It loads block 1, then prints `Now block 2: the ROM`.
2. Play the block 2 tape for the **same** game.
3. The game starts. A red border and a stop mean the ROM is missing, is for another game, or is a
   revision the tape was not built for.

## Supported sets

| MAME set | ROM | Game |
|---|---|---|
| gnw_tbridge | tl-28 | Turtle Bridge (TL-28) |
| gnw_fireatk | id-29 | Fire Attack (ID-29) |
| gnw_stennis | sp-30 | Snoopy Tennis (SP-30) |
| gnw_opanic | op-51 | Oil Panic (OP-51) |
| gnw_dkong | dk-52 | Donkey Kong (DK-52) |
| gnw_mickdon | dm-53_565 | Mickey & Donald (DM-53) |
| gnw_ghouse | gh-54 | Green House (GH-54) |
| gnw_dkong2 | jr-55_560 | Donkey Kong II (JR-55) |
| gnw_mario | mw-56 | Mario Bros. (MW-56) |
| gnw_rshower | lp-57 | Rain Shower (LP-57) |
| gnw_lboat | tc-58 | Life Boat (TC-58) |
| gnw_squish | mg-61 | Squish (MG-61) |
| gnw_dkjr | dj-101 | Donkey Kong Jr. (DJ-101) |
| gnw_mariocm | ml-102_577 | Mario's Cement Factory (ML-102) |
| gnw_manhole | nh-103 | Manhole (NH-103) |
| gnw_tfish | tf-104 | Tropical Fish (TF-104) |
| gnw_ssparky | bu-201 | Spitball Sparky (BU-201) |
| gnw_cgrab | ud-202 | Crab Grab (UD-202) |

Two tapes are complete and need no ROM tape, because their programs are our own:
- `demo.tzx`: a small demo program;
- `originals/2026-Munchy-MU-01.tzx`: Munchy, an original Game & Watch style maze game, with its own
  program, drawings and sounds.

Munchy's keys are Q / A / O / P (or 9 / 8 / 6 / 7) to move, 1 for Game A, 2 for Game B (faster), and
ENTER for ACL.

## A short history of Game & Watch

In 1980 Nintendo engineer **Gunpei Yokoi** is said to have watched a bored businessman on the
Shinkansen killing time by poking at a pocket calculator. Yokoi's thought: what if that calculator
were a game? The result was **Game & Watch**, a credit-card-sized LCD handheld that played one game
and, because a gadget in 1980 had to earn its keep, was also a clock with an alarm. Hence the name.

The screens came from the same liquid-crystal technology Sharp was putting into calculators, and the
brains were Sharp's tiny 4-bit microcontrollers. The SM510 used by most of the later models has
4 KB of program ROM, 128 four-bit cells of RAM, and a leisurely 16,384 clock cycles a second.
Every figure on the screen is a fixed LCD segment printed in place: Mario does not move, he simply
appears in the next pose. That is why Game & Watch characters "teleport" with that unmistakable
click-click rhythm.

The line ran from 1980 to 1991, sold over 40 million units, and grew through several series:
Silver and Gold, **Wide Screen**, the clamshell **Multi Screen** (two screens hinged together, a
shape Nintendo returned to with the DS twenty years later), **New Wide Screen**, Tabletop, Panorama
and **Super Color**. The 1982 Multi Screen *Donkey Kong* introduced the cross-shaped directional pad,
the "+" button that ended up on almost every game controller since. In 2020 Nintendo even released a
new Game & Watch for the 35th anniversary of *Super Mario Bros.*

Almost every model has **Game A** and **Game B** (B is the "you thought A was hard?" mode), a miss
counter, and in many games a reward at 200 or 500 points that wipes your misses away, sometimes with
a "chance time" of double points. The ACL button, pressed with a pen tip, resets the whole thing,
including the clock you just set.

## The games on these tapes

Eighteen Game & Watch models built on the Sharp SM510, each in a sentence or two:

- **Turtle Bridge (TL-28, 1982)**: deliver parcels across a river on the backs of turtles. The turtles
  have their own priorities and dive for fish at the worst possible moment.
- **Fire Attack (ID-29, 1982)**: defend a wooden fort from attackers lobbing torches. A fire brigade of
  one, with a very small bucket.
- **Snoopy Tennis (SP-30, 1982)**: Snoopy, racket in paw, returning the balls Lucy keeps sending his
  way. Lucy has never once in her life lost an argument, and she does not intend to lose this one.
- **Oil Panic (OP-51, 1982)**: catch oil leaking from a gas-station ceiling and pour it to your boss
  below, while customers stroll past at exactly the wrong time.
- **Donkey Kong (DK-52, 1982)**: Mario climbs the girders to rescue Pauline, on the model that gave the
  world the D-pad.
- **Mickey & Donald (DM-53, 1982)**: Mickey and Donald fight a fire with a hose that springs leaks
  faster than two people can plug them.
- **Green House (GH-54, 1982)**: an exterminator keeps caterpillars and spiders off the flowers on two
  floors at once.
- **Donkey Kong II (JR-55, 1983)**: Donkey Kong Jr. sets out to free his father, which in Game & Watch
  logic means a lot of keys and a lot of jumping.
- **Mario Bros. (MW-56, 1983)**: Mario and Luigi on the conveyor belts of a bottling plant. Drop a
  crate and the boss gives you a telling-off on screen. Fill the truck and you both get a break.
- **Rain Shower (LP-57, 1983)**: rescue the washing from four clothes lines before the rain gets it.
  British players will find this one realistic.
- **Life Boat (TC-58, 1983)**: catch people jumping from a burning ship in a rowing boat and paddle them
  to shore. Nobody jumps in an orderly queue.
- **Squish (MG-61, 1986)**: a creature trapped between closing walls of a crushing machine; keep the
  walls back and eat the bugs.
- **Donkey Kong Jr. (DJ-101, 1982)**: vines, keys, snapping traps and birds, on the New Wide Screen.
- **Mario's Cement Factory (ML-102, 1983)**: Mario runs the cement hoppers. Overfill one and a truck
  driver gets a lapful of concrete.
- **Manhole (NH-103, 1983)**: hold the covers in place under pedestrians who never look where they are
  walking.
- **Tropical Fish (TF-104, 1985)**: catch fish leaping between fish bowls. The fish are not grateful.
- **Spitball Sparky (BU-201, 1984)**: a breakout-style game on the Super Color series: keep a spitball
  in the air and knock out the blocks.
- **Crab Grab (UD-202, 1984)**: crabs on the march, a player outnumbered, and all of it in colour on
  the Super Color series.

And one that never existed until now: **Munchy (MU-01)**, an original Game & Watch style maze game made
for this collection, with its own program for the SM510, its own LCD drawings and sounds, a clock, an
alarm, and a demo that plays itself while the clock runs, just like the real thing.

## How it works

The ZX Spectrum's Z80 runs a full emulation of the Sharp SM510: every instruction, the clock divider,
the keyboard matrix, the LCD and the buzzer, paced to the original chip's real speed. The LCD is
redrawn on the Spectrum screen segment by segment, from graphics drawn for each game at the Spectrum's
resolution. The original game program, the 4 KB ROM, is loaded from a separate tape that you make from
your own copy, so each game runs its genuine program, beep for beep.

Game & Watch, Nintendo and the game titles above are trademarks of their owners; this project is not
affiliated with or endorsed by Nintendo. See [LICENSE](LICENSE).
