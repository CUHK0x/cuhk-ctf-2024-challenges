if [ -d $1 ]; then
    if [[ ! -d $1/prod || "$2" == "--build" ]]; then
        ./make_chall.sh $1
    fi
    cd $1/prod
    if [ "$2" == "--build" ]; then
        docker compose up -d --build
    else
        docker compose up -d
    fi
else
    echo "Invalid challenge $1"
fi
