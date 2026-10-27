# Game & Watch on the ZX Spectrum 48K

https://github.com/user-attachments/assets/6002bfec-042c-406d-9c05-a8ce425c4b6c

*Mario Bros. (MW-56) running on a ZX Spectrum 48K.*

**Nintendo Game & Watch LCD handhelds on the ZX Spectrum 48K**: a cycle-accurate Sharp SM510 emulator
written in Z80 assembly, with ready-to-load TZX tapes for 18 Game & Watch models and Munchy, an original
Pac-Man-style Game & Watch game with a clock and alarm. Runs on real Spectrums and in emulators.

Each tape here contains a loader and block 1. Block 1 holds the emulator (a Sharp SM510 emulator running
on the 48K ZX Spectrum) and the screen graphics drawn for the Spectrum. The game program itself, the 4
KB ROM of the original handheld, is not included. You supply it as a second tape, made from your own
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

In 1980, the story goes, Nintendo engineer **Gunpei Yokoi** watched a bored businessman on the
Shinkansen pass the time by prodding at a pocket calculator. Yokoi wondered what would happen if the
calculator were a game. The answer was **Game & Watch**, a credit-card-sized LCD handheld that played
one game. Because a gadget in 1980 had to earn its keep, it also told the time and woke you up.
Necessity may be the mother of invention, but boredom is its favourite uncle.

The screens used the liquid crystal Sharp was already putting into calculators, and the brains were
Sharp's 4-bit microcontrollers. The SM510, inside most of the later models, has 4 KB of program ROM,
128 four-bit cells of RAM and a clock of 16,384 cycles a second. Every figure is a segment printed in
place, so Mario never walks: he simply appears in his next pose. Animation is optional when
imagination is included.

The line ran from 1980 to 1991 and sold more than 40 million units, in series from Silver and Gold
through **Wide Screen** and **New Wide Screen** to **Super Color**. The clamshell **Multi Screen**, two
screens on a hinge, is the shape Nintendo came back to with the DS twenty years later. Its 1982 *Donkey
Kong* introduced the cross-shaped "+" pad that has sat on nearly every controller since. Good ideas
never age; they just wait for better batteries.

Nearly every model has **Game A** and **Game B**, where B is A with the gloves off. Most count your
misses, and many forgive them all at 200 or 500 points, sometimes with a spell of double points. The
ACL button, pressed with a pen tip, resets everything, including the clock you have just set. Every
reset button is a lesson in reading the manual first.

## The tapes at a glance

![Contact sheet: Munchy (MU-01) at the top, then all 18 Game & Watch models running on the ZX Spectrum 48K: Turtle Bridge, Fire Attack, Snoopy Tennis, Oil Panic, Donkey Kong, Mickey & Donald, Green House, Donkey Kong II, Mario Bros., Rain Shower, Life Boat, Squish, Donkey Kong Jr., Mario's Cement Factory, Manhole, Tropical Fish, Spitball Sparky and Crab Grab](images/game-and-watch-zx-spectrum-contact-sheet.png)

Every screen above is a real capture of the tape running on a 48K ZX Spectrum, a few seconds into Game
A. A picture is worth a thousand words, and a contact sheet is worth nineteen tapes.

## The games on these tapes

Eighteen Game & Watch models built on the Sharp SM510, each with its job and its moral:

- **Turtle Bridge (TL-28, 1982)**: carry parcels across a river on the backs of turtles, who dive for
  fish whenever they feel like it. Never build a bridge out of anyone with a lunch break.
- **Fire Attack (ID-29, 1982)**: defend a wooden fort from attackers hurling torches, one bucket against
  the world. Wood is a fine building material until someone brings matches.
- **Snoopy Tennis (SP-30, 1982)**: Snoopy, racket in paw, takes on Charlie Brown across the net. Good
  grief is the only sensible reply to a beagle with a backhand.
- **Oil Panic (OP-51, 1982)**: catch the oil dripping from a leaking ceiling and pass it down to your
  boss without soaking the customers. Every job is easy until somebody walks underneath it.
- **Donkey Kong (DK-52, 1982)**: Mario climbs the girders to rescue Pauline, on the model that gave the
  world the "+" pad. Some inventions change history; this one also changed your thumb.
- **Mickey & Donald (DM-53, 1982)**: Mickey and Donald fight a fire with a hose that springs leaks
  faster than two can plug them. Teamwork means two people blaming one hose.
- **Green House (GH-54, 1982)**: a gardener with a spray can guards the flowers from caterpillars on one
  floor and spiders on the other. Every garden is a battlefield with better scenery.
- **Donkey Kong II (JR-55, 1983)**: Donkey Kong Jr. sets out to free his father, which in Game & Watch
  terms means keys, chains and a great deal of jumping. Family loyalty is measured in keys collected.
- **Mario Bros. (MW-56, 1983)**: Mario and Luigi keep the crates moving on the conveyor belts of a
  bottling plant, and every dropped one earns a telling-off. Nothing bonds brothers like a boss
  shouting at both of them.
- **Rain Shower (LP-57, 1983)**: pull the washing in from four clothes lines before the rain soaks it.
  British players will recognise it as a documentary.
- **Life Boat (TC-58, 1983)**: row a little boat under a burning ship and catch the passengers as they
  jump. In the whole history of shipwrecks, nobody has ever jumped in an orderly queue.
- **Squish (MG-61, 1986)**: hold back the closing walls of a crushing machine while snacking on the bugs
  that wander in. Personal space is worth fighting for, especially when the walls disagree.
- **Donkey Kong Jr. (DJ-101, 1982)**: Junior swings through the vines, dodging traps and birds, to reach
  the key to his father's cage. A rescue is mostly running in circles with a purpose.
- **Mario's Cement Factory (ML-102, 1983)**: Mario works the cement hoppers, and an overfilled one empties
  onto a truck driver's lap. In construction, timing is everything and concrete forgives nothing.
- **Manhole (NH-103, 1983)**: hold the covers in place under pedestrians who never look where they are
  going. Every city runs on people quietly preventing disasters nobody notices.
- **Tropical Fish (TF-104, 1985)**: catch the fish leaping between bowls before they reach the floor.
  Saving lives is thankless work, especially when the lives are fish.
- **Spitball Sparky (BU-201, 1984)**: keep a spitball in the air and clear the blocks, breakout-style, in
  Super Color. Disgusting and fun are not opposites; they are teammates.
- **Crab Grab (UD-202, 1984)**: the crabs are on the march and you are badly outnumbered, in full Super
  Color. On any beach, the crabs outnumber the people with a plan.

And one that never existed until now: **Munchy (MU-01)**, an original maze game written for the SM510,
with its own drawings and sounds. Like the classics, it keeps time, rings an alarm and plays itself
while nobody is looking. Every collection needs one game nobody has a high score in yet.

## How it works

The Spectrum's Z80 emulates the Sharp SM510 in full, at the original chip's own speed: every
instruction, the clock divider, the keys, the LCD and the buzzer. Each LCD figure appears on the
Spectrum's screen from graphics made for its resolution. The game's own program, the 4 KB ROM, loads
from a tape you make from your own copy, so every game runs its genuine code, beep for beep. Forty years
on, the old programs still know their jobs; they just needed a new office.

Game & Watch, Nintendo and the game titles above are trademarks of their owners; this project is not
affiliated with or endorsed by Nintendo. See [LICENSE](LICENSE).
