import falcon

from decouple import config

__all__ = (
    'TokenAuthMiddleware',
)


class HTTPForbiddenError(falcon.HTTPForbidden):
    @property
    def has_representation(self):
        return False


class TokenAuthMiddleware:

    def process_request(self, req, resp):
        token = req.get_header('X-Auth-Token')
        if not token or token != config('AUTH_TOKEN'):
            raise HTTPForbiddenError()
