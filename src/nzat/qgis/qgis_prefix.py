CONTAINER_PREFIX = "/usr"


def qgis_prefix(env_value, default=CONTAINER_PREFIX):
    """Return the QGIS prefix. An empty value keeps the container prefix."""
    text = (env_value or "").strip()
    return text or default
