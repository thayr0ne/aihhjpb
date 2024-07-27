from flask import Flask, request, render_template, send_file
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, TextStringObject
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

    # Criar um dicionário com os campos preenchidos
    fields = {
        "1": "HOSPITAL DR. JOSÉ PEDRO BEZERRA",
        "3": "HOSPITAL DR. JOSÉ PEDRO BEZERRA",
        "5": nome_paciente,
        "6": numero_prontuario,
        "11": nome_mae,
        "16": municipio_residencia,
        "20": sinais_sintomas,
        "21": condicoes_justificam,
        "22": resultados_provas,
        "23": diagnostico_inicial,
        "24": cid10_principal,
        "27": descricao_procedimento,
        "30": carater_internacao,
        "33": nome_profissional,
        "34": datetime.now().strftime("%d/%m/%Y"),
        "35": assinatura_profissional
    }

    # Preencher os campos do PDF
    for field_key, field_value in fields.items():
        for j in range(0, len(page['/Annots'])):
            field = page['/Annots'][j].getObject()
            if field.get('/T') == field_key:
                field.update({
                    NameObject("/V"): TextStringObject(field_value)
                })

    # Adicionar a página preenchida ao escritor de PDF
    pdf_writer.add_page(page)

    # Escrever o PDF preenchido em um buffer
    pdf_buffer = io.BytesIO()
    pdf_writer.write(pdf_buffer)
    pdf_buffer.seek(0)

    return send_file(pdf_buffer, as_attachment=True, download_name='laudo_preenchido.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
