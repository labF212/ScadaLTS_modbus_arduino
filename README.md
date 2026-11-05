# Como executar o ScadaLTS

## start docker:

docker compose up -d

## close docker:

docker-compose down

## endereço do scada:

http://localhost:8080/Scada-LTS/

Como atualizar:
mudar para a pasta:
/mnt/dados/scadalts-projeto/

1. download

docker compose pull

2. desligar o atual

docker compose down

3. enviar o novo

docker compose up -d

alterar o fciheiro de configuração

nano docker-compose.yml
image: scadalts/scadalts:2.8.1 ou escolher a próxima
