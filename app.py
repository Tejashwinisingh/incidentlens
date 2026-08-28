import os

import streamlit as st
from neo4j import GraphDatabase
from graphviz import Digraph


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="IncidentLens",
    page_icon="🔎",
    layout="wide"
)


# ---------------------------------------------------------
# Environment variables
# ---------------------------------------------------------
URI = os.getenv("COGNODB_URI")
USER = os.getenv("COGNODB_USER", "cognodb")
PASSWORD = os.getenv("COGNODB_PASSWORD")


# ---------------------------------------------------------
# Database connection
# ---------------------------------------------------------
def create_driver():
    """Create a Neo4j driver for CognoDB."""

    if not URI or not PASSWORD:
        return None

    return GraphDatabase.driver(
        URI,
        auth=(USER, PASSWORD),
        connection_timeout=30,
        connection_acquisition_timeout=30,
        max_connection_lifetime=300
    )


# ---------------------------------------------------------
# Run Cypher query
# ---------------------------------------------------------
def run_query(query, params=None):
    """Execute a parameterized Cypher query."""

    driver = create_driver()

    if not driver:
        raise RuntimeError(
            "CognoDB is not configured. "
            "Set COGNODB_URI and COGNODB_PASSWORD."
        )

    try:
        # Verify connection before running queries
        driver.verify_connectivity()

        with driver.session() as session:
            result = session.run(query, params or {})
            return [record.data() for record in result]

    finally:
        driver.close()


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.title("🔎 IncidentLens")
st.caption("Graph-based IT incident relationship explorer")


# ---------------------------------------------------------
# Configuration check
# ---------------------------------------------------------
if not URI or not PASSWORD:
    st.warning(
        "Database not configured. "
        "Set COGNODB_URI and COGNODB_PASSWORD in your environment."
    )

    st.code(
        "COGNODB_URI=bolt+s://<instance-id>.databases.cognodb.cloud\n"
        "COGNODB_USER=cognodb\n"
        "COGNODB_PASSWORD=<your-password>"
    )

    st.stop()


# ---------------------------------------------------------
# Load dashboard data
# ---------------------------------------------------------
try:

    counts = run_query(
        """
        MATCH (n)
        RETURN labels(n)[0] AS type, count(n) AS count
        ORDER BY type
        """
    )

    incidents = run_query(
        """
        MATCH (i:Incident)
        RETURN i.id AS id, i.title AS title
        ORDER BY i.id
        """
    )

except Exception as e:

    st.error(
        f"Unable to reach CognoDB: {e}"
    )

    st.info(
        "Make sure your CognoDB instance is running "
        "and your environment variables are correct."
    )

    st.stop()


# ---------------------------------------------------------
# Dashboard metrics
# ---------------------------------------------------------
incident_count = next(
    (
        item["count"]
        for item in counts
        if item["type"] == "Incident"
    ),
    0
)

service_count = next(
    (
        item["count"]
        for item in counts
        if item["type"] == "Service"
    ),
    0
)

change_count = next(
    (
        item["count"]
        for item in counts
        if item["type"] == "Change"
    ),
    0
)


c1, c2, c3 = st.columns(3)

c1.metric(
    "Incidents",
    incident_count
)

c2.metric(
    "Services",
    service_count
)

c3.metric(
    "Changes",
    change_count
)


st.divider()


# ---------------------------------------------------------
# Incident selection
# ---------------------------------------------------------
incident_ids = [
    item["id"]
    for item in incidents
]


if not incident_ids:

    st.info(
        "No seed data found. "
        "Run database/seed.cypher in CognoDB."
    )

    st.stop()


selected = st.selectbox(
    "Select an incident",
    incident_ids
)


if st.button(
    "Explore incident",
    type="primary"
):

    st.session_state["selected"] = selected


selected = st.session_state.get(
    "selected",
    selected
)


# ---------------------------------------------------------
# Incident details
# ---------------------------------------------------------
try:

    detail_results = run_query(
        """
        MATCH (i:Incident {id: $id})

        OPTIONAL MATCH (i)-[r]-(n)

        RETURN
            i.id AS id,
            i.title AS title,
            i.severity AS severity,
            i.status AS status,
            i.description AS description,

            collect({
                rel: type(r),
                nodeId: coalesce(n.id, n.name),
                nodeType: labels(n)[0]
            }) AS links
        """,
        {
            "id": selected
        }
    )

    if not detail_results:

        st.warning(
            "Incident not found."
        )

        st.stop()


    detail = detail_results[0]


    # -----------------------------------------------------
    # Incident information
    # -----------------------------------------------------
    st.subheader(
        f'{detail["id"]} — {detail["title"]}'
    )


    a, b, c = st.columns(3)


    with a:
        st.write(
            f'**Severity:** {detail["severity"]}'
        )


    with b:
        st.write(
            f'**Status:** {detail["status"]}'
        )


    with c:
        st.write(
            f'**Description:** {detail["description"]}'
        )


    st.divider()


    # -----------------------------------------------------
    # Two-column layout
    # -----------------------------------------------------
    left, right = st.columns(
        [1, 1]
    )


    # =====================================================
    # LEFT COLUMN - Graph
    # =====================================================
    with left:

        st.markdown(
            "### 🔗 Relationship Network"
        )


        dot = Digraph()

        dot.attr(
            rankdir="LR"
        )


        # Main incident
        dot.node(
            detail["id"],
            detail["id"]
        )


        # Connected nodes
        for link in detail["links"]:

            if not link["nodeId"]:
                continue


            node_id = str(
                link["nodeId"]
            ).replace(
                " ",
                "_"
            )


            node_type = (
                link["nodeType"]
                or "Node"
            )


            dot.node(
                node_id,
                f'{node_type}\n{link["nodeId"]}'
            )


            dot.edge(
                detail["id"],
                node_id,
                label=link["rel"]
            )


        st.graphviz_chart(
            dot.source,
            use_container_width=True
        )


    # =====================================================
    # RIGHT COLUMN - Related incidents
    # =====================================================
    with right:

        st.markdown(
            "### 🔥 Related Incidents"
        )


        related = run_query(
            """
            MATCH
                (i:Incident {id: $id})
                -[:AFFECTS]->
                (s:Service)
                <-[:AFFECTS]-
                (r:Incident)

            WHERE r.id <> $id

            RETURN DISTINCT
                r.id AS id,
                r.title AS title,
                r.severity AS severity

            ORDER BY r.id
            """,
            {
                "id": selected
            }
        )


        if related:

            st.dataframe(
                related,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No related incidents found."
            )


        # -------------------------------------------------
        # Multi-hop traversal
        # -------------------------------------------------
        st.markdown(
            "### 🧭 Multi-hop Infrastructure Path"
        )


        hops = run_query(
            """
            MATCH
                (i:Incident {id: $id})
                -[:AFFECTS]->
                (s:Service)
                -[:USES]->
                (a:Application)
                -[:RUNS_ON]->
                (srv:Server)
                -[:CONTAINS]->
                (c:Component)

            RETURN
                s.name AS service,
                a.name AS application,
                srv.name AS server,
                c.name AS component

            LIMIT 20
            """,
            {
                "id": selected
            }
        )


        if hops:

            st.dataframe(
                hops,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No infrastructure path found."
            )


except Exception as e:

    st.error(
        f"Query failed: {e}"
    )