"""
Permission Matrix System for Allamni v4.0
Defines what each role can do in the system
"""
from typing import List, Dict, Set
from shared.models import UserRole, Permission

# Resource definitions
RESOURCES = {
    "dashboard": "User dashboard access",
    "profile": "User profile management",
    "learning_content": "Learning content access",
    "assessments": "Assessment creation and taking",
    "roadmap": "Learning roadmap access",
    "analytics": "Analytics and reports",
    "students": "Student data access",
    "teachers": "Teacher data access",
    "institutions": "Institution management",
    "subscriptions": "Subscription management",
    "billing": "Billing and payments",
    "content_management": "Content creation and editing",
    "codes": "Student/teacher code generation",
    "parent_data": "Parent data access",
    "ai_companion": "AI companion access",
    "notifications": "Notification management",
    "reports": "Report generation and export",
    "settings": "System settings",
    "integration": "External integrations (Odoo, etc.)",
    "audit": "Audit trail access",
}

# Action definitions
ACTIONS = {
    "view": "Read-only access",
    "create": "Create new resources",
    "edit": "Edit existing resources",
    "delete": "Delete resources",
    "manage": "Full management access",
    "export": "Export data",
    "approve": "Approve content/actions",
    "assign": "Assign resources to users",
}

# Scope definitions
SCOPES = {
    "own": "Only own data",
    "institution": "Data within own institution",
    "all": "All data across platform",
}

