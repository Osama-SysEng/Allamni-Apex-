"""
Manual test script for Phase 1 features
Run without pytest to verify basic functionality
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime, date, timedelta
from uuid import uuid4
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


def test_institution_models():
    """Test institution data models"""
    print("Testing Institution Models...")
    
    institution = Institution(
        id=uuid4(),
        name_ar="مدرسة المستقبل",
        name_en="Future School",
        type=InstitutionType.SCHOOL,
        sub_type="secondary",
        country="Egypt",
        city="Cairo",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    assert institution.type == InstitutionType.SCHOOL
    assert institution.name_ar == "مدرسة المستقبل"
    assert institution.is_active is True
    print("[PASS] Institution model test passed")


def test_subscription_models():
    """Test subscription data models"""
    print("Testing Subscription Models...")
    
    subscription = Subscription(
        id=uuid4(),
        institution_id=uuid4(),
        plan_type=SubscriptionPlan.PROFESSIONAL,
        status=SubscriptionStatus.TRIAL,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=30),
        max_students=500,
        max_teachers=50,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    assert subscription.plan_type == SubscriptionPlan.PROFESSIONAL
    assert subscription.status == SubscriptionStatus.TRIAL
    assert subscription.max_students == 500
    print("[PASS] Subscription model test passed")


def test_permission_system():
    """Test enhanced RBAC permission system"""
    print("Testing Permission System...")
    
    # Test student permissions
    assert has_permission(UserRole.STUDENT, "dashboard", "view", "own")
    assert has_permission(UserRole.STUDENT, "learning_content", "view", "own")
    assert not has_permission(UserRole.STUDENT, "students", "view", "institution")
    print("[PASS] Student permissions test passed")
    
    # Test teacher permissions
    assert has_permission(UserRole.TEACHER, "dashboard", "view", "institution")
    assert has_permission(UserRole.TEACHER, "learning_content", "create", "institution")
    assert not has_permission(UserRole.TEACHER, "institutions", "edit", "own")
    print("[PASS] Teacher permissions test passed")
    
    # Test institution admin permissions
    assert has_permission(UserRole.INSTITUTION_ADMIN, "institutions", "edit", "own")
    assert has_permission(UserRole.INSTITUTION_ADMIN, "codes", "create", "institution")
    assert not has_permission(UserRole.INSTITUTION_ADMIN, "institutions", "manage", "all")
    print("[PASS] Institution admin permissions test passed")
    
    # Test super admin permissions
    assert has_permission(UserRole.SUPER_ADMIN, "institutions", "manage", "all")
    assert has_permission(UserRole.SUPER_ADMIN, "billing", "manage", "all")
    print("[PASS] Super admin permissions test passed")


def test_code_system():
    """Test student and teacher code system"""
    print("Testing Code System...")
    
    # Test generating student code
    institution_id = str(uuid4())
    code_data = generate_student_code(
        institution_id=institution_id,
        class_id="Class-A",
        grade_level="Grade-10",
        academic_year="2024-2025",
        issued_by=str(uuid4())
    )
    
    assert code_data['institution_id'] == institution_id
    assert code_data['class_id'] == "Class-A"
    assert code_data['is_active'] is True
    assert code_data['student_id'] is None
    assert code_data['code'].startswith("STU-")
    print("[PASS] Student code generation test passed")
    
    # Test generating teacher code
    code_data = generate_teacher_code(
        institution_id=institution_id,
        department="Mathematics",
        subjects=["Algebra", "Geometry"],
        grade_levels=["Grade-9", "Grade-10"],
        issued_by=str(uuid4())
    )
    
    assert code_data['institution_id'] == institution_id
    assert code_data['department'] == "Mathematics"
    assert "Algebra" in code_data['subjects']
    assert code_data['code'].startswith("TCH-")
    print("[PASS] Teacher code generation test passed")
    
    # Test code validation
    student_code = generate_student_code(institution_id=institution_id)
    validated = validate_student_code(student_code['code'])
    assert validated is not None
    assert validated['code'] == student_code['code']
    print("[PASS] Student code validation test passed")
    
    teacher_code = generate_teacher_code(institution_id=institution_id)
    validated = validate_teacher_code(teacher_code['code'])
    assert validated is not None
    assert validated['code'] == teacher_code['code']
    print("[PASS] Teacher code validation test passed")
    
    # Test invalid code
    invalid = validate_student_code("INVALID-CODE")
    assert invalid is None
    print("[PASS] Invalid code rejection test passed")


def test_store_integration():
    """Test store integration with new collections"""
    print("Testing Store Integration...")
    
    # Test that store has new collections
    assert hasattr(store, 'institutions')
    assert hasattr(store, 'subscriptions')
    assert hasattr(store, 'student_codes')
    assert hasattr(store, 'teacher_codes')
    print("[PASS] Store collections test passed")
    
    # Test store reset
    institution_id = str(uuid4())
    store.institutions[institution_id] = {'id': institution_id, 'name': 'Test'}
    
    store.reset()
    
    assert len(store.institutions) == 0
    assert len(store.subscriptions) == 0
    print("[PASS] Store reset test passed")


def test_role_enums():
    """Test new role enums"""
    print("Testing Role Enums...")
    
    assert UserRole.STUDENT.value == "student"
    assert UserRole.TEACHER.value == "teacher"
    assert UserRole.PARENT.value == "parent"
    assert UserRole.INSTITUTION_ADMIN.value == "institution_admin"
    assert UserRole.SUPER_ADMIN.value == "super_admin"
    print("[PASS] User roles enum test passed")
    
    assert InstitutionType.SCHOOL.value == "school"
    assert InstitutionType.UNIVERSITY.value == "university"
    assert InstitutionType.TRAINING_CENTER.value == "training_center"
    print("[PASS] Institution types enum test passed")
    
    assert SubscriptionPlan.BASIC.value == "basic"
    assert SubscriptionPlan.PROFESSIONAL.value == "professional"
    assert SubscriptionPlan.ENTERPRISE.value == "enterprise"
    print("[PASS] Subscription plans enum test passed")


def main():
    """Run all tests"""
    print("=" * 60)
    print("PHASE 1 MANUAL TESTS - Allamni v4.0")
    print("=" * 60)
    print()
    
    try:
        test_institution_models()
        test_subscription_models()
        test_permission_system()
        test_code_system()
        test_store_integration()
        test_role_enums()
        
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