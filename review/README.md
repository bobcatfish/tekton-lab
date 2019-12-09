# Review bot

This is my review bot! The goal is to automate a lot of the stuff I find
myself repeatedly saying in reviews.

```bash
k apply -f review/release.yaml

# Make sure to build validation image
ko apply -f review/triggers.yaml
```

## Release notes

First iteration, we're gonna say something when folks leave the "Release Notes"
section exactly as-is.
