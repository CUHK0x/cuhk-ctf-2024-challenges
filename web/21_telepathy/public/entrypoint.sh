POSTGRES_READONLY_PASSWORD=$(hexdump -vn16 -e'4/4 "%08X" 1 "\n"' /dev/urandom) /go/bin/app 
