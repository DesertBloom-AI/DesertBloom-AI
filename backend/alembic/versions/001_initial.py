"""initial

Revision ID: 001
Revises: 
Create Date: 2024-02-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_superuser', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)

    # Create apikey table
    op.create_table(
        'apikey',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('last_used', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_apikey_id'), 'apikey', ['id'], unique=False)
    op.create_index(op.f('ix_apikey_key'), 'apikey', ['key'], unique=True)

    # Create project table
    op.create_table(
        'project',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('PLANNING', 'IN_PROGRESS', 'COMPLETED', 'ON_HOLD', name='projectstatus'), nullable=True),
        sa.Column('progress', sa.Float(), default=0.0),
        sa.Column('start_date', sa.String(), nullable=True),
        sa.Column('end_date', sa.String(), nullable=True),
        sa.Column('budget', sa.Float(), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_id'), 'project', ['id'], unique=False)

    # Create milestone table
    op.create_table(
        'milestone',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('PLANNING', 'IN_PROGRESS', 'COMPLETED', 'ON_HOLD', name='projectstatus'), nullable=True),
        sa.Column('progress', sa.Float(), default=0.0),
        sa.Column('due_date', sa.String(), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_milestone_id'), 'milestone', ['id'], unique=False)

    # Create user_project association table
    op.create_table(
        'user_project',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'project_id')
    )

    # Create robot table
    op.create_table(
        'robot',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('model', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('IDLE', 'WORKING', 'MAINTENANCE', 'ERROR', name='robotstatus'), nullable=True),
        sa.Column('battery_level', sa.Float(), default=100.0),
        sa.Column('location', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('current_task', sa.String(), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_robot_id'), 'robot', ['id'], unique=False)

    # Create robottask table
    op.create_table(
        'robottask',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('robot_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('IDLE', 'WORKING', 'MAINTENANCE', 'ERROR', name='robotstatus'), nullable=True),
        sa.Column('progress', sa.Float(), default=0.0),
        sa.Column('start_time', sa.String(), nullable=True),
        sa.Column('end_time', sa.String(), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['robot_id'], ['robot.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_robottask_id'), 'robottask', ['id'], unique=False)

    # Create species table
    op.create_table(
        'species',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('scientific_name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('growth_rate', sa.Float(), nullable=True),
        sa.Column('water_requirement', sa.Float(), nullable=True),
        sa.Column('temperature_range', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_species_id'), 'species', ['id'], unique=False)

    # Create vegetationscheme table
    op.create_table(
        'vegetationscheme',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('species_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('PLANNED', 'PLANTED', 'GROWING', 'MATURE', 'DECLINING', name='vegetationstatus'), nullable=True),
        sa.Column('area', sa.Float(), nullable=True),
        sa.Column('planting_density', sa.Float(), nullable=True),
        sa.Column('planting_date', sa.String(), nullable=True),
        sa.Column('expected_maturity_date', sa.String(), nullable=True),
        sa.Column('location', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
        sa.ForeignKeyConstraint(['species_id'], ['species.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vegetationscheme_id'), 'vegetationscheme', ['id'], unique=False)

    # Create maintenancerecord table
    op.create_table(
        'maintenancerecord',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('scheme_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('performed_by', sa.String(), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['scheme_id'], ['vegetationscheme.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_maintenancerecord_id'), 'maintenancerecord', ['id'], unique=False)

    # Create tokentransaction table
    op.create_table(
        'tokentransaction',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('from_address', sa.String(), nullable=False),
        sa.Column('to_address', sa.String(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('transaction_hash', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'COMPLETED', 'FAILED', name='transactionstatus'), nullable=True),
        sa.Column('block_number', sa.Integer(), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tokentransaction_id'), 'tokentransaction', ['id'], unique=False)
    op.create_index(op.f('ix_tokentransaction_transaction_hash'), 'tokentransaction', ['transaction_hash'], unique=True)

    # Create smartcontract table
    op.create_table(
        'smartcontract',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('abi', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('network', sa.String(), nullable=False),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_smartcontract_id'), 'smartcontract', ['id'], unique=False)
    op.create_index(op.f('ix_smartcontract_address'), 'smartcontract', ['address'], unique=True)

    # Create contractinteraction table
    op.create_table(
        'contractinteraction',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('contract_id', sa.Integer(), nullable=False),
        sa.Column('function_name', sa.String(), nullable=False),
        sa.Column('parameters', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('transaction_hash', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'COMPLETED', 'FAILED', name='transactionstatus'), nullable=True),
        sa.Column('block_number', sa.Integer(), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['contract_id'], ['smartcontract.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contractinteraction_id'), 'contractinteraction', ['id'], unique=False)
    op.create_index(op.f('ix_contractinteraction_transaction_hash'), 'contractinteraction', ['transaction_hash'], unique=True)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_contractinteraction_transaction_hash'), table_name='contractinteraction')
    op.drop_index(op.f('ix_contractinteraction_id'), table_name='contractinteraction')
    op.drop_table('contractinteraction')

    op.drop_index(op.f('ix_smartcontract_address'), table_name='smartcontract')
    op.drop_index(op.f('ix_smartcontract_id'), table_name='smartcontract')
    op.drop_table('smartcontract')

    op.drop_index(op.f('ix_tokentransaction_transaction_hash'), table_name='tokentransaction')
    op.drop_index(op.f('ix_tokentransaction_id'), table_name='tokentransaction')
    op.drop_table('tokentransaction')

    op.drop_index(op.f('ix_maintenancerecord_id'), table_name='maintenancerecord')
    op.drop_table('maintenancerecord')

    op.drop_index(op.f('ix_vegetationscheme_id'), table_name='vegetationscheme')
    op.drop_table('vegetationscheme')

    op.drop_index(op.f('ix_species_id'), table_name='species')
    op.drop_table('species')

    op.drop_index(op.f('ix_robottask_id'), table_name='robottask')
    op.drop_table('robottask')

    op.drop_index(op.f('ix_robot_id'), table_name='robot')
    op.drop_table('robot')

    op.drop_table('user_project')

    op.drop_index(op.f('ix_milestone_id'), table_name='milestone')
    op.drop_table('milestone')

    op.drop_index(op.f('ix_project_id'), table_name='project')
    op.drop_table('project')

    op.drop_index(op.f('ix_apikey_key'), table_name='apikey')
    op.drop_index(op.f('ix_apikey_id'), table_name='apikey')
    op.drop_table('apikey')

    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')

    # Drop enums
    op.execute('DROP TYPE projectstatus')
    op.execute('DROP TYPE robotstatus')
    op.execute('DROP TYPE vegetationstatus')
    op.execute('DROP TYPE transactionstatus') 