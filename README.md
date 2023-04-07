# tt_web3_ETH
A backend service that interacts with an ERC-721 contract on the Ethereum blockchain

### Установка
Clone the project to the local machine, install the virtual environment and run it

Install all dependencies from a file ```requirements.txt```
```sh
pip install -r requirements.txt
```
Set the environment settings in the file ```.env```
```sh
PRIVATE_KEY = your private key
ETH_NODE_URL = your node url
FROM_ADDRESS = addres of your wallet
CONTRACT_ADDRESS = contract address

DB_NAME= name of the db
DB_USER= user of db
DB_PASSWORD= db user password
DB_HOST= db host
DB_PORT= db port
```
### API
A few examples of interaction with the API:

http://127.0.0.1:8000/tokens/create
Request method: ```POST```
Creation of a unique token in the blockchain and recording its parameters in db

http://127.0.0.1:8000/tokens/list
Request method: ```GET```
List of all objects of the Token model

http://127.0.0.1:8000/tokens/total_supply
Request method: ```GET```
Information on the total number of tokens in the network