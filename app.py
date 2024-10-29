from flask import Flask, render_template, request, flash, redirect, url_for, send_file
import subprocess
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from docx import Document
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production!

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/network_scanner', methods=['GET', 'POST'])
def network_scanner():
    if request.method == 'POST':
        target_ip = request.form['target_ip']
        port_selection = request.form['port_selection']
        authorized = request.form.get('authorized')

        if authorized:
            # Simulate a dummy network scan
            results = subprocess.run(['python', 'scripts/network_scanner.py', target_ip, port_selection], capture_output=True, text=True)
            output = results.stdout

            # Generate PDF report
            pdf_file = create_pdf_report(target_ip, port_selection, output)
            word_file = create_word_report(target_ip, port_selection, output)

            return render_template('report.html', output=output, tool='Network Scanner', pdf_file=pdf_file, word_file=word_file)
        else:
            flash('You must agree to the Terms of Service.')
            return redirect(url_for('network_scanner'))

    return render_template('network_scanner.html')

def create_pdf_report(target_ip, port_selection, output):
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    pdf.drawString(100, 750, f"Network Scan Report for {target_ip}")
    pdf.drawString(100, 730, f"Ports Selected: {port_selection}")
    pdf.drawString(100, 710, "Scan Results:")
    pdf.drawString(100, 690, output)
    pdf.save()
    pdf_buffer.seek(0)
    return pdf_buffer

def create_word_report(target_ip, port_selection, output):
    doc = Document()
    doc.add_heading('Network Scan Report', level=1)
    doc.add_paragraph(f'Target IP: {target_ip}')
    doc.add_paragraph(f'Ports Selected: {port_selection}')
    doc.add_heading('Scan Results:', level=2)
    doc.add_paragraph(output)
    
    word_buffer = BytesIO()
    doc.save(word_buffer)
    word_buffer.seek(0)
    return word_buffer

@app.route('/download_report/<report_type>')
def download_report(report_type):
    if report_type == 'pdf':
        return send_file(create_pdf_report("dummy_target", "dummy_ports", "No results"), as_attachment=True, download_name='scan_report.pdf')
    elif report_type == 'word':
        return send_file(create_word_report("dummy_target", "dummy_ports", "No results"), as_attachment=True, download_name='scan_report.docx')
    return "Invalid report type", 400

@app.route('/website_scanner', methods=['GET', 'POST'])
def website_scanner():
    if request.method == 'POST':
        target_url = request.form['target_url']
        
        # Simulate a dummy website scan
        results = subprocess.run(['python', 'scripts/web_scanner.py', target_url], capture_output=True, text=True)
        output = results.stdout

        return render_template('report.html', output=output, tool='Website Scanner')

    return render_template('website_scanner.html')

if __name__ == '__main__':
    app.run(debug=True)
