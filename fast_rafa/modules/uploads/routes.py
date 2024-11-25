import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter()


# Configuração do diretório de upload
UPLOAD_DIR = Path('fast_rafa/static/img/uploads/profile_images')
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post('/profile-image')
async def upload_profile_image(file: UploadFile = File(...)):
    try:
        # Verificar se é uma imagem
        if not file.content_type.startswith('image/'):
            return JSONResponse(
                status_code=400,
                content={'detail': 'O arquivo deve ser uma imagem'},
            )

        # Gerar nome único para o arquivo
        file_extension = Path(file.filename).suffix.lower()
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif'}

        if file_extension not in allowed_extensions:
            return JSONResponse(
                status_code=400,
                content={'detail': 'Formato de arquivo não permitido'},
            )

        unique_filename = f'{uuid.uuid4()}{file_extension}'
        file_path = UPLOAD_DIR / unique_filename

        # Salvar arquivo
        with file_path.open('wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Retornar URL relativa
        return {'url': f'/img/uploads/profile_images/{unique_filename}'}

    except Exception:
        # Log do erro aqui se necessário
        return JSONResponse(
            status_code=500,
            content={'detail': 'Erro ao processar o upload da imagem'},
        )
