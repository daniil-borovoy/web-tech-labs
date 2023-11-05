DEFAULT_PAGE_LIMIT = 10


def pagination_param_is_valid(param):
    return param is not None and int(param) > 0
