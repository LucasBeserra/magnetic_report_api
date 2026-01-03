# Script para testar a conexão com o banco de dados PostgreSQL

from sqlalchemy import create_engine, text
from app.config import settings

def testar_conexao():
    print("=" * 60)
    print("🔍 TESTE DE CONEXÃO COM BANCO DE DADOS")
    print("=" * 60)
    
    print(f"\n📋 Configurações:")
    print(f"   URL do Banco: {settings.DATABASE_URL}")
    print(f"   App Name: {settings.APP_NAME}")
    print(f"   Debug Mode: {settings.DEBUG}")
    
    try:
        print("\n🔌 Tentando conectar ao banco de dados...")
        engine = create_engine(settings.DATABASE_URL, echo=True)
        
        # Testar conexão
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            
            print("\n✅ CONEXÃO BEM-SUCEDIDA!")
            print(f"\n📦 Versão do PostgreSQL:")
            print(f"   {version}")
            
            # Testar criação de tabela
            print("\n🏗️  Testando criação de tabela temporária...")
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    teste VARCHAR(100)
                );
            """))
            connection.commit()
            
            print("✅ Tabela de teste criada com sucesso!")
            
            # Limpar tabela de teste
            connection.execute(text("DROP TABLE IF EXISTS test_table;"))
            connection.commit()
            
            print("✅ Tabela de teste removida!")
            
        print("\n" + "=" * 60)
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        print("\n👉 Próximo passo: Rodar o backend com 'uvicorn app.main:app --reload'")
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERRO NA CONEXÃO!")
        print("=" * 60)
        print(f"\n💥 Erro: {str(e)}")
        print("\n🔧 Possíveis soluções:")
        print("   1. Verifique se o PostgreSQL está rodando")
        print("   2. Confirme usuário e senha no arquivo .env")
        print("   3. Verifique se o banco 'magnetic_report' existe")
        print("   4. Teste a conexão: psql -U postgres -d magnetic_report")
        
        return False

if __name__ == "__main__":
    testar_conexao()