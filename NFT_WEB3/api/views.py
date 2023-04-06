from rest_framework.decorators import api_view
from rest_framework.response import Response

from nft_token.models import Token

from .serializers import TokenSerializer


@api_view(['GET'])
def tokens_list(reqiest):
    tokens = Token.objects.all()
    serializer = TokenSerializer(tokens, many=True)
    return Response(serializer.data)

