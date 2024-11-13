if [ -d $1 ]; then
    if [ ! -d $1/prod ]; then
        echo "Creating production folder for challenge $1"
        mkdir $1/prod
    else
        while : ; do
            echo -n "Production folder already exists. Overwrite? (y/n) "
            read var
            if [ "${var,,}" = "y" ]; then
                rm -rf $1/prod
                mkdir $1/prod
                break
            elif [ "${var,,}" = "n" ]; then
                echo "Script terminated"
                exit 0
            fi
        done
    fi

    if [ -d $1/public ]; then
        cp -r $1/public/* $1/prod
    fi
    if [ -d $1/deploy ]; then
        cp -r $1/deploy/* $1/prod
    fi

    echo "Challenge $1 production folder created"
else
    echo "Invalid challenge $1"
fi