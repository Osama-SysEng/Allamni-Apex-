# Allamni v4.0 - Phase 2 API Documentation

## Overview
This document describes the new API endpoints and features introduced in Phase 2 of Allamni v4.0 development.

**Phase 2 Features:**
- Institution management service
- Code generation (student/teacher codes)
- Institution dashboard and analytics
- Student and teacher management
- Subscription management
- Billing and invoicing system
- Enhanced Odoo integration

---

## Base URL
```
http://localhost:8000/api
```

---

## Authentication
All endpoints require JWT authentication via `Authorization: Bearer <token>` header.

**Required Roles:**
- `institution_admin` - Institution management
- `super_admin` - Platform-level operations

---

## INSTITUTION SERVICE ENDPOINTS

### 1. Generate Student Codes
Generate student registration codes for an institution.

**Endpoint:** `POST /institution/codes/student/generate`

**Request Body:**
```json
{
  "institution_id": "inst_123456",
  "class_id": "Class-A",
  "grade_level": "Grade-10",
  "academic_year": "2024-2025",
  "quantity": 10
}
```

**Response:**
```json
{
  "institution_id": "inst_123456",
  "codes": [
    {
      "code": "STU-A1B2C3D4",
      "class_id": "Class-A",
      "grade_level": "Grade-10",
      "academic_year": "2024-2025",
      "expires_at": "2025-09-09T00:00:00",
      "created_at": "2026-09-09T10:30:00"
    }
  ],
  "quantity": 10,
  "generated_by": "user_abc123",
  "generated_at": "2026-09-09T10:30:00"
}
```

**Error Responses:**
- `403` - Subscription limit exceeded or insufficient permissions
- `404` - Institution not found

---

### 2. Generate Teacher Codes
Generate teacher registration codes for an institution.

**Endpoint:** `POST /institution/codes/teacher/generate`

**Request Body:**
```json
{
  "institution_id": "inst_123456",
  "department": "Mathematics",
  "subjects": ["Algebra", "Geometry"],
  "grade_levels": ["Grade-9", "Grade-10"],
  "quantity": 5
}
```

**Response:**
```json
{
  "institution_id": "inst_123456",
  "codes": [
    {
      "code": "TCH-E5F6G7H8",
      "department": "Mathematics",
      "subjects": ["Algebra", "Geometry"],
      "grade_levels": ["Grade-9", "Grade-10"],
      "expires_at": "2025-09-09T00:00:00",
      "created_at": "2026-09-09T10:30:00"
    }
  ],
  "quantity": 5,
  "generated_by": "user_abc123",
  "generated_at": "2026-09-09T10:30:00"
}
```

---

### 3. List Student Codes
List all student codes for an institution.

**Endpoint:** `GET /institution/codes/student/list?institution_id={institution_id}`

**Response:**
```json
{
  "institution_id": "inst_123456",
  "codes": [
    {
      "id": "code_abc123",
      "code": "STU-A1B2C3D4",
      "student_id": null,
      "class_id": "Class-A",
      "grade_level": "Grade-10",
      "is_active": true,
      "used_at": null,
      "expires_at": "2025-09-09T00:00:00",
      "created_at": "2026-09-09T10:30:00"
    }
  ],
  "total": 10,
  "active": 8,
  "used": 2
}
```

---

### 4. Revoke Student Code
Revoke an unused student code.

**Endpoint:** `DELETE /institution/codes/student/{code_id}`

**Response:**
```json
{
  "status": "revoked",
  "code_id": "code_abc123"
}
```

**Error Responses:**
- `400` - Cannot revoke code that has been used
- `404` - Code not found

---

### 5. Institution Dashboard
Get comprehensive institution dashboard with stats and usage.

**Endpoint:** `GET /institution/institutions/{institution_id}/dashboard`

**Response:**
```json
{
  "institution_id": "inst_123456",
  "institution": {
    "id": "inst_123456",
    "name_ar": "مدرسة المستقبل",
    "name_en": "Future School",
    "type": "school",
    "is_active": true
  },
  "subscription": {
    "id": "sub_789012",
    "plan_type": "professional",
    "status": "active",
    "max_students": 500,
    "max_teachers": 50
  },
  "overview": {
    "total_students": 250,
    "total_teachers": 15,
    "active_student_codes": 50,
    "active_teacher_codes": 10,
    "active_learning_profiles": 240,
    "at_risk_students": 12
  },
  "usage": {
    "students": 250,
    "teachers": 15,
    "student_codes": 50,
    "teacher_codes": 10
  },
  "limits": {
    "students": 500,
    "teachers": 50
  },
  "utilization": {
    "students_percent": 50.0,
    "teachers_percent": 30.0
  }
}
```

---

### 6. List Students
List all students in an institution with pagination.

