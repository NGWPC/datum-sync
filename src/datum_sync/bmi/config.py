from pydantic import BaseModel, Field


class DatumSyncConfig(BaseModel):
    """Validates inputs to BMI model"""

    crs_input: int = Field(description="CRS of input values expressed as an EPSG integer (e.g. 4326)")
    crs_output: int = Field(description="CRS of output values expressed as an EPSG integer (e.g. 4326)")
    z_warn: bool = Field(
        description="Datum sync includes warnings about z values not being convereted. If you expect z values not to be converted or are running in batch environment, turn off."
    )
