# Mixed-unit PyMRIO Loader

A simple module (one fonction, really) to load the [mixed-unit version of Exiobase](https://www.exiobase.eu/index.php/data-download/exiobase3hyb) as a [PyMRIO](https://github.com/konstantinstadler/pymrio) object.

Only applies to the symmetric input-output (HIOT) version 3.3.17 of Hybrid Exiobase.



## Usage


```python

import mixedunit_pymrio_loader as ml

io = ml.load_pymrio_3_3_17('path-to-data-directory')

```

## Compatibility

As the original exiobase files are saved as `.xlsb` file, the function depends on version~1.0 of `pandas` and on `pyxlsb`.