**Endpoint:** `GET /institution/institutions/{institution_id}/students?skip=0&limit=50`

**Response:**
```json
{
  "institution_id": "inst_123456",
  "students": [
    {
      "id": "user_abc123",
      "email": "student1@school.edu",
      "full_name": "Omar Ali",
      "role": "student",
      "grade_level": "Grade-10",
      "has_profile": true,
      "skills_count": 4,
      "active": true
    }
  ],
  "total": 250,
  "skip": 0,
  "limit": 50
}
```

---

### 7. Student Detail
Get detailed information about a specific student.

**Endpoint:** `GET /institution/institutions/{institution_id}/students/{student_id}`

**Response:**
```json
{
  "student": {
    "id": "user_abc123",
    "email": "student1@school.edu",
    "full_name": "Omar Ali",
    "role": "student",
    "grade_level": "Grade-10",
    "active": true
  },
  "profile": {
    "student_id": "user_abc123",
    "goal_domain": "general",
    "skills": [...]
  },
  "cognitive": {
    "mastery": 0.45,
    "confidence": 0.52,
    "gap": 0.35,
    "stability": 0.48,
    "signals": ["large_learning_gap"]
  },
  "risk": {
    "score": 0.42,
    "level": "medium",
    "signals": ["large_learning_gap"]
  }
}
```

---

### 8. Subscription Details
Get current subscription details and usage.

**Endpoint:** `GET /institution/institutions/{institution_id}/subscription`

**Response:**
```json
{
  "subscription": {
    "id": "sub_789012",
    "institution_id": "inst_123456",
    "plan_type": "professional",
    "status": "active",
    "start_date": "2026-01-01",
    "end_date": "2026-12-31",
    "max_students": 500,
    "max_teachers": 50,
    "billing_cycle": "yearly"
  },
  "usage": {
    "students": 250,
    "teachers": 15
  },
  "remaining": {
    "students": 250,
    "teachers": 35
  }
}
```

---

### 9. Update Subscription
Update subscription plan or settings.

**Endpoint:** `PUT /institution/institutions/{institution_id}/subscription`

**Request Body:**
```json
{
  "plan_type": "enterprise",
  "auto_renew": true
}
```

**Response:**
```json
{
  "id": "sub_789012",
  "institution_id": "inst_123456",
  "plan_type": "enterprise",
  "status": "active",
  "max_students": null,
  "max_teachers": null,
  "auto_renew": true,
  "updated_at": "2026-09-09T10:30:00"
}
```

**Note:** Only super admin can change plan type. Institution admins can only change auto-renew.

---

### 10. Analytics Overview
Get analytics overview for institution.

**Endpoint:** `GET /institution/institutions/{institution_id}/analytics/overview?start_date=2026-01-01&end_date=2026-12-31`

**Response:**
```json
{
  "institution_id": "inst_123456",
  "period": {
    "start_date": "2026-01-01",
    "end_date": "2026-12-31"
  },
  "student_metrics": {
    "total_students": 250,
    "active_students": 240,
    "at_risk": 12,
    "on_track": 180,
    "advanced": 58
  },
  "learning_metrics": {
    "total_skills_tracked": 1000,
    "average_mastery": 0.52,
    "at_risk_rate": 4.8
  },
  "engagement_metrics": {
    "active_rate": 96.0
  }
}
```

---

## BILLING ENDPOINTS

### 1. Billing Summary
Get billing summary for institution.

**Endpoint:** `GET /institution/institutions/{institution_id}/billing/summary`

**Response:**
```json
{
  "total_invoices": 12,
  "total_invoiced": 15000.00,
  "total_paid": 12000.00,
  "total_pending": 3000.00,
  "outstanding_balance": 3000.00,
  "payment_rate": 80.0
}
```

---

### 2. List Invoices
List all invoices for an institution.

**Endpoint:** `GET /institution/institutions/{institution_id}/invoices?status=pending&skip=0&limit=50`

**Response:**
```json
{
  "institution_id": "inst_123456",
  "invoices": [
    {
      "id": "inv_abc123",
      "invoice_number": "INV-202609-1234",
      "status": "pending",
      "issue_date": "2026-09-01",
      "due_date": "2026-10-01",
      "currency": "USD",
      "total_amount": 299.00,
      "paid_date": null
    }
  ],
  "total": 12,
  "skip": 0,
  "limit": 50
}
```

---

### 3. Generate Invoice
Generate a new invoice for the institution.

**Endpoint:** `POST /institution/institutions/{institution_id}/invoices/generate?billing_cycle=monthly&due_days=30`

