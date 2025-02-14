# eLAB

curl -so docker-compose.yml "https://get.elabftw.net/?config"

curl -o docker-compose.yml https://raw.githubusercontent.com/elabftw/elabimg/master/src/docker-compose.yml-EXAMPLE

mkdir -p ~/elabftw/php-config
nano ~/elabftw/php-config/php-fpm.conf

[global]
daemonize = no
error_log = /proc/self/fd/2

[www]
listen = 9000
pm = dynamic
pm.max_children = 50
pm.start_servers = 5
pm.min_spare_servers = 5
pm.max_spare_servers = 35
clear_env = no

nano ~/elabftw/docker-compose.yml

    volumes:
      - ./php-config/php-fpm.conf:/etc/php83/php-fpm.conf
