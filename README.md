# JumpCutter GUI

**Automatically edits videos. [Explanation](https://www.youtube.com/watch?v=DQ8orIurGxw)**

This fork of [the original by CaryKH](https://github.com/carykh/jumpcutter) adds a Tkinter-based GUI for easier usage.

For a more polished version of this software that Cary and friends have been working on for the last year or so, visit [JumpCutter.com](https://jumpcutter.com/)

![Running on Ubuntu 20.04 with GNOME](https://user-images.githubusercontent.com/61561933/118718115-cc3cd300-b81e-11eb-8600-a0672cffe0a1.png)

## Installing

PyInstaller builds are available on [the GitHub releases page](https://github.com/19wintersp/JumpCutterGUI/releases/latest) of the repository, and contain executables for each platform. Download the one for your platform, and run it.

## Some heads-up

It uses Python 3.

It works on Ubuntu 16.04 and Windows 10. (It might work on other OSs too, we just haven't tested it yet.)

This program relies heavily on ffmpeg. It will start subprocesses that call ffmpeg, so be aware of that!

As the program runs, it saves every frame of the video as an image file in a
temporary folder. If your video is long, this could take a LOT of space.
I have processed 17-minute videos completely fine, but be wary if you're gonna go longer.

## Building with nix

`nix-build` to get a script with all the libraries and ffmpeg, `nix-build -A bundle` to get a single binary. (this has not been tested on this fork)
