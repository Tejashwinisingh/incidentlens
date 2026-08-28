# IncidentLens 🔎

### Graph-Based IT Incident Relationship & Root-Cause Explorer

IncidentLens is a graph-powered IT incident investigation application built for the **Wexa AI CognoDB Take-Home Assignment**.

It helps users explore relationships between incidents, services, applications, servers, components, teams, and changes using **CognoDB** as the graph database.

---

## 🌐 Live Demo

**IncidentLens:**  
https://incidentlens-5tdnchtwcunubq9ykojazm.streamlit.app/

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

The dashboard provides a quick view of the current incident landscape.

---

### 2. Incident Explorer

Users can select an IT incident and view:

- Incident ID
- Title
- Severity
- Status
- Description

Example:

```text
INC-1042
Payment Service Unavailable
Severity: HIGH
Status: RESOLVED

⚙️ Local Setup
1. Create a CognoDB Cloud Instance
Create a CognoDB instance and obtain the Bolt connection URI and database credentials.

2. Configure Environment Variables
Create a local .env or configure the variables in your environment:
COGNODB_URI=bolt+s://<your-instance>.databases.cognodb.com
COGNODB_USER=cognodb
COGNODB_PASSWORD=<your-password>
Do not commit .env or database credentials to GitHub.

3. Create Python Virtual Environment
On Windows:
python -m venv .venv
Activate it
.venv\Scripts\activate

4. Install Dependencies
pip install -r requirements.txt

5. Load Seed Data
Open:
database/seed.cypher
Run the query in CognoDB Browser.

6. Start the Application
streamlit run app.py
The application will be available at:
http://localhost:8501

🔐 Security
Database credentials are read from environment variables.
Sensitive credentials are not stored in the source code.

The repository should never contain:
.env
or actual database passwords.

A configuration template is provided through:
.env.example
For the hosted deployment, CognoDB credentials are configured using Streamlit Secrets.