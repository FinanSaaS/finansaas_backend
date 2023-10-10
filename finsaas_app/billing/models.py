from abc import ABC, abstractmethod
from django.db import models
from system_accounts.models import SystemAccount,Address, PhoneNumber, Email

class LegalEntity(models.Model):
    LEGAL_ENTITY_TYPES = (
        ('person', 'Person'),
        ('company', 'Company'),
    )
    
    system_account = models.ForeignKey(SystemAccount, on_delete=models.CASCADE, related_name='legal_entities')
    legal_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=14)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='legal_entities') 
    phone_numbers = models.ManyToManyField(PhoneNumber, related_name='legal_entities') 
    emails = models.ManyToManyField(Email, related_name='legal_entities') 

    is_active = models.BooleanField(default=True, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.legal_name
    

class RecurrencyPlan(models.Model):
    FREQUENCIES = (
        ('monthly', 'Monthly'),
        ('annually', 'Annually'),
    )
    system_account = models.ForeignKey(SystemAccount, on_delete=models.CASCADE, related_name='recurrency_plans')
    name = models.CharField(max_length=255)
    frequency = models.CharField(choices=FREQUENCIES, max_length=10)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    days_before_due_invoice_generation = models.IntegerField()
    default_due_day = models.IntegerField()

    is_active = models.BooleanField(default=True, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SalesInvoice(models.Model):
    STATUSES = (
        ('overdue', 'Overdue'),
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('waiting', 'Waiting'),
    )
    legal_entity = models.ForeignKey(LegalEntity, on_delete=models.CASCADE)
    recurrency_plan = models.ForeignKey(RecurrencyPlan, on_delete=models.PROTECT, null=True, blank=True)
    description = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    accounting_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(choices=STATUSES, max_length=20, default='waiting')

    is_active = models.BooleanField(default=True, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.legal_entity.legal_name} - {self.recurrency_plan.name} - {self.accounting_date}"
    

class BillingService:
    def __init__(self, billing_provider):
        self.billing_provider = billing_provider

    def create_invoice(self, amount, due_date):
        return self.billing_provider.generate_billing_invoice(amount, due_date)

    def check_invoice_status(self, invoice_id):
        return self.billing_provider.get_billing_invoice_status(invoice_id)


class BillingProvider(ABC):
    # TODO Define methods as we go (likely to follow endpoints structure)

    @abstractmethod
    def generate_billing_invoice(self, legal_name, registration_number, legal_entity_id):
        pass

    @abstractmethod
    def generate_billing_invoice(self, amount, due_date):
        pass

    @abstractmethod
    def get_billing_invoice_status(self, invoice_id):
        pass

    
class BillingProviderConfig(models.Model):
    BILLING_PROVIDERS =[
        ('iugu', 'Iugu'), 
    ]
    provider_name = models.CharField(choices=BILLING_PROVIDERS, max_length=50)
    api_key = models.CharField(max_length=255)  # TODO Define encryption or move to settings / env variable
    
    base_endpoint = models.URLField()
    create_billing_invoice_endpoint = models.URLField()
    get_billing_invoice_endpoint = models.URLField()
    list_billing_invoice_endpoint = models.URLField()

    is_active = models.BooleanField(default=True, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.provider_name


class BillingInvoice(models.Model):
    sales_invoice = models.ForeignKey(SalesInvoice, on_delete=models.CASCADE)
    external_service = models.ForeignKey(BillingProviderConfig, on_delete=models.PROTECT)
    external_invoice_id = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sales_invoice} @ {self.external_service}"