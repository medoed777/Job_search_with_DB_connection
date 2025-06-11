import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()


def create_database() -> None:
    """Функция для создания базы данных"""
    db_name = os.getenv("DATABASE_NAME")
    user = os.getenv("DATABASE_USER")
    password = os.getenv("DATABASE_PASSWORD")

    connection = psycopg2.connect(user=user, password=password)
    connection.autocommit = True
    cursor = connection.cursor()

    try:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        print(f"База данных '{db_name}' успешно создана.")
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        cursor.close()
        connection.close()


def create_tables() -> None:
    """Функция для создания таблиц"""
    db_name = os.getenv("DATABASE_NAME")
    user = os.getenv("DATABASE_USER")
    password = os.getenv("DATABASE_PASSWORD")

    connection = psycopg2.connect(dbname=db_name, user=user, password=password)
    cursor = connection.cursor()

    create_employers_table = """
    CREATE TABLE IF NOT EXISTS employers (
        id SERIAL PRIMARY KEY,
        employer_id VARCHAR(255) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        url VARCHAR(255),
    );
    """

    create_vacancies_table = """
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        vacancy_id VARCHAR(255) UNIQUE NOT NULL,
        title VARCHAR(255) NOT NULL,
        salary_min INTEGER,
        salary_max INTEGER,
        currency VARCHAR(10),
        published_at TIMESTAMP,
        employer_id INTEGER REFERENCES employers(id) ON DELETE CASCADE
    );
    """

    try:
        cursor.execute(create_employers_table)
        cursor.execute(create_vacancies_table)
        connection.commit()
        print("Таблицы успешно созданы.")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
    finally:
        cursor.close()
        connection.close()

#
# if __name__ == "__main__":
#     create_database()
#     create_tables()