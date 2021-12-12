# EE629-IOT

[Link to Google Site!](https://sites.google.com/view/ee-629-chai/home)

# Project
* Reference from the [cpudata project](https://github.com/kevinwlu/iot/tree/master/lesson4/mycpu) and run cpu_spreadsheet.py and system_info.py

### Sign up and log in the Google Cloud Platform Identity and Access Management [(IAM)](https://console.developers.google.com/projectselector/iam-admin/iam)

* Click "Create" and enter the project name, e.g., rpidata
* &equiv; > APIs & Services > + Enable APIs & Services > Enable both Drive API and Sheets API
* Credential > Create Credentials > Create service account key > Service account > rpidata > JSON key type > Create > download rpidata-xxxxxxxxxxxx.json

### Install gspread and oauth2client
```sh
$ sudo pip3 install -U gspread oauth2client
$ cd demo
$ cp ~/iot/lesson7/rpi_spreadsheet.py .
```

### Go to [Google Sheets](https://docs.google.com/spreadsheets/u/0)

* Start a new spreadsheet rpidata
* Share the spreadsheet with the "client_email" address in the .json file, select “Can edit,” and click "Send"
  * Will receive an email with the subject "Delivery Status Notification (Failure)" and the message "Address not found" from mailer-daemon@google.com
* Delete Rows 2 to 1000, and enter Date / Time, CPU Usage %, Temperature C to header cells

### Edit cpu_spreadsheet.py

```sh
$ nano cpu_spreadsheet.py
```
> GDOCS_OAUTH_JSON = 'rpidata-xxxxxxxxxxxx.json'
> GDOCS_SPREADSHEET_NAME = 'rpidata'
### Run rpi_spreadsheet.py
```sh
$ python3 cpu_spreadsheet.py
```
