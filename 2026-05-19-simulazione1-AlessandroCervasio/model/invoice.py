from dataclasses import dataclass
from datetime import date

# informazioni della fattura nel suo complesso
@dataclass
class Invoice:
    InvoiceId: int
    CustomerId: int
    InvoiceDate: date
    BillingAddress: str
    BillingCity: str
    BillingState: str
    BillingCountry: str
    BillingPostalCode: str
    Total: float    #spesa totale

    def __hash__(self):
        return hash(self.InvoiceId)

    def __eq__(self, other):
        return self.InvoiceId == other.InvoiceId

    def __str__(self):
        return f"{self.InvoiceId} -- {self.InvoiceDate}"