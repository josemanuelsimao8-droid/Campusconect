-- Campus Connect
-- Migration: link student profiles to concrete course offerings.
-- This file is for the local PostgreSQL database only.
--
-- Expected state before running:
--   student_profiles.course_offering_id exists as INTEGER
--   course_offerings exists with id as primary key
--
-- Safe to run once. The final constraint is guarded so rerunning
-- the migration does not fail because the constraint already exists.

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'student_profiles_course_offering_id_fkey'
          AND conrelid = 'student_profiles'::regclass
    ) THEN
        ALTER TABLE student_profiles
        ADD CONSTRAINT student_profiles_course_offering_id_fkey
        FOREIGN KEY (course_offering_id)
        REFERENCES course_offerings(id);
    END IF;
END
$$;
