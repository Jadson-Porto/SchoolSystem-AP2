import os
from datetime import timedelta

class Config:
    """Configurações base da aplicação"""
    
    # Configurações do Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configurações do SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///school_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True
    }
    
    # Configurações JWT (se for usar autenticação)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Configurações de ambiente
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    TESTING = os.getenv('TESTING', 'False').lower() == 'true'
    
    # Configurações de API
    API_TITLE = 'School Management API - App Service'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'


class DevelopmentConfig(Config):
    """Configurações para ambiente de desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///school_app_dev.db')


class TestingConfig(Config):
    """Configurações para ambiente de testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///school_app_test.db')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Configurações para ambiente de produção"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # Em produção, as chaves devem vir de variáveis de ambiente
    @classmethod
    def validate_config(cls):
        required_vars = ['SECRET_KEY', 'JWT_SECRET_KEY', 'DATABASE_URL']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Variáveis de ambiente obrigatórias faltando: {', '.join(missing_vars)}")


# Configuração padrão
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Retorna a configuração baseada no ambiente"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])