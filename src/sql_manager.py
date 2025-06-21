import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql
from typing import Any, Dict

load_dotenv()


def get_db_config() -> Dict[str, Any]:
    """Берет переменные из .env"""
    return {
        'dbname': os.getenv("DATABASE_NAME"),
        'user': os.getenv("DATABASE_USER"),
        'password': os.getenv("DATABASE_PASSWORD"),
        'host': os.getenv("DATABASE_HOST", "localhost"),
        'port': os.getenv("DATABASE_PORT", "5432")
    }


def create_database() -> None:
    """Функция для создания базы данных"""
    config = get_db_config()

    connection = psycopg2.connect(**config)
    connection.autocommit = True
    cursor = connection.cursor()

    try:
        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(sql.Identifier(config['dbname']))
        )
        print(f"База данных '{config['dbname']}' успешно создана.")
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        cursor.close()
        connection.close()


def create_tables() -> None:
    """Функция для создания таблиц"""
    config = get_db_config()

    connection = psycopg2.connect(**config)
    cursor = connection.cursor()

    create_employers_table = """
    CREATE TABLE IF NOT EXISTS employers (
        id SERIAL PRIMARY KEY,
        employer_id VARCHAR(255) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        url VARCHAR(255)
    );
    """

    create_vacancies_table = """
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        vacancy_id VARCHAR(255) UNIQUE NOT NULL,
        title VARCHAR(255) NOT NULL,
        salary_min INTEGER,
        salary_max INTEGER,
        avg_salary INTEGER,
        link VARCHAR(255),
        currency VARCHAR(10),
        employer_id VARCHAR(255) REFERENCES employers(employer_id) ON DELETE CASCADE
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
