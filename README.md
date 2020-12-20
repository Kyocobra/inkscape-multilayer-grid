# inkscape-multilayer-grid
## Arrange objects into grids that overflow onto new layers (Inkscape 1.0.X)
I use this for arranging 50+ playing card scans into 3x3 grids onto several layers. I use [inkscape-export-layers](https://github.com/Kyocobra/inkscape-export-layers) to export these layers into PDFs for printing.

## Installation
- **Install this extension** by dropping the .inx and .py files directly into: C:\Users\John Smith\AppData\Roaming\inkscape\extensions
- This is not backwards compatible with Inkscape 0.9X.X. You can check your current Inkscape version in **Help > About Inkscape** from Inkscape's top menu bar.

## Usage
First, **SAVE YOUR FILE!** Moving a large number of objects can cause Inkscape to crash!

Once your objects are selected:
1. Go to **Extensions > Arrange > Multilayer Grid**
2. Choose rows and columns of grid
3. Set maximum number of layers to process (i.e., up to n = (rows * cols * layers) objects are arranged)

## Note:
- Objects are arranged by their z-axis order (lowest first)
- Grid dimensions are determined by sampling the width and height of the lowest object
- There is no "spacing" feature; objects placements are calculated to directly contact assuming all objects have the same dimensions as the lowest
- Grid is centered on page
- Using this extension on the same object multiple times will exhibit odd behavior. This extension takes the current location of an object and "translates" it to specific position on the page. Inkscape then saves (i) the original position and (ii) the translation. It uses these to calculate the current position. However, subsequent translations overwrite the current translation, rather than add to it, causing objects to move around unexpectedly. Not sure how to fix that bug, but you can reset a translation by moving an object manually.
