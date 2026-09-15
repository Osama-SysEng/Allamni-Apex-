"""
Billing and Invoice Management for Allamni v4.0
Handles invoice generation, payment tracking, and billing operations
"""
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta, timezone
from uuid import uuid4
from typing import List, Optional, Dict
from enum import Enum
from decimal import Decimal

class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"
    CHECK = "check"

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    EGP = "EGP"
    SAR = "SAR"
    AED = "AED"

@dataclass
class InvoiceItem:
    id: str
    description: str
    quantity: int
    unit_price: Decimal
    total: Decimal
    metadata: Dict = field(default_factory=dict)

@dataclass
class Invoice:
    id: str
    institution_id: str
    subscription_id: str
    invoice_number: str
    status: InvoiceStatus
    issue_date: date
    due_date: date
    currency: Currency
    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    items: List[InvoiceItem] = field(default_factory=list)
    payment_method: Optional[PaymentMethod] = None
    paid_date: Optional[date] = None
    notes: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict = field(default_factory=dict)

@dataclass
class Payment:
    id: str
    invoice_id: str
    amount: Decimal
    payment_method: PaymentMethod
    payment_date: datetime
    transaction_id: Optional[str] = None
    status: str = "completed"
    notes: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

# Pricing configuration
PRICING_PLANS = {
    "basic": {
        "monthly": 99.00,
        "yearly": 990.00,
        "currency": "USD",
        "per_student": 0,
        "per_teacher": 0
    },
    "professional": {
        "monthly": 299.00,
        "yearly": 2990.00,
        "currency": "USD",
        "per_student": 2.00,
        "per_teacher": 10.00
    },
    "enterprise": {
        "monthly": 999.00,
        "yearly": 9990.00,
        "currency": "USD",
        "per_student": 1.00,
        "per_teacher": 5.00
    }
}

