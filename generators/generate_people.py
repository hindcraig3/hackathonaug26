"""Generate PERSON table - synthetic H&S staff at each school."""
import pandas as pd
import numpy as np
import os
from config import PERSON_ROLES, START_DATE

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')

# Synthetic NZ first names (mix of European and Maori names)
FIRST_NAMES = [
    'Aroha', 'Tane', 'Hemi', 'Mere', 'Wiremu', 'Anika', 'Rawiri', 'Moana',
    'Nikau', 'Kaia', 'Matiu', 'Aria', 'Ihaia', 'Tia', 'Kauri', 'Maia',
    'James', 'Sarah', 'Michael', 'Emma', 'David', 'Rachel', 'Andrew', 'Karen',
    'Matthew', 'Lisa', 'Daniel', 'Michelle', 'Chris', 'Donna', 'Mark', 'Paula',
    'Simon', 'Joanne', 'Grant', 'Tracey', 'Shane', 'Hayley', 'Craig', 'Stacey',
    'Ben', 'Nicola', 'Scott', 'Kylie', 'Nathan', 'Amber', 'Ryan', 'Jessica',
    'Luke', 'Holly', 'Josh', 'Brooke', 'Sam', 'Georgia', 'Jack', 'Sophie',
    'Liam', 'Charlotte', 'Mason', 'Isla', 'Ethan', 'Amelia', 'Noah', 'Olivia',
    'Reuben', 'Zara', 'Caleb', 'Freya', 'Finn', 'Ruby', 'Max', 'Grace',
]

LAST_NAMES = [
    'Thompson', 'Wilson', 'Taylor', 'Anderson', 'Campbell', 'Mitchell', 'Roberts',
    'Harris', 'Williams', 'Martin', 'Brown', 'Walker', 'Jones', 'Smith', 'King',
    'White', 'Edwards', 'Clarke', 'Wright', 'Robinson', 'Turner', 'Baker', 'Hill',
    'Te Huia', 'Tamati', 'Harawira', 'Henare', 'Mahuta', 'Rewi', 'Taukiri',
    'Patel', 'Singh', 'Kumar', 'Chen', 'Wong', 'Lee', 'Kim', 'Nguyen',
    'Morgan', 'Bennett', 'Murray', 'Scott', 'Stewart', 'Young', 'Hall', 'Green',
    'Cooper', 'Parker', 'Russell', 'Gray', 'Watson', 'Palmer', 'Henderson', 'Collins',
    'Fraser', 'Hamilton', 'Johnston', 'Crawford', 'Gallagher', 'Fitzgerald', 'Burns',
]


def generate_people(sites_df: pd.DataFrame, seed: int = 44) -> pd.DataFrame:
    """Generate 3-4 H&S staff per school."""
    rng = np.random.default_rng(seed)
    people = []
    person_id = 1

    for _, site in sites_df.iterrows():
        # Every school gets a principal and at least one other role
        num_staff = rng.integers(3, 5)  # 3-4 people
        roles = PERSON_ROLES[:num_staff]

        for role in roles:
            first = rng.choice(FIRST_NAMES)
            last = rng.choice(LAST_NAMES)
            email_domain = site['site_name'].lower().replace(' ', '').replace("'", '')[:15] + '.school.nz'
            email = f"{first.lower()}.{last.lower()}@{email_domain}"
            phone = f"02{rng.integers(1,9)}-{rng.integers(100,999)}-{rng.integers(1000,9999)}"
            start = pd.Timestamp(START_DATE) + pd.Timedelta(days=int(rng.integers(0, 1000)))

            people.append({
                'person_id': person_id,
                'site_id': site['site_id'],
                'first_name': first,
                'last_name': last,
                'role': role,
                'email': email,
                'phone': phone,
                'start_date': start.strftime('%Y-%m-%d'),
                'is_active': True,
            })
            person_id += 1

    return pd.DataFrame(people)


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sites = pd.read_csv(os.path.join(OUTPUT_DIR, 'site.csv'))
    people = generate_people(sites)
    people.to_csv(os.path.join(OUTPUT_DIR, 'person.csv'), index=False)
    print(f"Generated {len(people)} people across {len(sites)} sites")
