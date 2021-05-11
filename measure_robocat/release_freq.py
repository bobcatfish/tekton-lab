#!/usr/bin/env python3.7
#
# ./release_freq.py --token=$GITHUB_PERSONAL_TOKEN

import argparse
import datetime
from packaging import version
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
            headers={"Authorization":"token {}".format(self._token)},
            # try to shortcut pagination b/c i am lazy
            params={"per_page":1000},
        )
        r.raise_for_status()
        return r.json()

    def get_releases(self, proj):
        return Releases(self._get_json("https://api.github.com/repos/{}/releases".format(proj)))


def avg_date_diff(pubs):
    diffs = []
    for i in range (0, len(pubs)-1):
        diffs.append((pubs[i] - pubs[i+1]))
    return sum(diffs, datetime.timedelta(0)) / len(diffs)


class Releases():
    def __init__(self, releases):
        self._releases = releases
    
    def minor(self):
        return [r for r in self.all() if version.parse(r['tag_name']).micro == 0]
    
    def patch(self):
        return [r for r in self.all() if version.parse(r['tag_name']).micro != 0]
    
    def all(self):
        # ignore pre-releases
        return [r for r in self._releases if version.parse(r['tag_name']).pre is None]

def get_release_freqs(releases):
    pubs = []
    for r in releases:
        pubs.append(datetime.datetime.strptime(r['published_at'], "%Y-%m-%dT%H:%M:%SZ"))
    return avg_date_diff(pubs)

def minors_with_patches(releases):
    mwp = set()
    for r in releases.patch():
        v = version.parse(r['tag_name'])
        mwp.add(v.minor)
    return len(mwp) / len(releases.minor())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='get stats from the robocat')
    parser.add_argument('--token', help='github personal token for making requests')
    args = parser.parse_args()

    g = GitHub(args.token)

    for p in PROJS:
        releases = g.get_releases(p)
        minor = get_release_freqs(releases.minor())
        all = get_release_freqs(releases.all())
        mwm = minors_with_patches(releases)

        print("*********** {} *************".format(p))
        print("Release freq (all): {}".format(all))
        print("Release freq (minor): {}".format(minor))
        print("% minor with patch: {}".format(mwm))
