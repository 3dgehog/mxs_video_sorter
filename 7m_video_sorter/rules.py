# Before Matching
def before_matching(fse, match, config):
    valid = False
    if match['title'].upper() in config.valid_list:
        match = _before_matching(fse, match)
        valid = True
    return match, valid


def _before_matching(fse, match):
    if match['title'] == "Boruto":
        match['title'] = match['title'] + ' ' + match['alternative_title']
    return match


# Before Transfering
def before_transfering():
    pass
