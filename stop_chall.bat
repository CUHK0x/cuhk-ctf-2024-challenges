@echo off
if exist %1\prod (
    cd %1\prod
    docker compose down
    cd ..\..\..
) else (
    echo "Invalid challenge %1"
)