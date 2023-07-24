
from zipfile import ZipFile

import zipfile

with ZipFile("testing.zip", 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zip:

    zip.write("10000.jpg")
