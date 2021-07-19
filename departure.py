class Departure:

    def __init__(self, date, actual_price_usd = "", original_price_usd = "", actual_price_aud = "", original_price_aud = "", type = "", status = "", available = "", notes = ""):
        self.date = date
        self.actual_price_usd = actual_price_usd
        self.original_price_usd = original_price_usd
        self.actual_price_aud = actual_price_aud
        self.original_price_aud = original_price_aud
        self.type = type
        self.status = status
        self.available = available
        self.notes = notes