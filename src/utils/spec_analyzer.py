"""
Spec2Verify Tiered Specification Analyzer
Expounds and breaks down hardware specifications across Beginner, Intermediate, and Expert levels
for educational and verification deep-dive analysis.
"""

def analyze_requirement_tiered(req_id: str, description: str, category: str) -> dict:
    """Generates multi-tier educational and verification breakdowns for a given requirement."""
    
    # Tier 1: Beginner (Intuitive Analogy & Plain English)
    beginner = (
        f"Imagine a physical delivery pipeline or mailing slot. Rule [{req_id}] ensures that the component "
        f"handles data safely without dropping items, causing data jams, or violating timing constraints. "
        f"In plain English: {description}"
    )
    
    # Tier 2: Intermediate (Protocol & Verification View)
    intermediate = (
        f"Category: [{category}]. From a verification perspective, this rule governs "
        f"signal state transitions and handshake handshakes between master and slave endpoints. "
        f"Engineers must write constrained-random transaction sequences to toggle control lines "
        f"and monitor bus stability during active transfer cycles."
    )
    
    # Tier 3: Expert (Formal Assertion & Safety Sign-Off)
    expert = (
        f"Formal Property / SVA Invariant: Enforces strict temporal bounds and cycle-accurate handshakes. "
        f"Risk analysis requires checking Asynchronous Clock Domain (CDC) boundary hazards, propagation delays, and "
        f"proving zero deadlock states to satisfy ISO 26262 / DO-254 safety compliance mandates."
    )
    
    return {
        "beginner": beginner,
        "intermediate": intermediate,
        "expert": expert
    }
