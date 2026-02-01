#!/bin/bash
# Script para inicializar repositório Git e preparar para GitHub

# Garante que estamos na raiz do projeto
cd "$(dirname "$0")/.."

echo "📦 Inicializando repositório Git..."
git init

# Criar .gitignore robusto para Python/AI
if [ ! -f .gitignore ]; then
    echo "📝 Criando .gitignore..."
    cat <<EOT >> .gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Env
venv/
env/
.env

# IDEs
.vscode/
.idea/

# Logs e Dados (Ignorar bancos vetoriais e logs)
logs/
*.log
data/
!data/.gitkeep
*.db
*.sqlite3
EOT
fi

# Adicionar arquivos e fazer commit inicial
echo "stage files..."
git add .

echo "commit..."
git commit -m "feat: Initial commit - Ecossistema de Mentes Foundation"

echo ""
echo "✅ Repositório local inicializado com sucesso!"
echo "---------------------------------------------------"
echo "🚀 PRÓXIMOS PASSOS:"
echo "1. Acesse: https://github.com/new"
echo "2. Crie um repositório chamado 'ecossistema-mentes'"
echo "3. Execute os comandos abaixo no terminal:"
echo ""
echo "git branch -M main"
echo "git remote add origin https://github.com/pretinhuu1-boop/ecossistema-mentes.git"
echo "git push -u origin main"