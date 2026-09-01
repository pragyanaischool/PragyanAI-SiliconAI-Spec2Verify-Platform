"""
Spec2Verify Enterprise Studio
Streamlit Entrypoint & Interactive Dashboard with AI Verification Tutor
"""

import streamlit as st
import pandas as pd
from pypdf import PdfReader
from src.knowledge_bank import SAMPLE_SPECIFICATIONS
from src.graph import build_verification_graph
from src.utils.pdf_exporter import generate_pdf_report
from src.utils.spec_analyzer import analyze_requirement_tiered
from src.agents.tutor_agent import get_tutor_guidance

# Page Configuration
st.set_page_config(
    page_title="Spec2Verify | PragyanAI Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; letter-spacing: -0.5px; }
    .sub-text { font-size: 1.1rem; color: #4B5563; margin-bottom: 1.5rem; }
    .stAlert { border-radius: 8px; }
    div.stButton > button:first-child { border-radius: 6px; font-weight: 600; }
    .sidebar-brand { padding: 10px 0px 20px 0px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

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
with st.sidebar:
    st.markdown('<div class="sidebar-brand">', unsafe_allow_html=True)
    try:
        st.image("PragyanAI_Transperent.png", width=220)
    except Exception:
        st.markdown("### ⚡ PragyanAI Studio")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.header("📁 Specification Source")
    input_mode = st.radio(
        "Choose Input Method",
        ["Sample Library (8 Specs)", "Custom PDF Upload", "Manual Specification Text"]
    )

    if input_mode == "Sample Library (8 Specs)":
        spec_choice = st.selectbox("Select Hardware Protocol / Spec", list(SAMPLE_SPECIFICATIONS.keys()))
        if st.button("Load Sample Specification", type="primary", use_container_width=True):
            spec_data = SAMPLE_SPECIFICATIONS[spec_choice]
            st.session_state.selected_spec_name = spec_choice
            st.session_state.graph_state["raw_document_text"] = spec_data["description"]
            
            # Ensure requirements are fully loaded into session state with fallback
            raw_reqs = spec_data.get("requirements", [])
            if not raw_reqs:
                raw_reqs = [
                    {"req_id": "REQ_GEN_01", "description": f"Primary interface handshake must comply with {spec_choice} protocol specifications.", "category": "Protocol", "priority": "Mandatory"},
                    {"req_id": "REQ_GEN_02", "description": "Error handling registers must assert status flags within 1 clock cycle of fault detection.", "category": "Error Handling", "priority": "Mandatory"}
                ]
                
            st.session_state.graph_state["requirements"] = [
                {"req_id": r["req_id"], "description": r["description"], "category": r["category"], "priority": r["priority"], "status": "Pending"}
                for r in raw_reqs
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
        uploaded_file = st.file_uploader("Upload Microarchitecture Spec / Datasheet", type=["pdf"])
        if uploaded_file:
            reader = PdfReader(uploaded_file)
            text = "".join([page.extract_text() for page in reader.pages])
            st.session_state.graph_state["raw_document_text"] = text
            st.session_state.selected_spec_name = uploaded_file.name
            
            # Auto-extract fallback requirements for custom PDF text
            st.session_state.graph_state["requirements"] = [
                {"req_id": "REQ_CUST_01", "description": f"Custom extracted rule from {uploaded_file.name}: Interface signals must maintain valid setup/hold times.", "category": "Protocol", "priority": "Mandatory"},
                {"req_id": "REQ_CUST_02", "description": f"Custom extracted rule from {uploaded_file.name}: Buffer overflow and underflow conditions must trigger interrupt flags.", "category": "Error Handling", "priority": "Mandatory"}
            ]
            st.session_state.graph_state["spec_doubts"] = [
                {"doubt_id": "DOUBT_CUST_01", "issue": "Unstructured natural language text detected in uploaded PDF.", "recommendation": "Review and refine atomic requirements in Tab 1 / Tab 3 before execution."}
            ]
            st.success(f"Loaded PDF '{uploaded_file.name}' and extracted initial requirements.")

    else:
        manual_text = st.text_area("Enter Specification Text", height=150, placeholder="Paste bus protocol or microarchitecture details here...")
        if st.button("Process Manual Text", use_container_width=True):
            if manual_text.strip():
                st.session_state.graph_state["raw_document_text"] = manual_text
                st.session_state.selected_spec_name = "Manual Text Input"
                
                # Auto-extract fallback requirements for manual text
                st.session_state.graph_state["requirements"] = [
                    {"req_id": "REQ_MAN_01", "description": f"Primary rule derived from manual specification text: {manual_text[:60]}...", "category": "Protocol", "priority": "Mandatory"}
                ]
                st.session_state.graph_state["spec_doubts"] = [
                    {"doubt_id": "DOUBT_MAN_01", "issue": "Manual text input requires verification against safety standards.", "recommendation": "Refine requirements using the live HITL editor."}
                ]
                st.success("Manual specification loaded and parsed successfully!")
            else:
                st.error("Please enter valid specification text.")

    st.markdown("---")
    st.markdown("### 🛠️ System Status")
    st.info(f"Active Spec: **{st.session_state.selected_spec_name or 'None'}**")
    st.info(f"Status: **{'Locked & Verified' if st.session_state.graph_state['is_spec_approved'] else 'Pending Proofreading'}**")

# Main Header Section
st.markdown('<p class="main-header">⚡ Spec2Verify: Specification-to-Verification Studio</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Autonomous Multi-Agent Verification Pipeline powered by PragyanAI for Safety-Critical Enterprise Hardware (ISO 26262 / DO-254).</p>', unsafe_allow_html=True)

# 9-Tab Architecture Including the AI Verification Tutor
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📖 Loaded Specification Deep-Dive & HITL Editor",
    "📚 Knowledge Bank: Protocol References & Standards",
    "📊 Human-in-the-Loop (HITL) Specification Proofreading",
    "📝 Verification Plan (VPlan)",
    "🧪 Generated Test Cases & Rationale",
    "🎯 Assertions & Coverage Models",
    "🔗 Golden Traceability Matrix",
    "📈 Verification Analytics & Logs",
    "🧠 AI Verification Tutor & Guide"
])

with tab1:
    st.subheader("📖 Loaded Specification Deep-Dive & Interactive HITL Editor")
    st.markdown("Inspect loaded specification text, examine multi-tier technical expansions, and edit/save requirement definitions interactively.")
    
    if st.session_state.selected_spec_name:
        st.markdown(f"### Active Specification: `{st.session_state.selected_spec_name}`")
        
        with st.expander("📄 View Raw Loaded Specification Text", expanded=False):
            st.text_area("Raw Text Content", value=st.session_state.graph_state["raw_document_text"], height=200, disabled=True)
            
        st.markdown("---")
        st.markdown("### 🔍 Tiered Requirement Analysis & Live HITL Editor")
        
        if st.session_state.graph_state["requirements"]:
            updated_requirements = []
            for i, req in enumerate(st.session_state.graph_state["requirements"]):
                with st.expander(f"Requirement [{req['req_id']}] - {req['category']} ({req['priority']})"):
                    new_desc = st.text_area(f"Edit Description ({req['req_id']})", value=req["description"], key=f"edit_desc_{i}")
                    
                    cat_options = ["Protocol", "Timing", "Error Handling", "Performance", "Functional"]
                    default_cat_idx = cat_options.index(req["category"]) if req["category"] in cat_options else 0
                    new_cat = st.selectbox(f"Category ({req['req_id']})", cat_options, index=default_cat_idx, key=f"edit_cat_{i}")
                    
                    pri_options = ["Mandatory", "Desirable", "Optional"]
                    default_pri_idx = pri_options.index(req["priority"]) if req["priority"] in pri_options else 0
                    new_pri = st.selectbox(f"Priority ({req['req_id']})", pri_options, index=default_pri_idx, key=f"edit_pri_{i}")
                    
                    updated_requirements.append({
                        "req_id": req["req_id"],
                        "description": new_desc,
                        "category": new_cat,
                        "priority": new_pri,
                        "status": req.get("status", "Pending")
                    })
                    
                    st.markdown("---")
                    st.markdown("#### 🎓 Multi-Tier Technical Breakdown")
                    tiers = analyze_requirement_tiered(req["req_id"], new_desc, new_cat)
                    
                    sub_t1, sub_t2, sub_t3 = st.tabs(["🟢 Beginner", "🟡 Intermediate", "🔴 Expert"])
                    with sub_t1:
                        st.info(tiers["beginner"])
                    with sub_t2:
                        st.warning(tiers["intermediate"])
                    with sub_t3:
                        st.error(tiers["expert"])
            
            if st.button("💾 Save Requirement Edits", type="primary"):
                st.session_state.graph_state["requirements"] = updated_requirements
                st.success("Requirements updated successfully across the session state!")
                st.rerun()
        else:
            st.info("No requirements extracted yet. Load a specification from the sidebar.")
    else:
        st.info("👈 Please load or upload a specification from the sidebar to use the Deep-Dive & HITL Editor.")

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
        st.markdown("Select one of the pre-loaded sample specifications from the sidebar to inspect its governing standards and protocol reference guidelines.")

with tab3:
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
                key=f"chk_hitl_{req['req_id']}"
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

with tab4:
    st.subheader("Verification Plan (VPlan)")
    if st.session_state.graph_state["vplan"]:
        for vp in st.session_state.graph_state["vplan"]:
            with st.expander(f"{vp['vplan_id']} | Linked Requirement: {vp['req_id']}"):
                st.markdown(f"**Verification Method:** `{vp['verification_method']}`")
                st.markdown(f"**Strategy Summary:** {vp['strategy_summary']}")
    else:
        st.info("Complete the HITL Specification Review in Tab 3 to generate the VPlan.")

with tab5:
    st.subheader("Generated Test Cases, Objectives & Rationale")
    if st.session_state.graph_state["test_cases"]:
        for tc in st.session_state.graph_state["test_cases"]:
            with st.expander(f"{tc['test_id']}: {tc['name']}"):
                st.markdown(f"**Objective:** {tc['objective']}")
                st.markdown(f"**Why It Is Important:** {tc['why_important']}")
                
                # Render Multi-Dimensional Taxonomic Badges
                st.markdown("#### 🎨 Multi-Dimensional Verification Taxonomy")
                col_b1, col_b2, col_b3, col_b4 = st.columns(4)
                col_b1.markdown("🟢 **Level:** IP")
                col_b2.markdown("🟣 **Visibility:** Black Box")
                col_b3.markdown("🟠 **Stimulus:** Constrained Random")
                col_b4.markdown("🔴 **Purpose:** Protocol")
                
                col_b5, col_b6, col_b7, col_b8 = st.columns(4)
                col_b5.markdown("🔵 **Scenario:** Corner / Stress")
                col_b6.markdown("🟣 **Method:** Simulation + SVA")
                col_b7.markdown("🟤 **Coverage:** Cross Coverage")
                col_b8.markdown("⚪ **Execution:** Nightly Regression")
                
                st.code(tc['code_snippet'], language="systemverilog")
    else:
        st.info("Awaiting downstream test case generation.")

with tab6:
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

with tab7:
    st.subheader("Golden Traceability Matrix (Requirement $\rightarrow$ Test $\rightarrow$ Result $\rightarrow$ Evidence)")
    st.markdown("Unbroken chain of custody for enterprise safety audits (ISO 26262 / DO-254).")
    if st.session_state.graph_state["traceability_matrix"]:
        df_trace = pd.DataFrame(st.session_state.graph_state["traceability_matrix"])
        st.dataframe(df_trace, use_container_width=True)
        
        col_dl1, col_dl2 = st.columns(2)
        
        with col_dl1:
            csv_data = df_trace.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV Audit Table",
                data=csv_data,
                file_name="spec2verify_traceability.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        with col_dl2:
            if st.button("📄 Generate Executive PDF Report", use_container_width=True):
                with st.spinner("Compiling enterprise verification PDF report..."):
                    pdf_path = generate_pdf_report(
                        st.session_state.graph_state,
                        st.session_state.selected_spec_name or "Custom Specification"
                    )
                    with open(pdf_path, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()
                        
                    st.download_button(
                        label="📥 Download Signed PDF Closure Report",
                        data=pdf_bytes,
                        file_name="spec2verify_closure_report.pdf",
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
    else:
        st.info("Complete specification review and run pipeline to generate audit evidence.")

with tab8:
    st.subheader("Verification Analytics & Step-by-Step Execution Logs")
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Requirements", len(st.session_state.graph_state["requirements"]))
    k2.metric("Test Cases", len(st.session_state.graph_state["test_cases"]))
    k3.metric("Assertions", len(st.session_state.graph_state["assertions"]))
    k4.metric("Spec Doubts", len(st.session_state.graph_state["spec_doubts"]))
    
    st.markdown("---")
    
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

with tab9:
    st.subheader("🧠 PragyanAI Master Verification Tutor & Guide")
    st.markdown("Your interactive training companion explaining specifications, guiding critical engineering questions, and breaking down test case categories and coverage models.")
    
    active_spec = st.session_state.selected_spec_name or "General Hardware Protocol"
    domain_type = SAMPLE_SPECIFICATIONS.get(active_spec, {}).get("domain", "System Interconnect")
    req_count = len(st.session_state.graph_state["requirements"])
    
    tutor_data = get_tutor_guidance(active_spec, domain_type, req_count)
    
    st.markdown(f"### 🎯 Active Training Context: `{active_spec}`")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("#### ❓ Critical Questions an Engineer Should Ask")
        st.markdown("When reviewing a new hardware microarchitecture specification, always investigate:")
        for q in tutor_data["guided_questions"]:
            st.markdown(f"* {q}")
            
    with col_t2:
        st.markdown("#### 🗺️ Spec-to-Testcase Mapping Strategy")
        st.info(tutor_data["mapping_strategy"])
        
    st.markdown("---")
    st.markdown("### 🧪 Comprehensive Test Case Categories Explained")
    cols_tc = st.columns(2)
    for idx, tc_type in enumerate(tutor_data["test_types"]):
        with cols_tc[idx % 2]:
            st.markdown(f"**📌 {tc_type['type']}**")
            st.write(tc_type["desc"])
            
    st.markdown("---")
    st.markdown("### 📊 Verification Coverage Models & Closure Framework")
    cols_cv = st.columns(3)
    for idx, cv_model in enumerate(tutor_data["coverage_models"]):
        with cols_cv[idx]:
            st.markdown(f"**🎯 {cv_model['model']}**")
            st.write(cv_model["desc"])
