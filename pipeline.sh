#!/bin/bash

echo "===== [SAST] Escaneando código con Bandit ====="
python -m bandit -r . -f txt -o reporte_bandit.txt
cat reporte_bandit.txt

echo "===== [Build & Deploy] Lanzando servidor Flask ====="
# Esto lo puedes hacer manual o con otro script
# python app.py &

sleep 5  # Tiempo para que el servidor arranque

echo "===== [DAST] Atacando endpoint con SQLMap ====="
python sqlmap/sqlmap.py -u "http://127.0.0.1:5000/buscar?id=1" --batch --dump
