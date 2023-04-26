import psycopg2
import datetime
from typing import List, Tuple

from api.constants import DATABASE_URL
from api.utils import Message, create_chat_message
from loguru import logger

def save_chat_log(user_id: str, user_message: str, ai_reply: str) -> None:
    timestamp = datetime.datetime.now()
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO chat_logs (timestamp, user_id, user_message, ai_reply) VALUES (%s, %s, %s, %s)',
                (timestamp, user_id, user_message, ai_reply)
            )
        conn.commit()

def get_last_n_chat_logs(user_id: str, n: int = 9) -> List[Message]:
    try:
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            with conn.cursor() as cur:
                cur.execute(
                    '''
                    SELECT * FROM (
                        SELECT * FROM chat_logs WHERE user_id = %s ORDER BY timestamp DESC LIMIT %s
                    ) subquery ORDER BY timestamp ASC
                    ''',
                    (user_id, n)
                )
                return _parse_chat_logs(cur.fetchall())
    except Exception as e:
        logger.warning(f"Error getting chat logs: {str(e)}")
        return []
        
def _parse_chat_logs(chat_logs: List[Tuple[int, str, str, str, str]]) -> List[Message]:
    chat_messages = []
    for log in chat_logs:
        user_message = log[3]
        ai_reply = log[4]
        chat_messages.append(create_chat_message("user", user_message))
        chat_messages.append(create_chat_message("assistant", ai_reply))
    return chat_messages