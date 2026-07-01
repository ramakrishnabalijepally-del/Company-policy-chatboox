"""
Run this script once to generate sample policy PDFs for testing.
Requirements: pip install fpdf2
"""
from fpdf import FPDF
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "policies")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def make_pdf(filename: str, title: str, sections: list[tuple[str, str]]):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 12, title, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, "Effective Date: January 1, 2024  |  Version 2.0", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)

    for heading, body in sections:
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, heading, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, body)
        pdf.ln(3)

    path = os.path.join(OUTPUT_DIR, filename)
    pdf.output(path)
    print(f"Created: {path}")


# ── HR Policy ──────────────────────────────────────────────────────────────────
make_pdf("HR_Policy.pdf", "Human Resources Policy", [
    ("1. Purpose", (
        "This HR Policy establishes the standards and procedures governing employment at our company. "
        "It applies to all full-time, part-time, and contract employees across all departments and locations."
    )),
    ("2. Recruitment & Hiring", (
        "All open positions must be approved by the department head and HR before posting. "
        "Job advertisements will be posted internally for a minimum of 5 business days before external posting. "
        "Interviews will be conducted by a panel of at least two people including the direct manager. "
        "Reference checks are mandatory for all final candidates. "
        "Employment offers are contingent upon successful background verification."
    )),
    ("3. Onboarding", (
        "New employees undergo a structured 30-day onboarding program. "
        "On Day 1, employees receive equipment, system access, and a welcome kit. "
        "During Week 1, they attend mandatory orientation covering company culture, policies, and compliance. "
        "A designated buddy is assigned for the first 60 days. "
        "Probationary period is 90 days for all new hires."
    )),
    ("4. Performance Reviews", (
        "Performance reviews are conducted bi-annually in June and December. "
        "Each employee sets SMART goals with their manager at the start of each review period. "
        "Ratings scale: Exceeds Expectations, Meets Expectations, Needs Improvement, Unsatisfactory. "
        "Employees rated 'Unsatisfactory' for two consecutive reviews may face a Performance Improvement Plan (PIP). "
        "Merit increases are linked to performance ratings and are effective from January 1 each year."
    )),
    ("5. Compensation & Benefits", (
        "Salaries are reviewed annually. Market benchmarking is conducted every two years. "
        "The company offers health insurance, dental, and vision coverage from Day 1 of employment. "
        "Employees are eligible for the 401(k) plan with a 4% company match after 3 months of service. "
        "Remote work stipend of $50/month is provided for approved remote employees."
    )),
    ("6. Termination", (
        "Employees wishing to resign must provide at least 2 weeks written notice. "
        "The company may terminate employment with cause immediately or without cause with 2 weeks severance. "
        "Exit interviews are conducted by HR for all departing employees. "
        "All company property must be returned on or before the last working day."
    )),
])

# ── Leave Policy ───────────────────────────────────────────────────────────────
make_pdf("Leave_Policy.pdf", "Leave & Time-Off Policy", [
    ("1. Overview", (
        "This policy outlines the types of leave available to employees and the procedures for requesting time off. "
        "All leave requests must be submitted through the HR portal unless stated otherwise."
    )),
    ("2. Annual Leave (Paid Time Off)", (
        "Full-time employees accrue 1.5 days of PTO per month (18 days per year). "
        "PTO begins accruing from Day 1 but may not be taken during the 90-day probationary period. "
        "A maximum of 5 unused PTO days may be carried over to the next calendar year. "
        "PTO requests must be submitted at least 3 business days in advance for durations up to 3 days, "
        "and at least 2 weeks in advance for longer periods. "
        "Approval is subject to business needs and manager discretion."
    )),
    ("3. Sick Leave", (
        "Employees are entitled to 10 paid sick days per calendar year. "
        "Sick days do not carry over and are not paid out upon termination. "
        "For absences exceeding 3 consecutive days, a doctor's note is required. "
        "Chronic illness accommodation requests should be directed to HR."
    )),
    ("4. Maternity Leave", (
        "Primary caregivers (birthing parents) are entitled to 16 weeks of fully paid maternity leave. "
        "Leave may begin up to 4 weeks before the expected due date. "
        "An additional 4 weeks of unpaid leave may be requested. "
        "Employees must notify HR at least 8 weeks before the intended start of leave."
    )),
    ("5. Paternity / Secondary Caregiver Leave", (
        "Secondary caregivers (non-birthing parents, adoptive parents) receive 4 weeks of fully paid leave. "
        "Leave must be taken within 6 months of the birth or adoption. "
        "Requests must be submitted to HR at least 4 weeks in advance."
    )),
    ("6. Bereavement Leave", (
        "Employees may take up to 5 days of paid bereavement leave for the death of an immediate family member "
        "(spouse, child, parent, sibling). "
        "Up to 2 days are granted for extended family members (grandparents, in-laws, aunts/uncles)."
    )),
    ("7. Public Holidays", (
        "The company observes 11 federal public holidays. "
        "A list of observed holidays is published on the HR portal each December for the following year. "
        "Employees required to work on a public holiday receive compensatory time off."
    )),
    ("8. Unpaid Leave", (
        "Employees with at least 1 year of service may apply for up to 30 days of unpaid leave per year. "
        "Approval is at management and HR discretion based on business requirements."
    )),
])

