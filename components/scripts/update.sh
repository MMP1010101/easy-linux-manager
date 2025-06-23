#!/bin/bash
# Script de actualización del sistema
# Este script actualiza la lista de paquetes del sistema

echo "=========================================="
echo "🔄 ACTUALIZANDO REPOSITORIOS DEL SISTEMA"
echo "=========================================="
echo ""
echo "📋 Fecha de actualización: $(date)"
echo "👤 Usuario: $USER"
echo ""
echo "⏳ Actualizando lista de paquetes..."
echo ""

# Ejecutar actualización
sudo apt update

echo ""
if [ $? -eq 0 ]; then
    echo "✅ Repositorios actualizados correctamente"
else
    echo "❌ Hubo un problema al actualizar los repositorios"
fi

echo ""
echo "📊 Paquetes actualizables:"
apt list --upgradable

echo ""
echo "=========================================="
echo "Para instalar las actualizaciones, ejecuta:"
echo "sudo apt upgrade -y"
echo "=========================================="