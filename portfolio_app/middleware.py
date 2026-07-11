class MediaProtectionHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault("X-Content-Type-Options", "nosniff")
        response.setdefault("Referrer-Policy", "same-origin")
        response.setdefault("Permissions-Policy", "display-capture=(), screen-wake-lock=()")
        response.setdefault("Content-Security-Policy", "frame-ancestors 'self'")
        return response
