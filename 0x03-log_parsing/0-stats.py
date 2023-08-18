#!/usr/bin/python3
'''
Parsing HTTP request logs
'''
import re


def extract_input(input_line):
    '''
    Extracts sections of a line of an HTTP request log

    Args:
        input_line: Receives info from stdin

    Return: Status code and file size
    '''
    ln = (
        r'\s*(?P<ip>\S+)\s*',
        r'\s*\[(?P<date>\d+\-\d+\-\d+ \d+:\d+:\d+\.\d+)\]',
        r'\s*"(?P<request>[^"]*)"\s*',
        r'\s*(?P<status_code>\S+)',
        r'\s*(?P<file_size>\d+)'
    )
    stat = {
        'status_code': 0,
        'file_size': 0,
    }
    log_fmt = '{}\\-{}{}{}{}\\s*'.format(ln[0], ln[1], ln[2], ln[3], ln[4])
    res_match = re.fullmatch(log_fmt, input_line)
    if res_match is not None:
        status_code = res_match.group('status_code')
        file_size = int(res_match.group('file_size'))
        stat['status_code'] = status_code
        stat['file_size'] = file_size
    return stat


def print_statistics(total_file_size, status_codes_stats):
    '''
    Prints the statistics of the HTTP request log

    Args:
        total_file_size: Total file size
        status_codes_stats: Status code occurance

    Return: Number of each status code and file size
    '''
    print('File size: {:d}'.format(total_file_size), flush=True)
    for status_code in sorted(status_codes_stats.keys()):
        num = status_codes_stats.get(status_code, 0)
        if num > 0:
            print('{:s}: {:d}'.format(status_code, num), flush=True)


def update_metrics(line, total_file_size, status_codes_stats):
    '''
    Updates the metrics from a given HTTP request log

    Args:
        line: The part of input from which to retrieve the metrics
        total_file_size: Total file size
        status_code_stats: Number of times each status code occurs

    Returns: The new total file size
    '''
    line_info = extract_input(line)
    status_code = line_info.get('status_code', '0')
    if status_code in status_codes_stats.keys():
        status_codes_stats[status_code] += 1
    return total_file_size + line_info['file_size']


def run():
    '''
    Initiates log parser
    '''
    line_num = 0
    total_file_size = 0
    status_codes_stats = {
        '200': 0,
        '301': 0,
        '400': 0,
        '401': 0,
        '403': 0,
        '404': 0,
        '405': 0,
        '500': 0,
    }
    try:
        while True:
            line = input()
            total_file_size = update_metrics(
                line,
                total_file_size,
                status_codes_stats,
            )
            line_num += 1
            if line_num % 10 == 0:
                print_statistics(total_file_size, status_codes_stats)
    except (KeyboardInterrupt, EOFError):
        print_statistics(total_file_size, status_codes_stats)


if __name__ == '__main__':
    run()
