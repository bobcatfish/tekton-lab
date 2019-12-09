# Tekton Lab

This repo holds my experiments with [Tekton!](https://github.com/tektoncd/pipeline).

## Prerequisites

You must install into your kube cluster:

* [Tekton Pipelines](https://github.com/tektoncd/pipeline/blob/master/docs/install.md#installing-tekton-pipelines-1)
* [Tekton Triggers](https://github.com/tektoncd/triggers/tree/master/docs/getting-started)

The triggers that interact with github expect 
kubernetes secret to exist called `webhook-secret` in the `default`
namespace with `token` and `secret` `stringData`.

