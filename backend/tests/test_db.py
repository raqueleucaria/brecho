from sqlalchemy import create_engine, text

from src.settings import Settings

settings = Settings()
engine = create_engine(settings.DATABASE_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('Conexão bem-sucedida!', result.scalar())
except Exception as e:
    print('Erro ao conectar:', e)
