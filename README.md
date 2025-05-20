# datum-sync
A BMI-compliant module to convert vertical datum between inland and coastal models.

This function wraps the library pyproj (a Python implementation of geospatial PROJ library) to convert between defined EPSG CRS. It includes focus on ensuring z (elevation) variables are correctly handled by producing meaningful warnings if CRS input/output did not change z values when the user may have expected this.

An example notebook `examples/example_convert.ipynb` demonstrates the function itself. Interacting with the BMI module is demonstrated in `examples/run_bmi_datum_sync.py`. `tests` individually tests both the base function and BMI wrapper.

To run the python function:
`pip install -e .`

To run examples and/or develop:
`pip install -r pyproject.toml --extra dev_examples`

To test:
`pip install -r pyproject.toml --extra test`
