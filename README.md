#RhinoTools:

## Description:
These tools are created to enhance the working with Rhino.
For examples and more info a blog post is coming soon.
Current Version: 1.1


## Current Tools:
###BlockTools:
#### ResetBlockScale:
Resets the scale of a block, keeping the rotation around the insertion point.
Inspired by the ResetBlock script by Dale Fugier. Thank you.
#### MakeUnique:
Takes one or many blocks and creates a unique copy with own block definitions.
#### SelectSameBlocks:
Selects all the blocks with the same definition as the selected blocks.


## Installation:
    1. Download the .rhi file found in the installer folder.
    2. Doubleclick it or drag drop into rhino window.
    3. Optionally drag drop the matching .rui file from the UI folder into window to get a toolbar.
    4. Enjoy.

## How to use:
    Run with the following commands as normal or use the buttons from the toolbar files (.rui)
    
## Known issues:
    1. If a block is scale negatively (like -1) and you use the make unique it will flip it back to normal scale (1).
    I will work on fixing this as soon as time permits.
    
## Uninstall:
    To uninstall the plugin remove the BlockTools folder from the plugin folder.
    Ie. on windows found here:
    "C:\Users\[USERNAME]\AppData\Roaming\McNeel\Rhinoceros\5.0\Plug-ins"

## Further info:
See the [WIKI](https://github.com/ejnaren/rhinotools/wiki)


