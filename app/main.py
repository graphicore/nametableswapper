# [START app]
from __future__ import print_function
import logging
from flask import Flask, make_response, request
from tools.ot_names_tool import makeNames, makeOS2, makeHead
from tools.ot_tables_tool import writeData
from fontTools.ttLib import TTFont
import struct
from io import BytesIO
import json
import zipfile
app = Flask(__name__)


def _unpack(stream):
    # L = unsignedlong 4 bytes
    while True:
        head = stream.read(8)
        if not head:
            break
        jsonlen, fontlen = struct.unpack('II', head)
        desc = json.loads(stream.read(jsonlen).decode('utf-8'))
        font = TTFont(BytesIO(stream.read(fontlen)))
        yield (desc, font)

def changefont(desc, font):
    ot_setup = {}
    familyName = desc['familyName']
    weightName = desc['weightName']
    isItalic = desc['isItalic']
    version = desc['version']
    vendorID = desc['vendorID']

    ot_setup['name'] = makeNames( '0x409', familyName, weightName, isItalic
                                                        ,version, vendorID)
    # NOTE: we expect TrueType at this point, setting usWeightClass
    # of OS/2 there should be no CFF table. If there is a CFF table:
    # ot_setup['CFF '].append(['Weight', weightClass])
    ot_setup['OS/2'] = makeOS2( font['OS/2'].fsSelection, weightName
                                                    ,isItalic , vendorID)
    ot_setup['head'] = makeHead( font['head'].macStyle, weightName , isItalic)
    writeData(font, ot_setup);

@app.route('/changenames', methods=['POST'])
def changenames():
    result = BytesIO()
    zipf = zipfile.ZipFile(result,  "w")
    i=0
    for desc, font in _unpack(request.stream):
        i += 1
        print('#',i,'got oldname', font['name'].getDebugName(6))
        changefont(desc, font)
        filename = desc['filename']
        print('changed', filename)

        # write the font file to the zip
        fontIO = BytesIO()
        font.save(fontIO)
        fontData = fontIO.getvalue()
        zipf.writestr(filename, fontData)

    zipf.close()
    data = result.getvalue()
    response = make_response(data)
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=fonts-with-changed-names.zip'
    return response

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
