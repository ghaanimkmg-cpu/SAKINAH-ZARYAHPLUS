"""core_models

Revision ID: e08f4a861ae1
Revises: 
Create Date: 2026-06-05 19:13:02.165066

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'e08f4a861ae1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. nis_users
    op.create_table(
        'nis_users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('zaryah_user_id', sa.String(), nullable=False),
        sa.Column('eligibility_status', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nis_users_zaryah_user_id'), 'nis_users', ['zaryah_user_id'], unique=True)
    op.create_index(op.f('ix_nis_users_id'), 'nis_users', ['id'], unique=False)

    # 2. nis_kyc_verifications
    op.create_table(
        'nis_kyc_verifications',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('verified_name', sa.String(), nullable=True),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('gender', sa.String(), nullable=True),
        sa.Column('verification_status', sa.String(), nullable=True),
        sa.Column('kyc_provider_reference', sa.String(), nullable=True),
        sa.Column('identity_hash', sa.String(), nullable=True),
        sa.Column('human_review_required', sa.Boolean(), nullable=True),
        sa.Column('review_reason', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['nis_users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_nis_kyc_verifications_identity_hash'), 'nis_kyc_verifications', ['identity_hash'], unique=False)
    op.create_index(op.f('ix_nis_kyc_verifications_id'), 'nis_kyc_verifications', ['id'], unique=False)

    # 3. nis_match_preferences
    op.create_table(
        'nis_match_preferences',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('age_range_min', sa.Integer(), nullable=True),
        sa.Column('age_range_max', sa.Integer(), nullable=True),
        sa.Column('location_preference', sa.String(), nullable=True),
        sa.Column('relocation_openness', sa.Boolean(), nullable=True),
        sa.Column('nikah_timeline', sa.String(), nullable=True),
        sa.Column('tradition_preference', sa.String(), nullable=True),
        sa.Column('wali_involvement_preference', sa.String(), nullable=True),
        sa.Column('marital_status_preference', sa.String(), nullable=True),
        sa.Column('financial_expectation_preference', sa.String(), nullable=True),
        sa.Column('family_expectation_notes', sa.Text(), nullable=True),
        sa.Column('deal_breakers', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['nis_users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_nis_match_preferences_id'), 'nis_match_preferences', ['id'], unique=False)

    # 4. nis_user_signal_profiles
    op.create_table(
        'nis_user_signal_profiles',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('emotional_steadiness', sa.Float(), nullable=True),
        sa.Column('communication_style', sa.String(), nullable=True),
        sa.Column('conflict_repair_style', sa.String(), nullable=True),
        sa.Column('family_responsibility', sa.String(), nullable=True),
        sa.Column('deen_alignment', sa.String(), nullable=True),
        sa.Column('marriage_readiness', sa.Float(), nullable=True),
        sa.Column('financial_expectation', sa.String(), nullable=True),
        sa.Column('wali_comfort', sa.String(), nullable=True),
        sa.Column('life_direction', sa.String(), nullable=True),
        sa.Column('self_awareness_level', sa.Float(), nullable=True),
        sa.Column('social_lifestyle', sa.String(), nullable=True),
        sa.Column('safety_risk_level', sa.String(), nullable=True),
        sa.Column('confidence_level', sa.String(), nullable=True),
        sa.Column('missing_signal_areas', sa.JSON(), nullable=True),
        sa.Column('review_required', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['nis_users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_nis_user_signal_profiles_id'), 'nis_user_signal_profiles', ['id'], unique=False)

    # 5. nis_compatibility_evaluations
    op.create_table(
        'nis_compatibility_evaluations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_a_id', sa.UUID(), nullable=False),
        sa.Column('user_b_id', sa.UUID(), nullable=False),
        sa.Column('compatibility_score', sa.Float(), nullable=True),
        sa.Column('compatibility_status', sa.String(), nullable=True),
        sa.Column('evaluation_reasons', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_a_id'], ['nis_users.id'], ),
        sa.ForeignKeyConstraint(['user_b_id'], ['nis_users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nis_compatibility_evaluations_id'), 'nis_compatibility_evaluations', ['id'], unique=False)

    # 6. nis_considered_pools
    op.create_table(
        'nis_considered_pools',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('candidate_id', sa.UUID(), nullable=False),
        sa.Column('pool_status', sa.String(), nullable=True),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['candidate_id'], ['nis_users.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['nis_users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nis_considered_pools_id'), 'nis_considered_pools', ['id'], unique=False)

    # 7. nis_match_interests
    op.create_table(
        'nis_match_interests',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('sender_id', sa.UUID(), nullable=False),
        sa.Column('receiver_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['receiver_id'], ['nis_users.id'], ),
        sa.ForeignKeyConstraint(['sender_id'], ['nis_users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nis_match_interests_id'), 'nis_match_interests', ['id'], unique=False)

    # 8. nis_matchflows
    op.create_table(
        'nis_matchflows',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_a_id', sa.UUID(), nullable=False),
        sa.Column('user_b_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('current_step', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_a_id'], ['nis_users.id'], ),
        sa.ForeignKeyConstraint(['user_b_id'], ['nis_users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nis_matchflows_id'), 'nis_matchflows', ['id'], unique=False)

    # 9. nis_structured_conversations
    op.create_table(
        'nis_structured_conversations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('matchflow_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('topic_unlocked', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['matchflow_id'], ['nis_matchflows.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('matchflow_id')
    )
    op.create_index(op.f('ix_nis_structured_conversations_id'), 'nis_structured_conversations', ['id'], unique=False)

    # 10. nis_conversation_messages
    op.create_table(
        'nis_conversation_messages',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('conversation_id', sa.UUID(), nullable=False),
        sa.Column('sender_id', sa.UUID(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('is_system_message', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['nis_structured_conversations.id'], ),
        sa.ForeignKeyConstraint(['sender_id'], ['nis_users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nis_conversation_messages_id'), 'nis_conversation_messages', ['id'], unique=False)

    # 11. nis_reports
    op.create_table(
        'nis_reports',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('reporter_id', sa.UUID(), nullable=False),
        sa.Column('target_id', sa.UUID(), nullable=False),
        sa.Column('reason', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['reporter_id'], ['nis_users.id'], ),
        sa.ForeignKeyConstraint(['target_id'], ['nis_users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nis_reports_id'), 'nis_reports', ['id'], unique=False)

    # 12. nis_safety_flags
    op.create_table(
        'nis_safety_flags',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('reporter_id', sa.UUID(), nullable=False),
        sa.Column('target_id', sa.UUID(), nullable=False),
        sa.Column('flag_type', sa.String(), nullable=False),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['reporter_id'], ['nis_users.id'], ),
        sa.ForeignKeyConstraint(['target_id'], ['nis_users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nis_safety_flags_id'), 'nis_safety_flags', ['id'], unique=False)

    # 13. nis_human_reviews
    op.create_table(
        'nis_human_reviews',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('report_id', sa.UUID(), nullable=True),
        sa.Column('kyc_id', sa.UUID(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('decision', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['kyc_id'], ['nis_kyc_verifications.id'], ),
        sa.ForeignKeyConstraint(['report_id'], ['nis_reports.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nis_human_reviews_id'), 'nis_human_reviews', ['id'], unique=False)

    # 14. nis_identity_bans
    op.create_table(
        'nis_identity_bans',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('identity_hash', sa.String(), nullable=False),
        sa.Column('reason', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nis_identity_bans_identity_hash'), 'nis_identity_bans', ['identity_hash'], unique=False)
    op.create_index(op.f('ix_nis_identity_bans_id'), 'nis_identity_bans', ['id'], unique=False)

    # 15. nis_audit_logs
    op.create_table(
        'nis_audit_logs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('actor_id', sa.String(), nullable=True),
        sa.Column('target_id', sa.String(), nullable=True),
        sa.Column('metadata_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nis_audit_logs_id'), 'nis_audit_logs', ['id'], unique=False)


def downgrade() -> None:
    # Safely drop in reverse dependency order
    op.drop_table('nis_audit_logs')
    op.drop_table('nis_identity_bans')
    op.drop_table('nis_human_reviews')
    op.drop_table('nis_safety_flags')
    op.drop_table('nis_reports')
    op.drop_table('nis_conversation_messages')
    op.drop_table('nis_structured_conversations')
    op.drop_table('nis_matchflows')
    op.drop_table('nis_match_interests')
    op.drop_table('nis_considered_pools')
    op.drop_table('nis_compatibility_evaluations')
    op.drop_table('nis_user_signal_profiles')
    op.drop_table('nis_match_preferences')
    op.drop_table('nis_kyc_verifications')
    op.drop_table('nis_users')
