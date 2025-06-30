# Test Athena on a Machine Day

This page describes how to commission Athena onto a beamline for regular machine day testing and is only valid after following the [migration guide](migration.md).

> :question: Throughout, the placeholder `${BEAMLINE}` is used. If you are uncertain what value to use (e.g. your beamline is known both as j20 or i20-1, or has multiple branches with names), from a beamline workstation `echo $BEAMLINE`. This will ensure the value is used consistently.

## Objectives

The purpose of a regular testing day on Athena beamlines is to verify that the services and libraries that are deployed still communicate and behave as expected. This is especially useful as some of these, including ophyd-async, are still in active development and subject to change.

The ethos is that testing on these days takes the versions of all necessary repositories on their primary branches and tests them against a known benchmark, e.g. a pre-configured bluesky plan.

Any problems encountered during these tests should be documented in the [athena-components Slack channel](https://diamondlightsource.slack.com/channels/C051NDJH6BZ). You may wish to try and debug/solve the problem yourself, but if unsure just raise issues in the relevant repositories, and write up in that Slack channel.

Note that **for beamlines not currently using Athena**, [most setup work](#setup) may be done remotely and should not interrupt beamline operations. However, if they are using it in production for experiments, you will have to [prepare Athena](#preparing-athena) on the machine day itself and with clearance of the beamline scientist(s).

> :warning: Ensure that instructions are followed completely to ensure a successful teardown. Failure to do so may result in an unknown beamline state, in turn frustrating beamline users, beamline scientists and support engineers, who may not know what has occurred on the beamline.

## Prerequisites

Before starting the test, ensure that [the migration guide](migration.md) has been folowed, including:

- Commissioning of a kubernetes cluster
- Definition of the beamline devices as a dodal module
- Creation of a beamline plan repository, which has been checked out for local development
- Templating of a DAQ-Deployments Umbrella Helm chart
- Secret credentials for the RabbitMQ deployment

And that:

- You have negotiated with beamline scientist(s) for the beamline you will be testing on, to ensure all necessary hardware is turned on and ready to use. If you are unsure speak to your DAQ support teams.
- You are in the `dls_dasc` group. `$ groups <fedid>` should contain `dls_dasc`. To request membership [make a SCHelpDesk ticket](https://jira.diamond.ac.uk/servicedesk/customer/portal/2)
- You are able to access repositories on gerrit. Ensure you can [access gerrit from the command line](https://confluence.diamond.ac.uk/pages/viewpage.action?pageId=83732611) first.
- You are working on the correct cluster and in the correct namespace. Check the [general docs](https://dev-portal.diamond.ac.uk/guide/kubernetes/tutorials/getting_started/) if not sure, but the most specific instructions will be in the [daq-deployments README](https://gitlab.diamond.ac.uk/daq/d2acq/examples/daq-deployments).
  - Set up [DAQ deployments](https://gitlab.diamond.ac.uk/daq/d2acq/examples/daq-deployments), follow the guide for setting up on a beamline workstation.
- You are a user on the `$BEAMLINE-daq` namespace on the `k8s-$BEAMLINE` cluster. Your fedid should be a label on the namespace in the form `user.diamond.ac.uk/$fedid=$fedid`. To get all of the labels on a namespace `$ kubectl get namespace $namespace --show-labels`
- :exclamation: you have sufficient space in your Diamond home directory.

## Setup

### Preparing GDA

#### Materialising GDA

[Follow instructions on how to provision GDA on a beamline](https://alfred.diamond.ac.uk/documentation/manuals/GDA_Developer_Guide/master/build_infrastructure/provisioning.html), filling the `Installation folder name` with "gda-master-YYYY-MM-DD", filling in the current date. Within Eclipse open the `Git Repositories` view (`Window -> Show View -> Others...`)

> :exclamation: Hereafter, the `Installation folder name` will be refered to as `gda-master-YYYY-MM-DD/`

[Ensure the GDA instance is communicating over RMQ-style JMS](migration.md#gda): to find the properties for `$BEAMLINE`, find `$BEAMLINE-config` in the Package Explorer view, then `properties/live/live_instance_java.properties`. If it does not contain `gda.message.broker.impl = rabbitmq`, follow the steps in the [migration guide](migration.md#gda)
`

Note that **for some beamlines**, the filepath might be slightly different, for instance `properties/live/instance.properties`.

**If there are merge conflicts, report in the [athena-components Slack channel](https://diamondlightsource.slack.com/channels/C051NDJH6BZ)**

[Follow instructions for building the GDA product](https://alfred.diamond.ac.uk/documentation/manuals/GDA_Developer_Guide/master/build_infrastructure/building.html#performing-a-build)

### Link the new instance of GDA

Once the build has succesfully completed, check that the symlinks were created

```bash
$ cd ../..  # from daq-aggregator.git/ go to gda-master-YYYY-MM-DD/
$ ls -l
lrwxrwxrwx.  1 fedid dls_dasc   28 <today> <now> client -> clients/client_<today>_<now>
drwxrwsr-x.  3 fedid dls_dasc 4096 <today> <now> clients
drwxrwsr-x.  6 fedid dls_dasc 4096 <today> <now> eclipse
lrwxrwxrwx.  1 fedid dls_dasc   28 <today> <now> server -> servers/server_<today>_<now>
drwxrwsr-x.  3 fedid dls_dasc 4096 <today> <now> servers
drwxrwsr-x.  4 fedid dls_dasc 4096 <today> <now> workspace
drwxrwsr-x. 17 fedid dls_dasc 4096 <today> <now> workspace_git
```

One additional, beamline specific symlink is required once per GDA materialization:

```bash
# In gda-master-YYYY-MM-DD/ link ./config to the config for this beamline
$ ln -s workspace_git/gda-diamond.git/configurations/$BEAMLINE-config config
$ ls -l 
lrwxrwxrwx.  1 fedid dls_dasc   28 <today> <now> client -> clients/client_<today>_<now>
drwxrwsr-x.  3 fedid dls_dasc 4096 <today> <now> clients
lrwxrwxrwx.  1 fedid dls_dasc   56 <today> <now> config -> workspace_git/gda-diamond.git/configurations/$BEAMLINE-config
drwxrwsr-x. 10 fedid dls_dasc 4096 <today> <now> eclipse
lrwxrwxrwx.  1 fedid dls_dasc   28 <today> <now> server -> servers/server_<today>_<now>
drwxrwsr-x.  3 fedid dls_dasc 4096 <today> <now> servers
drwxrwsr-x.  4 fedid dls_dasc 4096 <today> <now> workspace
drwxrwsr-x. 17 fedid dls_dasc 4096 <today> <now> workspace_git
```

We must now create a symlnk so that our version of GDA starts when the user runs the `gda` command.

```bash
# from gda-master-YYYY-MM-DD/ go to /dls_sw/$BEAMLINE/software/gda_versions
$ cd ..
$ ls -l
# It is unlikely to actually be this tidy!
lrwxrwxrwx.  1 fedid dls_dasc    7 <the past> gda -> foo/
lrwxrwxrwx.  1 fedid dls_dasc    7 <the past> gda_logs -> ../logs
lrwxrwxrwx.  1 fedid dls_dasc    3 <the past> gda_var -> var
drwxrwsr-x. 27 fedid dls_dasc 4096 <the past> gda_versions
```

In the above, `gda` currently points to a previously created version of GDA: `foo`. Either note down the previous version being used, or create a new symlink e.g.

```bash
ln -s gda_versions/foo $gdaprevious  # There will likely already be a gda-previous, find a name that works for your purposes
```

> :warning: Ensure that the beamline is not currently using GDA!

```bash
rm gda  # remove the existing link
ln -s gda-master-YYYY-MM-DD gda  # link your new installation
```

> :warning: **The following command **must** be run from a beamline workstation, else the server will start in dummy mode on the current machine, rather than starting the server on the beamline control machine.**
>
>
> :warning: **You should be logged into the beamline machine as your own fedid. This will become a must as Athena services develop**

If you do not have an active visit on the beamline, you must also be added to `config/xml/beamlinestaff.xml`: follow the format in the existing file, and set your permission level to 3. **This requires that you are a member of dls_dasc, as detailed above.**

```bash
gda server stop  # Shuts down the current GDA server
gda server start  # Start your new version
```

### Preparing Athena

The following require that helm and kubectl are configured for the beamline instance of kubernetes.

`CLUSTER`, `NAMESPACE` are defined in the `.env` file in [your beamline's daq-deployments directory](https://gitlab.diamond.ac.uk/daq/d2acq/examples/daq-deployments): follow the "[Usage and Procedures](https://gitlab.diamond.ac.uk/daq/d2acq/examples/daq-deployments#usage-and-procedures)" in that repository to update the dependencies and install the chart. In most cases you will be using the latest versions of the dependencies.

#### Downloading repositories into the mounted scratch directory

If the daq-deployments chart defines a value for `blueapi.scratch.hostPath`, this location on the DLS filesystem is mounted to the blueapi pod to allow for tight-loop development of plans and devices by building `dodal` and the beamline plans repository from them. **If any repositories are already present make a new local branch, stash the existing state of the repository, but do not push as it may contain sensitive details**, then checkout main and pull.

To allow the Kubernetes user that is running the pod to read, write and (as appropriate) execute files within the repository, run the following command in the root directory of each checked out repository. The Kubernetes user will at least need to write a `_version.py` in the repository to track the deployed version.

```bash
chmod -R o+wrX .
```

## Testing

This is the only step that requires access to the beamline. Start the GDA client and logpanel:

```bash
gda logpanel
gda client
```

If prompted for a visit, select any, preferring any with a prefix of cm (commissioning visit). The GDA client should open with the Jython console displayed.

Run your specified test plan(s): if your plan requires specific hardware, be sure to speak to the beamline prior to testing to ensure they are in a known state.

To execute a plan from the Jython console call the `run_plan` function- if this isn't available, contact the DAQ Core team- with the first argument as the name of the plan as it is registered for the blueapi context: this is the name of the plan function and  the arguments of the method as keyword arguments.

```python
# For the plan def foo(i: int) -> MsgGenerator:
>>> run_plan("foo", i=1)
```

This is a blocking call which will then return the status of the task. If the task failed check the logs of the blueapi container on the Kubernetes dashboard (see "Install or upgrade the Umbrella Helm chart"): remember to select the namespace.

If issues arise and debugging is impractical or the error message is unclear, try to discern where the exception was thrown and make an issue for that repository. If you cannot discern where the issue lies, make the issue on the blueapi repository. Include as much detail as possible in the ticket, including stack traces, devices, plans and versions of the repositories (if you have a virtual  `python -m <module name> --version`, else check `<module>/src/<module>/_version.py` for the value of `__version__`) and draw attention to it in the [athena-components Slack channel](https://diamondlightsource.slack.com/channels/C051NDJH6BZ).

- the beamline's plan repository if the plan's behaviour is wrong or problematic
- [dodal](https://github.com/DiamondLightSource/dodal) if the behaviour of devices is incomplete or missing
- [blueapi](https://github.com/DiamondLightSource/blueapi) if the problem relates to how the plan or devices are loaded or parsed
- [ophyd_async](https://github.com/bluesky/ophyd-async)
- [bluesky](https://github.com/bluesky/bluesky/)

## Teardown

### Tearing down Athena

#### Removing /scratch directory

If you made any changes to the repositories checked out at your `blueapi.scratch.hostPath` which should be brought forward, commit and push them, opening issues as required, then restore the branches and apply any stashes.

#### Uninstalling the helm chart

If you require to return to a previously installed chart version, or to simply remove the current deployment, follow the instructions in the [daq deployments readme](https://gitlab.diamond.ac.uk/daq/d2acq/examples/daq-deployments/-/blob/master/Readme.md?ref_type=heads#completely-remove-chart)

### Tearing down GDA

Leaving too many instances of GDA deployed on a beamline uses up space on `/dls_sw/` which is at a premium. You may wish to preserve the current deployment of GDA if there may be major changes by the next test, but otherwise the deployment should be cleaned up entirely.

**If you built GDA from the beamline machine, be sure to clean up `/scratch/.m2` if you created this repository. Just delete it all `rm -rf /scratch/.m2`.

#### Restoring symlinks

Restore the version of symlink `gda` to as it was prior to your [setting of the symlinks](#link-the-new-instance-of-gda).

```bash
cd /dls_sw/$BEAMLINE/software/
rm gda
ln -s gda_versions/foo gda  # Whichever deployment of GDA was being used previously
```

#### Reverting message bus changes

> :info: If you created a new instance of GDA, skip this step and leave this instance of GDA in a known state.

If you made modifications to the the GDA config `live_instance_java.properties`, revert any changes to `gda.message.broker.uri` or `gda.message.broker.impl`. Other properties are silently ignored.

#### Restarting GDA servers

The GDA servers may now be restarted, which will use the prior version once again.

```bash
gda servers --stop
gda logpanel
gda servers --start
```

GDA will likely have restarted at this point. There may be exceptions logged. If `gda servers` returns, try starting the client to ensure it can connect.
