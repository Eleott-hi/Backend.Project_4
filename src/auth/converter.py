import schemas


class Converter():
    def __init__(self) -> None:
        self.mapper = {
            schemas.RegistrationRequest: self.__to_pydantic_registration_request,
            schemas.LoginRequest: self.__to_pydantic_login_request,
            schemas.ForgotPasswordRequest: self.__to_pydantic_forgot_password_request,
            schemas.ChangePasswordRequest: self.__to_pydantic_change_password_request
        }


    def convert_to(self, request, to_cls):
        if to_cls not in self.mapper:
            raise ValueError(f"No such cls type in mapper: {to_cls}")

        return self.mapper[to_cls](request)

    def __to_pydantic_registration_request(self, request):
        return schemas.RegistrationRequest(
            name=request.name,
            surname=request.surname,
            email=request.email,
            phone_number=request.phone_number,
            password=request.password
        )

    def __to_pydantic_login_request(self, request):
        return schemas.LoginRequest(
            email=request.email,
            password=request.password
        )

    def __to_pydantic_forgot_password_request(self, request):
        return schemas.ForgotPasswordRequest(
            email=request.email
        )

    def __to_pydantic_change_password_request(self, request):
        return schemas.ChangePasswordRequest(
            email=request.email,
            old_password=request.old_password,
            new_password=request.new_password
        )
