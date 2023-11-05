import os
import sqlite3
from core.config import Config


class Database:
    database = None
    current_savefile = ""
    has_unsaved_data = False

    @staticmethod
    def init_DB():
        Database.database = sqlite3.connect(':memory:')
        Database.database.row_factory = lambda C, R: {c[0]: R[i] for i, c in enumerate(C.description)} # get dict output (https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query)

        Database.database.execute("CREATE TABLE hosts(id integer primary key autoincrement not null, os text, ip, hostname, mac, highlight text, pwned integer not null default 0 check(pwned IN (0,1)) , nmap, notes)")
        Database.database.execute("CREATE TABLE hosts_ports(host_id integer, proto text, port, status text, description text)")
        Database.database.execute("CREATE TABLE hosts_tabs(id integer primary key autoincrement not null, host_id integer, job_id integer, title text, text)")
        Database.database.execute("CREATE TABLE hosts_creds(id INTEGER primary key autoincrement not null, host_id integer, type TEXT DEFAULT 'password', domain TEXT DEFAULT '', username TEXT DEFAULT '', password TEXT DEFAULT '')")
        Database.database.execute("CREATE TABLE logs(id integer primary key autoincrement not null, date, type, log)")
        Database.database.execute("CREATE TABLE jobs(id integer primary key autoincrement not null, host_id integer, type, timestamp, state, command)")

        Database.has_unsaved_data = False
        Database.current_savefile = ""

    @staticmethod
    def request(request: str, args: tuple = ()) -> sqlite3.Cursor:
        if Database.database is None:
            Database.init_DB()

        cursor = Database.database.cursor()
        try:
            res = cursor.execute(request, args)
        except sqlite3.Error as e:
            print(f"Error while requesting sqlite database: {e}")
            print(f"Request: '{request}', args: '{args}'")
        else:
            if args.count('RUNTIME') != 1 and any(request.lower().startswith(command.lower()) for command in ['update', 'insert', 'delete']):
                Database.has_unsaved_data = True

        return res

    @staticmethod
    def import_DB(filename: str):
        if not os.path.isfile(filename) or not os.access(filename, os.R_OK):
            return f'database file "{filename}" not found.'

        try:
            source = sqlite3.connect(filename)
        except sqlite3.OperationalError as e:
            return e

        Database.init_DB()

        source.backup(Database.database)

        # Compatibility code : if table hosts_creds does not exist (QtRecon < 1.2), then create it
        if not Database.request("SELECT name FROM sqlite_schema WHERE type = 'table' AND name = 'hosts_creds'").fetchall():
            Database.database.execute("CREATE TABLE hosts_creds(id INTEGER primary key autoincrement not null, host_id integer, type TEXT DEFAULT 'password', domain TEXT DEFAULT '', username TEXT DEFAULT '', password TEXT DEFAULT '')")

        Database.database.commit()
        Database.current_savefile = filename

    @staticmethod
    def export_DB(filename: str) -> Exception:
        Database.database.commit()

        try:
            dest = sqlite3.connect(filename)
            Database.database.backup(dest, pages=1, sleep=1)

            # Delete all jobs
            dest.execute("DELETE FROM jobs;")
            # DO NOT Reset database rowID counter for jobs, as it MUST be uniq in db !

            if Config.get()['user_prefs']['delete_logs_on_save']:
                # Delete all logs
                dest.execute("DELETE FROM logs;")
                # Reset database rowID counter
                dest.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='logs';")
            else:
                # Ignore RUNTIME logs
                dest.execute("DELETE FROM logs WHERE type == 'RUNTIME';")

            dest.commit()

        except sqlite3.OperationalError as e:
            return e

        Database.current_savefile = filename