from urllib3 import PoolManager, disable_warnings
disable_warnings()
import json
import requirements

def get_pkg_info(pkg_name, pkg_ver = ''):
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


def parse_require_dist(require_dist):
    """Read f'{pkg_name}{boole_operator}{pkg_ver}'
    example: pandas==1.1.5
    or read f{pkg_name} ({bool_operator}{pkgver})
    example: pandas (>=1.15)

    Parameters:
        require_dist : str

    Returns:
        pkg_name : str
        pkg_ver : str
    """
    pkg_name = next(requirements.parse(require_dist)).name
    pkg_specs = next(requirements.parse(require_dist)).specs
    if len(pkg_specs) == 0:
        return (pkg_name, '')
    else:
        # This is right only for the case == and >= or <=
        return (pkg_name, pkg_specs[0][1])


def get_basic_info(pkg_info, filename='', requires_format=True):
    """Get basic information such as name, requires_dist, size
    from what get_pkg_info() returns

    Parameters:
        pkg_info : json/dict
        filename : str
        requires_format : bool

    Returns:
        json/dict
    """
    basic_info = {}
    basic_info['name'] = pkg_info['info']['name']

    if requires_format:
        basic_info['requires_dist'] = [parse_require_dist(dist)
        for dist in pkg_info['info']['requires_dist']]
    else:
        basic_info['requires_dist'] = pkg_info['info']['requires_dist']

    if filename == '':
        basic_info['size'] = pkg_info['urls'][0]['size']
    else:
        for url_info in pkg_info['urls']:
            if url_info['filename'] == filename:
                basic_info['size'] = url_info['size']

    return basic_info
