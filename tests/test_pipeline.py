"""
Spec2Verify Automated Test Suite
Validates LangGraph multi-agent orchestration, Human-in-the-Loop gates,
and downstream verification artifact generation.
"""

from src.graph import build_verification_graph

def test_verification_graph_execution():
    """Tests full pipeline execution from approved specification to audit traceability."""
    graph = build_verification_graph()
    
    initial_state = {
        "raw_document_text": "Sample microarchitecture specification text for AXI4-Stream FIFO controller data interface.",
        "requirements": [
            {
                "req_id": "REQ_TEST_01",
                "description": "TVALID must remain asserted until TREADY is sampled high.",
                "category": "Protocol",
                "priority": "Mandatory",
                "status": "Pending"
            }
        ],
        "spec_doubts": [],
        "human_feedback": "",
        "is_spec_approved": True,  # Bypasses HITL pause for automated testing
        "vplan": [],
        "test_cases": [],
        "assertions": [],
        "coverage_models": [],
        "traceability_matrix": [],
        "execution_logs": []
    }
    
    # Invoke the compiled LangGraph workflow
    result_state = graph.invoke(initial_state)
    
    # Assertions to verify correct multi-agent output generation
    assert len(result_state["requirements"]) > 0, "Requirements extraction failed."
    assert len(result_state["vplan"]) > 0, "Verification Plan generation failed."
    assert len(result_state["test_cases"]) > 0, "UVM test case generation failed."
    assert len(result_state["assertions"]) > 0, "SystemVerilog Assertion generation failed."
    assert len(result_state["coverage_models"]) > 0, "Coverage model generation failed."
    assert len(result_state["traceability_matrix"]) > 0, "Traceability matrix compilation failed."
    assert len(result_state["execution_logs"]) > 0, "Step-by-step execution logging failed."
    
    # Validate structure of the golden traceability record
    trace_record = result_state["traceability_matrix"][0]
    assert "Requirement" in trace_record
    assert "Test" in trace_record
    assert "Result" in trace_record
    assert "Evidence" in trace_record
    assert trace_record["Result"] == "PASS"
