import csv
from pathlib import Path

data_dir = Path(__file__).resolve().parent.joinpath('data')
password_csv = data_dir.joinpath('lastpass.csv')

fixed_csv = data_dir.joinpath('dashlane.csv')
if not fixed_csv.exists():
    fixed_csv.touch()

site_name_to_proper_url_name = {'steam': 'store.steampowered'}


def fix_bad_url(_site_name, _url):
    http_type = _url.split(':')[0]
    if _site_name:
        formatted_site_name = _site_name.replace("'", '').replace(' ', '').lower()
        formatted_site_name = fix_edgecase_site_name(formatted_site_name)
    else:
        formatted_site_name = ''
    fixed_url = f'{http_type}://www.{formatted_site_name}.com'
    return fixed_url


def fix_edgecase_site_name(_site_name):
    if _site_name.lower() in site_name_to_proper_url_name:
        _site_name = site_name_to_proper_url_name[_site_name]
    return _site_name


if __name__ == '__main__':
    with open(password_csv, 'r') as pw_csv:
        with open(fixed_csv, 'w') as fixed_csv:
            csv_writer = csv.writer(fixed_csv)
            csv_reader = csv.reader(pw_csv, delimiter=',')
            for row in csv_reader:
                username = row[1]
                password = row[2]
                url = row[0]
                site_name = row[5]
                if url == 'https://' or url == 'http://'  or url is None:
                    url = fix_bad_url(site_name, url)
                csv_writer.writerow([site_name, url, username, password])

