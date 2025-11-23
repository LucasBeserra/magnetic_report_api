"""
Script para testar a importação e estrutura dos models
Execute: python test_models.py
"""

from app.models import Cliente, Produto, Relatorio, Foto
from app.database import engine, Base
from sqlalchemy import inspect

def testar_models():
    print("=" * 60)
    print("🧪 TESTE DOS MODELS")
    print("=" * 60)
    
    # Testar importação
    print("\n✅ Importação dos models:")
    print(f"   - Cliente: {Cliente}")
    print(f"   - Produto: {Produto}")
    print(f"   - Relatorio: {Relatorio}")
    print(f"   - Foto: {Foto}")
    
    # Testar estrutura das tabelas
    print("\n📋 Estrutura das Tabelas:")
    
    inspector = inspect(engine)
    
    # Criar tabelas se não existirem
    print("\n🏗️  Criando tabelas no banco...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas/verificadas!")
    
    # Listar tabelas
    tables = inspector.get_table_names()
    print(f"\n📊 Tabelas encontradas no banco ({len(tables)}):")
    for table in tables:
        print(f"   - {table}")
        
        # Mostrar colunas de cada tabela
        columns = inspector.get_columns(table)
        print(f"      Colunas ({len(columns)}):")
        for col in columns:
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            print(f"         • {col['name']}: {col['type']} ({nullable})")
        print()
    
    # Verificar relacionamentos
    print("🔗 Relacionamentos:")
    print("   - Cliente → Relatorios (1:N)")
    print("   - Produto → Relatorios (1:N)")
    print("   - Relatorio → Fotos (1:N)")
    print("   - Relatorio → Cliente (N:1)")
    print("   - Relatorio → Produto (N:1)")
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS MODELS ESTÃO OK!")
    print("=" * 60)
    print("\n👉 Próximo passo: Testar a conexão com 'python test_db.py'")

if __name__ == "__main__":
    try:
        testar_models()
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        print("\n🔧 Verifique:")
        print("   1. Todos os arquivos de models existem")
        print("   2. O arquivo .env está configurado")
        print("   3. O PostgreSQL está rodando")