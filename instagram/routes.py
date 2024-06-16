class IntagramRoutes:
    BASE_URL = "https://www.instagram.com/"

    def _resolve_url(self, url: str) -> str:
        return self.BASE_URL + url
    
    @property
    def home(self):
        return self.BASE_URL

    @property
    def login(self):
        return self._resolve_url("accounts/login/")
    
    @property
    def two_factor_auth(self):
        return self._resolve_url("accounts/login/two_factor?next=%2F")
    
    @property
    def account_onetap_modal(self):
        return self._resolve_url("accounts/onetap/?next=%2F")

    @property
    def dm(self):
        return self._resolve_url("direct/inbox/")