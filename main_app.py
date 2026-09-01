"""
Spec2Verify Enterprise Studio
Streamlit Entrypoint & Interactive Dashboard
"""

import streamlit as st
import pandas as pd
from pypdf import PdfReader
from src.knowledge_bank import SAMPLE_SPECIFICATIONS
from src.graph import build_verification_graph

# Page Configuration
st.set_page_config(
    page_title="Spec2Verify Enterprise Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling for Enterprise Polish
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; }
    .sub-text { font-size: 1.1rem; color: #4B5563; }
    .stAlert { border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<p class="main-header">⚡ Spec2Verify: Specification-to-Verification Studio</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Autonomous Multi-Agent Verification Pipeline from Hardware Specs to Golden Audit Evidence.</p>', unsafe_allow_html=True)
st.markdown("---")

# Initialize Session State
if "graph_state" not in st.session_state:
    st.session_state.graph_state = {
        "raw_document_text": "",
        "requirements": [],
        "spec_doubts": [],
        "human_feedback": "",
        "is_spec_approved": False,
        "vplan": [],
        "test_cases": [],
        "assertions": [],
        "coverage_models": [],
        "traceability_matrix": [],
        "execution_logs": []
    }
if "selected_spec_name" not in st.session_state:
    st.session_state.selected_spec_name = None

app_graph = build_verification_graph()

# Sidebar Control Panel
st.sidebar.header("📁 Specification Source")
input_mode = st.sidebar.radio(
    "Choose Input Method",
    ["Sample Library (8 Specs)", "Custom PDF Upload", "Manual Specification Text"]
)

if input_mode == "Sample Library (8 Specs)":
    spec_choice = st.sidebar.selectbox("Select Hardware Protocol / Spec", list(SAMPLE_SPECIFICATIONS.keys()))
    if st.sidebar.button("Load Sample Specification", type="primary"):
        spec_data = SAMPLE_SPECIFICATIONS[spec_choice]
        st.session_state.selected_spec_name = spec_choice
        st.session_state.graph_state["raw_document_text"] = spec_data["description"]
        st.session_state.graph_state["requirements"] = [
            {"req_id": r["req_id"], "description": r["description"], "category": r["category"], "priority": r["priority"], "status": "Pending"}
            for r in spec_data["requirements"]
        ]
        st.session_state.graph_state["spec_doubts"] = [
            {"doubt_id": "DOUBT_01", "issue": f"Protocol boundary condition ambiguity identified in {spec_choice}.", "recommendation": "Cross-verify against governing standard specification."}
        ]
        st.session_state.graph_state["is_spec_approved"] = False
        st.session_state.graph_state["vplan"] = []
        st.session_state.graph_state["test_cases"] = []
        st.session_state.graph_state["assertions"] = []
        st.session_state.graph_state["coverage_models"] = []
        st.session_state.graph_state["traceability_matrix"] = []
        st.session_state.graph_state["execution_logs"] = []
        st.success(f"Loaded '{spec_choice}' successfully!")
        st.rerun()

elif input_mode == "Custom PDF Upload":
    uploaded_file = st.sidebar.file_uploader("Upload Microarchitecture Spec / Datasheet", type=["pdf"])
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        text = "".join([page.extract_text() for page in reader.pages])
        st.session_state.graph_state["raw_document_text"] = text
        st.session_state.selected_spec_name = uploaded_file.name
        st.success(f"Loaded PDF '{uploaded_file.name}' ({len(text)} characters).")

else:  # Manual Text Input
    manual_text = st.sidebar.text_area("Enter Specification Text", height=200, placeholder="Paste bus protocol or microarchitecture details here...")
    if st.sidebar.button("Process Manual Text"):
        if manual_text.strip():
            st.session_state.graph_state["raw_document_text"] = manual_text
            st.session_state.selected_spec_name = "Manual Text Input"
            st.success("Manual specification loaded successfully!")
        else:
            st.sidebar.error("Please enter valid specification text.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ System Status")
st.sidebar.info(f"Active Spec: `{st.session_state.selected_spec_name or 'None'}`")
st.sidebar.info(f"Spec Status: `{'Approved & Locked' if st.session_state.graph_state['is_spec_approved'] else 'Pending Proofreading'}`")

# Multi-Output Dashboard Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Knowledge Map & HITL Review",
    "📚 Knowledge Bank & Standards",
    "📝 Verification Plan",
    "🧪 Test Cases & Rationale",
    "🎯 Assertions & Coverage",
    "🔗 Traceability Matrix",
    "📈 Analytics & Step Logs"
])

with tab1:
    st.subheader("Human-in-the-Loop (HITL) Specification Proofreading")
    st.markdown("Review extracted atomic requirements and address AI-flagged specification doubts before launching downstream agentic generation.")
    
    if st.session_state.graph_state["spec_doubts"]:
        st.warning("⚠️ Specification Ambiguities & Doubts Flagged by Auditor Agent:")
        for doubt in st.session_state.graph_state["spec_doubts"]:
            st.markdown(f"* **{doubt['doubt_id']}**: {doubt['issue']}")
            st.info(f"💡 **Recommendation:** {doubt['recommendation']}")
    
    st.markdown("### 📋 Extracted Requirements Ledger")
    if st.session_state.graph_state["requirements"]:
        for req in st.session_state.graph_state["requirements"]:
            st.checkbox(
                f"**{req['req_id']}** (`{req['category']}` - `{req['priority']}`): {req['description']}",
                value=True,
                key=f"chk_{req['req_id']}"
            )

        st.markdown("---")
        if not st.session_state.graph_state["is_spec_approved"]:
            if st.button("✅ Finalize Specification & Launch Downstream Agents", type="primary"):
                with st.spinner("Executing LangGraph Pipeline: VPlan $\rightarrow$ Testbench $\rightarrow$ Assertions $\rightarrow$ Coverage $\rightarrow$ Audit..."):
                    st.session_state.graph_state["is_spec_approved"] = True
                    st.session_state.graph_state = app_graph.invoke(st.session_state.graph_state)
                st.success("Specification locked and verification bundle successfully generated!")
                st.rerun()
        else:
            st.success("🔒 Specification is locked. Downstream verification artifacts have been synthesized.")
    else:
        st.info("👈 Select a sample specification from the sidebar or upload a document to begin.")

