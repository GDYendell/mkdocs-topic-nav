# Getting Started

## Assumptions

- You are familiar with what a [container](https://kubernetes.io/docs/concepts/containers/) is
- You are familiar with what a [container image](https://kubernetes.io/docs/concepts/containers/images/) is

## Access

To get access to a cluster, you need to "do a module load" in a similar way to how you access the HPC clusters. This will set up kubectl in your PATH, as well as access to other useful tools such as helm, kubeseal, kubelinter and kustomize. More on these later...

Run:

```shell
module load argus
source <(kubectl completion bash)
kubectl get nodes
```

When you run kubectl for the first time you will be prompted for a username and password. Enter your fedid and password. This gives you an authentication token that is valid for 1 week.  Subsequent kubectl commands will not require username/password until the token expires, where it will prompt you again.

In case you are seeing any error messages related to login, please try to run the command **klogout,**  this should clear the cache and hence you will be effectively logged out. Once you enter any other kubectl command it will ask for username and password, which in turn will create new token for the cluster.

kubectl is the main command line tool for interacting with the Kubernetes cluster.

!!! hint

    To have the kubectl command completion available in every terminal without running it manually, you can add the following bash script to your ~/.bashrc_local

    ```shell
    if [ -d "/dls_sw/apps/kubernetes/kubectl" ]; then
        kubectl="/dls_sw/apps/kubernetes/kubectl/$(ls /dls_sw/apps/kubernetes/kubectl/ | sort -r | head -n 1)/kubectl"
        if [ -f "$kubectl" ]; then
            source <($kubectl completion bash)
        fi
    fi
    ```

## Namespaces

Namespaces are a way of partitioning up a Kubernetes cluster into logical "areas", for example "production" or "dev". We use namespaces to create an area of the cluster in which you can freely experiment without worrying about impacting other applications in other namespaces. There are two types of namespace that we make use of:

### Fedid Namespaces

When you run "kubectl" for the first time you will be prompted for your username and password. This authentication triggers the one-time creation of a namespace for you, which is named after your fedid. Remember to add `--namespace=<fedid>` to your kubectl commands as you won't be able to see/schedule inside the namespace "default". You don't need `--namespace=<fedid>` if you set it as the default by doing:

```shell
kubectl config set-context --current --namespace=<your fedid>
```

You are free to deploy pretty much anything inside your fedid namespace. It is not intended to run production applications though.

!!! warning

    Don't run production applications in your fedid namespace! Your fedid namespace will be removed as soon as you leave DLS!

### Project Namespaces

As you move to production, it's likely that you will need a namespace that can be administered my multiple users. This is where "Project Namespaces" come in. SciComp will create these namespaces upon request. Please create a Cloud Computing helpdesk ticket of type "New Namespace" [here](https://jira.diamond.ac.uk/servicedesk/customer/portal/2/group/27).

We will require a named list of (human) admins of the namespace. If the application requires /dls access via hostPath mounts (you can read about these in the [storage](storage.md) section), we will also set up a new unix user that can be used by pods in the namespace. Admins of the namespace can effectively run processes inside containers as this user. When setting up project namespaces, SciComp Cloud team will need to be provided with:

- A sensible name for the project namespace. Use dashes for separation.
- The DNS name(s) for your application if you are using an ingress or loadBalanced service.
- A named list of people who can admin/control K8s resources inside the project namespace.
- A named list of people to receive basic alerts from our centralized prometheus/alertmanager.

Please note that the list of admins of a namespace are collectively responsible for telling SciComp if people should be added/removed from the list. You can list the people who are admins of the namespace by doing:

`kubectl describe namespace <namespace name>`

!!! example

    The labels will show the fedids of admins:

    ```terminal
    [user@hostname:~]$ kubectl describe namespaces controls-monitoring 
    Name:         controls-monitoring
    Labels:       kubernetes.io/metadata.name=controls-monitoring
                  nstype=project
                  user.diamond.ac.uk/lju57382=lju57382
                  user.diamond.ac.uk/tdq39642=tdq39642
                  user.diamond.ac.uk/ton99817=ton99817
    Annotations:  <none>
    Status:       Active

    No resource quota.

    No LimitRange resource.
    ```

You can also list all namespaces your fedid is an admin for by doing:

`kubectl get ns -l user.diamond.ac.uk/<fedid>`

!!! example

    ```terminal
    [user@hostname:~]$ kubectl get ns -l user.diamond.ac.uk/hko55533
    NAME          STATUS   AGE
    rabbitmq      Active   452d
    zocalo        Active   516d
    zocalo-test   Active   193d
    ```

## Running a Simple Pod

The yaml snippet below shows how to run a single container in a pod on Kubernetes. What is a pod? It is a group of one or more [containers](https://kubernetes.io/docs/concepts/containers/), with shared storage and network resources, and a specification for how to run the containers.  Note that a pod can have many containers in it, but generally only has one. The container in this example uses a rockylinux:8 image. It runs a small shell loop as the first process to keep the container from exiting. It also sets some limits for the amount of CPUs and Memory the container needs. The yaml manifest is:

```yaml title="my_pod.yaml"
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: my-container
    image: rockylinux:8
    command: ["/bin/sh"]
    args: ["-c", "while true; do sleep 10; done"]
    resources:
      limits:
        cpu: "1"
        memory: 300M
```

To make the pod run on the cluster, you need to copy the yaml snippet to a file called "my_pod.yaml" (the name of the file doesn't matter) and then tell Kubernetes to make the declared pod "live" using the kubectl tool:

```terminal
[user@hostname:~]$ module load argus # only needs doing once to set up the PATH to kubectl
[user@hostname:~]$ kubectl apply -f my_pod.yaml
```

The pod details can be shown:

```terminal
[user@hostname:~]$ kubectl get pod
[user@hostname:~]$ kubectl describe pod my-pod
```

To get a shell in the pod:

```terminal
[user@hostname:~]$ kubectl exec -it my-pod -- /bin/bash
```

You can have a poke around in the container, e.g. inspecting the process tree by running `dnf install -y procps-ng && ps fauxww`, view the network interfaces by running `dnf install -y iproute && ip a s`, and viewing your uid/gid by typing `id`. Type exit to leave the container (it will stay running). To delete the pod:

```terminal
[user@hostname:~]$ kubectl delete -f my_pod.yaml
```

One important point to note is that the pod has a "private" IP address in the range 10.10.xx.xx. This is because all pods are connected using an "overlay" network that is separate from the underlying DLS network. This has some important implications as discussed in the section on [Services](services.md).

## Resource quotas

As you go through this guide, be aware that your namespace is restricted by a resource quota. You will probably not exceed the quota while following the guide, but when you are finished you should delete any resources that you no longer need.

You can check your current usage and hard limits by running `kubectl describe resourcequota`, and you should consider coming back later to read more about resource quotas in the [dedicated page](quotas.md).

## Advanced Debugging

[Ephemeral containers](https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/) are useful for interactive troubleshooting when `kubectl exec` is insufficient because a container has crashed or a container image doesn't include debugging utilities, such as with [distroless images](https://github.com/GoogleContainerTools/distroless)

An example is as follows:

```terminal
[user@hostname:~]$ kubectl debug -it my-pod --image=rockylinux:8 --target=my-container
```

This will create a container that runs alongside my-container and gives you a debug shell. You can inspect the container processes (using ps).

## Next Steps

You can now read about more complex Kubernetes constructs like:

[Deployments](deployments.md) - a way to always have a certain number of replicas of a pod running. E.g if the replica count is 1, Kubernetes will watch over the cluster and make sure your 1 pod is always running, even if nodes are removed for maintenance.

[Services](services.md) - Kubernetes runs  your pod inside a private "overlay" network. Addresses assigned to pods start with 10.10.x.x. Because your pods might be moved between worker nodes in the event of worker node failure or maintenance, Kubernetes cannot direct traffic to your pods based on their IP address in the private network as the pod address might change. Kubernetes instead uses something called a "service" to map traffic to your pods. The traffic can be connections coming from your workstation or any DLS machine with a network address of 172.23.x.x, or it can be traffic originating from other pods in the cluster. Services provide this mapping, by maintaining a list of pods and their current IP addresses. If a pod is moved, the IP address of the pod is updated inside the service map. Instead of connecting to a pod directly, you can connect to the service which will forward your connection to the pod(s).

[Storage](storage.md) - See the storage section in the page tree for an overview of how Kubernetes can attach a storage volume to your pod. It uses [dynamic volume provisioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning) to do this.

[Helm](helm.md) - Helm is a package manager for Kubernetes and can be used to install whole applications (that may use multiple containers, storage, services etc). Example helm charts include Grafana and Prometheus.

______________________________________________________________________

[Continue](deployments.md) through the documentation to learn more about some of these constructs in more detail...
