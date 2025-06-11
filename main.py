from src.hh_api import EmployerAPI
from src.db_manager import DBManager

def main():
    employers_ids = ["3529", "16498", "1137303", "2822182", "3469631", "819979", "546422", "72404", "587386", "576774"]

    api = EmployerAPI()
    db_manager = DBManager(db_name='your_db_name', user='your_user', password='your_password')

    for employer_id in employers_ids:
        try:
            employer_info = api.fetch_employer(employer_id)
            db_manager.create_employer(employer_info)

            vacancies = api.fetch_vacancies(employer_id)
            for vacancy in vacancies:
                vacancy['employer_id'] = employer_info['id']  # Добавляем ID работодателя к вакансии
                db_manager.create_vacancy(vacancy)

        except Exception as e:
            print(f"Ошибка при обработке работодателя {employer_id}: {e}")

    db_manager.close()


if __name__ == "__main__":
    main()