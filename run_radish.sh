#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root (directory containing this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check for mandatory environment parameter
ENVIRONMENT=""
for arg in "$@"; do
    if [[ "$arg" == "--env" || "$arg" == "-e" ]]; then
        # Get the next argument as environment value
        continue
    elif [[ "$arg" =~ ^--env= || "$arg" =~ ^-e= ]]; then
        # Extract environment from --env=value or -e=value format
        ENVIRONMENT="${arg#*=}"
        break
    elif [[ "$ENVIRONMENT" == "" && "$arg" != "--env" && "$arg" != "-e" ]]; then
        # If we haven't found environment yet and this isn't a flag, it might be the environment
        if [[ "$arg" == "dev" || "$arg" == "qa" || "$arg" == "prod" ]]; then
            ENVIRONMENT="$arg"
            break
        fi
    fi
done

# Validate environment parameter
if [[ -z "$ENVIRONMENT" ]]; then
    echo "Error: Environment parameter is required."
    echo "Usage: $0 [--env dev|qa|prod] [radish options...]"
    echo "   or: $0 [dev|qa|prod] [radish options...]"
    exit 1
fi

# Set URL based on environment
case "$ENVIRONMENT" in
    "dev")
        export IFLOW_BASE_URL="http://localhost:8080"
        ;;
    "qa")
        export IFLOW_BASE_URL="http://localhost:8081"
        ;;
    "prod")
        export IFLOW_BASE_URL="http://localhost:9000"
        ;;
    *)
        echo "Error: Invalid environment '$ENVIRONMENT'. Must be one of: dev, qa, prod"
        exit 1
        ;;
esac

echo "Using environment: $ENVIRONMENT (URL: $IFLOW_BASE_URL)"

# Prepend tests directory to PYTHONPATH
export PYTHONPATH="${SCRIPT_DIR}/tests${PYTHONPATH+:${PYTHONPATH}}"

# If no basedir (-b/--basedir) was provided, add "-b tests"
ADD_BASEDIR=true
for arg in "$@"; do
    if [[ "$arg" == "-b" || "$arg" == "--basedir" ]]; then
        ADD_BASEDIR=false
        break
    fi
done

if $ADD_BASEDIR; then
    exec radish "$@" -b "${SCRIPT_DIR}/tests"
else
    exec radish "$@"
fi
