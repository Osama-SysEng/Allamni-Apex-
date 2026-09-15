"""
Manual test script for Phase 2 features
Testing Institution Management, Billing, and Odoo Integration
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime, date, timedelta
from uuid import uuid4
from decimal import Decimal
from shared.models import UserRole, SubscriptionPlan, SubscriptionStatus
from shared.identity import generate_student_code, generate_teacher_code
from shared.store import store
from shared.billing import get_billing_service, InvoiceStatus, PaymentMethod, PRICING_PLANS


def test_code_generation():
    """Test student and teacher code generation"""
    print("Testing Code Generation...")
    
    institution_id = str(uuid4())
    
    # Test student code generation
    student_code = generate_student_code(
        institution_id=institution_id,
        class_id="Class-A",
        grade_level="Grade-10",
        academic_year="2024-2025",
        issued_by=str(uuid4())
    )
    
    assert student_code['institution_id'] == institution_id
    assert student_code['class_id'] == "Class-A"
    assert student_code['is_active'] is True
    assert student_code['code'].startswith("STU-")
    print("[PASS] Student code generation test passed")
    
    # Test teacher code generation
    teacher_code = generate_teacher_code(
        institution_id=institution_id,
        department="Mathematics",
        subjects=["Algebra", "Geometry"],
        grade_levels=["Grade-9", "Grade-10"],
        issued_by=str(uuid4())
    )
    
    assert teacher_code['institution_id'] == institution_id
    assert teacher_code['department'] == "Mathematics"
    assert "Algebra" in teacher_code['subjects']
    assert teacher_code['code'].startswith("TCH-")
    print("[PASS] Teacher code generation test passed")


def test_billing_service():
    """Test billing service functionality"""
    print("Testing Billing Service...")
    
    billing_service = get_billing_service(store)
    
    # Test pricing plans
    assert "basic" in PRICING_PLANS
    assert "professional" in PRICING_PLANS
    assert "enterprise" in PRICING_PLANS
    print("[PASS] Pricing plans test passed")
    
    # Test cost calculation
    cost = billing_service.calculate_subscription_cost(
        plan_type="professional",
        billing_cycle="monthly",
        student_count=50,
        teacher_count=5
    )
    
    assert cost['subtotal'] > 0
    assert cost['tax_amount'] > 0
    assert cost['total'] > 0
    assert cost['currency'] == "USD"
    print("[PASS] Cost calculation test passed")
    
    # Test invoice creation
    institution_id = str(uuid4())
    subscription_id = str(uuid4())
    
    invoice = billing_service.create_invoice(
        institution_id=institution_id,
        subscription_id=subscription_id,
        plan_type="professional",
        billing_cycle="monthly",
        student_count=50,
        teacher_count=5
    )
    
    assert invoice.institution_id == institution_id
    assert invoice.subscription_id == subscription_id
    assert invoice.status == InvoiceStatus.PENDING
    assert len(invoice.items) > 0
    assert invoice.total_amount > 0
    print("[PASS] Invoice creation test passed")
    
    # Test invoice retrieval
    retrieved_invoice = billing_service.get_invoice(invoice.id)
    assert retrieved_invoice is not None
    assert retrieved_invoice.id == invoice.id
    print("[PASS] Invoice retrieval test passed")
    
    # Test payment recording
    payment = billing_service.record_payment(
        invoice_id=invoice.id,
        amount=invoice.total_amount,
        payment_method=PaymentMethod.CREDIT_CARD,
        transaction_id="txn_12345"
    )
    
    assert payment.invoice_id == invoice.id
    assert payment.amount == invoice.total_amount
    assert payment.payment_method == PaymentMethod.CREDIT_CARD
    print("[PASS] Payment recording test passed")
    
    # Test invoice status update
    updated_invoice = billing_service.update_invoice_status(invoice.id, InvoiceStatus.PAID)
    assert updated_invoice.status == InvoiceStatus.PAID
    assert updated_invoice.paid_date is not None
    print("[PASS] Invoice status update test passed")
    
    # Test billing summary
    summary = billing_service.get_billing_summary(institution_id)
    assert summary['total_invoices'] == 1
    assert summary['total_paid'] > 0
    assert summary['payment_rate'] == 100.0
    print("[PASS] Billing summary test passed")


def test_pricing_plans():
    """Test pricing plan calculations"""
    print("Testing Pricing Plans...")
    
    billing_service = get_billing_service(store)
    
    # Test basic plan
    basic_monthly = billing_service.calculate_subscription_cost("basic", "monthly")
    assert basic_monthly['base_price'] == Decimal('99.00')
    print("[PASS] Basic plan monthly test passed")
    
    basic_yearly = billing_service.calculate_subscription_cost("basic", "yearly")
    assert basic_yearly['base_price'] == Decimal('990.00')
    assert basic_yearly['discount_amount'] > 0  # Yearly discount
    print("[PASS] Basic plan yearly test passed")
    
    # Test professional plan with users
    professional_with_users = billing_service.calculate_subscription_cost(
        "professional", "monthly", student_count=100, teacher_count=10
    )
    assert professional_with_users['per_student_cost'] > 0
    assert professional_with_users['per_teacher_cost'] > 0
    print("[PASS] Professional plan with users test passed")
    
    # Test enterprise plan
    enterprise = billing_service.calculate_subscription_cost("enterprise", "monthly")
    assert enterprise['base_price'] == Decimal('999.00')
    print("[PASS] Enterprise plan test passed")


def test_store_billing_collections():
    """Test that store has billing collections"""
    print("Testing Store Billing Collections...")
    
    billing_service = get_billing_service(store)
    
    assert hasattr(store, 'invoices')
    assert hasattr(store, 'payments')
    assert hasattr(store, 'billing_service')
    print("[PASS] Store billing collections test passed")


def test_invoice_item_creation():
    """Test invoice item structure"""
    print("Testing Invoice Item Creation...")
    
    from shared.billing import InvoiceItem
    
    item = InvoiceItem(
        id=str(uuid4()),
        description="Test Service",
        quantity=2,
        unit_price=Decimal("50.00"),
        total=Decimal("100.00")
    )
    
    assert item.description == "Test Service"
    assert item.quantity == 2
    assert item.unit_price == Decimal("50.00")
    assert item.total == Decimal("100.00")
    print("[PASS] Invoice item creation test passed")


def test_payment_methods():
    """Test payment method enum"""
    print("Testing Payment Methods...")
    
    assert PaymentMethod.CREDIT_CARD.value == "credit_card"
    assert PaymentMethod.BANK_TRANSFER.value == "bank_transfer"
    assert PaymentMethod.CASH.value == "cash"
    assert PaymentMethod.CHECK.value == "check"
    print("[PASS] Payment methods enum test passed")


def test_invoice_statuses():
    """Test invoice status enum"""
    print("Testing Invoice Statuses...")
    
    assert InvoiceStatus.DRAFT.value == "draft"
    assert InvoiceStatus.PENDING.value == "pending"
    assert InvoiceStatus.PAID.value == "paid"
    assert InvoiceStatus.OVERDUE.value == "overdue"
    assert InvoiceStatus.CANCELLED.value == "cancelled"
    print("[PASS] Invoice statuses enum test passed")


def test_invoice_number_generation():
    """Test invoice number generation"""
    print("Testing Invoice Number Generation...")
    
    billing_service = get_billing_service(store)
    
    invoice_number_1 = billing_service.generate_invoice_number()
    invoice_number_2 = billing_service.generate_invoice_number()
    
    assert invoice_number_1 != invoice_number_2
    assert invoice_number_1.startswith("INV-")
    assert invoice_number_2.startswith("INV-")
    print("[PASS] Invoice number generation test passed")


def test_overdue_invoices():
    """Test overdue invoice detection"""
    print("Testing Overdue Invoice Detection...")
    
    billing_service = get_billing_service(store)
    
    # Create an invoice with past due date
    institution_id = str(uuid4())
    subscription_id = str(uuid4())
    
    invoice = billing_service.create_invoice(
        institution_id=institution_id,
        subscription_id=subscription_id,
        plan_type="basic",
        billing_cycle="monthly"
    )
    
    # Manually set due date to past
    invoice.due_date = date.today() - timedelta(days=10)
    
    # Check overdue
    overdue = billing_service.check_overdue_invoices()
    
    # Our invoice should be marked as overdue
    updated_invoice = billing_service.get_invoice(invoice.id)
    assert updated_invoice.status == InvoiceStatus.OVERDUE
    print("[PASS] Overdue invoice detection test passed")


def main():
    """Run all tests"""
    print("=" * 60)
    print("PHASE 2 MANUAL TESTS - Allamni v4.0")
    print("=" * 60)
    print()
    
    try:
        test_code_generation()
        test_billing_service()
        test_pricing_plans()
        test_store_billing_collections()
        test_invoice_item_creation()
        test_payment_methods()
        test_invoice_statuses()
        test_invoice_number_generation()
        test_overdue_invoices()
        
        print()
        print("=" * 60)
        print("[SUCCESS] ALL TESTS PASSED!")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"[FAILED] TEST FAILED: {e}")
        print("=" * 60)
        return 1
    except Exception as e:
        print()
        print("=" * 60)
        print(f"[ERROR] ERROR: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())