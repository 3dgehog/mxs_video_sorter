# Before Matching
def before_matching(config, match, fse):
    if match['title'] in config.rule_book.keys():
        rules = config.rule_book[match['title']]

        if 'alt_name_merge' in rules:
            fse.title = match['title'] + ' - ' + match['alternative_title']
    return fse


# Before Transfering
def before_transfering():
    pass
