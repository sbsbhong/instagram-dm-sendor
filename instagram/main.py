from instagram import dm

class InstagramFeautures:
    def __init__(self, context, default_timewait=1):
        self._context = context
        self._timewait = default_timewait

    @property
    def dm(self):
        return dm.InstagramDM(self._context, self._timewait)