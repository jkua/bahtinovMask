# Bahtinov mask generator
This is a Python 3 script for generating Bahtinov mask design files for a laser 
cutter such as a GlowForge. Bahtinov masks are used in astrophotography to 
set the focus.

The output is an SVG file with a set of paths in blue for the mask lines, 
intended to be scored, and an outline path in red, intended to be cut.

This should be fabricated from a thin, transparent plastic.

The `samples` folder contains a sample of the default output, a 100 mm square 
mask with 1 mm line spacing, 20 deg mask angle, and 5 mm rounded corners.

## Install requirements
`pip3 install -r requirements.txt`

## Run
`./bahtinovMask.py --size <size in mm> --spacing <line spacing in mm> --angle <mask angle in deg> --cornerRadius <corner radius in mm>`

Options
* `--size` height and width of the mask in mm. Defaults to 100 mm.
* `--spacing` space between the horizontal lines on the mask. Defaults to 1 mm
* `--angle` mask angle in degrees. Defaults to 20 deg.
* `--cornerRadius` rounds the corner of the mask. Defaults to 5 mm.