with tab2:
    st.subheader("Knowledge Bank: Protocol References & Standards Mapping")
    if st.session_state.selected_spec_name and st.session_state.selected_spec_name in SAMPLE_SPECIFICATIONS:
        spec_info = SAMPLE_SPECIFICATIONS[st.session_state.selected_spec_name]
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Domain:** `{spec_info['domain']}`")
            st.markdown(f"**Governing Standard:** `{spec_info['standard_ref']}`")
        with col2:
            st.markdown(f"**Overview:** {spec_info['description']}")
        
        st.markdown("---")
        st.markdown("### 📖 Governing Standard Reference Snippets")
        for ref in spec_info["reference_snippets"]:
            st.info(f"• {ref}")
    else:
        st.markdown("Select one of the 8 pre-loaded sample specifications from the sidebar to inspect its governing standards and protocol reference guidelines.")

with tab3:
    st.subheader("Verification Plan (VPlan)")
    if st.session_state.graph_state["vplan"]:
        for vp in st.session_state.graph_state["vplan"]:
            with st.expander(f"{vp['vplan_id']} | Linked Requirement: {vp['req_id']}"):
                st.markdown(f"**Verification Method:** `{vp['verification_method']}`")
                st.markdown(f"**Strategy Summary:** {vp['strategy_summary']}")
    else:
        st.info("Complete the HITL Specification Review in Tab 1 to generate the VPlan.")

with tab4:
    st.subheader("Generated Test Cases, Objectives & Rationale")
    if st.session_state.graph_state["test_cases"]:
        for tc in st.session_state.graph_state["test_cases"]:
            with st.expander(f"{tc['test_id']}: {tc['name']}"):
                st.markdown(f"**Objective:** {tc['objective']}")
                st.markdown(f"**Why It Is Important:** {tc['why_important']}")
                st.code(tc['code_snippet'], language="systemverilog")
    else:
        st.info("Awaiting downstream test case generation.")

with tab5:
    st.subheader("SystemVerilog Assertions (SVA) & Functional Coverage Models")
    if st.session_state.graph_state["assertions"]:
        st.markdown("### 🎯 Formal SVA Checkers")
        for sva in st.session_state.graph_state["assertions"]:
            st.markdown(f"**{sva['assertion_id']}** (`{sva['name']}`)")
            st.code(sva['sva_code'], language="systemverilog")
        
        st.markdown("---")
        st.markdown("### 📊 Functional Coverage Models")
        for cov in st.session_state.graph_state["coverage_models"]:
            st.markdown(f"**{cov['cover_id']} Group:** `{cov['group_name']}`")
            st.caption(cov['bins_description'])
    else:
        st.info("Assertions and coverage models will render here once pipeline completes.")

with tab6:
    st.subheader("Golden Traceability Matrix (Requirement $\rightarrow$ Test $\rightarrow$ Result $\rightarrow$ Evidence)")
    st.markdown("Unbroken chain of custody for enterprise safety audits (ISO 26262 / DO-254).")
    if st.session_state.graph_state["traceability_matrix"]:
        df_trace = pd.DataFrame(st.session_state.graph_state["traceability_matrix"])
        st.dataframe(df_trace, use_container_width=True)
        
        # Export options
        csv_data = df_trace.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Traceability Matrix (CSV)",
            data=csv_data,
            file_name="spec2verify_traceability_matrix.csv",
            mime="text/csv"
        )
    else:
        st.info("Audit package available after simulation execution runs.")

with tab7:
    st.subheader("Verification Analytics & Step-by-Step Execution Logs")
    
    # KPI Metrics Row
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Requirements", len(st.session_state.graph_state["requirements"]))
    k2.metric("Test Cases", len(st.session_state.graph_state["test_cases"]))
    k3.metric("Assertions", len(st.session_state.graph_state["assertions"]))
    k4.metric("Spec Doubts", len(st.session_state.graph_state["spec_doubts"]))
    
    st.markdown("---")
    
    # Charts Section
    if st.session_state.graph_state["requirements"]:
        ch1, ch2 = st.columns(2)
        with ch1:
            st.markdown("### Requirements by Category")
            df_reqs = pd.DataFrame(st.session_state.graph_state["requirements"])
            if "category" in df_reqs.columns:
                st.bar_chart(df_reqs["category"].value_counts())
        with ch2:
            st.markdown("### Verification Priority Distribution")
            if "priority" in df_reqs.columns:
                st.bar_chart(df_reqs["priority"].value_counts())
    else:
        st.info("Load a specification to render analytics charts.")
        
    st.markdown("---")
    st.markdown("### 📋 Multi-Agent Execution Trace Logs")
    logs = st.session_state.graph_state.get("execution_logs", [])
    if logs:
        df_logs = pd.DataFrame(logs)
        st.dataframe(df_logs, use_container_width=True)
    else:
        st.info("No execution logs recorded yet. Finalize the specification to trigger agent execution.")
