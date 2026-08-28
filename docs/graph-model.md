# IncidentLens Graph Model

```text
Customer -> Incident -> Service -> Application -> Server -> Component
                  |         |            |
                  |         +-> Team     +-> Change
                  +-> Change
Incident -> Incident (RELATED_TO)
```

## Nodes
Incident, Service, Application, Server, Component, Team, Change, Customer.

## Relationships
AFFECTS, RELATED_TO, CAUSED_BY, OWNED_BY, USES, RUNS_ON, CONTAINS, MODIFIES, ASSIGNED_TO.

## Why a graph database?
Incident investigation is relationship-heavy. Finding a path from an incident through a service and application to infrastructure, or finding incidents connected through a shared service, requires repeated joins in a relational schema. A graph model stores those connections directly and makes multi-hop traversal natural.
