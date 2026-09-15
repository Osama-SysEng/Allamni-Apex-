# Allamni v4.0 - Phase 1 API Documentation

## Overview
This document describes the new API endpoints and features introduced in Phase 1 of Allamni v4.0 development.

**Phase 1 Features:**
- Institution registration and subscription management
- Enhanced RBAC with 5 user roles
- Student and teacher code-based registration
- Gemini AI integration for AI Companion
- Permission matrix system

---

## Base URL
```
http://localhost:8000/api
```

---

## Authentication
All endpoints require JWT authentication via `Authorization: Bearer <token>` header.

**Token Types:**
- Access Token: 15-minute validity
- Refresh Token: 7-day validity

---

## New User Roles

### Role Hierarchy
1. **SUPER_ADMIN** - Platform-level management
2. **INSTITUTION_ADMIN** - Institution management
3. **TEACHER** - Classroom management
4. **PARENT** - Child monitoring
5. **STUDENT** - Learning access

### Permission Scopes
- **own** - User's own data only
- **institution** - Data within user's institution
- **all** - All platform data (super admin only)

---

## AUTH SERVICE ENDPOINTS

### 1. Institution Registration
Register a new institution with subscription.

**Endpoint:** `POST /auth/register/institution`

**Request Body:**
```json
{
  "name_ar": "مدرسة المستقبل",
  "name_en": "Future School",
  "type": "school",
  "sub_type": "secondary",
  "country": "Egypt",
  "city": "Cairo",
  "address": "123 Education Street",
  "phone": "+201234567890",
  "email": "contact@futureschool.edu",
  "website": "https://futureschool.edu",
  "admin_name": "Ahmed Mohamed",
  "admin_email": "admin@futureschool.edu",
  "admin_phone": "+201234567891",
  "plan_type": "professional"
}
```

**Institution Types:** `school`, `university`, `training_center`

**Subscription Plans:** `basic`, `professional`, `enterprise`

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "session_id": "session_abc123",
  "user": {
    "id": "user_xyz789",
    "email": "admin@futureschool.edu",
    "full_name": "Ahmed Mohamed",
    "role": "institution_admin"
  },
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
    "status": "trial",
    "start_date": "2026-09-09",
    "end_date": "2026-10-09",
    "max_students": 500,
    "max_teachers": 50
  },
  "requires_password_change": true
}
```

---

### 2. Student Code Registration
Register a student using institution-issued code.

**Endpoint:** `POST /auth/register/student-code`

**Request Body:**
```json
{
  "code": "STU-A1B2C3D4",
  "full_name": "Omar Ali",
  "email": "omar@student.edu",
  "phone": "+201234567892",
  "password": "SecurePass123!",
  "date_of_birth": "2010-05-15",
  "guardian_contact": "+201234567893"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "session_id": "session_def456",
  "user": {
    "id": "user_abc123",
    "email": "omar@student.edu",
    "full_name": "Omar Ali",
    "role": "student"
  },
  "consent_required": true,
  "institution_id": "inst_123456"
}
```

**Error Responses:**
- `404` - Invalid or inactive code
- `409` - Code already used or email already registered
- `400` - Code expired

---

### 3. Teacher Code Registration
Register a teacher using institution-issued code.

**Endpoint:** `POST /auth/register/teacher-code`

**Request Body:**
```json
{
  "code": "TCH-E5F6G7H8",
  "full_name": "Dr. Fatima Hassan",
  "email": "fatima@futureschool.edu",
  "phone": "+201234567894",
  "password": "SecurePass123!",
  "specialization": "Mathematics",
  "qualifications": "PhD in Mathematics Education"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "session_id": "session_ghi789",
  "user": {
    "id": "user_def456",
    "email": "fatima@futureschool.edu",
    "full_name": "Dr. Fatima Hassan",
    "role": "teacher"
  },
  "institution_id": "inst_123456"
}
```

---

### 4. Self Registration
Register independent learners without institution affiliation.

**Endpoint:** `POST /auth/register/self`

**Request Body:**
```json
{
  "full_name": "Sara Ahmed",
  "email": "sara@gmail.com",
  "phone": "+201234567895",
  "password": "SecurePass123!",
  "role": "student",
  "level": "university",
  "goals": ["learn programming", "career change"]
}
```

**Roles:** `student`, `teacher`, `parent`

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "session_id": "session_jkl012",
  "user": {
    "id": "user_ghi789",
    "email": "sara@gmail.com",
    "full_name": "Sara Ahmed",
    "role": "student"
  },
  "consent_required": true
}
```

