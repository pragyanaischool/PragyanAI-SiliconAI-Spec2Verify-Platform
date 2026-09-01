"""
Spec2Verify Central Graph State Definition
Defines shared typing and data structures for multi-agent hardware verification workflows.
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

class VPlanItem(TypedDict):
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

class AssertionItem(TypedDict):
    assertion_id: str
    req_id: str
    name: str
    sva_code: str

class CoverageModel(TypedDict):
    cover_id: str
    req_id: str
    group_name: str
    bins_description: str

class TraceabilityRow(TypedDict):
    req_id: str
    requirement: str
    vplan_id: str
    test_id: str
    assertion_id: str
    status: str

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
    vplan: List[VPlanItem]
    test_cases: List[TestCase]
    assertions: List[AssertionItem]
    coverage_models: List[CoverageModel]
    traceability_matrix: List[TraceabilityRow]
    execution_logs: List[LogRecord]
