import subprocess, datetime
from ._utils import get_registry_from_name_or_login_server
from ._docker_utils import get_access_credentials

def parse_number(string):
    string=str(string)
    try:
        number=int(string)
        return number
    except ValueError:
        return -1

def print_nice_matrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

def get_logs(
    registry_name,
    login_server,
    startTime: datetime.datetime,
    endTime: datetime.datetime,
    username,
    password,
    days):

    print('Getting logs for last {} day(s) ...'.format(days))

    logs = [
        # Timestamp, Action, Image, Manifest
        [
            datetime.datetime.now() - datetime.timedelta(seconds=60*60*24*3 - 60), # 3 days (minus 1 minute) ago
            "push",
            "repo:tag1",
            "sha@sha"
        ],
        [
            datetime.datetime.now() - datetime.timedelta(seconds=60*60*24*2 - 60), # 2 days (minus 1 minute) ago
            "push",
            "repo:tag2",
            "sha@sha"
        ],
        [
            datetime.datetime.now() - datetime.timedelta(seconds=60*60*24 + 60*60*12), # 1 day and 12 hours ago
            "untag",
            "repo:tag1", # star for deleting a manifest
            "sha@sha"
        ],
        [
            datetime.datetime.now() - datetime.timedelta(seconds=60*60*12), # 12 hours ago
            "delete", # deleting a tag also deletes it manifest and all related tags
            "[ repo:tag2 ]",
            "sha@sha"
        ]
    ]

    filtered_logs = [log for log in logs if (log[0] >= startTime and log[0] <= endTime)]
    if len(filtered_logs) == 0:
        print('No logs for the time range specified.')
    else:
        parsed_logs = [ ["TIMESTAMP", "ACTION", "TAG NAME", "DIGEST"] ]
        parsed_logs = parsed_logs + filtered_logs
        print_nice_matrix(parsed_logs)



def acr_test(
    cmd,
    registry_name,
    show_logs=False,
    days=1,
    tenant_suffix=None,
    username=None,
    password=None):

    # Getting login server name and credentials
    login_server, username, password = get_access_credentials(
        cmd=cmd,
        registry_name=registry_name,
        tenant_suffix=tenant_suffix,
        username=username,
        password=password)
    
    dnsCheckOutput = subprocess.getoutput('nslookup {}'.format(login_server))
    if dnsCheckOutput.count("can't find {}: Non-existent domain".format(login_server)) > 0:
        print('Could not connect to {}. Please check your connection.'.format(login_server))
    else:
        print('Could connect to {} successfully.'.format(login_server))
    
    if show_logs > 0:
        days = parse_number(days)
        if days <= 0:
            print("'days' parameter must be a positive integer.")
            return
        endTime = datetime.datetime.now()
        startTime = endTime - datetime.timedelta(seconds=60*60*24*days)
        get_logs(
            registry_name,
            login_server,
            startTime,
            endTime,
            username,
            password,
            days
        )
