"""
@name:          ResetBlockScale
@description:   Resets the scale of a block, keeping the rotation around the insertion point.
@author:        Ejnar Brendsdal
@version:       1.2
@attribution:   Inspired by the ResetBlock script by Dale Fugier. Thank you.
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
                2. Add a new button with the following macro: ( _NoEcho !-_RunPythonScript "ResetBlockScale.py" _Echo )
                3. Add an alias with the above command
                3. Call the script directly by using this command: "-RunPythonScript SelectSameBlocks.py"

@Changelog:
    1.1: Make script into a command to be included in the BlockTools part of RhinoTools.
    1.2: Fix a bug when resetting a negatively scaled bug. Biproduct: it does not insert a new block. It scales the existing one. So all properties are kept. It also simplifies the heck out of it :)

"""

#******* Imports ********************
#************************************

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.Geometry as G

#******* Main function ********************
#******************************************

def RunCommand( is_interactive ):
    if sc.escape_test(False):
        print "script cancelled" #do something

    print "Resetting..."

    #******* Get blocks ***********''****
    #************************************

    objectIds = rs.GetObjects("Pick some blocks", 4096, preselect=True)
    if not objectIds:
        print "No objects"
        return False

    rs.EnableRedraw(False)

    #******* Ref Geometry ***************
    #************************************

    points = [
     G.Point3d(0,0,0),
     G.Point3d(1,0,0),
     G.Point3d(0,1,0),
     G.Point3d(0,0,1)
    ]

    #gather all new objects when done
    finalObjs = []

    for id in objectIds:

        #Get the block transformation matrix and name
        blockXForm = rs.BlockInstanceXform(id)
        blockName = rs.BlockInstanceName(id)

        #Add reference geometry
        pts = G.Polyline(points)
        
        #Apply block transformation matrix to ref geometry
        pts.Transform(blockXForm)
        
        #create final plane
        finalOrigin = pts[1]
        finalXaxis = rs.VectorSubtract( pts[1], pts[0] )
        finalYaxis = rs.VectorSubtract( pts[2], pts[0] )
        finalPlane = G.Plane(finalOrigin, finalXaxis, finalYaxis)

        #create scaling factors
        xFac = 1 / rs.Distance(pts[1],pts[0])
        yFac = 1 / rs.Distance(pts[2],pts[0])
        zFac = 1 / rs.Distance(pts[3],pts[0])
        
        #Scale block
        newXForm = G.Transform.Scale(finalPlane, xFac, yFac, zFac)
        rs.TransformObject(id,newXForm)

    rs.EnableRedraw(True)

    #Select all new objects
    rs.SelectObjects(objectIds)

    print "...aaand its done."
    #End RunCommand()

    #end sane
    return 0

RunCommand(True) #Run script
