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

    # Definir as posições dos campos no PDF
    texts_positions = {
        "HOSPITAL DR. JOSÉ PEDRO BEZERRA": (70, 765),  # Campo 1
        "HOSPITAL DR. JOSÉ PEDRO BEZERRA": (70, 750),  # Campo 3
        datetime.now().strftime("%d/%m/%Y"): (445, 753),  # Campo 34
        nome_paciente: (135, 662),  # Campo 5
        numero_prontuario: (500, 662),  # Campo 6
        nome_mae: (135, 645),  # Campo 11
        municipio_residencia: (135, 627),  # Campo 16
        sinais_sintomas: (135, 579),  # Campo 20
        condicoes_justificam: (135, 562),  # Campo 21
        resultados_provas: (135, 545),  # Campo 22
        diagnostico_inicial: (135, 528),  # Campo 23
        cid10_principal: (135, 511),  # Campo 24
        descricao_procedimento: (135, 450),  # Campo 27
        carater_internacao: (135, 400),  # Campo 30
        nome_profissional: (135, 315),  # Campo 33
        assinatura_profissional: (445, 315)  # Campo 35
    }

    # Criar o PDF com os textos adicionados
    input_pdf_path = "static/aih_laudo_internacao.pdf"
    output_pdf_path = "static/aih_laudo_internacao_filled.pdf"

    add_text_to_pdf(input_pdf_path, output_pdf_path, texts_positions)

    # Enviar o PDF preenchido para o usuário
    return send_file(output_pdf_path, as_attachment=True, download_name='laudo_preenchido.pdf', mimetype='application/pdf')

def add_text_to_pdf(input_pdf_path, output_pdf_path, texts_positions, font_size=10):
    # Criar um PDF temporário com o texto
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", font_size)
    for text, (x, y) in texts_positions.items():
        can.drawString(x, y, text)
    can.save()
    
    # Ler o PDF original e o PDF temporário
    existing_pdf = PdfReader(input_pdf_path)
    temp_pdf = PdfReader(packet)
    output = PdfWriter()

    # Adicionar o texto à primeira página do PDF original
    page = existing_pdf.pages[0]
    page.merge_page(temp_pdf.pages[0])
    output.add_page(page)

    # Adicionar as páginas restantes
    for i in range(1, len(existing_pdf.pages)):
        output.add_page(existing_pdf.pages[i])

    # Escrever o PDF preenchido no arquivo de saída
    with open(output_pdf_path, "wb") as outputStream:
        output.write(outputStream)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
