import io
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib
from weasyprint import HTML, CSS
from django.template.loader import render_to_string

matplotlib.use('Agg')  # Non-GUI backend


def generate_biomarker_chart(results, biomarker):
    """
    Generate a matplotlib chart image (PNG) for a biomarker trend.
    Returns the image as bytes.
    """
    fig, ax = plt.subplots(figsize=(8, 4), dpi=100)

    test_dates = [r.test_date for r in results]
    values = [float(r.value) for r in results]

    ax.plot(test_dates, values, marker='o', linewidth=2, markersize=6, color='#2f6fed')

    # Add reference range as shaded area if available
    if biomarker.reference_min is not None and biomarker.reference_max is not None:
        ax.axhspan(
            float(biomarker.reference_min),
            float(biomarker.reference_max),
            alpha=0.2,
            color='green',
            label='Reference range',
        )

    ax.set_xlabel('Date')
    ax.set_ylabel(f'{biomarker.name} ({biomarker.unit})')
    ax.set_title(f'{biomarker.name} Trend')
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Rotate x-axis labels
    fig.autofmt_xdate()

    # Save to bytes
    img_bytes = io.BytesIO()
    fig.savefig(img_bytes, format='png', bbox_inches='tight')
    img_bytes.seek(0)
    plt.close(fig)

    return img_bytes.getvalue()


def generate_report_pdf(patient, biomarker, results, recorded_by):
    """
    Generate a PDF report from HTML template.
    Returns the PDF as bytes.
    """
    # Generate chart image
    chart_bytes = generate_biomarker_chart(results, biomarker)
    chart_base64 = __import__('base64').b64encode(chart_bytes).decode('utf-8')

    # Prepare context
    context = {
        'patient': patient,
        'biomarker': biomarker,
        'results': results,
        'chart_base64': chart_base64,
        'generated_at': datetime.now(),
        'generated_by': recorded_by.username,
    }

    # Render HTML template
    html_string = render_to_string('reports/patient_report.html', context)

    # Convert HTML to PDF
    html = HTML(string=html_string, base_url='.')
    pdf_bytes = html.write_pdf()

    return pdf_bytes