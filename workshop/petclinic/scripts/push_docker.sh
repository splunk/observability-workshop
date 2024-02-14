#!/bin/bash
docker push localhost:9999/spring-petclinic-admin-server:local
docker push localhost:9999/spring-petclinic-api-gateway:local
docker push localhost:9999/spring-petclinic-discovery-server:local
docker push localhost:9999/spring-petclinic-config-server:local
docker push localhost:9999/spring-petclinic-visits-service:local
docker push localhost:9999/spring-petclinic-vets-service:local
docker push localhost:9999/spring-petclinic-customers-service:local
