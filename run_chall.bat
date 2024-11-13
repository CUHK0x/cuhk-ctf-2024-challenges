@echo off
if exist %1\ (
    if not exist %1\prod (
        make_chall.bat %1
    ) else (
        if "%~2" == "--build" (
            make_chall.bat %1
        )
    )
    cd %1\prod
    if "%~2" == "--build" (
        docker compose up -d --build
    ) else (
        docker compose up -d
    )
    cd ..\..\..
) else (
    echo "Invalid challenge %1"
)