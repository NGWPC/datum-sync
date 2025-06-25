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

# NextGen inflows & outflows dataset to coastal area
Dataset related to NextGen inflows and outflows has been added to 'examples/data/NextGen'

To verify that the dataset meets the required criteria, run the following test code:  
'pytest -v tests/unit/test_NGen_datum_sync.py'

To convert the NextGen dataset into the crs that the coastal model needs, please run the following code:
'examples/NGen_bmi_datum_sync.py'  
prior to run the code, verify that the bmi_config.yaml file in examples/data/NextGen/ is properly configured to match your current coordinate reference system (CRS) and target output CRS.
