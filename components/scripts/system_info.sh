#!/bin/bash
# Script de información del sistema
# Muestra información detallada sobre el sistema

echo "==============================================" 
echo "       🖥️  INFORMACIÓN DEL SISTEMA           " 
echo "=============================================="
echo ""
echo "📅 Fecha y hora: $(date)"
echo "👤 Usuario: $USER"
echo "🏠 Directorio: $(pwd)"
echo ""
echo "📊 INFORMACIÓN DEL SISTEMA:"
echo "-----------------------------------"
echo "🐧 Sistema operativo: $(uname -s)"
echo "💻 Versión del kernel: $(uname -r)"
echo "🔷 Arquitectura: $(uname -m)"
echo ""
echo "📝 INFORMACIÓN DE CPU:"
echo "-----------------------------------"
cat /proc/cpuinfo | grep "model name" | head -n1 | awk -F: '{print $2}'
echo "Núcleos: $(grep -c processor /proc/cpuinfo)"
echo ""
echo "📊 MEMORIA RAM:"
echo "-----------------------------------"
free -h | grep "Mem:" | awk '{print "Total: " $2 ", Usada: " $3 ", Libre: " $4}'
echo ""
echo "💾 INFORMACIÓN DE DISCO:"
echo "-----------------------------------"
df -h / | grep -v "Filesystem" | awk '{print "Total: " $2 ", Usado: " $3 ", Libre: " $4 ", % Usado: " $5}'