---

## AI SERVICE ENDPOINTS

### 1. AI Companion Chat
Chat with AI Companion supporting Arabic dialects.

**Endpoint:** `POST /ai/students/chat`

**Request Body:**
```json
{
  "student_id": "user_abc123",
  "message": "شرح لي مفهوم البرمجة الكائنية",
  "conversation_history": [
    {
      "role": "user",
      "content": "مرحباً"
    },
    {
      "role": "assistant",
      "content": "مرحباً بك! كيف يمكنني مساعدتك؟"
    }
  ],
  "dialect": "egyptian"
}
```

**Dialects:** `modern_standard`, `egyptian`, `gulf`, `levantine`

**Response:**
```json
{
  "content": "البرمجة الكائنية هي طريقة في البرمجة بننظم فيها الكود على شكل كائنات...",
  "model_used": "gemini-1.5-pro",
  "tokens_used": 450,
  "cost": 0.0023,
  "latency_ms": 1250,
  "metadata": {
    "provider": "gemini",
    "message_count": 3
  }
}
```

---

### 2. AI Content Explanation
Get AI explanation for highlighted text in learning content.

**Endpoint:** `POST /ai/students/explain`

**Request Body:**
```json
{
  "student_id": "user_abc123",
  "text": "الوراثة في البرمجة الكائنية تسمح للكلاس الجديد بالاستفادة من خصائص الكلاس القديم",
  "context": {
    "subject": "Programming",
    "topic": "OOP Inheritance"
  }
}
```

**Response:**
```json
{
  "content": "الوراثة هي مفهوم أساسي في البرمجة الكائنية. تخيلها مثل الوراثة في الحياة الواقعية...",
  "model_used": "gemini-1.5-pro",
  "tokens_used": 320,
  "latency_ms": 890,
  "metadata": {
    "provider": "gemini"
  }
}
```

---

### 3. Voice Input Transcription
Transcribe voice input to text (placeholder).

**Endpoint:** `POST /ai/students/voice-transcribe`

**Request Body:**
```json
{
  "student_id": "user_abc123",
  "audio_data": "base64_encoded_audio_data",
  "language": "ar"
}
```

**Response:**
```json
{
  "transcribed_text": "النص المقترح من الصوت (خاصية قيد التطوير)",
  "confidence": 0.95,
  "language": "ar",
  "status": "placeholder"
}
```

---

### 4. Teacher AI Assistant
Get AI assistance for lesson planning and content creation.

**Endpoint:** `POST /ai/teachers/assistant`

**Request Body:**
```json
{
  "student_id": "user_def456",
  "prompt": "Generate 10 quiz questions about algebraic equations",
  "context": {
    "grade_level": "Grade 10",
    "difficulty": "medium",
    "topic": "Algebra"
  }
}
```

**Response:**
```json
{
  "content": "Here are 10 quiz questions about algebraic equations:\n1. Solve for x: 2x + 5 = 15\n...",
  "model_used": "gemini-1.5-pro",
  "tokens_used": 890,
  "latency_ms": 2100,
  "metadata": {
    "provider": "gemini"
  }
}
```

---

### 5. Institution AI Insights
Get AI-powered insights for institution administrators.

**Endpoint:** `POST /ai/institutions/insights`

**Request Body:**
```json
{
  "student_id": "user_xyz789"
}
```

**Response:**
```json
{
  "content": "Institution Analysis:\n- Total Students: 450\n- Total Teachers: 25\n- Risk Students: 12\n- Recommendations:...",
  "model_used": "gemini-1.5-pro",
  "tokens_used": 650,
  "latency_ms": 1800,
  "metadata": {
    "provider": "gemini"
  }
}
```

