# Mixed-unit PyMRIO Loader

A simple module (one fonction, really) to load the [mixed-unit version of Exiobase](https://www.exiobase.eu/index.php/data-download/exiobase3hyb) as a [PyMRIO](https://github.com/konstantinstadler/pymrio) object.

Only applies to the symmetric input-output (HIOT) version 3.3.17 of Hybrid Exiobase.



## Usage with Exiobase files as downloaded


```python

import mixedunit_pymrio_loader as ml

io = ml.load_pxp_io('path-to-data-directory', version='3.3.17')

```

Note that, as the original exiobase files are saved as `.xlsb` file, the function depends on version~1.0 of `pandas` and on `pyxlsb`.

## Alternative, compatibility option

If we save the original files (.xlsb) as OfficeOpen XML files (.xls):

```python

import mixedunit_pymrio_loader as ml

io = ml.load_pxp_io('path-to-data-directory', version='3.3.17', file_format='xlsx')

```
