from flask import Flask, request, render_template, send_file
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import io

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Obtendo os dados do formulário
    data = request.form
    nome_paciente = data.get('nome_paciente')
    numero_prontuario = data.get('numero_prontuario')
    nome_mae = data.get('nome_mae')
    municipio_residencia = data.get('municipio_residencia')
    sinais_sintomas = data.get('sinais_sintomas')
    condicoes_justificam = data.get('condicoes_justificam')
    resultados_provas = data.get('resultados_provas')
    diagnostico_inicial = data.get('diagnostico_inicial')
    cid10_principal = data.get('cid10_principal')
    descricao_procedimento = data.get('descricao_procedimento')
    carater_internacao = data.get('carater_internacao')
    nome_profissional = data.get('nome_profissional')
    assinatura_profissional = data.get('assinatura_profissional')

    # Leitura do PDF original
    input_pdf_path = "static/aih_laudo_internacao.pdf"
    pdf_reader = PdfReader(input_pdf_path)
    pdf_writer = PdfWriter()

    # Selecionar a primeira página do PDF
    page = pdf_reader.pages[0]

    # Adicionar a página ao escritor de PDF
    pdf_writer.add_page(page)

    # Criar um buffer para o novo PDF
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Adicionar texto ao PDF
    can.drawString(100, 800, "HOSPITAL DR. JOSÉ PEDRO BEZERRA")  # Campo 1
    can.drawString(100, 780, "HOSPITAL DR. JOSÉ PEDRO BEZERRA")  # Campo 3
    can.drawString(100, 760, datetime.now().strftime("%d/%m/%Y"))  # Campo 34

    can.drawString(100, 740, nome_paciente)  # Campo 5
    can.drawString(100, 720, numero_prontuario)  # Campo 6
    can.drawString(100, 700, nome_mae)  # Campo 11
    can.drawString(100, 680, municipio_residencia)  # Campo 16
    can.drawString(100, 660, sinais_sintomas)  # Campo 20
    can.drawString(100, 640, condicoes_justificam)  # Campo 21
    can.drawString(100, 620, resultados_provas)  # Campo 22
    can.drawString(100, 600, diagnostico_inicial)  # Campo 23
    can.drawString(100, 580, cid10_principal)  # Campo 24
    can.drawString(100, 560, descricao_procedimento)  # Campo 27
    can.drawString(100, 540, carater_internacao)  # Campo 30
    can.drawString(100, 520, nome_profissional)  # Campo 33
    can.drawString(100, 500, assinatura_profissional)  # Campo 35

    can.save()

    # Mover o buffer para o início
    packet.seek(0)
    new_pdf = PdfReader(packet)
    new_page = new_pdf.pages[0]

    # Mesclar a nova página com o PDF original
    page.merge_page(new_page)
    pdf_writer.add_page(page)

    # Escrever o PDF preenchido em um buffer
    pdf_buffer = io.BytesIO()
    pdf_writer.write(pdf_buffer)
    pdf_buffer.seek(0)

    return send_file(pdf_buffer, as_attachment=True, download_name='laudo_preenchido.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
