from django.test import TestCase

from users.models import CustomUser


class CustomUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(
            username="test_user",
            password="1X<ISRUkw+tuK",
            first_name="first",
            last_name="last",
            email="krk12@wp.pl",
            pesel="12345678911",
            bank_account="1234756890123456789123450",
            secondary_email="walmart@wp.pl",
            address="New York",
            postal_code="32-576",
            role=2,
            reviews=3.5,
        )

    """Test Model field label """

    def test_username_label(self):
        user = CustomUser.objects.last()
        field_label = user._meta.get_field("username").verbose_name
        self.assertEqual(field_label, "username")

    def test_username_max_length(self):
        user = CustomUser.objects.last()
        max_length = user._meta.get_field("username").max_length
        self.assertEqual(max_length, 150)

    def test_email_label(self):
        user = CustomUser.objects.last()
        field_label = user._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "Email")

    def test_email_max_length(self):
        user = CustomUser.objects.last()
        max_length = user._meta.get_field("email").max_length
        self.assertEqual(max_length, 50)

    def test_pesel_label(self):
        user = CustomUser.objects.last()
        field_label = user._meta.get_field("pesel").verbose_name
        self.assertEqual(field_label, "Pesel")

    def test_pesel_max_length(self):
        user = CustomUser.objects.last()
        max_length = user._meta.get_field("pesel").max_length
        self.assertEqual(max_length, 11)

    def test_bank_account_label(self):
        user = CustomUser.objects.last()
        field_label = user._meta.get_field("bank_account").verbose_name
        self.assertEqual(field_label, "Bank Account Number")

    def test_bank_account_max_length(self):
        user = CustomUser.objects.last()
        max_length = user._meta.get_field("bank_account").max_length
        self.assertEqual(max_length, 25)

    def test_created_at_label(self):
        user = CustomUser.objects.last()
        field_label = user._meta.get_field("created_at").verbose_name
        self.assertEqual(field_label, "created at")

    def test_secondary_email_label(self):
        user = CustomUser.objects.last()
        field_label = user._meta.get_field("secondary_email").verbose_name
        self.assertEqual(field_label, "Secondary Email")

    def test_secondary_email_max_length(self):
        user = CustomUser.objects.last()
        max_length = user._meta.get_field("secondary_email").max_length
        self.assertEqual(max_length, 50)

    def test_address_label(self):
        user = CustomUser.objects.last()
        field_label = user._meta.get_field("address").verbose_name
        self.assertEqual(field_label, "Address")

    def test_address_max_length(self):
        user = CustomUser.objects.last()
        max_length = user._meta.get_field("address").max_length
        self.assertEqual(max_length, 100)

    def test_postal_code_label(self):
        user = CustomUser.objects.last()
        field_label = user._meta.get_field("postal_code").verbose_name
        self.assertEqual(field_label, "Postal Code")

    def test_postal_code_max_length(self):
        user = CustomUser.objects.last()
        max_length = user._meta.get_field("postal_code").max_length
        self.assertEqual(max_length, 6)

    def test_role_label(self):
        user = CustomUser.objects.last()
        field_label = user._meta.get_field("role").verbose_name
        self.assertEqual(field_label, "role")

    def test_reviews_label(self):
        user = CustomUser.objects.last()
        field_label = user._meta.get_field("reviews").verbose_name
        self.assertEqual(field_label, "reviews")

    def test_reviews_max_digits(self):
        user = CustomUser.objects.last()
        max_digits = user._meta.get_field("reviews").max_digits
        self.assertEqual(max_digits, 6)

    """Test Model field data"""

    def test_model_str_method_output(self):
        user = CustomUser.objects.last()
        expected = f"{user.first_name} {user.last_name}"
        self.assertEqual(str(user), expected)

    def test_username_test_user(self):
        user = CustomUser.objects.last()
        username = user.username
        self.assertEqual(username, "test_user")
        self.assertNotEqual(username, "Abraham")

    def test_email_test_krk12(self):
        user = CustomUser.objects.last()
        email = user.email
        self.assertEqual(email, "krk12@wp.pl")
        self.assertNotEqual(email, "Abraham@wp.pl")

    def test_pesel_test_12345678911(self):
        user = CustomUser.objects.last()
        pesel = user.pesel
        self.assertEqual(pesel, "12345678911")
        self.assertNotEqual(pesel, "19995678911")

    def test_bank_account_test_1234756890123456789123450(self):
        user = CustomUser.objects.last()
        bank_account = user.bank_account
        self.assertEqual(bank_account, "1234756890123456789123450")
        self.assertNotEqual(bank_account, "1234756890123456789098765")

    def test_secondary_email_test_walmart(self):
        user = CustomUser.objects.last()
        secondary_email = user.secondary_email
        self.assertEqual(secondary_email, "walmart@wp.pl")
        self.assertNotEqual(secondary_email, "qwer@wp.pl")

    def test_address_test_new_york(self):
        user = CustomUser.objects.last()
        address = user.address
        self.assertEqual(address, "New York")
        self.assertNotEqual(address, "Yorktown")

    def test_postal_code_test_32_576(self):
        user = CustomUser.objects.last()
        postal_code = user.postal_code
        self.assertEqual(postal_code, "32-576")
        self.assertNotEqual(postal_code, "888888")

    def test_role_test_2(self):
        user = CustomUser.objects.last()
        role = user.role
        self.assertEqual(role, 2)
        self.assertNotEqual(role, 3)

    def test_reviews_test_3_5(self):
        user = CustomUser.objects.last()
        reviews = user.reviews
        self.assertEqual(reviews, 3.5)
        self.assertNotEqual(reviews, 5.0)
