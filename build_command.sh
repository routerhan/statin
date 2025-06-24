#!/bin/bash

"$(which pyinstaller)" --onefile --windowed --name "StatinHelper_CK_LV" \
--add-data "/Users/chen/anaconda3/lib/tcl8.6:tcl" \
--add-data "/Users/chen/anaconda3/lib/tk8.6:tk" \
"statin_CK_LV.py"