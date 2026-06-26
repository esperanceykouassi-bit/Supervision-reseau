#!/usr/bin/env bash
# Génère un certificat TLS auto-signé pour le dashboard HTTPS.
# Usage (depuis ~/supervision/src) : bash gen_cert.sh
cd "$(dirname "$0")"
mkdir -p certs
rm -f certs/cert.pem certs/key.pem
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout certs/key.pem -out certs/cert.pem -days 365 \
  -subj "/CN=192.168.1.50" -addext "subjectAltName=IP:192.168.1.50"
echo "----------------------------------------"
echo "Certificat genere :"
ls -l certs/
echo "Verification (doit afficher BEGIN ...) :"
head -1 certs/cert.pem
head -1 certs/key.pem
