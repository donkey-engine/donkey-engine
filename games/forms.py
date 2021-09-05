from django import forms

from games.models import Game
from servers.helpers.adapters import ALLOWED_GAMES


class GameForm(forms.ModelForm):

    build_key = forms.ChoiceField(choices=zip(ALLOWED_GAMES, ALLOWED_GAMES))

    class Meta:
        model = Game
        exclude = ()
