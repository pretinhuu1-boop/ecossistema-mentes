#!/bin/bash
# Conecta ao repositório remoto e faz o push inicial

# Garante que estamos na raiz do projeto
cd "$(dirname "$0")/.."

echo "🔗 Configurando remote origin..."

# Remove origin anterior se existir para evitar conflitos
git remote remove origin 2>/dev/null

git remote add origin https://github.com/pretinhuu1-boop/ecossistema-mentes.git
git branch -M main

echo "🚀 Enviando para o GitHub..."
git push -u origin main