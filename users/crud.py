from users.schemas import CreateUser


def create_user(user: CreateUser):
    user = user.model_dump()
    return {
        "Success": True,
        "user": user,
    }
