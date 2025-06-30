"""JWT Blacklisting Module."""

from db import local as db_local


def blacklist_token(jti: str):
    with db_local.get_db() as conn:
        conn.execute(
            """--sql 
            INSERT OR IGNORE INTO blacklisted_tokens (jti) VALUES (?)
            """,
            (jti,),
        )
        conn.commit()


def is_token_blacklisted(jti: str) -> bool:
    with db_local.get_db() as conn:
        cur = conn.execute(
            """--sql 
            SELECT 1 FROM blacklisted_tokens WHERE jti = ?
            """,
            (jti,),
        )
        return cur.fetchone() is not None
