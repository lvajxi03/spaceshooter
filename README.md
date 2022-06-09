# SpaceShooter

Simple shooter game prototype. Written in `Python`, utilizes `PySide` library capabilities.

Not decided yet what will be the target platform and SDK: C++/SDL/multiplatform or C++/WinAPI only.

## Description and play

Very simple space shooter, made as a cooperation with my son, Antoni.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/plLSaAU3At8/0.jpg)](https://www.youtube.com/watch?v=plLSaAU3At8)

Goal: shoot down all the enemies and the boss at the end.

Game contains 5 levels (so far!) and all of them produces few sets of enemies to shoot down.

Enemies can also shoot you, same as the guns at the bottom.

Watch the drops falling down, which are also deadly.

You have 3 life points (drawn as 3 little rockets at the bottom), all of them is worth of 10 minipoints
(also seen there) -- whenever you lost all 10 small points, you loose main life point. No life points means you're dead.

You can shoot your enemies and also the guns. You can use bombs to do this as well (however, bombs are significantly)
slower.

Boss appears at the end and can shoot at you with 3 streams of missiles.

Several items are quite useful and can be collected:
* `tnt box` -- allows to use `TNT` (shoot down 3 enemies at once)
* `lightball` -- allows you to use 3 streams of light missiles (for 10s)
* `shield` -- you can be immortal (for 10s)
* `medical kit` -- can increase your minipoints
* `icebox` -- can freeze all the enemies (for 10s)

## Installation and configuration

All you need to do is

```bash
$ python -m pip install spaceshooter
```

`PySide6` will also be installed as it's required to run.

## Running

Running is as easy as typing

```bash
$ python -m spaceshooter
```

in your terminal.

Default font is ugly, so please download some free `TTF` file that resembles you the 80s and install.
Then, please let the program know about it -- use `-f "font name"` in the command line:

```bash
python -m spaceshooter -f "Best font I found in all the Internets"
```

Remember about the quotes!

On the next run, font will be used again, as it's stored in the configuration file now.

To reset all the settings (including hi scores, so beware!), you may use:

```bash
python -m spaceshooter -r
```

This will run the program with default settings.

Options can be combined.

### Windowing mode

By default, application is using full screen to display its content. To run this in windowing mode, please use `-w` parameter:

```bash
python -m spaceshooter -w
```

This one:
```bash
$ python -m spaceshooter -h
```
gives you the full list of available options and their arguments.

## Navigation

### Menu

You can use `up/down arrow` keys and `Enter` to select a menu option, as well as mouse left button.
Language icons are available only with mouse.

Also `q` terminates the program.

### Ship selection

You can use `left/right arrow` keys and `Enter` to select you ship, as well as mouse left button.
Language icons are available only with mouse.

### Other screens

Follow the status line about available keys and actions.

### Game play

Default keys are as follows:

* `up/down/left/right arrows` for ship navigation
* `space` for missiles
* `b` for bombs
* `t` for TNTs, if available
* `ESC` for pause
* `q` for leaving game and back to the menu

You can reconfigure navigation keys, missiles, bombs and TNTs.

## Other

No, there is no sound. Maybe later.
