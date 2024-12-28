from fpdf import FPDF
from tempfile import NamedTemporaryFile
import pandas as pd


def gerar_resumo_pdf(atendimentos, total, total_liquido):
    """
    Gera um arquivo PDF com o resumo do mês.

    Args:
        atendimentos (list): Lista com os dados do resumo.
        total (float): Valor total bruto.
        total_liquido (float): Valor total líquido.

    Returns:
        str: Caminho temporário para o arquivo PDF.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Resumo Mensal de Atendimentos", ln=True, align="C")
    pdf.ln(10)

    # Tamanho das colunas
    col_servico = 60
    col_quantidade = 20
    col_total = 45
    col_valor_liquido = 55  # Nova coluna para o valor após 30%

    # Cabeçalho da tabela
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(col_servico, 10, txt="Serviço", border=1, align="C")
    pdf.cell(col_quantidade, 10, txt="Qtd", border=1, align="C")
    pdf.cell(col_total, 10, txt="Total (R$)", border=1, align="C")
    pdf.cell(col_valor_liquido, 10, txt="Valor Líquido (R$)", border=1, align="C")
    pdf.ln()

    # Preenchendo a tabela com os atendimentos
    pdf.set_font("Arial", size=12)
    for item in atendimentos:
        valor_atendimento = item['total']
        valor_liquido = valor_atendimento * 0.7  # 30% de desconto

        # Preenchendo os dados na tabela
        pdf.cell(col_servico, 10, txt=item['nome'], border=1)
        pdf.cell(col_quantidade, 10, txt=str(item['quantidade']), border=1, align="C")
        pdf.cell(col_total, 10, txt=f"R${valor_atendimento:.2f}", border=1, align="R")
        pdf.cell(col_valor_liquido, 10, txt=f"R${valor_liquido:.2f}", border=1, align="R")
        pdf.ln()

    # Totais
    pdf.ln(10)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(col_servico, 10, txt="Valor Total do Mês:", ln=True)
    pdf.cell(col_total, 10, txt=f"R${total:.2f}", align="R")
    pdf.ln(5)
    pdf.cell(col_servico, 10, txt="Valor Líquido (após 30%):", ln=True)
    pdf.cell(col_total, 10, txt=f"R${total_liquido:.2f}", align="R")

    # Salvar em arquivo temporário
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        pdf.output(temp_file.name)
        return temp_file.name

def gerar_resumo_excel(atendimentos, total, total_liquido):
    """
    Gera um arquivo Excel com o resumo do mês.

    Args:
        atendimentos (list): Lista com os dados do resumo.
        total (float): Valor total bruto.
        total_liquido (float): Valor total líquido.

    Returns:
        str: Caminho temporário para o arquivo Excel.
    """
    # Calcular o valor líquido para cada atendimento (30% de desconto)
    for item in atendimentos:
        item['Valor Líquido (R$)'] = item['total'] * 0.7  # 30% de desconto

    # Criar DataFrame para os dados do resumo
    df = pd.DataFrame(atendimentos)
    df.columns = ["Serviço", "Quantidade", "Total (R$)", "Valor Líquido (R$)"]

    # Adicionar totais
    totais = {
        "Serviço": ["Valor Total", "Valor Líquido"],
        "Quantidade": ["", ""],
        "Total (R$)": [total, total_liquido],
        "Valor Líquido (R$)": [total_liquido, total_liquido],
    }
    df_totais = pd.DataFrame(totais)
    df_final = pd.concat([df, df_totais], ignore_index=True)

    # Salvar em arquivo temporário
    with NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        df_final.to_excel(temp_file.name, index=False)
        return temp_file.name