---

## PERMISSION SYSTEM

### Permission Matrix

#### Student Permissions
- ✅ `dashboard:view:own`
- ✅ `profile:edit:own`
- ✅ `learning_content:view:own`
- ✅ `assessments:view:own`
- ✅ `assessments:create:own`
- ✅ `roadmap:view:own`
- ✅ `analytics:view:own`
- ✅ `ai_companion:view:own`
- ✅ `notifications:view:own`

#### Teacher Permissions
- ✅ `dashboard:view:institution`
- ✅ `profile:edit:own`
- ✅ `learning_content:view:institution`
- ✅ `learning_content:create:institution`
- ✅ `learning_content:edit:institution`
- ✅ `assessments:view:institution`
- ✅ `assessments:create:institution`
- ✅ `assessments:edit:institution`
- ✅ `roadmap:view:institution`
- ✅ `analytics:view:institution`
- ✅ `students:view:institution`
- ✅ `students:edit:institution`
- ✅ `ai_companion:view:own`
- ✅ `notifications:view:institution`
- ✅ `notifications:create:institution`
- ✅ `reports:view:institution`
- ✅ `reports:export:institution`

#### Institution Admin Permissions
- ✅ `dashboard:view:institution`
- ✅ `profile:edit:own`
- ✅ `learning_content:manage:institution`
- ✅ `assessments:manage:institution`
- ✅ `roadmap:view:institution`
- ✅ `analytics:view:institution`
- ✅ `students:manage:institution`
- ✅ `teachers:manage:institution`
- ✅ `institutions:edit:own`
- ✅ `subscriptions:view:own`
- ✅ `subscriptions:edit:own`
- ✅ `billing:view:own`
- ✅ `content_management:manage:institution`
- ✅ `codes:create:institution`
- ✅ `parent_data:view:institution`
- ✅ `ai_companion:view:own`
- ✅ `notifications:manage:institution`
- ✅ `reports:view:institution`
- ✅ `reports:export:institution`
- ✅ `settings:edit:institution`
- ✅ `integration:view:institution`
- ✅ `audit:view:institution`

#### Super Admin Permissions
- ✅ All permissions with `all` scope
- Full platform management access

---

## CODE GENERATION (Admin Endpoints)

### Generate Student Code
*Endpoint to be added in Phase 2*

### Generate Teacher Code
*Endpoint to be added in Phase 2*

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
REDIS_URL=redis://:password@host:6379/0

# AI Provider
AI_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-1.5-pro

# Security
JWT_SECRET=your_jwt_secret_key
JWT_ACCESS_MINUTES=15
JWT_REFRESH_DAYS=7

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://app.puter.site
```

### Development Defaults
```env
AI_PROVIDER=mock
JWT_SECRET=dev-secret-key
```

---

## TESTING

### Manual Test Script
Run Phase 1 tests:
```bash
cd backend
python tests/manual_test_phase1.py
```

### Test Coverage
- ✅ Institution models
- ✅ Subscription models
- ✅ Permission system (all roles)
- ✅ Code generation and validation
- ✅ Store integration
- ✅ Role enums

---

## NEXT PHASES

### Phase 2 - Institution Management
- Code generation endpoints
- Institution dashboard
- Subscription management
- Billing integration

### Phase 3 - Enhanced AI Features
- Advanced Gemini integration
- Self-learning pipeline
- Arabic dialect NLP
- Voice input implementation

### Phase 4 - Frontend Development
- Flutter project setup
- Student dashboard
- Teacher dashboard
- Institution admin dashboard

### Phase 5 - Production Deployment
- Puter.com deployment
- Security scanning
- Performance optimization
- Monitoring setup

---

## SUPPORT

For technical support or questions about Phase 1 implementation:
- Review the test cases in `backend/tests/test_phase1_institutions.py`
- Check the implementation in `backend/shared/` modules
- Consult the database schema in `infrastructure/scripts/migrations/`

---

*Document Version: 1.0*
*Last Updated: 2026-09-09*
*Phase: 1 Complete*