**Response:**
```json
{
  "invoice": {
    "id": "inv_xyz789",
    "invoice_number": "INV-202609-5678",
    "status": "pending",
    "issue_date": "2026-09-09",
    "due_date": "2026-10-09",
    "currency": "USD",
    "subtotal": 299.00,
    "tax_amount": 41.86,
    "discount_amount": 0.00,
    "total_amount": 340.86,
    "items": [
      {
        "description": "Professional Plan (monthly)",
        "quantity": 1,
        "unit_price": 299.00,
        "total": 299.00
      },
      {
        "description": "Student licenses (250 students)",
        "quantity": 250,
        "unit_price": 2.00,
        "total": 500.00
      }
    ]
  },
  "billing_summary": {
    "student_count": 250,
    "teacher_count": 15,
    "plan_type": "professional",
    "billing_cycle": "monthly"
  }
}
```

**Note:** Only super admin can generate invoices.

---

### 4. Invoice Details
Get detailed invoice information.

**Endpoint:** `GET /institution/invoices/{invoice_id}`

**Response:**
```json
{
  "invoice": {
    "id": "inv_xyz789",
    "invoice_number": "INV-202609-5678",
    "institution_id": "inst_123456",
    "subscription_id": "sub_789012",
    "status": "pending",
    "issue_date": "2026-09-09",
    "due_date": "2026-10-09",
    "currency": "USD",
    "subtotal": 799.00,
    "tax_amount": 111.86,
    "discount_amount": 0.00,
    "total_amount": 910.86,
    "items": [...]
  },
  "payments": [
    {
      "id": "pay_abc123",
      "amount": 500.00,
      "payment_method": "credit_card",
      "payment_date": "2026-09-15T10:30:00",
      "transaction_id": "txn_12345",
      "status": "completed"
    }
  ],
  "amount_paid": 500.00,
  "amount_remaining": 410.86
}
```

---

### 5. Record Payment
Record a payment for an invoice.

**Endpoint:** `POST /institution/invoices/{invoice_id}/payments`

**Request Body:**
```json
{
  "amount": 910.86,
  "payment_method": "credit_card",
  "transaction_id": "txn_67890",
  "notes": "Payment via Stripe"
}
```

**Response:**
```json
{
  "payment": {
    "id": "pay_def456",
    "invoice_id": "inv_xyz789",
    "amount": 910.86,
    "payment_method": "credit_card",
    "payment_date": "2026-09-15T10:30:00",
    "transaction_id": "txn_67890",
    "status": "completed",
    "notes": "Payment via Stripe"
  },
  "invoice_status": "paid"
}
```

**Note:** Only super admin can record payments.

---

### 6. Update Invoice Status
Update invoice status manually.

**Endpoint:** `PUT /institution/invoices/{invoice_id}/status?status=paid`

**Response:**
```json
{
  "id": "inv_xyz789",
  "invoice_number": "INV-202609-5678",
  "status": "paid",
  "updated_at": "2026-09-15T10:30:00"
}
```

**Note:** Only super admin can update invoice status.

---

## ODOO INTEGRATION ENDPOINTS

### 1. Sync Entity
Sync a single entity with Odoo.

**Endpoint:** `POST /integration/odoo/sync/entity`

**Request Body:**
```json
{
  "entity_type": "student",
  "entity_id": "user_abc123",
  "direction": "bidirectional",
  "force_sync": false
}
```

**Response:**
```json
{
  "id": "sync_abc123",
  "entity_type": "student",
  "entity_id": "user_abc123",
  "direction": "bidirectional",
  "status": "completed",
  "created_at": "2026-09-09T10:30:00",
  "processed_at": "2026-09-09T10:30:05",
  "odoo_external_id": "odoo_student_user_abc123"
}
```

**Entity Types:** `student`, `teacher`, `institution`, `subscription`, `course`, `payment`

**Sync Directions:** `allamni_to_odoo`, `odoo_to_allamni`, `bidirectional`

---

### 2. Bulk Sync
Bulk sync entities for an institution.

**Endpoint:** `POST /integration/odoo/sync/bulk`

**Request Body:**
```json
{
  "entity_type": "student",
  "institution_id": "inst_123456",
  "direction": "bidirectional",
  "date_range": {
    "start_date": "2026-01-01",
    "end_date": "2026-12-31"
  }
}
```

**Response:**
```json
{
  "total": 250,
  "successful": 245,
  "failed": 5,
  "results": [
    {
      "entity_id": "user_abc123",
      "status": "completed",
      "odoo_external_id": "odoo_student_user_abc123"
    },
    {
      "entity_id": "user_def456",
      "status": "failed",
      "error": "Connection timeout"
    }
  ]
}
```

---

### 3. Get Odoo Config
Get Odoo configuration for an institution.

**Endpoint:** `GET /integration/odoo/config?institution_id={institution_id}`