# Permission Matrix
PERMISSION_MATRIX: Dict[UserRole, List[Permission]] = {
    UserRole.STUDENT: [
        Permission(resource="dashboard", action="view", scope="own"),
        Permission(resource="profile", action="edit", scope="own"),
        Permission(resource="learning_content", action="view", scope="own"),
        Permission(resource="assessments", action="view", scope="own"),
        Permission(resource="assessments", action="create", scope="own"),  # Take assessments
        Permission(resource="roadmap", action="view", scope="own"),
        Permission(resource="analytics", action="view", scope="own"),
        Permission(resource="ai_companion", action="view", scope="own"),
        Permission(resource="notifications", action="view", scope="own"),
    ],
    
    UserRole.TEACHER: [
        Permission(resource="dashboard", action="view", scope="institution"),
        Permission(resource="profile", action="edit", scope="own"),
        Permission(resource="learning_content", action="view", scope="institution"),
        Permission(resource="learning_content", action="create", scope="institution"),
        Permission(resource="learning_content", action="edit", scope="institution"),
        Permission(resource="assessments", action="view", scope="institution"),
        Permission(resource="assessments", action="create", scope="institution"),
        Permission(resource="assessments", action="edit", scope="institution"),
        Permission(resource="roadmap", action="view", scope="institution"),
        Permission(resource="analytics", action="view", scope="institution"),
        Permission(resource="students", action="view", scope="institution"),
        Permission(resource="students", action="edit", scope="institution"),  # Assignments, grades
        Permission(resource="ai_companion", action="view", scope="own"),
        Permission(resource="notifications", action="view", scope="institution"),
        Permission(resource="notifications", action="create", scope="institution"),
        Permission(resource="reports", action="view", scope="institution"),
        Permission(resource="reports", action="export", scope="institution"),
    ],
    
    UserRole.PARENT: [
        Permission(resource="dashboard", action="view", scope="own"),
        Permission(resource="profile", action="edit", scope="own"),
        Permission(resource="students", action="view", scope="own"),  # Own children only
        Permission(resource="analytics", action="view", scope="own"),
        Permission(resource="notifications", action="view", scope="own"),
        Permission(resource="reports", action="view", scope="own"),
    ],
    
    UserRole.INSTITUTION_ADMIN: [
        Permission(resource="dashboard", action="view", scope="institution"),
        Permission(resource="profile", action="edit", scope="own"),
        Permission(resource="learning_content", action="view", scope="institution"),
        Permission(resource="learning_content", action="manage", scope="institution"),
        Permission(resource="assessments", action="manage", scope="institution"),
        Permission(resource="roadmap", action="view", scope="institution"),
        Permission(resource="analytics", action="view", scope="institution"),
        Permission(resource="students", action="view", scope="institution"),
        Permission(resource="students", action="manage", scope="institution"),
        Permission(resource="teachers", action="view", scope="institution"),
        Permission(resource="teachers", action="manage", scope="institution"),
        Permission(resource="institutions", action="edit", scope="own"),
        Permission(resource="subscriptions", action="view", scope="own"),
        Permission(resource="subscriptions", action="edit", scope="own"),
        Permission(resource="billing", action="view", scope="own"),
        Permission(resource="content_management", action="manage", scope="institution"),
        Permission(resource="codes", action="create", scope="institution"),
        Permission(resource="parent_data", action="view", scope="institution"),
        Permission(resource="ai_companion", action="view", scope="own"),
        Permission(resource="notifications", action="manage", scope="institution"),
        Permission(resource="reports", action="view", scope="institution"),
        Permission(resource="reports", action="export", scope="institution"),
        Permission(resource="settings", action="edit", scope="institution"),
        Permission(resource="integration", action="view", scope="institution"),
        Permission(resource="audit", action="view", scope="institution"),
    ],
    
    UserRole.SUPER_ADMIN: [
        Permission(resource="dashboard", action="view", scope="all"),
        Permission(resource="profile", action="edit", scope="own"),
        Permission(resource="learning_content", action="manage", scope="all"),
        Permission(resource="assessments", action="manage", scope="all"),
        Permission(resource="roadmap", action="view", scope="all"),
        Permission(resource="analytics", action="view", scope="all"),
        Permission(resource="students", action="manage", scope="all"),
        Permission(resource="teachers", action="manage", scope="all"),
        Permission(resource="institutions", action="manage", scope="all"),
        Permission(resource="subscriptions", action="manage", scope="all"),
        Permission(resource="billing", action="manage", scope="all"),
        Permission(resource="content_management", action="manage", scope="all"),
        Permission(resource="codes", action="create", scope="all"),
        Permission(resource="parent_data", action="manage", scope="all"),
        Permission(resource="ai_companion", action="view", scope="own"),
        Permission(resource="notifications", action="manage", scope="all"),
        Permission(resource="reports", action="manage", scope="all"),
        Permission(resource="settings", action="manage", scope="all"),
        Permission(resource="integration", action="manage", scope="all"),
        Permission(resource="audit", action="view", scope="all"),
    ],
}

def get_permissions_for_role(role: UserRole) -> List[Permission]:
    """Get all permissions for a given role"""
    return PERMISSION_MATRIX.get(role, [])

def has_permission(role: UserRole, resource: str, action: str, scope: str = "own") -> bool:
    """Check if a role has a specific permission"""
    # `manage` implies all CRUD actions on the resource.
    _IMPLIED_BY_MANAGE = {"create", "read", "edit", "delete", "view", "manage"}
    permissions = get_permissions_for_role(role)
    for perm in permissions:
        if perm.resource == resource and (perm.action == action or (perm.action == "manage" and action in _IMPLIED_BY_MANAGE)):
            # Check scope hierarchy
            if scope == "own":
                return True
            elif scope == "institution" and perm.scope in ["institution", "all"]:
                return True
            elif scope == "all" and perm.scope == "all":
                return True
    return False

def get_allowed_resources(role: UserRole) -> Set[str]:
    """Get all resources a role can access"""
    permissions = get_permissions_for_role(role)
    return {perm.resource for perm in permissions}

def get_allowed_actions(role: UserRole, resource: str) -> Set[str]:
    """Get all actions a role can perform on a specific resource"""
    permissions = get_permissions_for_role(role)
    return {perm.action for perm in permissions if perm.resource == resource}