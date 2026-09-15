"""
Phase 1 Tests - Institutions, Codes, and Enhanced RBAC
Testing v4.0 new features
"""
import pytest
from datetime import datetime, date, timedelta
from uuid import uuid4
from shared.models import (
    UserRole, InstitutionType, SubscriptionPlan, SubscriptionStatus,
    Institution, Subscription, StudentCode, TeacherCode
)
from shared.permissions import has_permission, get_permissions_for_role
from shared.identity import (
    validate_student_code, validate_teacher_code,
    generate_student_code, generate_teacher_code
)
from shared.store import store


class TestInstitutionModels:
    """Test institution data models"""
    
    def test_institution_creation(self):
        """Test creating an institution object"""
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
    
    def test_subscription_creation(self):
        """Test creating a subscription object"""
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


class TestPermissionSystem:
    """Test enhanced RBAC permission system"""
    
    def test_student_permissions(self):
        """Test student role permissions"""
        assert has_permission(UserRole.STUDENT, "dashboard", "view", "own")
        assert has_permission(UserRole.STUDENT, "learning_content", "view", "own")
        assert has_permission(UserRole.STUDENT, "assessments", "create", "own")
        assert not has_permission(UserRole.STUDENT, "students", "view", "institution")
        assert not has_permission(UserRole.STUDENT, "content_management", "create", "own")
    
    def test_teacher_permissions(self):
        """Test teacher role permissions"""
        assert has_permission(UserRole.TEACHER, "dashboard", "view", "institution")
        assert has_permission(UserRole.TEACHER, "learning_content", "create", "institution")
        assert has_permission(UserRole.TEACHER, "students", "view", "institution")
        assert has_permission(UserRole.TEACHER, "assessments", "create", "institution")
        assert not has_permission(UserRole.TEACHER, "institutions", "edit", "own")
        assert not has_permission(UserRole.TEACHER, "billing", "view", "own")
    
    def test_institution_admin_permissions(self):
        """Test institution admin role permissions"""
        assert has_permission(UserRole.INSTITUTION_ADMIN, "institutions", "edit", "own")
        assert has_permission(UserRole.INSTITUTION_ADMIN, "subscriptions", "view", "own")
        assert has_permission(UserRole.INSTITUTION_ADMIN, "codes", "create", "institution")
        assert has_permission(UserRole.INSTITUTION_ADMIN, "students", "manage", "institution")
        assert not has_permission(UserRole.INSTITUTION_ADMIN, "institutions", "manage", "all")
    
    def test_super_admin_permissions(self):
        """Test super admin role permissions"""
        assert has_permission(UserRole.SUPER_ADMIN, "institutions", "manage", "all")
        assert has_permission(UserRole.SUPER_ADMIN, "subscriptions", "manage", "all")
        assert has_permission(UserRole.SUPER_ADMIN, "billing", "manage", "all")
        assert has_permission(UserRole.SUPER_ADMIN, "settings", "manage", "all")
    
    def test_permission_hierarchy(self):
        """Test permission scope hierarchy"""
        # own scope should work for own
        assert has_permission(UserRole.TEACHER, "students", "view", "own")
        
        # institution scope should work for institution or all
        assert has_permission(UserRole.TEACHER, "students", "view", "institution")
        assert not has_permission(UserRole.TEACHER, "institutions", "edit", "all")
        
        # all scope should only work for super admin
        assert has_permission(UserRole.SUPER_ADMIN, "institutions", "edit", "all")
        assert not has_permission(UserRole.INSTITUTION_ADMIN, "institutions", "edit", "all")


