# Guia de Deploy no Coolify (Sua VPS)

O **Coolify** é a melhor opção possível para hospedar esta API! Ele cuidará de:
1. Gerar **HTTPS (SSL Let's Encrypt) automático** para o seu domínio/subdomínio.
2. Manter a API rodando 24 horas por dia com reinicialização automática.
3. Consumo mínimo de recursos (a API consome menos de 50MB de RAM).

---

## Passo a Passo para Deploy no Coolify

### Método 1: Via Repositório Git (Recomendado)

1. **Suba o projeto para um repositório no GitHub ou GitLab** (pode ser privado ou público).
2. Acesse o painel do seu **Coolify**.
3. Vá em **Projects** > selecione seu projeto (ou crie um novo) > clique em **+ New Resource**.
4. Escolha **Public Repository** ou **Private Repository** (GitHub/GitLab).
5. Cole a URL do seu repositório Git.
6. Na tela de configuração do recurso:
   - **Build Pack**: Selecione **Dockerfile** (o Coolify detectará o `Dockerfile` que já deixamos pronto na raiz).
   - **Ports Exposes**: Coloque `8000`.
   - **Domains**: Defina o domínio ou subdomínio que deseja usar (ex: `https://cotacao.seudominio.com` ou `https://api-moedas.seudominio.com`).
     > *Dica: Lembre-se de apontar o registro tipo `A` do subdomínio no seu DNS (Cloudflare, Registro.br, etc.) para o IP da sua VPS.*
7. Clique em **Deploy**.

O Coolify vai construir a imagem Docker, iniciar o container e configurar o Traefik/Caddy com certificado SSL gratuito automaticamente!

---

### Método 2: Via Docker Compose no Coolify

Se preferir colar a configuração diretamente no Coolify sem Git:

1. No Coolify, clique em **+ New Resource** > **Docker Compose**.
2. Cole o conteúdo do arquivo `docker-compose.yml` da raiz do projeto.
3. No campo de domínio, coloque seu domínio com HTTPS: `https://cotacao.seudominio.com`.
4. Clique em **Deploy**.

---

## Testando sua API no Ar

Após o deploy no Coolify:
- **Painel & Simulador:** `https://cotacao.seudominio.com/`
- **Documentação Swagger:** `https://cotacao.seudominio.com/docs`
- **JSON Cotações:** `https://cotacao.seudominio.com/api/cotacoes`
- **Conversor:** `https://cotacao.seudominio.com/api/converter?valor=100`

### Como usar na Shopify e WordPress após o deploy:
Basta substituir a URL nos snippets pelo seu domínio com HTTPS gerado pelo Coolify:
```html
<script src="https://cotacao.seudominio.com/static/widget.js" data-ticker="#barra-cotacoes" async></script>
```
Como o Coolify já entrega com HTTPS válido, a Shopify e o WordPress aceitarão as requisições com 100% de compatibilidade e segurança.
