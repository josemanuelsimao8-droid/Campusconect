-- Campus Connect
-- Migration 002: complete academic profile structure.
-- PostgreSQL / local development
--
-- This migration extends the existing student profile and adds indexes
-- needed for university, campus, course and student lookups.

-- 1. Additional profile information used by signup/profile screens.
ALTER TABLE student_profiles
    ADD COLUMN IF NOT EXISTS phone VARCHAR(30),
    ADD COLUMN IF NOT EXISTS location VARCHAR(255);

-- 2. The student number must identify one student inside the platform.
-- A unique index is used instead of a UNIQUE constraint so this migration
-- remains safely re-runnable.
CREATE UNIQUE INDEX IF NOT EXISTS uq_student_profiles_student_number
    ON student_profiles (student_number);

-- Institutional e-mail should also belong to only one student profile.
CREATE UNIQUE INDEX IF NOT EXISTS uq_student_profiles_institutional_email
    ON student_profiles (institutional_email);

-- 3. Useful indexes for the academic discovery rules of Campus Connect.
CREATE INDEX IF NOT EXISTS ix_campuses_university_id
    ON campuses (university_id);

CREATE INDEX IF NOT EXISTS ix_schools_campus_id
    ON schools (campus_id);

CREATE INDEX IF NOT EXISTS ix_course_offerings_course_id
    ON course_offerings (course_id);

CREATE INDEX IF NOT EXISTS ix_course_offerings_university_id
    ON course_offerings (university_id);

CREATE INDEX IF NOT EXISTS ix_course_offerings_campus_id
    ON course_offerings (campus_id);

CREATE INDEX IF NOT EXISTS ix_course_offerings_school_id
    ON course_offerings (school_id);

CREATE INDEX IF NOT EXISTS ix_course_offerings_education_level_id
    ON course_offerings (education_level_id);

CREATE INDEX IF NOT EXISTS ix_student_profiles_campus_id
    ON student_profiles (campus_id);

CREATE INDEX IF NOT EXISTS ix_student_profiles_course_offering_id
    ON student_profiles (course_offering_id);

CREATE INDEX IF NOT EXISTS ix_student_profiles_verification_status
    ON student_profiles (verification_status);

-- 4. Basic consistency rule: the academic year is positive.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'student_profiles_academic_year_positive'
          AND conrelid = 'student_profiles'::regclass
    ) THEN
        ALTER TABLE student_profiles
        ADD CONSTRAINT student_profiles_academic_year_positive
        CHECK (academic_year > 0);
    END IF;
END
$$;
