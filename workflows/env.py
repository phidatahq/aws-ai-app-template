from os import getenv

# Expected values: `dev`, `stg` or `prd`
RUNTIME_ENV: str = getenv("RUNTIME_ENV", "dev")
