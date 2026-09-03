import csv
import json
import os


HEADER_NAMES = {'repo_url', 'url', 'link', 'links', 'repository', 'repo'}


def authenticate_gsheets():
    import pygsheets
    gc = pygsheets.authorize(service_account_env_var='GOOGLE_CREDENTIALS')
    return gc


def read_from_csv(path):
    repo_details_list = []
    repo_links = []
    repo_shas = []

    with open(path, newline='', encoding='utf-8-sig') as handle:
        reader = csv.reader(handle)
        rows = [row for row in reader if row and any(cell.strip() for cell in row)]

    if not rows:
        raise SystemExit(f'No rows found in {path}')

    start = 0
    first_cell = rows[0][0].strip().lower()
    if first_cell in HEADER_NAMES or first_cell.startswith('#'):
        if first_cell in HEADER_NAMES:
            start = 1

    for row in rows[start:]:
        link = (row[0] or '').strip()
        if not link or link.startswith('#'):
            continue
        sha = (row[1] if len(row) > 1 else '').strip()
        repo_links.append(link)
        repo_shas.append(sha)
        repo_details_list.append(f'{link};{sha}')

    if not repo_details_list:
        raise SystemExit(f'No repository links found in {path}')

    return repo_details_list, repo_links, repo_shas


def read_from_gsheet():
    gc = authenticate_gsheets()
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    links_tab_name = os.getenv('LINKS_TAB_NAME')

    sheet = gc.open_by_key(sheet_id)
    print('the sheet: ', sheet)
    print('the tab name: ', links_tab_name)

    wks = sheet.worksheet_by_title(links_tab_name)
    print('wks: ', wks)

    repo_links = wks.get_col(1, include_tailing_empty=False)
    repo_shas = wks.get_col(2, include_tailing_empty=False)

    repo_details_list = []
    for idx, link in enumerate(repo_links):
        sha = repo_shas[idx] if idx < len(repo_shas) and repo_shas[idx] is not None else ''
        repo_details_list.append(f'{link};{sha}')

    return repo_details_list, repo_links, repo_shas


def write_matrix_output(repo_details_list):
    matrix_json = json.dumps(repo_details_list)
    output_file = os.getenv('GITHUB_OUTPUT')
    if output_file:
        with open(output_file, 'a', encoding='utf-8') as handle:
            handle.write(f'matrix={matrix_json}\n')
    else:
        print(f'::set-output name=matrix::{matrix_json}')


def main():
    links_csv = (os.getenv('LINKS_CSV') or '').strip()

    if links_csv:
        print('reading links from csv: ', links_csv)
        repo_details_list, repo_links, repo_shas = read_from_csv(links_csv)
    else:
        repo_details_list, repo_links, repo_shas = read_from_gsheet()

    print('links: ', repo_links)
    print('shas: ', repo_shas)
    print('all details: ', repo_details_list)
    write_matrix_output(repo_details_list)


if __name__ == '__main__':
    main()
