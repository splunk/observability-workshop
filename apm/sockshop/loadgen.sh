#!/usr/bin/env bash

usage() {
  cat <<USAGE

  $0 [options]

  Options:
    -a <num>       Rate at which new clients are spawned, e.g. 5.
    -c <num>       Number of clients, e.g. 15.
    -h <host>      Target url, e.g. http://example.com.
    -r <duration>  Runtime of loadtest, e.g. 100s or 1m20s.
USAGE
}

exit_usage() {
    usage
    exit 1
}

run_test() {
  kubectl delete configmap -n sock-shop locust-file
  kubectl delete configmap -n sock-shop locust-config

  kubectl create configmap -n sock-shop locust-file --from-file loadgen/locustfile.py
  kubectl create configmap -n sock-shop locust-config \
      --from-literal=targetUrl="$TARGET_HOST" \
      --from-literal=locustOpts="--clients $CLIENTS --hatch-rate $HATCH_RATE --runtime $RUNTIME --no-web"
  kubectl apply -n sockshop -f loadgen/loadgen.yaml
}

while getopts ":a:c:h:r:" o; do
  case "${o}" in
    a)
        HATCH_RATE=${OPTARG:-5}
        ;;
    h)
        TARGET_HOST=${OPTARG:-http://$SOCKS_ENDPOINT}
        if  [ "${TARGET_HOST}" == "http://" ]; then
            echo "No target host given and SOCKS_ENDPOINT is not set. Please provide a target host."
            exit 1;
        fi
        ;;
    c)
        CLIENTS=${OPTARG:-15}
        ;;
    r)
        RUNTIME=${OPTARG:-1m}
        ;;
    *)
        exit_usage
        ;;
  esac
done
shift $((OPTIND -1))

run_test

