from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Iniciando Microsserviço App...")
    print(f"Host: {host}")
    print(f"Porta: {port}")
    print(f"Debug: {debug}")
    print(f"Documentação: http://{host}:{port}/docs/")
    print(f"Health Check: http://{host}:{port}/health")
    
    try:
        app.run(debug=debug, host=host, port=port)
    except Exception as e:
        print(f"Erro ao iniciar a aplicação: {e}")
        raise