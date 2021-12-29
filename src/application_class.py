class Application:
    def __init__(
        self,
        email_address: str,
        password: str,
        full_name: str,
        cover_letter: str,
        target_cv_name: str,
        job_title: str,
        job_location: str,
    ) -> None:
        self.email_address = email_address
        self.password = password

        self.job_title = job_title
        self.job_location = job_location

        self.full_name = full_name
        self.cover_letter = cover_letter
        self.target_cv_name = target_cv_name

    def __str__(self) -> str:
        return (
            f"{self.email_address}. Wants a {self.job_title} job in {self.job_location}"
        )
