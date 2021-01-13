from urllib3 import PoolManager, disable_warnings
disable_warnings()
import json
import pprint
import requirements

def request_pkg_info(pkg_name, pkg_ver = ''):
    """Get json response from pypi

    Parameters:
        pkg_name : str
        pkg_ver : str

    Returns:
        json/dict
    """
    url = ''
    if pkg_ver == '':
        url = f'https://pypi.org/pypi/{pkg_name}/json'
    else:
        url = f'https://pypi.org/pypi/{pkg_name}/{pkg_ver}/json'

    http = PoolManager()
    r = http.request('GET', url)
    r_json = json.loads(r.data.decode('utf-8'))
    return r_json


def get_basic_info(pkg_info, filename='', requires_format=True):
    """Get basic information such as name, requires_dist, size
    from what request_pkg_info() returns

    Parameters:
        pkg_info : json/dict
        filename : str
        requires_format : bool

    Returns:
        json/dict

    Notes:
        For `requires_dist` key, it is a list of tuples.
        Each tuple is a requirement of package.
        First element of that tuple is pkg_name
        Second element of that tuple is a list of conditions as tuples.

    Examples:
        Try to run this file and see the output in stdout.
    """
    basic_info = {}
    basic_info['name'] = pkg_info['info']['name']

    if requires_format and pkg_info['info']['requires_dist'] is not None:
        basic_info['requires_dist'] = [(ite.name, ite.specs) for ite in
        requirements.parse("\n".join(pkg_info['info']['requires_dist']))]

    else:
        basic_info['requires_dist'] = pkg_info['info']['requires_dist']

    if filename == '':
        basic_info['size'] = pkg_info['urls'][0]['size']
    else:
        for url_info in pkg_info['urls']:
            if url_info['filename'] == filename:
                basic_info['size'] = url_info['size']

    return basic_info


def lazy_get_pkg(pkg_name, pkg_ver = '', filename='', requires_format=True):
    return get_basic_info(request_pkg_info(pkg_name, pkg_ver),
                                            filename, requires_format)


if __name__ == '__main__':
    pkg_info = lazy_get_pkg('urllib3')
    pprint.PrettyPrinter(indent=2).pprint(pkg_info)
