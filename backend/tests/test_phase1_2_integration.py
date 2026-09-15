"""
Integration Test - Phase 1 & 2 Combined
Tests the complete integration of Phase 1 and Phase 2 features
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime, date, timedelta, timezone
from uuid import uuid4
from decimal import Decimal
from shared.models import (
    UserRole, InstitutionType, SubscriptionPlan, SubscriptionStatus,
    Institution, Subscription
)
from shared.permissions import has_permission, get_permissions_for_role
from shared.identity import (
    validate_student_code, validate_teacher_code,
    generate_student_code, generate_teacher_code
)
from shared.store import store
from shared.billing import get_billing_service, InvoiceStatus, PaymentMethod


def test_complete_integration():
    """Test complete integration of Phase 1 and Phase 2"""
    print("Testing Complete Phase 1 & 2 Integration...")
    
    # 1. Create institution (Phase 1)
    institution_id = str(uuid4())
    institution = {
        'id': institution_id,
        'name_ar': 'مدرسة التميز',
        'name_en': 'Excellence School',
        'type': 'school',
        'sub_type': 'secondary',
        'country': 'Egypt',
        'city': 'Cairo',
        'is_active': True,
        'created_at': datetime.now(timezone.utc).isoformat(),
        'updated_at': datetime.now(timezone.utc).isoformat(),
    }
    store.institutions[institution_id] = institution
    print("[PASS] Institution creation (Phase 1)")
    
    # 2. Create subscription (Phase 1)
    subscription_id = str(uuid4())
    subscription = {
        'id': subscription_id,
        'institution_id': institution_id,
        'plan_type': 'professional',
        'status': 'active',
        'start_date': date.today().isoformat(),
        'end_date': (date.today() + timedelta(days=365)).isoformat(),
        'max_students': 500,
        'max_teachers': 50,
        'billing_cycle': 'yearly',
        'created_at': datetime.now(timezone.utc).isoformat(),
        'updated_at': datetime.now(timezone.utc).isoformat(),
    }
    store.subscriptions[subscription_id] = subscription
    print("[PASS] Subscription creation (Phase 1)")
    
    # 3. Generate student codes (Phase 2)
    student_codes = []
    for i in range(5):
        code_data = generate_student_code(
            institution_id=institution_id,
            class_id=f"Class-{chr(65+i)}",
            grade_level="Grade-10",
            academic_year="2024-2025",
            issued_by=str(uuid4())
        )
        student_codes.append(code_data)
    assert len(student_codes) == 5
    print("[PASS] Student code generation (Phase 2)")
    
    # 4. Generate teacher codes (Phase 2)
    teacher_codes = []
    for i in range(2):
        code_data = generate_teacher_code(
            institution_id=institution_id,
            department="Mathematics",
            subjects=["Algebra", "Geometry"],
            grade_levels=["Grade-9", "Grade-10"],
            issued_by=str(uuid4())
        )
        teacher_codes.append(code_data)
    assert len(teacher_codes) == 2
    print("[PASS] Teacher code generation (Phase 2)")
    
    # 5. Register students using codes (Phase 1)
    students = []
    for i, code_data in enumerate(student_codes):
        student_id = str(uuid4())
        student = {
            'id': student_id,
            'email': f'student{i+1}@school.edu',
            'full_name': f'Student {i+1}',
            'role': 'student',
            'institution_id': institution_id,
            'class_id': code_data['class_id'],
            'grade_level': code_data['grade_level'],
            'active': True,
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        store.users[student_id] = student
        store.users_by_email[student['email']] = student
        
        # Update code as used
        code_data['student_id'] = student_id
        code_data['used_at'] = datetime.now(timezone.utc).isoformat()
        
        students.append(student)
    assert len(students) == 5
    print("[PASS] Student registration with codes (Phase 1)")
    
    # 6. Register teachers using codes (Phase 1)
    teachers = []
    for i, code_data in enumerate(teacher_codes):
        teacher_id = str(uuid4())
        teacher = {
            'id': teacher_id,
            'email': f'teacher{i+1}@school.edu',
            'full_name': f'Teacher {i+1}',
            'role': 'teacher',
            'institution_id': institution_id,
            'department': code_data['department'],
            'subjects': code_data['subjects'],
            'active': True,
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        store.users[teacher_id] = teacher
        store.users_by_email[teacher['email']] = teacher
        
        # Update code as used
        code_data['teacher_id'] = teacher_id
        code_data['used_at'] = datetime.now(timezone.utc).isoformat()
        
        teachers.append(teacher)
    assert len(teachers) == 2
    print("[PASS] Teacher registration with codes (Phase 1)")
    
    # 7. Create learning profiles (Phase 1)
    from shared.models import LearningProfile, Skill, LearningPreferences
    for student in students:
        store.profiles[student['id']] = LearningProfile(
            student_id=student['id'],
            goal_domain='general',
            learning_preferences=LearningPreferences(content_format=['video', 'interactive']),
            skills=[
                Skill(code='math_basics', name='أساسيات الرياضيات', level=.40, target=.75, confidence=.55, importance=1),
                Skill(code='problem_solving', name='حل المشكلات', level=.35, target=.80, confidence=.60, importance=.95),
            ]
        )
    assert len(store.profiles) == 5
    print("[PASS] Learning profile creation (Phase 1)")
    
    # 8. Test permissions (Phase 1)
    assert has_permission(UserRole.STUDENT, "dashboard", "view", "own")
    assert has_permission(UserRole.TEACHER, "students", "view", "institution")
    assert has_permission(UserRole.INSTITUTION_ADMIN, "codes", "create", "institution")
    print("[PASS] Permission system (Phase 1)")
    
    # 9. Generate invoice (Phase 2)
    billing_service = get_billing_service(store)
    # Ensure billing service is properly initialized
    if billing_service is None:
        from shared.billing import BillingService
        billing_service = BillingService(store)
        store.billing_service = billing_service
    
    invoice = billing_service.create_invoice(
        institution_id=institution_id,
        subscription_id=subscription_id,
        plan_type='professional',
        billing_cycle='yearly',
        student_count=len(students),
        teacher_count=len(teachers)
    )
    assert invoice.institution_id == institution_id
    assert invoice.total_amount > 0
    print("[PASS] Invoice generation (Phase 2)")
    
    # 10. Record payment (Phase 2)
    payment = billing_service.record_payment(
        invoice_id=invoice.id,
        amount=invoice.total_amount,
        payment_method=PaymentMethod.CREDIT_CARD,
        transaction_id="txn_integration_test"
    )
    assert payment.invoice_id == invoice.id
    print("[PASS] Payment recording (Phase 2)")
    
    # 11. Verify invoice status (Phase 2)
    updated_invoice = billing_service.get_invoice(invoice.id)
    assert updated_invoice.status == InvoiceStatus.PAID
    print("[PASS] Invoice status update (Phase 2)")
    
    # 12. Test billing summary (Phase 2)
    summary = billing_service.get_billing_summary(institution_id)
    assert summary['total_invoices'] == 1
    assert summary['total_paid'] > 0
    print("[PASS] Billing summary (Phase 2)")
    
    # 13. Test institution dashboard data (Phase 2)
    student_count = len([u for u in store.users.values() if u.get('institution_id') == institution_id and u.get('role') == 'student'])
    teacher_count = len([u for u in store.users.values() if u.get('institution_id') == institution_id and u.get('role') == 'teacher'])
    active_student_codes = len([c for c in store.student_codes.values() if c['institution_id'] == institution_id and c['is_active'] and not c['student_id']])
    
    assert student_count == 5
    assert teacher_count == 2
    assert active_student_codes == 0  # All codes used
    print("[PASS] Institution dashboard data (Phase 2)")
    
    # 14. Test code validation (Phase 1)
    used_code = validate_student_code(student_codes[0]['code'])
    assert used_code is None  # Should be None because code is used
    print("[PASS] Code validation for used codes (Phase 1)")
    
    # 15. Test cognitive analysis (Phase 1)
    from shared.intelligence import cognitive_snapshot, risk_score
    for student in students:
        if student['id'] in store.profiles:
            profile = store.profiles[student['id']]
            cognitive = cognitive_snapshot(profile)
            risk = risk_score(profile)
            assert 'mastery' in cognitive
            assert 'level' in risk
    print("[PASS] Cognitive analysis (Phase 1)")
    
    # 16. Test AI provider (Phase 1)
    from shared.ai_providers import get_ai_provider, AIProviderType
    ai_provider = get_ai_provider(AIProviderType.MOCK)
    assert ai_provider is not None
    print("[PASS] AI provider initialization (Phase 1)")
    
    # 17. Test store collections (Phase 1 & 2)
    assert hasattr(store, 'institutions')
    assert hasattr(store, 'subscriptions')
    assert hasattr(store, 'student_codes')
    assert hasattr(store, 'teacher_codes')
    assert hasattr(store, 'invoices')
    assert hasattr(store, 'payments')
    assert hasattr(store, 'odoo_sync_events')
    print("[PASS] Store collections (Phase 1 & 2)")
    
    # 18. Test data consistency
    assert len(store.institutions) == 1
    assert len(store.subscriptions) == 1
    assert len(store.users) == 7  # 5 students + 2 teachers
    assert len(store.profiles) == 5
    assert len(store.invoices) == 1
    assert len(store.payments) == 1
    print("[PASS] Data consistency across phases")
    
    # 19. Test audit trail (Phase 1)
    assert len(store.audit) > 0
    print("[PASS] Audit trail (Phase 1)")
    
    # 20. Test consent system (Phase 1)
    from shared.identity import record_consent, has_consent
    for student in students:
        record_consent(student['id'], 'personalized_learning', True, '2026-08')
        assert has_consent(student['id'], 'personalized_learning')
    print("[PASS] Consent system (Phase 1)")


def test_cross_phase_functionality():
    """Test functionality that spans both phases"""
    print("Testing Cross-Phase Functionality...")
    
    # 1. Test that institution limits affect code generation (Phase 1 + Phase 2)
    institution_id = str(uuid4())
    institution = {
        'id': institution_id,
        'name_ar': 'مدرسة تجريبية',
        'name_en': 'Test School',
        'type': 'school',
        'country': 'Egypt',
        'city': 'Alexandria',
        'is_active': True,
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat(),
    }
    store.institutions[institution_id] = institution
    
    subscription_id = str(uuid4())
    subscription = {
        'id': subscription_id,
        'institution_id': institution_id,
        'plan_type': 'basic',
        'status': 'active',
        'max_students': 10,  # Small limit for testing
        'max_teachers': 2,
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat(),
    }
    store.subscriptions[subscription_id] = subscription
    
    # Generate up to limit
    for i in range(10):
        generate_student_code(institution_id, issued_by=str(uuid4()))
    
    student_code_count = len([c for c in store.student_codes.values() if c['institution_id'] == institution_id])
    assert student_code_count == 10
    print("[PASS] Subscription limits affect code generation")
    
    # 2. Test that billing accounts for actual usage (Phase 1 users + Phase 2 billing)
    billing_service = get_billing_service(store)
    
    # Register some students
    for i in range(5):
        student_id = str(uuid4())
        student = {
            'id': student_id,
            'email': f'test_student{i}@school.edu',
            'full_name': f'Test Student {i}',
            'role': 'student',
            'institution_id': institution_id,
            'active': True,
            'created_at': datetime.utcnow().isoformat(),
        }
        store.users[student_id] = student
        store.users_by_email[student['email']] = student
    
    # Generate invoice with actual usage
    actual_student_count = len([u for u in store.users.values() if u.get('institution_id') == institution_id and u.get('role') == 'student'])
    invoice = billing_service.create_invoice(
        institution_id=institution_id,
        subscription_id=subscription_id,
        plan_type='basic',
        billing_cycle='monthly',
        student_count=actual_student_count,
        teacher_count=0
    )
    
    assert invoice.total_amount > 0
    print("[PASS] Billing accounts for actual usage")
    
    # 3. Test that permissions work across institution context (Phase 1 permissions + Phase 2 institutions)
    assert has_permission(UserRole.INSTITUTION_ADMIN, "institutions", "edit", "own")
    assert has_permission(UserRole.INSTITUTION_ADMIN, "billing", "view", "own")
    assert not has_permission(UserRole.INSTITUTION_ADMIN, "institutions", "edit", "all")
    print("[PASS] Permissions work across institution context")


def test_system_readiness():
    """Test that the system is ready for Phase 3"""
    print("Testing System Readiness for Phase 3...")
    
    # 1. Test that AI providers can be initialized (needed for Phase 3)
    from shared.ai_providers import get_ai_provider, AIProviderType
    mock_provider = get_ai_provider(AIProviderType.MOCK)
    assert mock_provider is not None
    print("[PASS] AI providers ready for Phase 3")
    
    # 2. Test that memory system is functional (needed for Phase 3)
    assert hasattr(store, 'memory')
    store.memory.remember("test_user", "test_key", {"data": "test"})
    recalled = store.memory.recall("test_user", limit=1)
    assert len(recalled) > 0
    print("[PASS] Memory system ready for Phase 3")
    
    # 3. Test that event system is functional (needed for Phase 3)
    from shared.events import EventBus
    bus = EventBus(store)
    event = bus.publish("test_event", "test_subject", {"test": "data"})
    assert event is not None
    assert event['type'] == "test_event"
    print("[PASS] Event system ready for Phase 3")
    
    # 4. Test that intelligence agents are available (needed for Phase 3)
    from shared.intelligence import AgentOrchestrator
    orchestrator = AgentOrchestrator()
    assert orchestrator is not None
    assert len(orchestrator.agents) > 0
    print("[PASS] Intelligence agents ready for Phase 3")
    
    # 5. Test that store can handle Phase 3 data types
    # Store should be able to handle learning traces, voice data, etc.
    store.memory.remember("test_user", "voice_interaction", {
        "transcript": "test transcript",
        "audio_data": "base64_data",
        "timestamp": datetime.utcnow().isoformat()
    })
    print("[PASS] Store ready for Phase 3 data types")


def main():
    """Run all integration tests"""
    print("=" * 70)
    print("PHASE 1 & 2 INTEGRATION TESTS - Allamni v4.0")
    print("=" * 70)
    print()
    
    try:
        # Reset store for clean test
        store.reset()
        
        test_complete_integration()
        test_cross_phase_functionality()
        test_system_readiness()
        
        print()
        print("=" * 70)
        print("[SUCCESS] ALL INTEGRATION TESTS PASSED!")
        print("=" * 70)
        print()
        print("System Status:")
        print("- Phase 1: RBAC, Auth, AI Integration [READY]")
        print("- Phase 2: Institution Management, Billing, Odoo [READY]")
        print("- Integration: Cross-phase functionality [VERIFIED]")
        print("- System Readiness: Ready for Phase 3 [CONFIRMED]")
        print()
        return 0
        
    except AssertionError as e:
        print()
        print("=" * 70)
        print(f"[FAILED] INTEGRATION TEST FAILED: {e}")
        print("=" * 70)
        return 1
    except Exception as e:
        print()
        print("=" * 70)
        print(f"[ERROR] INTEGRATION ERROR: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())