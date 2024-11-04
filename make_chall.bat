@echo off
if exist %1\ (
    if not exist %1\prod\ (
        echo "Creating production folder for challenge %1"
        mkdir %1\prod
    ) else (
        :input
        set /p var="Production folder already exists. Overwrite? (y/n) "

        if /i "%var%" == "y" (
            del /Q %1\prod
        ) else if /i "%var%" == "n" (
            echo "Script terminated"
            exit 0
        ) else (
            goto :input
        )
    )

    if exist %1\public\ (
        xcopy /E /Y /Q %1\public %1\prod
    )
    if exist %1\deploy\ (
        xcopy /E /Y /Q %1\deploy %1\prod
    )

    echo "Challenge %1 production folder created"
) else (
    echo "Invalid challenge %1"
)