class TestCodeSystem:
    """Test student and teacher code system"""
    
    def test_generate_student_code(self):
        """Test generating a student code"""
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
        assert code_data['grade_level'] == "Grade-10"
        assert code_data['is_active'] is True
        assert code_data['student_id'] is None
        assert code_data['code'].startswith("STU-")
    
    def test_generate_teacher_code(self):
        """Test generating a teacher code"""
        institution_id = str(uuid4())
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
        assert code_data['is_active'] is True
        assert code_data['teacher_id'] is None
        assert code_data['code'].startswith("TCH-")
    
    def test_validate_student_code(self):
        """Test validating a student code"""
        institution_id = str(uuid4())
        code_data = generate_student_code(institution_id=institution_id)
        
        # Valid code
        validated = validate_student_code(code_data['code'])
        assert validated is not None
        assert validated['code'] == code_data['code']
        
        # Invalid code
        invalid = validate_student_code("INVALID-CODE")
        assert invalid is None
    
    def test_validate_teacher_code(self):
        """Test validating a teacher code"""
        institution_id = str(uuid4())
        code_data = generate_teacher_code(institution_id=institution_id)
        
        # Valid code
        validated = validate_teacher_code(code_data['code'])
        assert validated is not None
        assert validated['code'] == code_data['code']
        
        # Invalid code
        invalid = validate_teacher_code("INVALID-CODE")
        assert invalid is None
    
    def test_code_expiration(self):
        """Test code expiration validation"""
        institution_id = str(uuid4())
        
        # Create expired code
        code_data = generate_student_code(institution_id=institution_id)
        code_data['expires_at'] = (datetime.utcnow() - timedelta(days=1)).isoformat()
        
        # Should not validate expired code
        validated = validate_student_code(code_data['code'])
        assert validated is None
    
    def test_code_usage_limit(self):
        """Test that codes can only be used once"""
        institution_id = str(uuid4())
        code_data = generate_student_code(institution_id=institution_id)
        
        # Mark as used
        code_data['student_id'] = str(uuid4())
        
        # Should not validate used code
        validated = validate_student_code(code_data['code'])
        assert validated is None


class TestStoreIntegration:
    """Test store integration with new collections"""
    
    def test_store_has_new_collections(self):
        """Test that store has new v4.0 collections"""
        assert hasattr(store, 'institutions')
        assert hasattr(store, 'subscriptions')
        assert hasattr(store, 'student_codes')
        assert hasattr(store, 'teacher_codes')
        assert hasattr(store, 'institution_settings')
        assert hasattr(store, 'parent_student_relationships')
    
    def test_store_reset_clears_new_collections(self):
        """Test that store reset clears new collections"""
        # Add some data
        institution_id = str(uuid4())
        store.institutions[institution_id] = {'id': institution_id, 'name': 'Test'}
        
        # Reset
        store.reset()
        
        # Should be cleared
        assert len(store.institutions) == 0
        assert len(store.subscriptions) == 0
        assert len(store.student_codes) == 0
        assert len(store.teacher_codes) == 0


class TestRoleEnums:
    """Test new role enums"""
    
    def test_user_roles(self):
        """Test all user roles are defined"""
        assert UserRole.STUDENT.value == "student"
        assert UserRole.TEACHER.value == "teacher"
        assert UserRole.PARENT.value == "parent"
        assert UserRole.INSTITUTION_ADMIN.value == "institution_admin"
        assert UserRole.SUPER_ADMIN.value == "super_admin"
    
    def test_institution_types(self):
        """Test all institution types are defined"""
        assert InstitutionType.SCHOOL.value == "school"
        assert InstitutionType.UNIVERSITY.value == "university"
        assert InstitutionType.TRAINING_CENTER.value == "training_center"
    
    def test_subscription_plans(self):
        """Test all subscription plans are defined"""
        assert SubscriptionPlan.BASIC.value == "basic"
        assert SubscriptionPlan.PROFESSIONAL.value == "professional"
        assert SubscriptionPlan.ENTERPRISE.value == "enterprise"
    
    def test_subscription_status(self):
        """Test all subscription statuses are defined"""
        assert SubscriptionStatus.TRIAL.value == "trial"
        assert SubscriptionStatus.ACTIVE.value == "active"
        assert SubscriptionStatus.SUSPENDED.value == "suspended"
        assert SubscriptionStatus.CANCELLED.value == "cancelled"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])