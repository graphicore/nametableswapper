# OT Name Table Switcher

Suppose you want to install two very similar fonts on your system, like two different versions of the same font for comparison. You'll find out that there can be only one of these versions installed on the system at the same time.

Changing the file names won't help. This is because the system looks inside the font at the OpenType name table. That table of both your font versions is too similar for your two fonts to coexist installed on the system.

This tool changes the name tables of any font you drop at it. It does so by adding an extra part to the font family name in all places where it matters.

## Try it!

A live instance of this web-app is deployed at:
https://nametableswapper.appspot.com

## Installation instructions

First install the dependencies with:

```
pip install -t app/lib -r requirements.txt
```

And then run the webapp with:

```
dev_appserver.py app/
```

