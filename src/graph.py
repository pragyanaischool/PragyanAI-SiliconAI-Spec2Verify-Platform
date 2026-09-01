"""
Spec2Verify LangGraph Orchestration Pipeline with HITL & Execution Logging
Manages autonomous multi-agent hardware verification workflows, spec proofreading gates,
and structured trace logging.
"""

from datetime import datetime
from langgraph.graph import StateGraph, END
from src.state import AgentState, LogRecord
from src.agents.spec_agent import extract_spec_and_doubts
from src.agents.vplan_agent import generate_vplan
from src.agents.test_agent import generate_test_cases
from src.agents.assertion_agent import generate_assertions
from src.agents.coverage_agent import generate_coverage_models
from src.agents.audit_agent import generate_traceability_matrix

def log_step(state: AgentState, agent_name: str, message: str, status: str = "SUCCESS") -> AgentState:
    """Appends a timestamped execution trace log to the graph state."""
    if "execution_logs" not in state or state["execution_logs"] is None:
        state["execution_logs"] = []
    
    state["execution_logs"].append(
        LogRecord(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            agent=agent_name,
            message=message,
            status=status
        )
    )
    return state

def wrapped_extract_spec(state: AgentState) -> AgentState:
    """Node 1: Spec Ingestion, Atomic Requirement Extraction & Ambiguity Auditor."""
    try:
        state = extract_spec_and_doubts(state)
        req_count = len(state.get("requirements", []))
        doubt_count = len(state.get("spec_doubts", []))
        return log_step(state, "SpecAgent", f"Extracted {req_count} requirements and flagged {doubt_count} specification ambiguities.")
    except Exception as e:
        return log_step(state, "SpecAgent", f"Error during spec extraction: {str(e)}", status="ERROR")

def run_downstream_pipeline(state: AgentState) -> AgentState:
    """Executes the sequential downstream verification pipeline after human approval."""
    try:
        # Step 2: Verification Plan Generation
        state = generate_vplan(state)
        state = log_step(state, "VPlanAgent", f"Generated {len(state.get('vplan', []))} Verification Plan entries mapped to VPlan methods.")
        
        # Step 3: Test Case & UVM Testbench Synthesis
        state = generate_test_cases(state)
        state = log_step(state, "TestAgent", f"Synthesized {len(state.get('test_cases', []))} UVM test cases with taxonomic metadata and code snippets.")
        
        # Step 4: SystemVerilog Assertion (SVA) Synthesis
        state = generate_assertions(state)
        state = log_step(state, "AssertionAgent", f"Synthesized {len(state.get('assertions', []))} formal SystemVerilog Assertions (SVA).")
        
        # Step 5: Functional Coverage Model Synthesis
        state = generate_coverage_models(state)
        state = log_step(state, "CoverageAgent", f"Built {len(state.get('coverage_models', []))} functional coverage groups and cross-bins.")
        
        # Step 6: Audit Traceability & Compliance Package Compilation
        state = generate_traceability_matrix(state)
        state = log_step(state, "AuditAgent", f"Compiled bi-directional traceability matrix with {len(state.get('traceability_matrix', []))} records.")
        
        return log_step(state, "PipelineOrchestrator", "Successfully completed downstream verification pipeline generation for compliance sign-off.")
    except Exception as e:
        return log_step(state, "PipelineOrchestrator", f"Pipeline execution failed: {str(e)}", status="ERROR")

def human_review_gate(state: AgentState) -> str:
    """Conditional router that pauses execution for HITL proofreading or proceeds upon approval."""
    if state.get("is_spec_approved", False):
        return "approved"
    return "waiting_for_human"

def build_verification_graph():
    """Builds and compiles the complete LangGraph state machine workflow with HITL and trace logging."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("extract_spec", wrapped_extract_spec)
    workflow.add_node("downstream_pipeline", run_downstream_pipeline)
    
    # Entry point
    workflow.set_entry_point("extract_spec")
    
    # HITL conditional routing edge
    workflow.add_conditional_edges(
        "extract_spec",
        human_review_gate,
        {
            "waiting_for_human": END,  # Pauses execution for Streamlit UI review
            "approved": "downstream_pipeline"
        }
    )
    
    workflow.add_edge("downstream_pipeline", END)
    
    return workflow.compile()
