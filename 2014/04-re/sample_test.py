import unittest

import solution


class PrivacyFilterTest(unittest.TestCase):
    def test_obfuscates_simple_emails(self):
        self.assertEqual('Contact: [EMAIL]', solution.PrivacyFilter('Contact: someone@example.com').filtered())

    def test_allows_email_hostname_to_be_preserved(self):
        filter = solution.PrivacyFilter('someone@example.com')
        filter.preserve_email_hostname = True
        self.assertEqual('[FILTERED]@example.com', filter.filtered())

    def test_allows_email_usernames_to_be_partially_preserved(self):
        filter = solution.PrivacyFilter('someone@example.com')
        filter.partially_preserve_email_username = True
        self.assertEqual('som[FILTERED]@example.com', filter.filtered())

    def test_filters_phone_numbers(self):
        self.assertEqual('Reach me at: [PHONE]', solution.PrivacyFilter('Reach me at: 0885123123').filtered())

    def test_allows_country_code_to_be_preserved_for_internationally_formatted_phone_numbers(self):
        filter = solution.PrivacyFilter('Phone: +35925551212')
        filter.preserve_phone_country_code = True
        self.assertEqual('Phone: +359 [FILTERED]', filter.filtered())

class ValidationsTest(unittest.TestCase):
    def test_allows_validation_for_emails(self):
        self.assertTrue(solution.Validations.is_email('foo@bar.com'))
        self.assertFalse(solution.Validations.is_email('invalid@email'))

    def test_returns_boolean_True_or_False(self):
        self.assertTrue(solution.Validations.is_email('foo@bar.com'))
        self.assertFalse(solution.Validations.is_email('invalid@email'))

    def test_validates_phone_numbers(self):
        self.assertTrue(solution.Validations.is_phone('+35929555111'))
        self.assertFalse(solution.Validations.is_phone('123123'))

    def test_validates_hostnames(self):
        self.assertTrue(solution.Validations.is_hostname('domain.tld'))
        self.assertFalse(solution.Validations.is_hostname('not-a-hostname'))

    def test_validates_IP_addresses(self):
        self.assertTrue(solution.Validations.is_ip_address('1.2.3.4'))

    def test_validates_numbers(self):
        self.assertTrue(solution.Validations.is_number('42'))
        self.assertFalse(solution.Validations.is_number('x'))
        self.assertTrue(solution.Validations.is_number('42.42'))

    def test_validates_integers(self):
        self.assertTrue(solution.Validations.is_integer('42'))
        self.assertFalse(solution.Validations.is_integer('universe'))

    def test_validates_dates(self):
        self.assertTrue(solution.Validations.is_date('2012-11-19'))
        self.assertFalse(solution.Validations.is_date('Jamaica'))

    def test_validates_times(self):
        self.assertTrue(solution.Validations.is_time('12:00:00'))
        self.assertFalse(solution.Validations.is_time('not a time'))

    def test_validates_datetime_values(self):
        self.assertTrue(solution.Validations.is_datetime('2012-11-19 19:00:00'))
        self.assertFalse(solution.Validations.is_datetime('foo'))


if __name__ == '__main__':
    unittest.main()
