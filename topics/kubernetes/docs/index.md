# Kubernetes User Guide

## Introduction

This page tree details the DLS on premises Cloud which is based on Kubernetes. What is Kubernetes? Read [this](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) to find out!

For a _very_ high-level overview of some of the constructs of Kubernetes you can read a guide [here](https://medium.com/google-cloud/kubernetes-101-pods-nodes-containers-and-clusters-c1509e409e16). For a more detailed readable guide  see [here](https://www.ibm.com/cloud/garage/content/course/kubernetes-101/2)

If you prefer to watch a video, the following on YouTube are good:

[Containerisation Explained](https://www.youtube.com/watch?v=0qotVMX-J5s)

You can also read about containers [here](https://kubernetes.io/docs/concepts/containers/)

An official Quick Reference for the `kubectl` tool can be found [here](https://kubernetes.io/docs/reference/kubectl/quick-reference/).

## The DLS Kubernetes Environment

Diamond operates several Kubernetes clusters for general use. The clusters are multi-tenant. That means you share cluster nodes (nodes are Linux servers that run your pods) with other users. We make use of [namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) to provide multi-tenancy. More on that later....

We refer to the DLS Kubernetes clusters as "managed Kubernetes". We take care of managing the Kubernetes "stack" which includes:

- The Kubernetes version, the nodes, and the control plane
- Useful supporting tools (kustomize, helm etc)
- Essential cluster components such as load balancers and ingress controllers
- Persistent storage for pods

If you are interested in how the clusters are put together (including HA control planes), check out the [design page](https://confluence.diamond.ac.uk/x/BoswBg).

All clusters are covered by an SLA detailed [here](https://confluence.diamond.ac.uk/display/ITSM/Agreement%3A+Kubernetes+Clusters).

Maintenance work is announced [here](https://confluence.diamond.ac.uk/pages/viewrecentblogposts.action?key=CLOUD).

## [The Clusters](#the-clusters)

SciComp operate 2 clusters for general use. These are detailed in the table below. Note that clusters may have some additional nodes connected that have been reserved for exclusive use by a particular group. These are not shown in the table.

| Cluster Name  |      Purpose      |                   State                    |    Pool Load Balancer Range    |   Static Load Balancer Range   |
|-------------- |:----------------: |:-----------------------------------------: |:-----------------------------: |:-----------------------------: |
| argus         | Production\*      | [state](./tutorials/state.md#argus)  | 172.23.169.0-172.23.169.125    | 172.23.169.126-172.23.169.253  |
| pollux        | Pre-production\*\*| [state](./tutorials/state.md#pollux)  | 172.23.168.160-172.23.168.200  | 172.23.168.201-172.23.168.222  |
| hylas         | Controls\*        | [state](./tutorials/state.md#hylas)  | 172.23.228.224-172.23.228.239  | 172.23.228.240-172.23.228.254  |
| telamon       | SciComp testing   |                                            | NA                             | NA                             |
| castor        | SciComp testing   |                                            | NA                             | NA                             |

\* Changes will be minimal during a run, limited to minor admin only. Use this for a stable Kubernetes experience.

\*\* Acts as a testbed and debug platform for the production cluster. Upgrades will be tested here first which may cause cluster instability and short outages. Major maintenance during run and shutdown may be performed.

## Kubernetes Core Documentation

The core Kubernetes documentation can be found [here](./tutorials/getting_started.md). These documents are generally maintained by SciComp Cloud Team, but if you spot an error or want to contribute, please do prepare a merge request as described [here](../developer-portal/guide/how-tos/contribute-to-guide.md).

## Kubernetes Community Documentation

There is now a large community of users in DLS using Kubernetes. [This](https://confluence.diamond.ac.uk/x/BprNC) page in the SSCC space is editable by anyone and provides useful solutions, code snippets and docs supplied by the community. Feel free to contribute!

## GEM courses

There is a number of courses on Kubernetes on the Diamond's [GEM platform](https://gem.diamond.ac.uk/totara/catalog/index.php?catalog_fts=kubernetes). At the time of writing two are bookable workshops. Of particular interested may be 3 hour long [Kubernetes for Beginners](https://gem.diamond.ac.uk/enrol/index.php?id=986), or for a more advanced and specific use case, [Kubernetes Service Mesh with Istio](https://gem.diamond.ac.uk/course/view.php?id=987). Finally worth mentioning and checking out is the [Cloud Native with Kubernetes](https://gem.diamond.ac.uk/enrol/index.php?id=985), which is a link to a downloadable PDF book with 446 pages. Reading all of it is likely not the optimal course of action, but downloading it and keeping for reference might be useful.

## Support

Slack channel #kubernetes for general discussion.

To create a ticket use the SC Helpdesk [here](https://schelpdesk.diamond.ac.uk)
