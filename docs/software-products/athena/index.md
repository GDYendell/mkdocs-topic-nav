# Athena

Athena is the modernised experiment control/orchestration software platform for Diamond-II. In development with up-to-date technologies and software development practices, it aims to be easier to set up, support, extend and develop than GDA, which it is intended to replace.

- [Notes on the design and current state of implementation](explanations/architecture.md)
- [Instructions on how to migrate your beamline](how-tos/migration.md)
- [Working with data collected by Athena services](explanations/data-management.md)

## Bluesky

The [Bluesky tutorial](https://blueskyproject.io/bluesky/tutorial.html) is a good introduction to the general usage of Bluesky.

Central to the Athena architecture is [Bluesky, a set of Python libraries for experiment control and collection of data](https://blueskyproject.io/).
It was developed at National Synchrotron Light Source II (NSLS-II), Brookhaven National Laboratory and is currently used in several facilities around the world.

- Hardware is defined via complying to [ophyd protocols](https://github.com/bluesky/ophyd), **although [ophyd-async is the standard implementation at Diamond](https://blueskyproject.io/ophyd-async/main/index.html)**
- [Procedures are written as Plans](https://blueskyproject.io/bluesky/plans.html), which [may be created, modified or augmented](https://blueskyproject.io/bluesky/tutorial.html#tutorial-custom-plans) to enable new experimental types
- [Data is produced as Documents](https://blueskyproject.io/bluesky/documents.html), also known [as the Event Model](https://github.com/bluesky/event-model/)

{nav}
