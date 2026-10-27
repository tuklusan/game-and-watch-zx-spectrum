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
