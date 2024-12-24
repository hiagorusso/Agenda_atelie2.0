# from fpdf import FPDF
# from tempfile import NamedTemporaryFile
# import pandas as pd
#
# def gerar_resumo_pdf(atendimentos, total, total_liquido):
#     """
#     Gera um arquivo PDF com o resumo do mês.
#
#     Args:
#         atendimentos (list): Lista com os dados do resumo.
#         total (float): Valor total bruto.
#         total_liquido (float): Valor total líquido.
#
#     Returns:
#         str: Caminho temporário para o arquivo PDF.
#     """
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#
#     # Título
#     pdf.set_font("Arial", style="B", size=16)
#     pdf.cell(200, 10, txt="Resumo Mensal de Atendimentos", ln=True, align="C")
#     pdf.ln(10)
#
#     # Tabela de Resumo
#     pdf.set_font("Arial", size=12)
#     pdf.cell(60, 10, txt="Serviço", border=1, align="C")
#     pdf.cell(40, 10, txt="Quantidade", border=1, align="C")
#     pdf.cell(50, 10, txt="Total (R$)", border=1, align="C")
#     pdf.ln()
#
#     for item in atendimentos:
#         pdf.cell(60, 10, txt=item['nome'], border=1)
#         pdf.cell(40, 10, txt=str(item['quantidade']), border=1, align="C")
#         pdf.cell(50, 10, txt=f"R${item['total']:.2f}", border=1, align="R")
#         pdf.ln()
#
#     # Totais
#     pdf.ln(10)
#     pdf.set_font("Arial", style="B", size=12)
#     pdf.cell(60, 10, txt="Valor Total do Mês:", ln=True)
#     pdf.cell(0, 10, txt=f"R${total:.2f}", align="R")
#     pdf.cell(60, 10, txt="Valor Líquido (após 30%):", ln=True)
#     pdf.cell(0, 10, txt=f"R${total_liquido:.2f}", align="R")
#
#     # Salvar em arquivo temporário
#     with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
#         pdf.output(temp_file.name)
#         return temp_file.name
#
# def gerar_resumo_excel(atendimentos, total, total_liquido):
#     """
#     Gera um arquivo Excel com o resumo do mês.
#
#     Args:
#         atendimentos (list): Lista com os dados do resumo.
#         total (float): Valor total bruto.
#         total_liquido (float): Valor total líquido.
#
#     Returns:
#         str: Caminho temporário para o arquivo Excel.
#     """
#     # Criar DataFrame para os dados do resumo
#     df = pd.DataFrame(atendimentos)
#     df.columns = ["Serviço", "Quantidade", "Total (R$)"]
#
#     # Adicionar totais
#     totais = {
#         "Serviço": ["Valor Total", "Valor Líquido"],
#         "Quantidade": ["", ""],
#         "Total (R$)": [total, total_liquido],
#     }
#     df_totais = pd.DataFrame(totais)
#     df_final = pd.concat([df, df_totais], ignore_index=True)
#
#     # Salvar em arquivo temporário
#     with NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
#         df_final.to_excel(temp_file.name, index=False)
#         return temp_file.name
