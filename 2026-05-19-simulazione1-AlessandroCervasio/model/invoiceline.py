from dataclasses import dataclass


@dataclass
# informazioni relative alla singola fattura
class Invoiceline:
    InvoiceLineId: int
    InvoiceId: int
    TrackId: int
    UnitPrice: float #prezzo della singola traccia
    Quantity: int

    def __hash__(self):
        return hash(self.InvoiceLineId)

    def __eq__(self, other):
        return self.InvoiceLineId == other.InvoiceLineId

    def __str__(self):
        return f"{self.InvoiceLineId}"