import json
import random
import drawBot as db
import string

"""
Copyright (c) 2015, Erik van Blokland
All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions are met:

 1. Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
 ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES
 LOSS OF USE, DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

 The views and conclusions contained in the software and documentation are those
 of the authors and should not be interpreted as representing official policies,
 either expressed or implied, of the FreeBSD Project.
"""


parametersURL = "./parameters.json"

level = 5
withDescription = True
pages = 200
savePath =  "./TypeCooker-Level%s.pdf" % level
pageSize = (11*72, 8.5*72)
margin = 0.5*72

fontSize = 6
leading = 8.5
fontName = dict(regular="OperatorMono-Book", 
                italic="OperatorMono-BookItalic", 
                bold="OperatorMono-Bold", 
                boldItalic="OperatorMono-BoldItalic")

with open(parametersURL) as data_file:    
    parameterData = json.load(data_file)


def cap(txt):
    # Capitalize the first letter of the txt
    if len(txt) > 0:
        return string.upper(txt[0]) + txt[1:]
    
def buildSelection(selection, thisName):
    # Build this selection dictionary into a FormattedString
    txt = db.FormattedString()
    txt.append("\n%s: " % cap(thisName), font=fontName["italic"], fontSize=fontSize, fill=0, lineHeight=leading)
    txt.append(cap(selection["name"]), font=fontName["bold"], fontSize=fontSize, fill=0)
    if withDescription:
        if "description" in selection:
            txt.append(" %s" % selection["description"], font=fontName["italic"], fontSize=fontSize, fill=0.75)
    return txt

def makeSelection(level, data):
    # Make a random selection with the TypeCooker data, at a particular difficulty level
    
    selectionString = db.FormattedString()
    selectionString.append("Type Cooker ", font=fontName["boldItalic"], fontSize=fontSize, fill=0)
    selectionString.append("Level %s\n" % level, font=fontName["italic"], fontSize=fontSize, fill=0)
    
    parameterNames = data["keys"]
    
    for i, thisName in enumerate(parameterNames):
        optionsForThisName = []
        obj = data[thisName]
        levelOK = True
        for j, b in enumerate(obj):
            if not b["level"] > level:
                for x in range(b["weight"]):
                    optionsForThisName.append(b)
        if len(optionsForThisName) > 0:
            selection = random.choice(optionsForThisName)
            builtString = buildSelection(selection, thisName)
            selectionString.append(builtString)
    
    return selectionString


# Start drawing:
print "Cooking..."

db.newDrawing()
db.size(pageSize)

for pageNumber in range(pages):
    if not pageNumber == 0:
        db.newPage()
    # Make a selection and draw it
    selectedText = makeSelection(level, parameterData)
    db.textBox(selectedText, (margin, margin, pageSize[0]-margin*2, pageSize[1]-margin*2))
    
db.saveImage(savePath)

print "Done! Saved PDF"
    