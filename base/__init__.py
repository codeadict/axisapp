try:
    from . import gis
except Exception:
    import warnings
    warnings.warn(
        "Unable to import base.gis, geometry widgets not available")