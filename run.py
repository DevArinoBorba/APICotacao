"""
Script de inicialização da API de Cotação
"""
import uvicorn

if __name__ == "__main__":
    print("Iniciando API de Cotações em Tempo Real...")
    print("Documentação Swagger: http://localhost:8000/docs")
    print("Interface Web:        http://localhost:8000/")
    print("Endpoint Cotações:    http://localhost:8000/api/cotacoes")
    print("Endpoint Conversor:   http://localhost:8000/api/converter?valor=100")
    print("-" * 50)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
