from rest_framework.serializers import ModelSerializer

from nft_token.models import Token

class TokenSerializer(ModelSerializer):
    
    class Meta:
        model=Token
        fields=('id', 'unique_hash', 'tx_hash', 'media_usrl', 'owner')
