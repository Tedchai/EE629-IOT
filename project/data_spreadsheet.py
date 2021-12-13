import json
import sys
import time
import datetime
import gspread
import psutil
import subprocess

from oauth2client.service_account import ServiceAccountCredentials

GDOCS_OAUTH_JSON = 'cpudata-78c9ddc7b37e.json'
GDOCS_SPREADSHEET_NAME = 'Performance Recorder'
FREQUENCY_SECONDS = 10

def login_open_sheet(oauth_key_file, spreadsheet):
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file,
                                                                       scopes=['https://spreadsheets.google.com/feeds',
                                                                               'https://www.googleapis.com/auth/drive'])
        gc = gspread.authorize(credentials)
        worksheet = gc.open(spreadsheet).sheet1
        return worksheet
    except Exception as ex:
        print('Unable to login and get spreadsheet. Check OAuth credentials, spreadsheet name, and')
        print('make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)


print('Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS))
print('Press Ctrl-C to quit.')
worksheet = None
while True:
    if worksheet is None:
        worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)

    dat = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    mem = memory.available / (1024 ** 3)
    free = str(round(memory.free / (1024 ** 3), 4))
    count = psutil.cpu_count()
    load = psutil.getloadavg()
    stats = psutil.cpu_stats().interrupts
    disk = psutil.disk_usage('/').free / (1024 ** 3)
    net = psutil.net_if_addrs()["eth0"][0]

    print(dat)
    print('CPU Usage:        {0:0.1f}%'.format(cpu))
    print('Memory Available: ' + format(mem) + ' GB')
    print('Free Memory: ' + free)
    print('CPU Count: ' + str(count))
    print('System Load: ' + str(load))
    print('CPU Status: ' + str(stats))
    print('Disk free space: ' + format(disk) + ' GB' )
    print(net.address)

    try:
        worksheet.append_row((str(dat), cpu, mem, free, count, str(load), str(stats), disk, net.address))
    #   worksheet.append_row((dat, cpu, tmp))
    # gspread==0.6.2
    # https://github.com/burnash/gspread/issues/511
    except:
        print('Append error, logging in again')
        worksheet = None
        time.sleep(FREQUENCY_SECONDS)
        continue
    print('Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME))
    time.sleep(FREQUENCY_SECONDS)
