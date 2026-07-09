.PHONY: setup-k3d build deploy collector up down logs fix-nginx fix-payment-gateway fix-rabbitmq import-images fix-images verify-infra-apm verify-apm cleanup cleanup-apps

setup-k3d:
	bash scripts/setup-k3d.sh

build:
	bash scripts/build-images.sh

import-images:
	bash scripts/import-images-k3d.sh

fix-images:
	bash scripts/fix-image-pull.sh

deploy:
	bash scripts/deploy.sh

collector:
	bash scripts/install-splunk-collector.sh

up:
	docker compose --env-file .env up --build -d

down:
	docker compose down

logs:
	docker compose logs -f order-api payment-gateway payment-api fulfillment-worker gateway

fix-nginx:
	kubectl apply -f deploy/k8s/gateway-config.yaml
	kubectl -n cosmic-shop rollout restart deployment/gateway
	kubectl -n cosmic-shop rollout status deployment/gateway --timeout=180s

fix-payment-gateway:
	bash scripts/build-images.sh payment-gateway
	bash scripts/import-images-k3d.sh payment-gateway
	kubectl -n cosmic-shop rollout restart deployment/payment-gateway
	kubectl -n cosmic-shop rollout status deployment/payment-gateway --timeout=180s

fix-rabbitmq:
	bash scripts/build-images.sh payment-api fulfillment-worker
	bash scripts/import-images-k3d.sh payment-api fulfillment-worker
	kubectl -n cosmic-shop rollout restart deployment/payment-api
	kubectl -n cosmic-shop rollout restart deployment/fulfillment-worker
	kubectl -n cosmic-shop rollout status deployment/payment-api --timeout=180s
	kubectl -n cosmic-shop rollout status deployment/fulfillment-worker --timeout=180s

verify-infra-apm:
	bash scripts/verify-infra-apm-config.sh

verify-apm:
	bash scripts/verify-apm-export.sh

cleanup:
	bash scripts/cleanup.sh

cleanup-apps:
	bash scripts/cleanup.sh --apps-only
