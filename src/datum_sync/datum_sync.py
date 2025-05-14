import warnings
from typing import Any

import numpy as np
import pyproj
from pyproj import CRS, Transformer
from pyproj.transformer import TransformerGroup

from datum_sync.exceptions import TransformError, ZConversionWarning

FT_TO_M = 0.3048
M_TO_FT = 3.28084


def convert_datum(crs_input: int, crs_output: int, xx: Any, yy: Any, zz: Any = None) -> tuple:
    """Convert coordinates between input and output EPSG CRS.

    Wraps pyproj transformer. It is designed to be attentive to Z conversions and will warn when
    Z conversions do not happen or if the only difference is between meters <-> feet. Inputs values
    can be of any pyproj transformer accepted class. CRS must be input as EPSG integers.

    Requires network connectivity for some conversions.

    Args:
        xx (Any): Acalar or array. Input x coordinate(s).
        yy (Any): Scalar or array. Input y coordinate(s).
        zz (Any): Scalar or array. Input z coordinate(s).
        crs_input (int): The input EPSG CRS defined as int (e.g. 4326)
        crs_output (int): The input EPSG CRS defined as int (e.g. 5070)

    Returns
    -------
        tuple: Transformed coordinates in tuple matching input type

    From pyproj:
    Accepted numeric scalar or array:

        - :class:`int`
        - :class:`float`
        - :class:`numpy.floating`
        - :class:`numpy.integer`
        - :class:`list`
        - :class:`tuple`
        - :class:`array.array`
        - :class:`numpy.ndarray`
        - :class:`xarray.DataArray`
        - :class:`pandas.Series`
    """
    # This will allow transformation grids to be downloaded if they are not included in base package
    # TODO: Download grids a priori with package building; remove network connectivity
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

    # for transforming 3D coordinates
    if zz:
        output = transform.transform(xx, yy, zz)

        # check if Z was converted; warn if not
        if (np.array(output[2], dtype=float) == np.array(zz, dtype=float)).all():
            warnings.warn(
                "Z values were not altered. This could be expected. This may be because input and output CRS do not have vertical element.",
                ZConversionWarning,
                stacklevel=2,
            )

        # check if z was only changed between M and FT; warn if so
        if (np.round(np.array(output[2]), 2) == np.round(np.array(zz) * FT_TO_M, 2)).all() or (
            np.round(np.array(output[2]), 2) == np.round(np.array(zz) * M_TO_FT, 2)
        ).all():
            warnings.warn(
                "Z values were converted between meters and feet but were not altered."
                " This may be because input and output CRS do not have vertical element.",
                ZConversionWarning,
                stacklevel=2,
            )

        return output  # type:ignore[no-any-return]

    # 2D transformation
    else:
        return transform.transform(xx, yy)  # type:ignore[no-any-return]
