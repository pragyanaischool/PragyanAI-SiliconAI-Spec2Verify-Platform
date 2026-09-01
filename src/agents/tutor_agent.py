"""
Spec2Verify AI Verification Tutor Agent
Acts as an expert Master Verification Trainer, providing guided engineering questions,
spec-to-testcase mapping strategies, and deep explanations of test types and coverage models.
"""

def get_tutor_guidance(spec_name: str, domain: str, requirements_count: int) -> dict:
    """Generates structured expert tutoring content based on the active specification context."""
    
    guided_questions = [
        "1. **Reset & Initialization:** What is the explicit state of the interface registers and internal pointers immediately after asynchronous reset release?",
        "2. **Backpressure & Flow Control:** How does the design behave if the receiver (`TREADY`/`PREADY`) stays LOW indefinitely while the master is streaming data?",
        "3. **Protocol Violations & Illegal States:** What happens if control signals violate setup/hold windows or if invalid command opcodes are injected?",
        "4. **Buffer Boundary Limits:** How does the architecture handle exact-match full and empty thresholds without dropping or duplicating packets?",
        "5. **Clock Domain Crossing (CDC):** Are there asynchronous control lines that require multi-flop synchronizers to prevent meta-stability?"
    ]
    
    mapping_strategy = (
        f"**Specification-to-Testcase Mapping Strategy for [{spec_name}] ({domain}):**\n"
        f"• **Atomic Decomposition:** Each requirement extracted from the specification must map to at least one dedicated directed test and multiple constrained-random seeds.\n"
        f"• **Equivalence Class Partitioning:** Group input parameters into valid ranges (e.g., standard burst lengths 1 to 16) and invalid boundary ranges (e.g., burst length 0 or >16).\n"
        f"• **Negative Testing:** Verify that error flags (like buffer overflow or protocol mismatch interrupts) assert within the mandated 1-cycle window."
    )
    
    test_types_breakdown = [
        {"type": "Directed Smoke Tests", "desc": "Verifies basic sanity and power-on reset state transitions."},
        {"type": "Constrained-Random Verification (CRV)", "desc": "Injects randomized bus delays, transaction gaps, and payload data widths to stress-test interconnect arbiters."},
        {"type": "Corner-Case Stress Tests", "desc": "Simulates back-to-back zero-latency transfers alternating with maximum backpressure stalls."},
        {"type": "Fault-Injection Tests", "desc": "Deliberately corrupts framing parity or bus enable strobes to validate error-handling interrupt latencies."}
    ]
    
    coverage_models_breakdown = [
        {"model": "Functional Coverage (Covergroups & Cross-Bins)", "desc": "Tracks cross-combinations of control variables (e.g., Burst Length × Data Width × Backpressure State) to ensure 100% design space closure."},
        {"model": "Code Coverage (Toggle & Line/Branch)", "desc": "Measures RTL execution completeness to identify dead logic or untested conditional branches."},
        {"model": "Assertion Coverage (SVA Property Success)", "desc": "Proves that temporal formal properties fire and are actively evaluated during stimulus execution without vacuity."}
    ]
    
    return {
        "guided_questions": guided_questions,
        "mapping_strategy": mapping_strategy,
        "test_types": test_types_breakdown,
        "coverage_models": coverage_models_breakdown
    }
