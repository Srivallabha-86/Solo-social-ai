"""Add users and owner columns.

Revision ID: 0001_users_and_ownership
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_users_and_ownership"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    existing_tables = sa.inspect(op.get_bind()).get_table_names()
    if "users" not in existing_tables:
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("email", sa.String(length=320), nullable=False),
            sa.Column("password_hash", sa.String(length=255), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint("email", name="uq_users_email"),
        )
    existing_indexes = {
        index["name"] for index in sa.inspect(op.get_bind()).get_indexes("users")
    }
    if "ix_users_id" not in existing_indexes:
        op.create_index("ix_users_id", "users", ["id"], unique=False)
    if "ix_users_email" not in existing_indexes:
        op.create_index("ix_users_email", "users", ["email"], unique=True)
    if "content_ideas" not in existing_tables:
        op.create_table(
            "content_ideas",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("owner_id", sa.Integer(), nullable=True),
            sa.Column("topic", sa.String(length=255), nullable=False),
            sa.Column("platform", sa.String(length=50), nullable=False),
            sa.Column("content", sa.Text(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["owner_id"],
                ["users.id"],
                name="fk_content_ideas_owner_id_users",
                ondelete="CASCADE",
            ),
        )
        op.create_index("ix_content_ideas_id", "content_ideas", ["id"])
        op.create_index("ix_content_ideas_owner_id", "content_ideas", ["owner_id"])
    elif "owner_id" not in {
        column["name"] for column in sa.inspect(op.get_bind()).get_columns("content_ideas")
    }:
        with op.batch_alter_table("content_ideas") as batch_op:
            batch_op.add_column(sa.Column("owner_id", sa.Integer(), nullable=True))
            batch_op.create_index("ix_content_ideas_owner_id", ["owner_id"])
            batch_op.create_foreign_key(
                "fk_content_ideas_owner_id_users",
                "users",
                ["owner_id"],
                ["id"],
                ondelete="CASCADE",
            )

    if "calendar_posts" not in existing_tables:
        op.create_table(
            "calendar_posts",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("owner_id", sa.Integer(), nullable=True),
            sa.Column("scheduled_date", sa.DateTime(timezone=True), nullable=False),
            sa.Column("topic", sa.String(length=255), nullable=False),
            sa.Column("theme", sa.String(length=100), nullable=False),
            sa.Column("platform", sa.String(length=50), nullable=False),
            sa.Column("suggested_time", sa.String(length=5), nullable=False),
            sa.Column("status", sa.String(length=20), nullable=False),
            sa.Column("content", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(
                ["owner_id"],
                ["users.id"],
                name="fk_calendar_posts_owner_id_users",
                ondelete="CASCADE",
            ),
        )
        op.create_index("ix_calendar_posts_id", "calendar_posts", ["id"])
        op.create_index(
            "ix_calendar_posts_scheduled_date",
            "calendar_posts",
            ["scheduled_date"],
        )
        op.create_index("ix_calendar_posts_owner_id", "calendar_posts", ["owner_id"])
    elif "owner_id" not in {
        column["name"] for column in sa.inspect(op.get_bind()).get_columns("calendar_posts")
    }:
        with op.batch_alter_table("calendar_posts") as batch_op:
            batch_op.add_column(sa.Column("owner_id", sa.Integer(), nullable=True))
            batch_op.create_index("ix_calendar_posts_owner_id", ["owner_id"])
            batch_op.create_foreign_key(
                "fk_calendar_posts_owner_id_users",
                "users",
                ["owner_id"],
                ["id"],
                ondelete="CASCADE",
            )


def downgrade() -> None:
    with op.batch_alter_table("calendar_posts") as batch_op:
        batch_op.drop_constraint("fk_calendar_posts_owner_id_users", type_="foreignkey")
        batch_op.drop_index("ix_calendar_posts_owner_id")
        batch_op.drop_column("owner_id")

    with op.batch_alter_table("content_ideas") as batch_op:
        batch_op.drop_constraint("fk_content_ideas_owner_id_users", type_="foreignkey")
        batch_op.drop_index("ix_content_ideas_owner_id")
        batch_op.drop_column("owner_id")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
