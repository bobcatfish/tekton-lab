#!/usr/bin/env python3.7
#
# ./release_freq.py --token=$GITHUB_PERSONAL_TOKEN

import argparse
import datetime
import requests

PROJS = [
    'tektoncd/pipeline',
    'tektoncd/triggers',
    'tektoncd/cli',
    'tektoncd/dashboard',
    'tektoncd/hub',
    'tektoncd/results',
]

class GitHub():
    def __init__(self, token):
        self._token = token
    
    def _get_json(self, url):
        r = requests.get(url,
            headers={"Authorization":"token {}".format(self._token)}
        )
        r.raise_for_status()
        return r.json()

    def get_releases(self, proj):
        return self._get_json("https://api.github.com/repos/{}/releases".format(proj))


def avg_date_diff(pubs):
    diffs = []
    for i in range (0, len(pubs)-1):
        diffs.append((pubs[i] - pubs[i+1]))
    return sum(diffs, datetime.timedelta(0)) / len(diffs)


def get_release_freqs(g, proj):
    releases = g.get_releases(proj)
    major, all = [], []
    for r in releases:
        pub_time = datetime.datetime.strptime(r['published_at'], "%Y-%m-%dT%H:%M:%SZ")
        if r['tag_name'].endswith('.0'):
            major.append(pub_time)
        all.append(pub_time)

    return avg_date_diff(major), avg_date_diff(all)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='get stats from the robocat')
    parser.add_argument('--token', help='github personal token for making requests')
    args = parser.parse_args()

    g = GitHub(args.token)

    for p in PROJS:
        major, all = get_release_freqs(g, p)
        print("{} release frequency across all is {}, between major versions is {}".format(p, all, major))