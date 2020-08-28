Instruction how to clone and deploy
git clone https://github.com/henry0520/myproj.git
cd myproj
docker-compose build
docker-compose run -p 8000:8000 -d myproject


check the swagger for the api endpoint
http://<hostname.com>:8000/api/swagger
