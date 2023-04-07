import json
import os

from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware

from constants import LEN_RANDOM_STRING
from nft_token.models import Token

from .pagination import StandardPagination
from .serializers import TokenSerializer
from .string_generator import generate_random_string

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ETH_NODE_URL = os.getenv("ETH_NODE_URL")
FROM_ADDRESS = os.getenv("FROM_ADDRESS")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")


class TokenCreateView(APIView):
    def post(self, request):
        data = request.data
        media_url = data.get["media_url"]
        owner = data.get["owner"]
        unique_hash = generate_random_string(LEN_RANDOM_STRING)
        token = Token.objects.create(
            media_url=media_url, owner=owner, unique_hash=unique_hash
        )
        web3 = Web3(HTTPProvider(ETH_NODE_URL))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        contract_address = CONTRACT_ADDRESS
        with open("abi.json") as file:
            contract_abi = json.load(file)
        contract = web3.eth.contract(
            address=contract_address, abi=contract_abi
        )
        nonce = web3.eth.get_transaction_count(FROM_ADDRESS)
        gas_price = web3.eth.gas_price
        gas_price_gwei = web3.from_wei(gas_price, "gwei")
        mint_method = contract.functions.mint(
            token.owner, token.unique_hash, token.media_url
        ).build_transaction(
            {
                "chainId": 5,
                "nonce": nonce,
                "gasPrice": gas_price_gwei,
                "gas": 4000000,
            }
        )
        sign_txn = web3.eth.account.sign_transaction(
            mint_method, private_key=PRIVATE_KEY
        )
        tx_hash = web3.eth.send_raw_transaction(sign_txn.rawTransaction)
        token.tx_hash = web3.to_hex(tx_hash)
        token.save()
        serializer = TokenSerializer(token)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TokenListView(APIView):
    pagination_class = StandardPagination

    def get(self, request):
        tokens = Token.objects.all()
        serializer = TokenSerializer(tokens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TotalSupplyView(APIView):
    def get(self, request):
        web3 = Web3(HTTPProvider(ETH_NODE_URL))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        contract_address = CONTRACT_ADDRESS
        with open("abi.json") as file:
            contract_abi = json.load(file)
        contract = web3.eth.contract(
            address=contract_address, abi=contract_abi
        )
        total_supply = contract.functions.totalSupply().call()
        return Response({"result": total_supply}, status=status.HTTP_200_OK)
