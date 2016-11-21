"""
@name:          MakeUnique
@description:   Takes one or many blocks and creates a unique copy with own block definitions.
@author:        Ejnar Brendsdal
@version:       1.2
@link:          https://github.com/ejnaren/rhinotools
@notes:         Works with Rhino 5.

@license:

The MIT License (MIT)

Copyright (c) 2016 Ejnar Brendsdal

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


@Installation: Copy to the Rhino script folder. ie.: C:\Users\"USER"\AppData\Roaming\McNeel\Rhinoceros\5.0\scripts
                Options to use the function:
                1. Recommended: Import the bundled "Block Tools" toolbar with readymade buttons to call the functions.
                2. Add a new button with the following macro: ( _NoEcho !-_RunPythonScript "MakeUnique.py" _Echo )
                3. Add an alias with the above command
                3. Call the script directly by using this command: "-RunPythonScript MakeUnique.py"

@Changelog:
    1.1: Make script into a command to be included in the BlockTools part of RhinoTools.
    1.2: Fix scaling bug and retain properties from the original block. lso simplifies the script a lot making it faster by removing a lot of redundant code. Must have been drunk when I wrote the first version...
"""

#******* Imports ********************
#************************************

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.Geometry as G
import re

#******* Main function ********************
#******************************************

def RunCommand( is_interactive ):
    if sc.escape_test(False):
        print "script cancelled" #do something

    print "Making unique..."

    #******* Get blocks *****************
    #************************************

    objectIds = rs.GetObjects("Pick some blocks", 4096, preselect=True)
    if not objectIds:
        print "No objects"
        return False

    #pause viewport redraw
    rs.EnableRedraw(False)

    #******* Sort blocks by type ********
    #************************************
    blockTypes = {}
    for id in objectIds:
        blockName = rs.BlockInstanceName(id)
        if blockName not in blockTypes:
            blockTypes[blockName] = []
        blockTypes[blockName].append(id)


    #***** Define new block and add *****
    #************************************

    #Get block names
    blockNames = rs.BlockNames()

    #gather all new objects when done
    finalObjs = []

    for blockType in blockTypes:        
        for id in blockTypes[blockType]:
            #Get the block transformation matrix and name
            blockXForm = rs.BlockInstanceXform(id)
            blockName = rs.BlockInstanceName(id)

            #Insert new block in 0,0,0
            newBlock = rs.InsertBlock(blockName,[0,0,0])

            #Explode the block
            exObjs = rs.ExplodeBlockInstance(newBlock)

            #create new block name
            
            # if the string ends in digits m will be a Match object, or None otherwise.            
            strippedName = re.sub(r'#[0-9]+$', '', blockName)
            
            #test if block name exist and add to the end number if true.
            x = 0
            tryAgain = True
            while tryAgain:
                x += 1
                newerBlockName = strippedName+"#"+str(x)
                if newerBlockName not in blockNames:                    
                    tryAgain = False
                    break

            #insert exObjs as new block
            rs.AddBlock(exObjs, [0,0,0], newerBlockName, delete_input = True)
            newerBlock = rs.InsertBlock(newerBlockName, [0,0,0])
            
            #match properties from original
            rs.MatchObjectAttributes(newerBlock, id)
            
            #transform new block
            rs.TransformObject(newerBlock, blockXForm)

            #append for final selection
            finalObjs.append(newerBlock)

        #add name to list of used blocknames.
        blockNames.append(newerBlockName)


    #Delete original block
    rs.DeleteObjects(objectIds)

    rs.EnableRedraw(True)

    #Select all new objects
    rs.SelectObjects(finalObjs)

    print "...aaand its done."
    #End RunCommand()

    #end sane
    return 0

RunCommand(True) #Run script

#END MakeUnique
