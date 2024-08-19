from .wishsession import Wishsession

def wishsession(request):
    return {'wishsession':Wishsession(request)}