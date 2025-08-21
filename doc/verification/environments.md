# Enviornments

The following environments shall be used for different purposes:

<environment:local>
:   Local test environment pointing to the actual repository.

    -   uses a temporary database in /tmp
    -   runs on a port in range 7000..8000
    -   is controlled by start_server.py
    -   use run_radish.py to run against local environment like:
        - `run_radish.py local tests/features/ --local --debug --tags=smoke`

<environment:prod>
:   Productive environment

    - runs on port 9000
    - shall never be used for testing
    - shall only receive stable releses
    - uses productive database on `/opt/iflow/prod/database`

<enviornment:dev>
