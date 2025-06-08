import streamlit as st
import sqlite3
import os
from app.db import fetch_conflicts


st.set_page_config(page_title="RAG Conflict Review Dashboard", layout="wide")
DB_PATH = os.path.join(os.path.dirname(__file__), './storage/rag_data.db')

def fetch_conflicts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, doc_id, previous, current, resolution FROM conflicts ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_resolution(conflict_id, resolution_text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE conflicts SET resolution = ? WHERE id = ?", (resolution_text, conflict_id))
    conn.commit()
    conn.close()

def main():
    st.title("RAG Conflict Review Dashboard")
    st.markdown("Review and resolve knowledge conflicts flagged during document ingestion.")

    conflicts = fetch_conflicts()
    resolved = [c for c in conflicts if c[4] and c[4].strip().lower() != "none"]
    unresolved = [c for c in conflicts if not c[4] or c[4].strip().lower() == "none"]

    tab1, tab2 = st.tabs(["📝 Review Conflicts", "📊 Overview"])

    with tab1:
        if not conflicts:
            st.info("No conflicts to review.")
        else:
            for conflict in conflicts:
                conflict_id, doc_id, prev, new, resolution = conflict
                with st.expander(f"📄 Conflict #{conflict_id} – `{doc_id}`", expanded=False):
                    st.markdown(f"**Previous Version:** `{prev}`")
                    st.markdown(f"**New Version:** `{new}`")
                    st.markdown(f"**Current Resolution:** `{resolution if resolution else 'None'}`")

                    new_res = st.text_area(
                        f"✏️ Enter resolution for Conflict #{conflict_id}",
                        value=resolution or "",
                        key=f"res_{conflict_id}"
                    )
                    if st.button(f"💾 Save Resolution #{conflict_id}", key=f"btn_{conflict_id}"):
                        update_resolution(conflict_id, new_res)
                        st.success("Resolution updated!")
                        st.experimental_rerun()

    with tab2:
        st.subheader("Conflict Resolution Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("🧾 Total Conflicts", len(conflicts))
        col2.metric("✅ Resolved", len(resolved))
        col3.metric("❌ Unresolved", len(unresolved))

        progress = int(len(resolved) / max(len(conflicts), 1) * 100)
        st.progress(progress / 100, text=f"{progress}% conflicts resolved")

        with st.expander("📁 Resolved Conflicts", expanded=False):
            for c in resolved:
                st.markdown(f"✔️ **{c[1]}** – `{c[4]}`")

        with st.expander("📂 Unresolved Conflicts", expanded=False):
            for c in unresolved:
                st.markdown(f"⚠️ **{c[1]}** – No resolution yet")

if __name__ == "__main__":
    main()