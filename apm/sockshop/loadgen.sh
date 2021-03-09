#!/usr/bin/env bash

KC="sudo kubectl"

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
  $KC delete -n sock-shop -f loadgen/loadgen.yaml 2>/dev/null
  $KC delete configmap -n sock-shop locust-file 2> /dev/null
  $KC delete configmap -n sock-shop locust-config 2> /dev/null

  $KC create configmap -n sock-shop locust-file --from-file loadgen/locustfile.py
  $KC create configmap -n sock-shop locust-config \
      --from-literal=targetUrl="$TARGET_HOST" \
      --from-literal=locustOpts="--users $CLIENTS --hatch-rate $HATCH_RATE --run-time $RUNTIME --headless"
  $KC apply -n sock-shop -f loadgen/loadgen.yaml
}

validate() {
  set +u
  TARGET_HOST=${TARGET_HOST:-http://$SOCKS_ENDPOINT}
  set -u
  if [ "${TARGET_HOST}" == "http://" ]; then
    echo "No target host given and SOCKS_ENDPOINT is not set. Please provide a target host."
    exit 1;
  fi
}

HATCH_RATE=5
CLIENTS=15
RUNTIME=1m

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

validate
run_test
