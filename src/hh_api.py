import requests


class EmployerAPI:
    """Класс для работы с API работодателей на hh.ru."""

    BASE_URL = "https://api.hh.ru/employers/"

    def fetch_employer(self, employer_id: str) -> dict:
        """Получает информацию о компании по ID"""
        try:
            resp = requests.get(f"{self.BASE_URL}{employer_id}")
            resp.raise_for_status()
            data = resp.json()
            return {
                "id": data["id"],
                "name": data["name"],
                "url": data.get("url"),
                "description": data.get("description", ""),
            }
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            raise

    def fetch_vacancies(self, employer_id: str) -> list:
        """Получает информацию о вакансиях компании"""
        try:
            resp = requests.get(
                f"https://api.hh.ru/vacancies?employer_id={employer_id}"
            )
            resp.raise_for_status()
            data = resp.json()

            vacancies = []
            for vacancy in data["items"]:
                salary_min = (
                    vacancy["salary"]["from"]
                    if vacancy.get("salary")
                    and vacancy["salary"].get("from") is not None
                    else None
                )
                salary_max = (
                    vacancy["salary"]["to"]
                    if vacancy.get("salary")
                    and vacancy["salary"].get("to") is not None
                    else None
                )

                avg_salary = None
                if salary_min is not None and salary_max is not None:
                    avg_salary = (salary_min + salary_max) / 2

                vacancies.append(
                    {
                        "id": vacancy["id"],
                        "title": vacancy["name"],
                        "salary_min": salary_min,
                        "salary_max": salary_max,
                        "avg_salary": avg_salary,
                        "currency": (
                            vacancy["salary"]["currency"]
                            if vacancy.get("salary")
                            else None
                        ),
                        "alternate_url": vacancy["alternate_url"],
                    }
                )

            return vacancies
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
