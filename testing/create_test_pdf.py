from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path

output = Path("sample_data/test.pdf")
output.parent.mkdir(parents=True, exist_ok=True)

pdf = canvas.Canvas(str(output), pagesize=letter)

pdf.drawString(72, 740, "Enterprise Knowledge Assistant")
pdf.drawString(72, 710, "Test Banking Policy Document")
pdf.drawString(72, 670, "Section 1: Unauthorized Transactions")
pdf.drawString(72, 640, "The bank must investigate unauthorized debit complaints.")
pdf.drawString(72, 610, "Customers should report suspicious transactions immediately.")
pdf.drawString(72, 570, "Section 2: Customer Compensation")
pdf.drawString(72, 540, "Eligible customers may receive compensation under bank policy.")

pdf.save()

print(f"Created: {output}")