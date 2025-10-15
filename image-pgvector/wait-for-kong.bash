#!/bin/bash
set -e

if test -z "$KONG_API"
then
  echo "KONG_API is not set."
else
  echo "############################"
  echo "Waiting fot kong to kick in!"
  echo "############################"

  until curl -sSf $KONG_API > /dev/null; do
    >&2 echo "Kong is not ready"
    sleep 1
  done
  echo "Kong is ok!"
fi
