-- Allamni v4.0 - Phase 1 Migration
-- Institutions, Subscriptions, and Codes System
-- Date: 2026-09-09

-- Institutions Table
CREATE TABLE IF NOT EXISTS institutions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name_ar VARCHAR(255) NOT NULL,
    name_en VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('school', 'university', 'training_center')),
    sub_type VARCHAR(100), -- e.g., 'primary', 'secondary', 'private_university', etc.
    country VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(255),
    website VARCHAR(255),
    logo_url TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    admin_user_id UUID REFERENCES users(id)
);

-- Subscriptions Table
CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    institution_id UUID NOT NULL REFERENCES institutions(id) ON DELETE CASCADE,
    plan_type VARCHAR(50) NOT NULL CHECK (plan_type IN ('basic', 'professional', 'enterprise')),
    status VARCHAR(50) NOT NULL CHECK (status IN ('trial', 'active', 'suspended', 'cancelled')),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    max_students INTEGER,
    max_teachers INTEGER,
    max_admins INTEGER DEFAULT 1,
    features JSONB DEFAULT '{}',
    billing_cycle VARCHAR(20) NOT NULL CHECK (billing_cycle IN ('monthly', 'yearly')),
    auto_renew BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Student Codes Table
CREATE TABLE IF NOT EXISTS student_codes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    institution_id UUID NOT NULL REFERENCES institutions(id) ON DELETE CASCADE,
    code VARCHAR(50) UNIQUE NOT NULL,
    student_id UUID REFERENCES users(id) ON DELETE SET NULL,
    class_id VARCHAR(100),
    grade_level VARCHAR(50),
    academic_year VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    issued_by UUID REFERENCES users(id),
    issued_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    used_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'
);

-- Teacher Codes Table
CREATE TABLE IF NOT EXISTS teacher_codes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    institution_id UUID NOT NULL REFERENCES institutions(id) ON DELETE CASCADE,
    code VARCHAR(50) UNIQUE NOT NULL,
    teacher_id UUID REFERENCES users(id) ON DELETE SET NULL,
    department VARCHAR(100),
    subjects TEXT[], -- Array of subject names
    grade_levels VARCHAR(50)[], -- Array of grade levels they can teach
    is_active BOOLEAN DEFAULT true,
    issued_by UUID REFERENCES users(id),
    issued_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    used_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'
);

-- Institution Settings Table
CREATE TABLE IF NOT EXISTS institution_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    institution_id UUID NOT NULL UNIQUE REFERENCES institutions(id) ON DELETE CASCADE,
    branding JSONB DEFAULT '{}', -- colors, logo, custom themes
    content_policies JSONB DEFAULT '{}', -- what content can be accessed
    language_preferences VARCHAR(10) DEFAULT 'ar', -- ar, en, or both
    timezone VARCHAR(50) DEFAULT 'Africa/Cairo',
    academic_calendar JSONB DEFAULT '{}', -- semester dates, holidays
    notification_settings JSONB DEFAULT '{}',
    integration_settings JSONB DEFAULT '{}', -- Odoo, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Parent-Student Relationships Table
CREATE TABLE IF NOT EXISTS parent_student_relationships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL CHECK (relationship_type IN ('father', 'mother', 'guardian')),
    is_primary BOOLEAN DEFAULT false,
    can_view_progress BOOLEAN DEFAULT true,
    can_view_attendance BOOLEAN DEFAULT true,
    can_communicate BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(parent_id, student_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_institutions_type ON institutions(type);
CREATE INDEX IF NOT EXISTS idx_institutions_active ON institutions(is_active);
CREATE INDEX IF NOT EXISTS idx_subscriptions_institution ON subscriptions(institution_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_student_codes_code ON student_codes(code);
CREATE INDEX IF NOT EXISTS idx_student_codes_institution ON student_codes(institution_id);
CREATE INDEX IF NOT EXISTS idx_student_codes_student ON student_codes(student_id);
CREATE INDEX IF NOT EXISTS idx_teacher_codes_code ON teacher_codes(code);
CREATE INDEX IF NOT EXISTS idx_teacher_codes_institution ON teacher_codes(institution_id);
CREATE INDEX IF NOT EXISTS idx_teacher_codes_teacher ON teacher_codes(teacher_id);
CREATE INDEX IF NOT EXISTS idx_parent_student_parent ON parent_student_relationships(parent_id);
CREATE INDEX IF NOT EXISTS idx_parent_student_student ON parent_student_relationships(student_id);

-- Update trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_institutions_updated_at BEFORE UPDATE ON institutions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscriptions_updated_at BEFORE UPDATE ON subscriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_institution_settings_updated_at BEFORE UPDATE ON institution_settings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_parent_student_updated_at BEFORE UPDATE ON parent_student_relationships
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();