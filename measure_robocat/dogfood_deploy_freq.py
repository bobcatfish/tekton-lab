#!/usr/bin/env python3.7
#
# ./dogfood_deploy_freq.py --context robocat

import argparse
import collections
import datetime
import json
import re
import shlex
import subprocess

class Kubectl():
    def __init__(self, context):
        self._context = context
    
    def _run(self, command):
        return subprocess.check_output(shlex.split(
            "kubectl --context {} {}".format(self._context, command)
        ))

    def get_task_runs(self):
        output = self._run("get taskruns -o json --sort-by=.status.startTime")
        return [s for s in json.loads(output.decode())["items"]]


def get_deployed_service(run_name):
    pattern = "deploy-(.*)-release"
    service = re.findall(pattern, run_name)
    return service[0]


def avg_date_diff(pubs):
    diffs = []
    for i in range (0, len(pubs)-1):
        diffs.append((pubs[i] - pubs[i+1]))
    return sum(diffs, datetime.timedelta(0)) / len(diffs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='get deployment stats from the robocat cluster')
    parser.add_argument('--context', help='context to pass to kubectl')
    args = parser.parse_args()

    k = Kubectl(args.context)

    task_runs = k.get_task_runs()
    deploys = [tr for tr in task_runs if tr["metadata"]["name"].startswith("deploy-")]
    succeeded = [tr for tr in deploys if tr["status"]["conditions"][0]["status"] == "True"]

    by_project = collections.defaultdict(list)
    for tr in succeeded:
        service = get_deployed_service(tr["metadata"]["name"])
        by_project[service].append(datetime.datetime.strptime(tr["status"]["startTime"], "%Y-%m-%dT%H:%M:%SZ"))

    for project in by_project:
        by_project[project].append(datetime.datetime.now())
    
    for project, dates in by_project.items():
        avg  = avg_date_diff(list(reversed(dates)))
        print("{} is deployed to dogfood every {}".format(project, avg))
