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

class Release():
    def __init__(self, r):
        self._r = r
        self.v = version.parse(r['tag_name'])
        self.pub_time = datetime.datetime.strptime(r['published_at'], "%Y-%m-%dT%H:%M:%SZ")


class Releases():
    def __init__(self, releases):
        self._releases = [Release(r) for r in releases]
    
    def minor(self):
        return [r for r in self.all() if r.v.micro == 0]
    
    def patch(self):
        return [r for r in self.all() if r.v.micro != 0]
    
    def all(self):
        # ignore pre-releases
        return [r for r in self._releases if r.v.pre is None]


def avg_date_diff(pubs):
    diffs = []
    for i in range (0, len(pubs)-1):
        diffs.append((pubs[i] - pubs[i+1]))
    return sum(diffs, datetime.timedelta(0)) / len(diffs)


def get_release_freqs(releases):
    pubs = []
    for r in releases:
        pubs.append(r.pub_time)
    return avg_date_diff(pubs)


# TODO: should we also consider the patch releases which themselves need a patch release?
def minors_with_patches(releases):
    mwp = set()
    for r in releases.patch():
        mwp.add(r.v.minor)
    return len(mwp) / len(releases.minor())


def time_to_patch(releases):
    diffs = []
    all_releases = releases.all()
    for i, r in enumerate(all_releases):
        if r.v.micro != 0:
            diffs.append(r.pub_time - all_releases[i+1].pub_time)
    return sum(diffs, datetime.timedelta(0)) / len(diffs) if len(diffs) > 0 else 0




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
        ttp = time_to_patch(releases)

        print("*********** {} *************".format(p))
        print("Avg release freq (all): {}".format(all))
        print("Avg release freq (minor): {}".format(minor))
        print("% minor with patch: {}".format(mwm))
        print("Avg time to patch: {}".format(ttp))
