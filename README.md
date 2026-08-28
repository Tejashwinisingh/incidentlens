# IncidentLens 🔎

### Graph-Based IT Incident Relationship & Root-Cause Explorer

IncidentLens is a graph-powered IT incident investigation application built for the **Wexa AI CognoDB Take-Home Assignment**.

It helps users explore relationships between incidents, services, applications, servers, components, teams, and changes using **CognoDB** as the graph database.

---

## 🚀 Overview

In traditional IT incident management, an incident is often treated as an individual ticket.

However, understanding an incident usually requires answering relationship-based questions:

- Which service is affected?
- Which application is used by that service?
- Which server hosts the application?
- Which infrastructure component is involved?
- Are there other incidents affecting the same service?
- Was a recent change associated with the incident?

IncidentLens models these entities and their relationships as a graph so users can investigate an incident through connected data.

---

## ✨ Features

### 1. Incident Dashboard

Provides an overview of:

- Total incidents
- Total services
- Total changes

### 2. Incident Explorer

Users can select an IT incident and view:

- Incident ID
- Title
- Severity
- Status
- Description

### 3. Relationship Network

Displays connected entities around an incident, including:

- Services
- Changes
- Related incidents

### 4. Related Incident Discovery

Finds other incidents connected through a shared service.

Example:

```text
INC-1042
    ↓ AFFECTS
Payment Service
    ↑ AFFECTS
INC-1041