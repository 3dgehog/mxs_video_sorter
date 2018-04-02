# Before Matching
def before_matching(config, match, fse):
    if match['title'] == "Boruto":
        match['title'] = match['title'] + ' ' + match['alternative_title']
    return match


# Before Transfering
def before_transfering():
    pass
