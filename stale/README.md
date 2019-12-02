# Stale cron

The purpose of this [Tekton triggers](https://github.com/tektoncd/triggers)
cron is to prevent the situation where I've asked a contributor a question,
or given them feedback, and they've responded, but I lose it in the sea of
other notifications I get.

The [Tekton Task](https://github.com/tektoncd/pipeline/blob/master/docs/tasks.md)
[stale.yaml](./stale.yaml) will:

* Retrieve all the open Issues from the passed in repo
* Look for open Issues which have comments from the passed in username
* Identify which of those have had subsequent updates
* Send an email to the specified email address, from the specified from account,
  with the report of the Issues it found

The [Triggers configuration](./triggers.yaml) will create a cron that will run
[stale.yaml](./stale.yaml) once a day at 6am EST.

## Prerequisites

You must install into your kube cluster:

* [Tekton Pipelines](https://github.com/tektoncd/pipeline/blob/master/docs/install.md#installing-tekton-pipelines-1)
* [Tekton Triggers](https://github.com/tektoncd/triggers/tree/master/docs/getting-started)

Apply the types:

```bash
kubectl apply -f stale/stale.yaml
kubectl apply -f stale/triggers.yaml
```