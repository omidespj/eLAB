# eLAB

mkdir -p ~/elabftw && cd ~/elabftw

curl -o docker-compose.yml https://get.elabftw.net/docker-compose.yml

sudo docker-compose up -d



rm -f ~/elabftw/docker-compose.yml

wget https://get.elabftw.net/docker-compose.yml -O ~/elabftw/docker-compose.yml

cat ~/elabftw/docker-compose.yml | head -n 10

sudo docker-compose up -d
