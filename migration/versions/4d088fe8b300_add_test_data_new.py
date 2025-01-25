"""add test data new

Revision ID: 4d088fe8b300
Revises: cd73408b1f25
Create Date: 2025-01-24 21:45:35.715801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '4d088fe8b300'
down_revision: Union[str, None] = 'cd73408b1f25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавление тестовых данных для таблицы buildings
    op.bulk_insert(
        sa.table(
            'buildings',
            sa.column('id', sa.BigInteger),
            sa.column('address', sa.String),
            sa.column('latitude', sa.Float),
            sa.column('longitude', sa.Float),
        ),
        [
            {"id": 1, "address": "г. Москва, ул. Ленина, 1", "latitude": 55.7558, "longitude": 37.6173},
            {"id": 2, "address": "г. Санкт-Петербург, ул. Невский, 15", "latitude": 59.9343, "longitude": 30.3351},
        ]
    )

    # Добавление тестовых данных для таблицы activitys
    op.bulk_insert(
        sa.table(
            'activitys',
            sa.column('id', sa.Integer),
            sa.column('name', sa.String),
            sa.column('parent_id', sa.Integer),
        ),
        [
            {"id": 1, "name": "Еда", "parent_id": None},
            {"id": 2, "name": "Мясная продукция", "parent_id": 1},
            {"id": 3, "name": "Молочная продукция", "parent_id": 1},
            {"id": 4, "name": "Автомобили", "parent_id": None},
            {"id": 5, "name": "Грузовые", "parent_id": 4},
        ]
    )

    # Добавление тестовых данных для таблицы organizations
    op.bulk_insert(
        sa.table(
            'organizations',
            sa.column('id', sa.BigInteger),
            sa.column('name', sa.String),
            sa.column('phone_numbers', postgresql.ARRAY(sa.String)),
            sa.column('building_id', sa.BigInteger),
        ),
        [
            {"id": 1, "name": "ООО Рога и Копыта", "phone_numbers": ["8-800-555-35-35", "2-222-222"], "building_id": 1},
            {"id": 2, "name": "ИП МясоЕда", "phone_numbers": ["3-333-333"], "building_id": 2},
        ]
    )

    # Добавление тестовых данных для связи organization_activity
    op.bulk_insert(
        sa.table(
            'organization_activity',
            sa.column('organization_id', sa.BigInteger),
            sa.column('activity_id', sa.Integer),
        ),
        [
            {"organization_id": 1, "activity_id": 1},  # ООО Рога и Копыта занимается Едой
            {"organization_id": 1, "activity_id": 2},  # ООО Рога и Копыта занимается Мясной продукцией
            {"organization_id": 2, "activity_id": 3},  # ИП МясоЕда занимается Молочной продукцией
        ]
    )


def downgrade() -> None:
    # Удаление тестовых данных
    op.execute("DELETE FROM organization_activity WHERE organization_id IN (1, 2)")
    op.execute("DELETE FROM organizations WHERE id IN (1, 2)")
    op.execute("DELETE FROM activitys WHERE id IN (1, 2, 3, 4, 5)")
    op.execute("DELETE FROM buildings WHERE id IN (1, 2)")