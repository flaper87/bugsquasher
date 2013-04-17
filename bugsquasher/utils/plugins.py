import pkg_resources


def load_plugin(uri):

    if uri.startswith("egg:"):
        # uses entry points
        entry_str = uri.split("egg:")[1]
        try:
            dist, name = entry_str.rsplit("#", 1)
        except ValueError:
            dist = entry_str
            name = "sync"

        return pkg_resources.load_entry_point(dist, "bugsquasher.plugins",
                                              name)

    components = uri.split('.')
    if len(components) == 1:
        try:
            if uri.startswith("#"):
                uri = uri[1:]
            return pkg_resources.load_entry_point("bugsquasher",
                                                    "bugsquasher.plugins", uri)
        except ImportError:
            raise RuntimeError("arbiter uri invalid or not found")

    klass = components.pop(-1)
    mod = __import__('.'.join(components))
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return getattr(mod, klass)
