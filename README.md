Instruction how to clone and deploy
git clone https://github.com/henry0520/myproj.git
cd myproj
docker-compose build
docker-compose run -p 8000:8000 -d myproj


check the swagger for the api endpoint
http://<hostname.com>:8000/api/swagger

To test the endpoint, the postman is recommended

test credential
username: testuser
email: testuser@venn.bio
passwd: 1234
