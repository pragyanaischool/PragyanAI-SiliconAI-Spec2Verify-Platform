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
    """Appends a timestamped log record to the agent state execution logs."""
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
    """Node wrapper for specification ingestion and requirement extraction."""
    state = extract_spec_and_doubts(state)
    req_count = len(state.get("requirements", []))
    doubt_count = len(state.get("spec_doubts", []))
    return log_step(state, "SpecAgent", f"Extracted {req_count} requirements and {doubt_count} specification doubts.")

def run_downstream_pipeline(state: AgentState) -> AgentState:
    """Executes the sequential downstream verification pipeline after human specification approval."""
    state = generate_vplan(state)
    state = log_step(state, "VPlanAgent", f"Generated {len(state.get('vplan', []))} Verification Plan entries.")
    
    state = generate_test_cases(state)
    state = log_step(state, "TestAgent", f"Synthesized {len(state.get('test_cases', []))} UVM test cases.")
    
    state = generate_assertions(state)
    state = log_step(state, "AssertionAgent", f"Synthesized {len(state.get('assertions', []))} SystemVerilog Assertions.")
    
    state = generate_coverage_models(state)
    state = log_step(state, "CoverageAgent", f"Built {len(state.get('coverage_models', []))} functional coverage models.")
    
    state = generate_traceability_matrix(state)
    state = log_step(state, "AuditAgent", f"Compiled bi-directional traceability matrix with {len(state.get('traceability_matrix', []))} records.")
    
    return log_step(state, "PipelineOrchestrator", "Successfully completed downstream verification pipeline generation.")

def human_review_gate(state: AgentState) -> str:
    """Conditional router that pauses execution for human proofreading or proceeds upon approval."""
    if state.get("is_spec_approved", False):
        return "approved"
    return "waiting_for_human"

def build_verification_graph():
    """Builds and compiles the LangGraph state machine workflow."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("extract_spec", wrapped_extract_spec)
    workflow.add_node("downstream_pipeline", run_downstream_pipeline)
    
    # Define workflow entry point
    workflow.set_entry_point("extract_spec")
    
    # Add conditional routing for HITL proofreading gate
    workflow.add_conditional_edges(
        "extract_spec",
        human_review_gate,
        {
            "waiting_for_human": END,  # Pauses execution for UI review
            "approved": "downstream_pipeline"
        }
    )
    
    workflow.add_edge("downstream_pipeline", END)
    
    return workflow.compile()
