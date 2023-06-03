import random
import re
import unicodedata
from faker import Faker
import itertools

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def conditional_fake(cond, country):
    fake = Faker(country)
    freemails = []
    if country == 'fr_FR':
        freemails = ["@laposte.net", "@orange.fr", "@free.fr", "@sfr.fr", "@bbox.fr", "@numericable.fr", "@aliceadsl.fr", "@neuf.fr", "@gmail.com", "@yahoo.fr", "@hotmail.fr"]
    elif country == 'es_ES':
        freemails = ["@hotmail.es", "@yahoo.es", "@gmail.com", "@outlook.es", "@live.com", "@zonamail.com", "@telefonica.net", "@wanadoo.es", "@yahoo.com.mx", "@icloud.com", "@protonmail.com"]
    elif country == 'it_IT':
        freemails = ["@libero.it", "@yahoo.it", "@hotmail.it", "@gmail.com", "@tin.it", "@alice.it", "@virgilio.it", "@fastwebnet.it", "@tiscali.it", "@live.it", "@vodafone.it"]
    elif country == 'en_GB':
        freemails = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com", "@aol.com", "@icloud.com", "@protonmail.com", "@mail.com", "@zoho.com", "@yandex.com", "@gmx.com"]

    while True:
        full_name = fake.name()
        if cond(full_name):
            first_name, last_name = full_name.lower().split()
            email_formats = [f'{first_name[0]}.{last_name}', f'{first_name}.{last_name}']
            email_address = random.choice(email_formats)
            email_address = re.sub(r'[^a-zA-Z0-9._-]', lambda m: remove_accents(m.group()), email_address)
            freemail = random.choice(freemails)
            random_number = random.choice([None, random.randint(0, 9),
                                           random.randint(10, 99), random.randint(100, 999)])
            if random_number is not None:
                email_parts = email_address.split('@')
                email_parts[0] += str(random_number)
                email_address = '@'.join(email_parts)
            yield email_address + freemail

def generate_emails(country):
    emails = []
    for generated_email in itertools.islice(conditional_fake(lambda name: len(name) == 10, country), 50):
        emails.append(generated_email)
    return emails
