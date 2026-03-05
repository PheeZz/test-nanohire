import faker


class HHMockController:
    @classmethod
    def generate_random_resume_data(cls) -> dict:
        fake = faker.Faker(locale="ru_RU")
        return {
            "id": fake.uuid4(),
            "first_name": fake.first_name(),
            "middle_name": fake.middle_name(),
            "last_name": fake.last_name(),
            "position": "Software Engineer",
            "contact": [
                {
                    "comment": "Звонить после 12",
                    "contact_value": fake.phone_number(),
                    "kind": "phone",
                    "need_verification": True,
                    "preferred": False,
                    "type": {"id": "cell", "name": "Мобильный телефон"},
                    "verified": False,
                },
                {
                    "contact_value": fake.email(),
                    "kind": "email",
                    "preferred": True,
                    "type": {"id": "email", "name": "Эл. почта"},
                },
                {
                    "contact_value": "@nickname",
                    "kind": "primary",
                    "links": {
                        "android": f"https://t.me/{fake.user_name()}",
                        "ios": f"https://t.me/{fake.user_name()}",
                        "web": f"https://t.me/{fake.user_name()}",
                    },
                    "preferred": False,
                    "type": {"id": "telegram", "name": "telegram"},
                },
                {
                    "contact_value": f"set.ki/{fake.uuid4()}",
                    "kind": "primary",
                    "links": {
                        "android": f"set.ki/{fake.uuid4()}",
                        "ios": f"set.ki/{fake.uuid4()}",
                        "web": f"set.ki/{fake.uuid4()}",
                    },
                    "preferred": False,
                    "type": {"id": "setka", "name": "setka"},
                },
                {
                    "contact_value": f"https://linked.in/{fake.uuid4()}",
                    "kind": "secondary",
                    "preferred": False,
                    "type": {"id": "other", "name": "MyLinkedIn"},
                },
            ],
        }


if __name__ == "__main__":
    from pprint import pprint

    pprint(HHMockController.generate_random_resume_data())