# ── Code of Conduct ────────────────────────────────────────────────────────────
make_pdf("Code_of_Conduct.pdf", "Code of Conduct & Ethics Policy", [
    ("1. Introduction", (
        "This Code of Conduct outlines the ethical standards and behavioral expectations for all employees, "
        "contractors, and representatives of the company. Adherence to this code is a condition of employment."
    )),
    ("2. Workplace Behavior", (
        "All employees are expected to treat colleagues, clients, and visitors with respect and dignity. "
        "Bullying, harassment, intimidation, or any form of discrimination based on race, gender, religion, "
        "age, disability, sexual orientation, or national origin is strictly prohibited. "
        "Conflicts should be resolved professionally and escalated to HR if unresolved. "
        "Employees must maintain a positive and collaborative work environment."
    )),
    ("3. Anti-Harassment Policy", (
        "Sexual harassment, including unwanted physical contact, verbal abuse, and inappropriate digital "
        "communication, is a serious violation and grounds for immediate termination. "
        "Employees who experience or witness harassment must report it to HR or via the anonymous hotline. "
        "All reports are investigated promptly and confidentially. "
        "Retaliation against anyone who files a good-faith complaint is strictly prohibited."
    )),
    ("4. Ethics & Conflict of Interest", (
        "Employees must disclose any financial interest, personal relationship, or secondary employment "
        "that could create a conflict of interest with their duties. "
        "Acceptance of gifts or hospitality from vendors exceeding $50 in value must be reported to HR. "
        "Insider trading based on non-public company information is illegal and strictly prohibited."
    )),
    ("5. Confidentiality", (
        "Employees must protect confidential company information including business strategies, financial data, "
        "customer lists, and proprietary technology. "
        "Confidentiality obligations continue for 2 years after employment ends. "
        "Unauthorized sharing of confidential information may result in legal action."
    )),
    ("6. Dress Code", (
        "Business casual attire is required Monday through Thursday. "
        "Fridays are casual dress days. "
        "Client-facing meetings require business professional attire regardless of the day. "
        "Clothing with offensive graphics, slogans, or imagery is never permitted. "
        "Remote employees are expected to dress professionally for video calls."
    )),
    ("7. Use of Company Resources", (
        "Company equipment, software, and networks are for business use. "
        "Limited personal use is acceptable provided it does not interfere with work or violate other policies. "
        "Employees must not install unauthorized software on company devices. "
        "All activity on company networks may be monitored in accordance with applicable law."
    )),
    ("8. Social Media", (
        "Employees must not post confidential information or make statements that could damage the company's "
        "reputation on social media. "
        "Personal social media accounts are the employee's responsibility. "
        "Any official company communications must be approved by the Marketing department."
    )),
    ("9. Reporting Violations", (
        "Employees are encouraged to report suspected violations of this Code via the HR portal, "
        "directly to HR, or through the anonymous ethics hotline at 1-800-XXX-XXXX. "
        "All reports are taken seriously and investigated impartially. "
        "Knowingly filing a false report is itself a violation of this Code."
    )),
    ("10. Disciplinary Action", (
        "Violations of this Code may result in disciplinary action ranging from a verbal warning to "
        "immediate termination, depending on the severity of the violation. "
        "Serious violations such as harassment, theft, or fraud will result in immediate termination "
        "and may be referred to law enforcement."
    )),
])

print("\nAll sample policy PDFs generated successfully in ./data/policies/")
