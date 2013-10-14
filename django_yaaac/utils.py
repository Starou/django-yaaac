def lookup_dict_from_url_params(url_params):
    """Convert a url_params dict in a mapping suitable for ORM querying."""
    lookup_dict = {}
    for k, v in url_params.items():
        values = v.split(",")
        if len(values) > 1:
            lookup_dict[k] = values
        else:
            lookup_dict[k] = v
    return lookup_dict

def clean_fieldname_prefix(fieldname):
    import re
    try:
        fieldname = re.match(r'(.*)-(\w+)', fieldname).groups()[1]
    except AttributeError:
        pass
    return fieldname
