#!/usr/bin/env bash
# Génère un certificat TLS auto-signé (avec SAN IP) pour le dashboard HTTPS,
# puis vérifie qu'il se charge bien côté Python.
# Usage (depuis ~/supervision/src) : bash gen_cert.sh
cd "$(dirname "$0")"
mkdir -p certs
rm -f certs/cert.pem certs/key.pem
cat > certs/san.cnf <<'CNF'
[req]
distinguished_name = dn
x509_extensions = v3
prompt = no
[dn]
CN = 192.168.1.50
[v3]
subjectAltName = IP:192.168.1.50
basicConstraints = critical, CA:TRUE
keyUsage = critical, digitalSignature, keyCertSign
CNF
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout certs/key.pem -out certs/cert.pem -days 825 -config certs/san.cnf
echo "----------------------------------------"
ls -l certs/cert.pem certs/key.pem
echo "--- Test de chargement par Python ---"
PY=venv/bin/python; [ -x "$PY" ] || PY=python3
$PY -c "import ssl; ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER); ctx.load_cert_chain('certs/cert.pem','certs/key.pem'); print('>>> CERTIFICAT OK : chargement Python reussi')"
