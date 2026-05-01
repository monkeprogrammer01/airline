import random
import string


class FirstVisitPromoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get("has_visited_site"):
            promo_code = "WELCOME-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            request.session["has_visited_site"] = True
            request.session["promo_code"] = promo_code
            request.session["show_promo_banner"] = True

        response = self.get_response(request)
        return response
