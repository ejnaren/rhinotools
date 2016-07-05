"""
@name:          MakeUnique
@description:   Takes one or many blocks and creates a unique copy with own block definitions.
@author:        Ejnar Brendsdal
@version:       1.0
@link:
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
"""

#******* Imports ********************
#************************************

import rhinoscriptsyntax as rs
import Rhino.Geometry as G

def main():

    print "Making unique..."


    #******* Get blocks *****************
    #************************************

    objectIds = rs.GetObjects("Pick some blocks", 4096, preselect=True)
    if not objectIds:
        print "No objects"
        return False

    #******* Sort blocks by type ********
    #************************************
    blockTypes = {}
    for id in objectIds:
        ##blockXForm = rs.BlockInstanceXform(id)
        blockName = rs.BlockInstanceName(id)
        if blockName not in blockTypes:
            blockTypes[blockName] = []
        blockTypes[blockName].append(id)

    #pause viewport redraw
    rs.EnableRedraw(False)

    #******* Ref Geometry ***************
    #************************************

    points = [
     G.Point3d(0,0,0),
     G.Point3d(1,0,0),
     G.Point3d(0,1,0),
     G.Point3d(0,0,1)
    ]

    #Get block names
    blockNames = rs.BlockNames()

    #gather all new objects when done
    finalObjs = []

    for blockType in blockTypes:
        for id in blockTypes[blockType]:
            #Get the block transformation matrix and name
            blockXForm = rs.BlockInstanceXform(id)
            blockName = rs.BlockInstanceName(id)

            #Add reference geometry
            pts = G.Polyline(points)

            #Apply block transformation matrix to ref geometry
            pts.Transform(blockXForm)

            #Create initial plane and final plane
            initOrigin = G.Point3d(0,0,0)
            initXaxis = G.Vector3d(1,0,0)
            initYaxis = G.Vector3d(0,1,0)
            initPlane = G.Plane(initOrigin, initXaxis, initYaxis)

            finalOrigin = pts[0]
            finalXaxis = rs.VectorSubtract( pts[1], pts[0] )
            finalYaxis = rs.VectorSubtract( pts[2], pts[0] )
            finalPlane = G.Plane(finalOrigin, finalXaxis, finalYaxis)

            #Insert new block in 0,0,0
            newBlock = rs.InsertBlock(blockName,[0,0,0])

            #Explode the block
            exObjs = rs.ExplodeBlockInstance(newBlock)

            #create new block name
            import re
            ##m = re.search(r'#[0-9]+$', blockName)
            # if the string ends in digits m will be a Match object, or None otherwise.
            ##if m is not None:
            strippedName = re.sub(r'#[0-9]+$', '', blockName)
            #return False

            for x in range(1,10000):
                iter = x
                newerBlockName = strippedName+"#"+str(x)
                if newerBlockName not in blockNames:
                    break

            #insert exObjs as new block
            rs.AddBlock(exObjs, [0,0,0], newerBlockName, delete_input = True)
            newerBlock = rs.InsertBlock(newerBlockName, [0,0,0])

            #change basis to the new vectors
            basisXForm = rs.XformChangeBasis(finalPlane, initPlane)

            #transform new block
            rs.TransformObject(newerBlock, basisXForm)

            finalObjs.append(newerBlock)


    #Delete original block
    rs.DeleteObjects(objectIds)

    rs.EnableRedraw(True)

    #Select all new objects
    rs.SelectObjects(finalObjs)

    print "...aaand its done."
    #End Main()

main() #Run script

#END MakeUnique
