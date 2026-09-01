"""
Spec2Verify Central Graph State Definition
Defines shared typing, TypedDicts, and aliases for multi-agent hardware verification workflows.
"""

from typing import TypedDict, List, Dict, Any

class Requirement(TypedDict):
    req_id: str
    description: str
    category: str
    priority: str
    status: str

class SpecDoubt(TypedDict):
    doubt_id: str
    issue: str
    recommendation: str

class VerificationPlan(TypedDict):
    vplan_id: str
    req_id: str
    verification_method: str
    strategy_summary: str

# Backwards-compatibility alias
VPlanItem = VerificationPlan

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

# Backwards-compatibility alias
AssertionItem = Assertion

class CoverageModel(TypedDict):
    cover_id: str
    req_id: str
    group_name: str
    bins_description: str

class TraceRecord(TypedDict):
    req_id: str
    requirement: str
    vplan_id: str
    test_id: str
    assertion_id: str
    status: str

# Backwards-compatibility alias
TraceabilityRow = TraceRecord

class LogRecord(TypedDict):
    timestamp: str
    agent: str
    message: str
    status: str

class AgentState(TypedDict):
    raw_document_text: str
    requirements: List[Requirement]
    spec_doubts: List[SpecDoubt]
    human_feedback: str
    is_spec_approved: bool
    vplan: List[VerificationPlan]
    test_cases: List[TestCase]
    assertions: List[Assertion]
    coverage_models: List[CoverageModel]
    traceability_matrix: List[TraceRecord]
    execution_logs: List[LogRecord]
