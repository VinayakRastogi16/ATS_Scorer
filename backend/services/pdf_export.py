import io
import logging
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    PageBreak,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

logger = logging.getLogger("ats_resume_scorer")


import re

def html_to_text(html):
    # Remove style blocks completely
    html = re.sub(
        r'<style.*?>.*?</style>',
        '',
        html,
        flags=re.DOTALL | re.IGNORECASE
    )

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html)

    return text.strip()


def generate_combined_pdf(html_docs: dict[str, str]) -> bytes:
    """
    Generate a combined PDF from multiple HTML reports.
    Returns PDF bytes.
    """

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    story = []

    for index, (title, html_content) in enumerate(html_docs.items()):

        story.append(Paragraph(title, styles["Heading1"]))
        story.append(Spacer(1, 12))

        text = html_to_text(html_content)

        for line in text.split("\n"):
            line = line.strip()
            if line:
                story.append(Paragraph(line, styles["BodyText"]))

        if index < len(html_docs) - 1:
            story.append(PageBreak())

    doc.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes