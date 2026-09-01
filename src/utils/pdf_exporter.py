"""
Spec2Verify PDF Exporter Utility
Generates professional enterprise verification closure reports in PDF format
for ISO 26262 and DO-254 safety compliance audits.
"""

from fpdf import FPDF
import tempfile

class VerificationPDFReport(FPDF):
    def header(self):
        # Header banner styling
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(30, 58, 138)  # Deep Navy Blue
        self.cell(0, 10, 'Spec2Verify - Enterprise Verification Closure Report', 0, 1, 'L')
        self.set_font('helvetica', '', 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, 'Automated Specification-to-Verification Audit Package (ISO 26262 / DO-254)', 0, 1, 'L')
        self.line(10, 22, 200, 22)
        self.ln(8)

    def footer(self):
        # Page numbering footer
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()} | Generated autonomously by Spec2Verify Agentic Studio', 0, 0, 'C')

def generate_pdf_report(state: dict, spec_name: str) -> str:
    """Compiles agent state data into a downloadable PDF report file path."""
    pdf = VerificationPDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Metadata Section
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f'Target Specification: {spec_name}', 0, 1)
    
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, f'Total Requirements Extracted: {len(state.get("requirements", []))}', 0, 1)
    pdf.cell(0, 6, f'Test Cases Synthesized: {len(state.get("test_cases", []))}', 0, 1)
    pdf.cell(0, 6, f'SystemVerilog Assertions: {len(state.get("assertions", []))}', 0, 1)
    pdf.ln(5)
    
    # 1. Requirements Ledger
    pdf.set_font('helvetica', 'B', 11)
    pdf.set_fill_color(240, 243, 246)
    pdf.cell(0, 7, ' 1. Requirements Ledger', 0, 1, 'L', fill=True)
    pdf.set_font('helvetica', '', 9)
    for req in state.get("requirements", []):
        pdf.multi_cell(0, 6, f"• [{req['req_id']}] ({req['category']} - {req['priority']}): {req['description']}")
    pdf.ln(5)
    
    # 2. Verification Plan Summary
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 7, ' 2. Verification Plan (VPlan)', 0, 1, 'L', fill=True)
    pdf.set_font('helvetica', '', 9)
    for vp in state.get("vplan", []):
        pdf.multi_cell(0, 6, f"• [{vp['vplan_id']}] Linked to {vp['req_id']} | Method: {vp['verification_method']}")
    pdf.ln(5)
    
    # 3. Golden Traceability Matrix Table
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 7, ' 3. Golden Traceability Matrix (Requirement -> Test -> Result -> Evidence)', 0, 1, 'L', fill=True)
    
    # Table Header
    pdf.set_font('helvetica', 'B', 8)
    pdf.cell(35, 6, 'Requirement', 1, 0, 'C', fill=True)
    pdf.cell(40, 6, 'Test Case', 1, 0, 'C', fill=True)
    pdf.cell(20, 6, 'Result', 1, 0, 'C', fill=True)
    pdf.cell(95, 6, 'Evidence / Simulation Artifact', 1, 1, 'C', fill=True)
    
    # Table Rows
    pdf.set_font('helvetica', '', 8)
    for row in state.get("traceability_matrix", []):
        pdf.cell(35, 6, str(row.get('Requirement', '')), 1)
        pdf.cell(40, 6, str(row.get('Test', '')), 1)
        pdf.cell(20, 6, str(row.get('Result', '')), 1, 0, 'C')
        pdf.cell(95, 6, str(row.get('Evidence', '')), 1, 1)
        
    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name
