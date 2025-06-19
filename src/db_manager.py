import psycopg2
from psycopg2 import sql


class DBManager:
    """Класс для работы с базами данных"""
    def __init__(self, db_name, user, password, host='localhost', port='5432'):
        self.connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()

    def get_companies_and_vacancies_count(self):
        """Метод для получения списка компаний и количества вакансий"""
        query = """
        SELECT employers.name, COUNT(vacancies.id) AS vacancies_count
        FROM employers
        LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id
        GROUP BY employers.name;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        """Метод для получения списка всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        query = """
        SELECT vacancies.title, employers.name, vacancies.avg_salary, vacancies.link
        FROM vacancies
        JOIN employers ON vacancies.employer_id = employers.employer_id;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        """Метод для получения средней зарплаты по вакансиям"""
        query = "SELECT AVG(avg_salary) FROM vacancies;"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Метод для получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()
        query = sql.SQL("""
        SELECT vacancies.title, employers.name, vacancies.avg_salary, vacancies.link
        FROM vacancies
        JOIN employers ON vacancies.employer_id = employers.employer_id
        WHERE vacancies.avg_salary > %s;
        """)
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Метод для получения списка всех вакансий, в названии которых содержатся переданные в метод слова"""
        query = sql.SQL("""
        SELECT vacancies.title, employers.name, vacancies.avg_salary, vacancies.link
        FROM vacancies
        JOIN employers ON vacancies.employer_id = employers.employer_id
        WHERE vacancies.title ILIKE %s OR employers.name ILIKE %s 
        ORDER BY vacancies.avg_salary DESC
        """)
        self.cursor.execute(query, (f'%{keyword}%', f'%{keyword}%'))
        return self.cursor.fetchall()


    def close(self):
        """Метод отключения от БД"""
        self.cursor.close()
        self.connection.close()

