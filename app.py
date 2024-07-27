from flask import Flask, request, render_template, send_file
from reportlab.pdfgen import canvas
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
    
    # Gerando o PDF
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)
    
    # Campos automáticos
    c.drawString(50, 800, "HOSPITAL DR. JOSÉ PEDRO BEZERRA")
    c.drawString(50, 780, "HOSPITAL DR. JOSÉ PEDRO BEZERRA")
    c.drawString(50, 760, datetime.now().strftime("%d/%m/%Y"))
    
    # Campos do formulário
    c.drawString(50, 740, nome_paciente)
    c.drawString(50, 720, numero_prontuario)
    c.drawString(50, 700, nome_mae)
    c.drawString(50, 680, municipio_residencia)
    c.drawString(50, 660, sinais_sintomas)
    c.drawString(50, 640, condicoes_justificam)
    c.drawString(50, 620, resultados_provas)
    c.drawString(50, 600, diagnostico_inicial)
    c.drawString(50, 580, cid10_principal)
    c.drawString(50, 560, descricao_procedimento)
    c.drawString(50, 540, carater_internacao)
    c.drawString(50, 520, nome_profissional)
    c.drawString(50, 500, assinatura_profissional)
    
    c.showPage()
    c.save()
    
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, as_attachment=True, download_name='laudo_preenchido.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
