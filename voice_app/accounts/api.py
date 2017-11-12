from voice_app.accounts.models import User


def create_mentor(username: str, first_name: str, last_name: str,
                  password: str) -> User:
    """Create a Mentor"""

    user = User(username=username,
                first_name=first_name,
                last_name=last_name,
                is_mentor=True)
    user.set_password(password)

    # May throw IntegrityError
    user.save(force_insert=True)
    return user
