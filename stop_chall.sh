if [ -d $1/prod ]; then
    cd $1/prod
    docker compose down
else
    echo "Invalid challenge $1"
fi