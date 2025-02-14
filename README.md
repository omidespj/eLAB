ls ~/elabftw/

curl -so ~/elabftw/docker-compose.yml "https://get.elabftw.net/?config"


cat ~/elabftw/docker-compose.yml


cd ~/elabftw
sudo docker-compose up -d --build
