import numpy as np
import pyproj
from pyproj import CRS, Transformer
from pyproj.transformer import TransformerGroup

from datum_sync.exceptions import TransformError, ZConversionWarning

FT_TO_M = 0.3048
M_TO_FT = 3.28084


def convert_datum(xx, yy, zz, crs_input, crs_output) -> tuple:
    """"""
    # This will allow transformation grids to be downloaded if they are not included in base package
    # NOTE: Is this acceptable for a BMI module? Requires internet connection
    pyproj.network.set_network_enabled(active=True)

    try:
        crs_in = CRS.from_epsg(crs_input)
        crs_out = CRS.from_epsg(crs_output)
        transform = Transformer.from_crs(crs_from=crs_in, crs_to=crs_out, always_xy=True)

    except Exception as e:
        raise TransformError("Issue creating CRS and transformer. Check if CRS are valid.") from e

    transformer_group = TransformerGroup(crs_from=crs_in, crs_to=crs_out, always_xy=True)
    if len(transformer_group.transformers) == 0:
        raise TransformError("No methods to transform between CRS found. Try another CRS.")

    if zz:
        out_x, out_y, out_z = transform.transform(xx, yy, zz)

        # check if Z was converted
        if out_z == zz:
            raise ZConversionWarning(
                "Z values were not altered. This may be because input and output CRS do not have vertical element."
            )

        # check if z was only changed between M and FT
        if (np.round(out_z, 2) == np.round(zz * FT_TO_M, 2)) or (
            np.round(out_z, 2) == np.round(zz * M_TO_FT, 2)
        ):
            raise ZConversionWarning(
                "Z values were convereted between meters and feet but were not altered."
                " This may be because input and output CRS do not have vertical element."
            )

        return out_x, out_y, out_z

    else:
        out_x, out_y = transform.transform(xx, yy)
        return out_x, out_y


# create enum with common transforms
# debate what to do about set network enabled
# debate how to handle if it isn't transformed because of network issues
# test for NGVD -> NAVD88
# BMI
