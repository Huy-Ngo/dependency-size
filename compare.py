from preprocess import request_pkg_info
from pprint import PrettyPrinter

# TODO
# Handle the case that the conditions are NOT overlap
# Handle the case `==`
# Remove this todo
def get_possile_pkg_by(pkg_name, conditions):
    """Get possible packages by a list of conditions.

    Parameters:
        pkg_name : str
        conditions : list

    Returns:
        list

    Warning:
        This function is right for the case that the conditions overlap.
    """
    releases = list(request_pkg_info(pkg_name)['releases'].keys())
    for condi in conditions:
        if condi[1] not in releases:
            continue
        else:
            # if condi[0] == '==':
            #     possible_vers.append(condi[1])

            if condi[0] == '<':
                releases = releases[:releases.index(condi[1])]

            if condi[0] == '<=':
                releases = releases[:releases.index(condi[1])+1]

            if condi[0] == '>':
                releases = releases[releases.index(condi[1])+1:]

            if condi[0] == '>=':
                releases = releases[releases.index(condi[1]):]

            if condi[0] == '!=':
                releases.pop(releases.index(condi[1]))

    return [(pkg_name, pkg_ver) for pkg_ver in releases]

# TODO
# Handle the case that versions are not in the releases
# Remove this todo
def pkg_ver_compare(pkg_name, ver_1, ver_2):
    """Compare two versions of a package.

    Parameters:
        pkg_name : str
        ver_1 : str
        ver_2 : str

    Returns:
        true if ver_1 is greater than ver_2
        false if ver_1 is less than ver_2

    Warnings:
        This function is right for the case that both versions
        do EXIST in releases
    """
    releases = list(request_pkg_info(pkg_name)['releases'].keys())
    if releases.index(ver_1) >= releases.index(ver_2):
        return True

    if releases.index(ver_1) <= releases.index(ver_2):
        return False


if __name__ == '__main__':
    pkg_name = 'PySocks'
    conditions = [('<', '2.0'), ('!=', '1.5.7'), ('>=', '1.5.6')]
    PrettyPrinter(indent=2).pprint(get_possile_pkg_by(pkg_name, conditions))

    print(pkg_ver_compare('PySocks', '1.5.7', '1.5.6'))
    print(pkg_ver_compare('PySocks', '1.5.6', '1.5.7'))
