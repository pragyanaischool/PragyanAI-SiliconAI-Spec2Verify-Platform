from typing import List, Dict, Optional, TypedDict

class Requirement(TypedDict):
    req_id: str
    description: str
    category: str
    priority: str
    status: str

class VerificationPlan(TypedDict):
    vplan_id: str
    req_id: str
    verification_method: str
    strategy_summary: str

class TestCase(TypedDict):
    test_id: str
    req_id: str
    name: str
    objective: str
    why_important: str
    code_snippet: str

class Assertion(TypedDict):
    assertion_id: str
    req_id: str
    name: str
    sva_code: str

class CoverageModel(TypedDict):
    cover_id: str
    req_id: str
    group_name: str
    bins_description: str

class TraceRecord(TypedDict):
    Requirement: str
    Test: str
    Result: str
    Evidence: str

class LogRecord(TypedDict):
    timestamp: str
    agent: str
    message: str
    status: str

class AgentState(TypedDict):
    raw_document_text: str
    requirements: List[Requirement]
    spec_doubts: List[Dict[str, str]]
    human_feedback: Optional[str]
    is_spec_approved: bool
    vplan: List[VerificationPlan]
    test_cases: List[TestCase]
    assertions: List[Assertion]
    coverage_models: List[CoverageModel]
    traceability_matrix: List[TraceRecord]
    execution_logs: List[LogRecord]
