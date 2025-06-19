from src.hh_api import EmployerAPI
from src.db_manager import DBManager
from src.sql_manager import create_database, create_tables
import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()
db_name = os.getenv("DATABASE_NAME")
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")

employers_ids = ["3529", "16498", "1137303", "2822182", "3469631", "819979", "546422", "72404", "587386", "576774"]


def fill_tables(employer_ids: list) -> None:
    """Заполняет таблицы данными о работодателях и их вакансиях"""
    api = EmployerAPI()



    try:
        connection = psycopg2.connect(dbname=db_name, user=user, password=password)
        cursor = connection.cursor()

        for employer_id in employer_ids:
            try:
                employer_data = api.fetch_employer(employer_id)

                insert_employer_query = """
                    INSERT INTO employers (employer_id, name, url)
                    VALUES (%s, %s, %s) ON CONFLICT (employer_id) DO NOTHING;
                """
                cursor.execute(insert_employer_query,
                               (employer_data["id"], employer_data["name"], employer_data["url"]))

                if cursor.rowcount > 0:
                    vacancies = api.fetch_vacancies(employer_id)

                    for vacancy in vacancies:
                        insert_vacancy_query = """
                            INSERT INTO vacancies (vacancy_id, title, salary_min, salary_max, avg_salary, currency, link, employer_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (vacancy_id) DO NOTHING;
                        """
                        cursor.execute(insert_vacancy_query, (
                            vacancy["id"], vacancy["title"], vacancy["salary_min"], vacancy["salary_max"], vacancy["avg_salary"], vacancy["currency"], vacancy["alternate_url"],
                            employer_data["id"]))

            except Exception as e:
                print(f"Ошибка при обработке работодателя {employer_id}: {e}")

        connection.commit()
        print("Таблицы успешно заполнены данными.")

    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def user_interface():
    """Функция для взаимодействия с пользователем."""
    db_manager = DBManager(db_name, user, password)

    while True:
        print("\nВыберите действие:")
        print("1. Получить список всех компаний и количество вакансий у каждой компании.")
        print("2. Получить список всех вакансий.")
        print("3. Получить среднюю зарплату по вакансиям.")
        print("4. Получить вакансии с зарплатой выше средней.")
        print("5. Получить вакансии по ключевому слову.")
        print("6. Выход.")

        choice = input("Введите номер действия: ")

        if choice == '1':
            companies = db_manager.get_companies_and_vacancies_count()
            for company in companies:
                print(f"Компания: {company[0]}, Вакансий: {company[1]}")

        elif choice == '2':
            vacancies = db_manager.get_all_vacancies()
            for vacancy in vacancies:
                print(
                    f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, Ссылка: {vacancy[3]}")

        elif choice == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {avg_salary}")

        elif choice == '4':
            higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            for vacancy in higher_salary_vacancies:
                print(
                    f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, Ссылка: {vacancy[3]}")

        elif choice == '5':
            keyword = input("Введите ключевое слово для поиска вакансий: ")
            keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
            for vacancy in keyword_vacancies:
                print(
                    f"Компания: {vacancy[1]}, Вакансия: {vacancy[0]}, Зарплата: {vacancy[2]}, Ссылка: {vacancy[3]}")

        elif choice == '6':
            db_manager.close()
            print("Выход из программы.")
            break

        else:
            print("Некорректный ввод. Пожалуйста, выберите номер из меню.")


def main():
    create_database()
    create_tables()
    fill_tables(employers_ids)
    user_interface()


if __name__ == "__main__":
    main()
