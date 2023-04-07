import os
import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

from nft_token.models import Token


from .serializers import TokenSerializer


class TokenListView(APIView):
    def get(self, request):
        tokens = Token.objects.all()
        serializer = TokenSerializer(tokens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TotalSupplyView(APIView):
    def get(self, request):
        web3 = Web3(HTTPProvider(ETH_NODE_URL))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        contract_address = CONTRACT_ADDRESS
        with open('abi.json') as file:
            contract_abi = json.load(file)
        contract = web3.eth.contract(
            address=contract_address,
            abi=contract_abi
        )
        total_supply = contract.functions.totalSupply().call()
        return Response({'result':total_supply}, status=status.HTTP_200_OK)