import os
import uuid
from typing import Tuple
from fastapi import UploadFile, HTTPException
from PIL import Image
from app.config import settings

class UploadService:
    """
    Serviço para gerenciar upload e processamento de imagens.
    """
    
    @staticmethod
    def validar_extensao(filename: str) -> bool:
        """
        Valida se a extensão do arquivo é permitida.
        """
        extensao = filename.split('.')[-1].lower()
        return extensao in settings.ALLOWED_EXTENSIONS
    
    @staticmethod
    def gerar_nome_unico(filename: str) -> str:
        """
        Gera nome único para o arquivo usando UUID.
        
        Exemplo: foto.jpg -> a3f2b1c4-5678-9012-3456-789012345678.jpg
        """
        extensao = filename.split('.')[-1].lower()
        nome_unico = f"{uuid.uuid4()}.{extensao}"
        return nome_unico
    
    @staticmethod
    async def salvar_imagem(file: UploadFile) -> Tuple[str, str, int]:
        """
        Salva imagem no disco e retorna informações do arquivo.
        
        Returns:
            Tuple com (nome_arquivo, caminho_completo, tamanho_bytes)
        
        Raises:
            HTTPException: Se arquivo inválido ou erro ao salvar
        """
        # Validar extensão
        if not UploadService.validar_extensao(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Extensão não permitida. Use: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Validar tamanho
        conteudo = await file.read()
        tamanho = len(conteudo)
        
        if tamanho > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Arquivo muito grande. Máximo: {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        # Gerar nome único
        nome_arquivo = UploadService.gerar_nome_unico(file.filename)
        caminho_completo = os.path.join(settings.UPLOAD_DIR, nome_arquivo)
        
        try:
            # Salvar arquivo
            with open(caminho_completo, "wb") as f:
                f.write(conteudo)
            
            # Otimizar imagem (reduzir tamanho mantendo qualidade)
            UploadService.otimizar_imagem(caminho_completo)
            
            # Recalcular tamanho após otimização
            tamanho_final = os.path.getsize(caminho_completo)
            
            return nome_arquivo, caminho_completo, tamanho_final
            
        except Exception as e:
            # Se houver erro, remover arquivo se foi criado
            if os.path.exists(caminho_completo):
                os.remove(caminho_completo)
            raise HTTPException(status_code=500, detail=f"Erro ao salvar arquivo: {str(e)}")
    
    @staticmethod
    def otimizar_imagem(caminho: str, max_width: int = 1920, qualidade: int = 85):
        """
        Otimiza imagem redimensionando e comprimindo.
        
        Args:
            caminho: Caminho do arquivo
            max_width: Largura máxima (mantém proporção)
            qualidade: Qualidade JPEG (1-100)
        """
        try:
            with Image.open(caminho) as img:
                # Converter para RGB se necessário (PNG com transparência)
                if img.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = rgb_img
                
                # Redimensionar se necessário
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # Salvar com compressão
                img.save(caminho, 'JPEG', quality=qualidade, optimize=True)
        
        except Exception as e:
            # Se falhar a otimização, mantém arquivo original
            print(f"Aviso: Não foi possível otimizar imagem: {str(e)}")
    
    @staticmethod
    def deletar_imagem(caminho: str) -> bool:
        """
        Deleta arquivo de imagem do disco.
        
        Returns:
            True se deletado com sucesso, False caso contrário
        """
        try:
            if os.path.exists(caminho):
                os.remove(caminho)
                return True
            return False
        except Exception as e:
            print(f"Erro ao deletar arquivo: {str(e)}")
            return False