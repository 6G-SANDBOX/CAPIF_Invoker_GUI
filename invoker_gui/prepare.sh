#evolved5g register-and-onboard-to-capif --config_file_full_path="/usr/src/app/capif_registration.json"

# curl  -k --connect-timeout 5 \
#     --max-time 10 \
#     --retry-delay 0 \
#     --retry-max-time 40 \
#     --request GET "https://easy-rsa:$CAPIF_PORT/ca-root" 2>/dev/null | jq -r '.certificate' -j > ./capif_ops/certs/ca.crt

curl  -k --connect-timeout 5 \
    --max-time 10 \
    --retry-delay 0 \
    --retry-max-time 40 \
    --request GET "http://$CAPIF_HOSTNAME:$CAPIF_PORT/ca-root" 2>/dev/null | jq -r '.certificate' -j > ./capif_ops/certs/ca.crt


tail -f /dev/null