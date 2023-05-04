#!/bin/bash

docker-compose down --rmi all --remove-orphans || true

# sudo rm ./invoker_gui/capif_onboarding/*

# sudo rm ./invoker_gui/demo_values.json && sudo rm ./invoker_gui/ca.crt && sudo rm ./invoker_gui/cert_req.csr && sudo rm ./invoker_gui/dummy.crt && sudo rm ./invoker_gui/private.key && sudo rm ./invoker_gui/ca_service.crt

# sudo rm ./invoker_gui/demo_values.json
# sudo rm ./invoker_gui/ca.crt
# sudo rm ./invoker_gui/cert_req.csr
# sudo rm ./invoker_gui/dummy.crt
# sudo rm ./invoker_gui/private.key