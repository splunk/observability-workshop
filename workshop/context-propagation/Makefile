.PHONY: setup-k3d build deploy collector up down logs import-images cleanup cleanup-apps

setup-k3d:
	bash scripts/setup-k3d.sh

build:
	bash scripts/build-images.sh

import-images:
	bash scripts/import-images-k3d.sh

deploy:
	bash scripts/deploy.sh

collector:
	bash scripts/install-splunk-collector.sh

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f order-api payment-gateway payment-api fulfillment-worker gateway

cleanup:
	bash scripts/cleanup.sh

cleanup-apps:
	bash scripts/cleanup.sh --apps-only