**Response:**
```json
{
  "enabled": true,
  "url": "https://odoo.example.com",
  "db": "allamni_production",
  "username": "allamni_user",
  "last_sync": "2026-09-08T15:30:00",
  "sync_frequency": "daily"
}
```

---

### 4. Update Odoo Config
Update Odoo configuration for an institution.

**Endpoint:** `PUT /integration/odoo/config?institution_id={institution_id}`

**Request Body:**
```json
{
  "url": "https://odoo.example.com",
  "db": "allamni_production",
  "username": "allamni_user",
  "api_key": "odoo_api_key_here",
  "enabled": true
}
```

**Response:**
```json
{
  "status": "updated",
  "institution_id": "inst_123456"
}
```

---

### 5. Sync History
Get sync history for an institution.

**Endpoint:** `GET /integration/odoo/sync/history?institution_id={institution_id}&entity_type=student&limit=50`

**Response:**
```json
{
  "institution_id": "inst_123456",
  "history": [
    {
      "id": "sync_abc123",
      "entity_type": "student",
      "entity_id": "user_abc123",
      "direction": "bidirectional",
      "status": "completed",
      "created_at": "2026-09-09T10:30:00",
      "processed_at": "2026-09-09T10:30:05"
    }
  ],
  "total": 150,
  "limit": 50
}
```

---

### 6. Trigger Sync
Trigger immediate sync for an institution.

**Endpoint:** `POST /integration/odoo/sync/trigger?institution_id={institution_id}&entity_type=student`

**Response:**
```json
{
  "total": 250,
  "successful": 245,
  "failed": 5,
  "results": [...]
}
```

---

## PRICING PLANS

### Basic Plan
- **Monthly:** $99
- **Yearly:** $990 (20% discount)
- **Students:** Up to 100 included
- **Teachers:** Up to 10 included
- **Additional Students:** $0
- **Additional Teachers:** $0

### Professional Plan
- **Monthly:** $299
- **Yearly:** $2,990 (20% discount)
- **Students:** Up to 500 included
- **Teachers:** Up to 50 included
- **Additional Students:** $2 per student
- **Additional Teachers:** $10 per teacher

### Enterprise Plan
- **Monthly:** $999
- **Yearly:** $9,990 (20% discount)
- **Students:** Unlimited
- **Teachers:** Unlimited
- **Additional Students:** $1 per student
- **Additional Teachers:** $5 per teacher

### Additional Costs
- **Tax:** 14% VAT (example for Egypt)
- **Discounts:** 20% for yearly billing
- **Payment Methods:** Credit card, bank transfer, cash, check

---

## ERROR RESPONSES

### Standard Error Format
```json
{
  "detail": "Error message description"
}
```

### Common HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `500` - Internal Server Error

---

## ENVIRONMENT VARIABLES

### Required for Production
```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname

# Institution Service
INSTITUTION_URL=http://institution-service:8000

# Odoo Integration
ODOO_URL=https://odoo.example.com
ODOO_DB=allamni_production
ODOO_USERNAME=allamni_user
ODOO_API_KEY=your_odoo_api_key
```

---

## TESTING

### Manual Test Script
Run Phase 2 tests:
```bash
cd backend
python tests/manual_test_phase2.py
```

### Test Coverage
- ✅ Code generation (student/teacher)
- ✅ Billing service functionality
- ✅ Pricing plan calculations
- ✅ Invoice creation and management
- ✅ Payment recording
- ✅ Invoice status updates
- ✅ Billing summaries
- ✅ Store integration
- ✅ Payment methods and statuses

---

## SERVICE ARCHITECTURE

### New Service: Institution Service
- **Port:** 8005
- **Purpose:** Institution management, code generation, billing
- **Dependencies:** PostgreSQL, Redis

### Updated Services
- **API Gateway:** Added institution service routing
- **Integration Service:** Enhanced Odoo integration
- **Docker Compose:** Added institution service container

---

## NEXT PHASES

### Phase 3 - Enhanced AI Features
- Advanced Gemini integration
- Self-learning pipeline
- Arabic dialect NLP
- Voice input implementation

### Phase 4 - Frontend Development
- Flutter project setup
- Institution admin dashboard
- Student management UI
- Billing and invoice management

### Phase 5 - Production Deployment
- Puter.com deployment
- Security scanning
- Performance optimization
- Monitoring setup

---

## SUPPORT

For technical support or questions about Phase 2 implementation:
- Review the test cases in `backend/tests/manual_test_phase2.py`
- Check the implementation in `backend/services/institution-service/`
- Consult the billing module in `backend/shared/billing.py`
- Review Odoo integration in `backend/services/integration-service/`

---

*Document Version: 1.0*
*Last Updated: 2026-09-09*
*Phase: 2 Complete*