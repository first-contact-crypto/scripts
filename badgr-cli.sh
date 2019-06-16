#!/usr/bin/env bash

# params: refresh_token <print=false>
refresh_token() {
  if [ "$#" -eq 0 ]; then
      echo "Usasge: $0 refresh_token <print=false>"
      echo "    You must at least supply the refresh token as an argument"
      exit 1
  fi
  output = $(curl -X POST 'https://badgr.firstcontactcrypto.com/o/token' -d "grant_type=refresh_token&refresh_token=${1}")
}

