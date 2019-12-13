# Git Admission

On a pull request, this triggers a Pipeline that applies some kind of rules
to determine if the user is allowed to do something.

```bash
# Make sure to build validation image
ko apply -f git-admission/triggers.yaml

k apply -f git-admission/pvc.yaml
k apply -f git-admission/task.yaml
k apply -f git-admission/pipeline.yaml
```
