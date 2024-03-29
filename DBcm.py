import mysql.connector


class ConnectionError(Exception):
    """
    ошибка соеенения с БД
    """
    pass


class CredentialError(Exception):
    """
    ошибка ввода учетных данных БД,
    приводит к появлению ProgrammingError
    может возникать в ходе выполнения __enter__

    """
    pass


class SQLError(Exception):
    """
    ошибка SQL-запроса
    """
    pass


class UseDatabase:

    def __init__(self, config: dict) -> None:
        self.configuration = config

    def __enter__(self) -> 'cursor':
        try:
            self.conn = mysql.connector.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
        except mysql.connector.errors.InterfaceError as err:
            raise ConnectionError(err)
        except mysql.connector.errors.ProgrammingError as err:
            raise ConnectionError(err)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        """
        Если возникло ProgrammingError-возбудить SQLError.
        Возбудить исключение после выполнения 
        кода метода __exit__ 
        """
        if exc_type is mysql.connector.errors.ProgrammingError:
            raise SQLError(exc_val)
        elif exc_type:
            raise exc_type(exc_val)
