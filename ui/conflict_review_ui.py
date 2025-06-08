import streamlit as st
from app.db import fetch_all_conflicts, resolve_conflict

st.title("RAG Conflict Review UI")

conflicts = fetch_all_conflicts()

if not conflicts:
    st.info("✅ No conflicts to review.")
else:
    for conflict in conflicts:
        doc_id, old_text, new_text, resolution = conflict

        st.subheader(f"Conflict: {doc_id}")
        st.text_area("Old Version", old_text, height=100)
        st.text_area("New Version", new_text, height=100)

        if resolution:
            st.success(f"✅ Already resolved: {resolution}")
        else:
            selected = st.radio(
                "Choose resolution",
                ("keep_old", "keep_new", "keep_both", "needs_review"),
                key=doc_id
            )
            if st.button("Submit Resolution", key=f"submit_{doc_id}"):
                resolve_conflict(doc_id, selected)
                st.success("Resolution saved.")
