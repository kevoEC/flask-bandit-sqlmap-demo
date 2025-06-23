#!/bin/bash

echo "===== [SAST] Escaneando código con Bandit ====="
python -m bandit -r . -f txt -o reporte_bandit.txt || true
cat reporte_bandit.txt

echo ""
echo "===== [BUILD & DEPLOY] Lanzando servidor Flask ====="
# Ejecutar Flask en background y guardar el PID
python app.py &
FLASK_PID=$!

# Esperar unos segundos a que Flask inicie
sleep 5

echo ""
echo "===== [DAST] Atacando endpoint con SQLMap ====="
python sqlmap/sqlmap.py -u "http://127.0.0.1:5000/buscar?id=1" --batch --dump

# Matar el servidor Flask
echo ""
echo "===== [CI/CD] Deteniendo servidor Flask ====="
kill $FLASK_PID