class BillingService:
    """Service for billing operations"""
    
    def __init__(self, store):
        self.store = store
        # Initialize billing collections if not exist
        if not hasattr(store, 'invoices'):
            store.invoices = {}
        if not hasattr(store, 'payments'):
            store.payments = {}
    
    def generate_invoice_number(self) -> str:
        """Generate unique invoice number"""
        import random
        year = datetime.now(timezone.utc).year
        month = datetime.now(timezone.utc).month
        random_num = random.randint(1000, 9999)
        return f"INV-{year}{month:02d}-{random_num}"
    
    def calculate_subscription_cost(self, plan_type: str, billing_cycle: str, 
                                    student_count: int = 0, teacher_count: int = 0) -> Dict:
        """Calculate subscription cost based on plan and usage"""
        if plan_type not in PRICING_PLANS:
            raise ValueError(f"Invalid plan type: {plan_type}")
        
        pricing = PRICING_PLANS[plan_type]
        
        # Base price
        if billing_cycle == "yearly":
            base_price = Decimal(str(pricing["yearly"]))
        else:
            base_price = Decimal(str(pricing["monthly"]))
        
        # Per-user costs
        per_student_cost = Decimal(str(pricing["per_student"])) * student_count
        per_teacher_cost = Decimal(str(pricing["per_teacher"])) * teacher_count
        
        subtotal = base_price + per_student_cost + per_teacher_cost
        
        # Tax (simplified - in production would be based on location)
        tax_rate = Decimal("0.14")  # 14% VAT (example for Egypt)
        tax_amount = subtotal * tax_rate
        
        # Discount (simplified)
        discount_amount = Decimal("0.00")
        if billing_cycle == "yearly":
            # 20% discount for yearly plans
            discount_amount = subtotal * Decimal("0.20")
        
        total = subtotal + tax_amount - discount_amount
        
        return {
            "base_price": base_price,
            "per_student_cost": per_student_cost,
            "per_teacher_cost": per_teacher_cost,
            "subtotal": subtotal,
            "tax_rate": tax_rate,
            "tax_amount": tax_amount,
            "discount_amount": discount_amount,
            "total": total,
            "currency": pricing["currency"]
        }
    
    def create_invoice(self, institution_id: str, subscription_id: str, 
                      plan_type: str, billing_cycle: str,
                      student_count: int = 0, teacher_count: int = 0,
                      due_days: int = 30) -> Invoice:
        """Create a new invoice"""
        # Calculate costs
        cost_breakdown = self.calculate_subscription_cost(
            plan_type, billing_cycle, student_count, teacher_count
        )
        
        # Create invoice items
        items = [
            InvoiceItem(
                id=str(uuid4()),
                description=f"{plan_type.capitalize()} Plan ({billing_cycle})",
                quantity=1,
                unit_price=cost_breakdown["base_price"],
                total=cost_breakdown["base_price"]
            )
        ]
        
        if student_count > 0 and cost_breakdown["per_student_cost"] > 0:
            items.append(InvoiceItem(
                id=str(uuid4()),
                description=f"Student licenses ({student_count} students)",
                quantity=student_count,
                unit_price=Decimal(str(PRICING_PLANS[plan_type]["per_student"])),
                total=cost_breakdown["per_student_cost"]
            ))
        
        if teacher_count > 0 and cost_breakdown["per_teacher_cost"] > 0:
            items.append(InvoiceItem(
                id=str(uuid4()),
                description=f"Teacher licenses ({teacher_count} teachers)",
                quantity=teacher_count,
                unit_price=Decimal(str(PRICING_PLANS[plan_type]["per_teacher"])),
                total=cost_breakdown["per_teacher_cost"]
            ))
        
        # Create invoice
        invoice = Invoice(
            id=str(uuid4()),
            institution_id=institution_id,
            subscription_id=subscription_id,
            invoice_number=self.generate_invoice_number(),
            status=InvoiceStatus.PENDING,
            issue_date=date.today(),
            due_date=date.today() + timedelta(days=due_days),
            currency=Currency[PRICING_PLANS[plan_type]["currency"]],
            subtotal=cost_breakdown["subtotal"],
            tax_amount=cost_breakdown["tax_amount"],
            discount_amount=cost_breakdown["discount_amount"],
            total_amount=cost_breakdown["total"],
            items=items,
            metadata={
                "plan_type": plan_type,
                "billing_cycle": billing_cycle,
                "student_count": student_count,
                "teacher_count": teacher_count
            }
        )
        
        self.store.invoices[invoice.id] = invoice
        
        return invoice
    
    def get_invoice(self, invoice_id: str) -> Optional[Invoice]:
        """Get invoice by ID"""
        return self.store.invoices.get(invoice_id)
    
    def get_invoices_by_institution(self, institution_id: str) -> List[Invoice]:
        """Get all invoices for an institution"""
        return [
            inv for inv in self.store.invoices.values()
            if inv.institution_id == institution_id
        ]
    
    def update_invoice_status(self, invoice_id: str, status: InvoiceStatus) -> Optional[Invoice]:
        """Update invoice status"""
        invoice = self.store.invoices.get(invoice_id)
        if not invoice:
            return None
        
        invoice.status = status
        invoice.updated_at = datetime.now(timezone.utc)
        
        if status == InvoiceStatus.PAID:
            invoice.paid_date = date.today()
        
        return invoice
    
    def record_payment(self, invoice_id: str, amount: Decimal, 
                     payment_method: PaymentMethod, transaction_id: str = None,
                     notes: str = None) -> Payment:
        """Record a payment for an invoice"""
        invoice = self.store.invoices.get(invoice_id)
        if not invoice:
            raise ValueError("Invoice not found")
        
        payment = Payment(
            id=str(uuid4()),
            invoice_id=invoice_id,
            amount=amount,
            payment_method=payment_method,
            payment_date=datetime.now(timezone.utc),
            transaction_id=transaction_id,
            notes=notes
        )
        
        self.store.payments[payment.id] = payment
        
        # Update invoice status if fully paid
        total_paid = sum(
            p.amount for p in self.store.payments.values()
            if p.invoice_id == invoice_id
        )
        
        if total_paid >= invoice.total_amount:
            self.update_invoice_status(invoice_id, InvoiceStatus.PAID)
        
        return payment
    
    def get_payments_by_invoice(self, invoice_id: str) -> List[Payment]:
        """Get all payments for an invoice"""
        return [
            payment for payment in self.store.payments.values()
            if payment.invoice_id == invoice_id
        ]
    
    def check_overdue_invoices(self) -> List[Invoice]:
        """Check and mark overdue invoices"""
        overdue = []
        today = date.today()
        
        for invoice in self.store.invoices.values():
            if invoice.status == InvoiceStatus.PENDING and invoice.due_date < today:
                invoice.status = InvoiceStatus.OVERDUE
                invoice.updated_at = datetime.now(timezone.utc)
                overdue.append(invoice)
        
        return overdue
    
    def get_billing_summary(self, institution_id: str) -> Dict:
        """Get billing summary for an institution"""
        invoices = self.get_invoices_by_institution(institution_id)
        
        total_invoiced = sum(inv.total_amount for inv in invoices)
        total_paid = sum(
            inv.total_amount for inv in invoices 
            if inv.status == InvoiceStatus.PAID
        )
        total_pending = sum(
            inv.total_amount for inv in invoices 
            if inv.status in [InvoiceStatus.PENDING, InvoiceStatus.OVERDUE]
        )
        
        return {
            "total_invoices": len(invoices),
            "total_invoiced": total_invoiced,
            "total_paid": total_paid,
            "total_pending": total_pending,
            "outstanding_balance": total_pending,
            "payment_rate": round(total_paid / total_invoiced * 100, 1) if total_invoiced > 0 else 0
        }


# Global billing service instance
def get_billing_service(store) -> BillingService:
    """Get or create billing service instance"""
    if not hasattr(store, 'billing_service'):
        store.billing_service = BillingService(store)
    return store.billing_service