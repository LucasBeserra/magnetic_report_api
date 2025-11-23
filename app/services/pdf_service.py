from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from typing import Dict, Any
import os

class PDFService:
    """
    Serviço para geração de PDFs dos relatórios técnicos.
    """
    
    @staticmethod
    def gerar_relatorio_pdf(relatorio_data: Dict[str, Any], output_path: str) -> str:
        """
        Gera PDF do relatório técnico.
        
        Args:
            relatorio_data: Dicionário com dados do relatório
            output_path: Caminho onde salvar o PDF
            
        Returns:
            Caminho do arquivo PDF gerado
        """
        # Criar documento
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Elementos do PDF
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilos customizados
        titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        subtitulo_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Título principal
        elements.append(Paragraph("MAGNETIC REPORT", titulo_style))
        elements.append(Paragraph("Relatório Técnico", styles['Heading2']))
        elements.append(Spacer(1, 0.5*cm))
        
        # Informações básicas
        elements.append(Paragraph("Informações do Pedido", subtitulo_style))
        
        info_data = [
            ["Código do Pedido:", relatorio_data.get('codigo_pedido', 'N/A')],
            ["Cliente:", relatorio_data.get('cliente', {}).get('nome', 'N/A')],
            ["Produto:", relatorio_data.get('produto', {}).get('nome', 'N/A')],
            ["Data:", datetime.now().strftime('%d/%m/%Y')],
        ]
        
        info_table = Table(info_data, colWidths=[5*cm, 12*cm])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 0.8*cm))
        
        # Descrição
        if relatorio_data.get('descricao'):
            elements.append(Paragraph("Descrição", subtitulo_style))
            elements.append(Paragraph(relatorio_data['descricao'], styles['BodyText']))
            elements.append(Spacer(1, 0.5*cm))
        
        # Tabela dinâmica de dados
        if relatorio_data.get('dados_tabela'):
            elements.append(Paragraph("Dados Técnicos", subtitulo_style))
            tabela_dinamica = PDFService._criar_tabela_dinamica(relatorio_data['dados_tabela'])
            if tabela_dinamica:
                elements.append(tabela_dinamica)
                elements.append(Spacer(1, 0.8*cm))
        
        # Fotos
        if relatorio_data.get('fotos'):
            elements.append(Paragraph("Registro Fotográfico", subtitulo_style))
            
            for foto in relatorio_data['fotos']:
                if os.path.exists(foto['caminho']):
                    try:
                        # Adicionar imagem (max width 15cm)
                        img = Image(foto['caminho'], width=15*cm, height=10*cm, kind='proportional')
                        elements.append(img)
                        
                        # Descrição da foto
                        if foto.get('descricao'):
                            elements.append(Paragraph(
                                f"<i>{foto['descricao']}</i>",
                                styles['Normal']
                            ))
                        
                        elements.append(Spacer(1, 0.5*cm))
                    except:
                        pass
        
        # Observações
        if relatorio_data.get('observacoes'):
            elements.append(Paragraph("Observações", subtitulo_style))
            elements.append(Paragraph(relatorio_data['observacoes'], styles['BodyText']))
        
        # Gerar PDF
        doc.build(elements)
        return output_path
    
    @staticmethod
    def _criar_tabela_dinamica(dados_tabela: Dict[str, Any]) -> Table:
        """
        Cria tabela dinâmica para o PDF baseado na estrutura fornecida.
        """
        try:
            estrutura = dados_tabela.get('estrutura', {})
            dados = dados_tabela.get('dados', [])
            
            if not estrutura or not dados:
                return None
            
            colunas = estrutura.get('colunas', [])
            
            # Cabeçalho
            table_data = [colunas]
            
            # Dados
            table_data.extend(dados)
            
            # Criar tabela
            table = Table(table_data)
            table.setStyle(TableStyle([
                # Cabeçalho
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                
                # Dados
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
            ]))
            
            return table
            
        except Exception as e:
            print(f"Erro ao criar tabela dinâmica: {str(e)}")
            return None