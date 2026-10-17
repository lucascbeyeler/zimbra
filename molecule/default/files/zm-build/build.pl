#!/bin/bash
# A fake of Zimbra's build.pl, for the Molecule tests. It saves how it was run
# and packs the fake Zimbra installer like a build of the version it was asked.
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
for arg in "$@"; do
  case "$arg" in
    --build-release-no=*) release_no=${arg#*=} ;;
    --build-destination-base-dir=*) destination=${arg#*=} ;;
  esac
done

record="$here/../fake-build"
mkdir -p "$record"
printf '%s\n' "$@" > "$record/args"
printf 'USER=%s\nJAVA_HOME=%s\nENV_CACHE_CLEAR_FLAG=%s\n' \
  "$(id -un)" "${JAVA_HOME:-}" "${ENV_CACHE_CLEAR_FLAG:-}" > "$record/env"
echo run >> "$record/runs"

name="zcs-${release_no}_GA_1000.UBUNTU22_64.20261016000000"
work=$(mktemp -d)
cp -r "$here/zcs-fake" "$work/$name"
output="$destination/UBUNTU22_64/LIBERTY-${release_no//./}/20261016000000_FOSS"
mkdir -p "$output"
tar -C "$work" -czf "$output/$name.tgz" "$name"
rm -rf "$work"
echo "Built $output/$name.tgz"
