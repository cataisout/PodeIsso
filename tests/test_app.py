import subprocess
import time

def test_app_starts():
    """Testa se o app.py inicia sem erros"""
    try:
        # Inicia o subprocesso
        process = subprocess.Popen(
            ["python", "app/app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Aguarda alguns segundos para verificar se o app inicia sem erros
        time.sleep(10)
        
        # Verifica se o processo ainda está em execução
        assert process.poll() is None, "O app.py foi encerrado inesperadamente."
    finally:
        # Finaliza o subprocesso
        process.terminate()
        process.wait()
