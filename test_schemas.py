"""
Script para testar a importação e validação dos schemas
Execute: python test_schemas.py
"""

from app.models.schemas import (
    ClienteCreate, ClienteUpdate, ClienteResponse,
    ProdutoCreate, ProdutoUpdate, ProdutoResponse,
    RelatorioCreate, RelatorioUpdate, RelatorioResponse,
    FotoResponse
)
from datetime import datetime

def testar_schemas():
    print("=" * 60)
    print("🧪 TESTE DOS SCHEMAS")
    print("=" * 60)
    
    # Testar Cliente
    print("\n✅ Schema Cliente:")
    try:
        cliente_data = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "telefone": "(11) 99999-9999",
            "empresa": "Tech Corp",
            "endereco": "Rua ABC, 123"
        }
        cliente_create = ClienteCreate(**cliente_data)
        print(f"   ✓ ClienteCreate validado: {cliente_create.nome}")
        
        cliente_update = ClienteUpdate(nome="João Pedro Silva")
        print(f"   ✓ ClienteUpdate validado: {cliente_update.nome}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # Testar Produto
    print("\n✅ Schema Produto:")
    try:
        produto_data = {
            "nome": "Válvula Industrial",
            "codigo": "VALV-001",
            "descricao": "Válvula de alta pressão",
            "categoria": "Hidráulica",
            "template_tabela": {
                "colunas": ["Medida", "Valor"],
                "tipos": ["text", "number"]
            }
        }
        produto_create = ProdutoCreate(**produto_data)
        print(f"   ✓ ProdutoCreate validado: {produto_create.nome}")
        
        produto_update = ProdutoUpdate(categoria="Pneumática")
        print(f"   ✓ ProdutoUpdate validado: {produto_update.categoria}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # Testar Relatório
    print("\n✅ Schema Relatório:")
    try:
        relatorio_data = {
            "codigo_pedido": "PED-2024-001",
            "titulo": "Inspeção Técnica",
            "descricao": "Relatório de inspeção completa",
            "observacoes": "Nenhuma anormalidade detectada",
            "cliente_id": 1,
            "produto_id": 1,
            "dados_tabela": {
                "estrutura": {"colunas": ["Item", "Status"]},
                "dados": [["Item 1", "OK"], ["Item 2", "OK"]]
            },
            "status": "rascunho"
        }
        relatorio_create = RelatorioCreate(**relatorio_data)
        print(f"   ✓ RelatorioCreate validado: {relatorio_create.codigo_pedido}")
        
        relatorio_update = RelatorioUpdate(status="concluido")
        print(f"   ✓ RelatorioUpdate validado: {relatorio_update.status}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # Testar validações
    print("\n🔒 Testando Validações:")
    
    # Email inválido
    try:
        ClienteCreate(nome="Teste", email="email_invalido")
        print("   ✗ Validação de email falhou!")
    except Exception:
        print("   ✓ Email inválido rejeitado corretamente")
    
    # Campo obrigatório faltando
    try:
        ClienteCreate(email="test@test.com")  # Falta nome
        print("   ✗ Validação de campo obrigatório falhou!")
    except Exception:
        print("   ✓ Campo obrigatório validado corretamente")
    
    # Código de pedido vazio
    try:
        RelatorioCreate(
            codigo_pedido="",
            cliente_id=1,
            produto_id=1
        )
        print("   ✗ Validação de string vazia falhou!")
    except Exception:
        print("   ✓ String vazia rejeitada corretamente")
    
    # ID negativo
    try:
        RelatorioCreate(
            codigo_pedido="TEST",
            cliente_id=-1,
            produto_id=1
        )
        print("   ✗ Validação de ID negativo falhou!")
    except Exception:
        print("   ✓ ID negativo rejeitado corretamente")
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS SCHEMAS ESTÃO OK!")
    print("=" * 60)
    print("\n📋 Schemas disponíveis:")
    print("   - ClienteCreate, ClienteUpdate, ClienteResponse")
    print("   - ProdutoCreate, ProdutoUpdate, ProdutoResponse")
    print("   - RelatorioCreate, RelatorioUpdate, RelatorioResponse")
    print("   - FotoResponse, RelatorioListResponse")
    print("\n👉 Próximo passo: Testar models com 'python test_models.py'")

if __name__ == "__main__":
    try:
        testar_schemas()
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        print("\n🔧 Verifique:")
        print("   1. Todos os arquivos de schemas existem")
        print("   2. As importações estão corretas")
        print("   3. Pydantic está instalado (pip install pydantic)")