from datetime import datetime

from utils.commands_mysql_utils import execute_sql_modify, execute_sql_query


def add_task(task_id: str, username: str, since: datetime, until: datetime, created: datetime,
             scrap_session_id: str, queue_name: str):
    execute_sql_modify(
        '''INSERT INTO twint_distributed_tasks.UserTweetScrapTasks(task_id, username, since, until, created, finished,
         scrap_session_id, queue_name) VALUE (%s, %s, %s, %s, %s, %s, %s, %s);''',
        [task_id, username, since, until, created, None, scrap_session_id, queue_name])
    return


def add_sub_task(sub_task_id: str, task_id: str, since: datetime, until: datetime, created: datetime):
    execute_sql_modify(
        '''INSERT INTO twint_distributed_tasks.UserTweetScrapSubTasks(sub_task_id, task_id, since, until, created, 
        finished) VALUE (%s, %s, %s, %s, %s, %s);''',
        [sub_task_id, task_id, since, until, created, None])
    return


def set_task_finished(task_id: str, finished: datetime):
    execute_sql_modify(
        '''UPDATE twint_distributed_tasks.UserTweetScrapTasks
        SET finished = %s
        WHERE task_id = %s''',
        [finished, task_id])
    return


def set_sub_task_finished(sub_task_id: str, finished: datetime):
    execute_sql_modify(
        '''UPDATE twint_distributed_tasks.UserTweetScrapSubTasks
        SET finished = %s
        WHERE sub_task_id = %s''',
        [finished, sub_task_id])
    return


def get_session_id(task_id: str) -> str:
    return execute_sql_query(
        'SELECT * FROM twint_distributed_tasks.UserTweetScrapTasks WHERE task_id=%s',
        [task_id]
    )['scrap_session_id'].to_numpy()[0]


def get_all_not_finished_sub_tasks_by_task_id(task_id: str):
    return execute_sql_query(
        'SELECT * FROM twint_distributed_tasks.UserTweetScrapSubTasks WHERE task_id=%s AND finished IS NULL',
        [task_id])


def get_task_id_sub_task_id(sub_task_id: str) -> str:
    return execute_sql_query(
        'SELECT * FROM twint_distributed_tasks.UserTweetScrapSubTasks WHERE sub_task_id=%s',
        [sub_task_id]
    )['task_id'].to_numpy()[0]


def get_all_tasks_by_username(username: str):
    return execute_sql_query(
        'SELECT * FROM twint_distributed_tasks.UserTweetScrapTasks WHERE username=%s',
        [username]
    )


def get_all_tasks():
    return execute_sql_query(
        '''SELECT task_id, username, created, finished, queue_name, scrap_session_name, since, until
        FROM twint_distributed_tasks.UserTweetScrapTasks t 
            JOIN twint_distributed_tasks.ScrapSession s ON t.scrap_session_id = s.scrap_session_id''',
        [])
