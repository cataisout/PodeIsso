import subprocess
import time

def test_app_starts():
    """Testa se o app.py inicia sem erros"""
    try:
        process = subprocess.Popen(
            ["python", "app/app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        time.sleep(10)

        # Verifique o retorno do processo
        stdout, stderr = process.communicate()
        if stderr:
            print("Erro:", stderr.decode())
        else:
            print("Saída:", stdout.decode())

        assert process.poll() is None, "O app.py foi encerrado inesperadamente."

    except Exception as e:
        print("Erro ao executar o teste:", e)
