# RhinoTools
## Custom tools for Rhino

### Description:
These tools are created to enhance the working with Rhino.

### Current Tools:

## Block Tools:

## ResetBlockScale:
Resets the scale of a block, keeping the rotation around the insertion point.
Inspired by the ResetBlock script by Dale Fugier. Thank you.

## MakeUnique:
Takes one or many blocks and creates a unique copy with own block definitions.

## SelectSameBlocks:
Selects alle the blocks with the same definition as the selected blocks.

### Installation:
With each file comes installation instructions.
As a general rule of thumb:
* All python files are installed by copying to the Rhino script folder. ie.: C:\Users\"USER"\AppData\Roaming\McNeel\Rhinoceros\5.0\scripts

Options to use the function:
1. Recommended: Import the bundled "Block Tools.rui" toolbar with readymade buttons to call the functions.
2. Add a new button with the following macro: ( _NoEcho !-_RunPythonScript "MakeUnique.py" _Echo )
3. Add an alias with the above command
3. Call the script directly by using this command: "-RunPythonScript MakeUnique.py"

_If any Rhino developers read this:
It would be nice to be able to register python scripts to run on startup. That way we can do away with the whole inport ".rui" files thing...
And maybe drag and drop support so .py files are same citizens as .rvb scripts..? Pirty pwease..?_

For examples and more info a blog post is coming soon.


