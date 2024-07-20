from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
from faker import Faker
import random
import pandas as pd
from datetime import datetime, timedelta

# Set up Azure Blob Storage connection
AZURE_CONNECTION_STRING = "BlobEndpoint=https://zeineb.blob.core.windows.net/;QueueEndpoint=https://zeineb.queue.core.windows.net/;FileEndpoint=https://zeineb.file.core.windows.net/;TableEndpoint=https://zeineb.table.core.windows.net/;SharedAccessSignature=sv=2022-11-02&ss=bfqt&srt=co&sp=rwdlacupiytfx&se=2024-09-05T05:38:41Z&st=2024-07-15T21:38:41Z&spr=https&sig=%2BnTq1TtIfhd082WAR3Mxd%2BOXa2zG1MK2iqhVa3%2BStYM%3D"
AZURE_CONTAINER_NAME = 'dataset'  # Replace with your container name
BLOB_NAME = 'data.csv'
LOCAL_FILE_PATH = r"C:\Users\21629\Desktop\airflow\dags\data.csv"

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

try:
    container_client.create_container()
    print(f"Container '{AZURE_CONTAINER_NAME}' created successfully.")
except Exception as e:
    print(f"Container '{AZURE_CONTAINER_NAME}' already exists or there was an error: {e}")

# Check if the blob already exists
blob_client = container_client.get_blob_client(BLOB_NAME)
try:
    # Download the existing data
    with open(LOCAL_FILE_PATH, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())
    existing_data = pd.read_csv(LOCAL_FILE_PATH)
    print("Existing data downloaded successfully.")
except Exception as e:
    print(f"No existing data found or there was an error: {e}")
    existing_data = pd.DataFrame()

# Generate fake data
fake = Faker()

def generate_unique_random_dates(start_year, end_year, num_dates):
  """Generates a list of unique random dates within the specified year range.

  Args:
    start_year: The starting year.
    end_year: The ending year.
    num_dates: The number of unique dates to generate.

  Returns:
    A list of unique random dates.
  """

  start_date = datetime(start_year, 1, 1)
  end_date = datetime(end_year, 12, 31)
  total_days = (end_date - start_date).days + 1

  if num_dates > total_days:
    raise ValueError("Number of requested dates exceeds the number of days in the given range.")

  # Generate a set of unique random day offsets
  used_days = set()
  random_days = []
  while len(random_days) < num_dates:
    random_day = random.randint(0, total_days - 1)
    if random_day not in used_days:
      used_days.add(random_day)
      random_days.append(random_day)

  # Create a list of unique random dates
  unique_dates = [start_date + timedelta(days=day) for day in random_days]
  return unique_dates

def generate_project_dates(start_year, end_year):
  # Generate unique effective open date, win date, and close date
  effective_open_date, win_date, effective_close_date = generate_unique_random_dates(start_year, end_year, 3)
  return effective_open_date, win_date, effective_close_date

stage_list = ['Identify', 'Declined', 'Won', 'Pursue', 'Lost', 'Closing', 'Qualify']
SL_List = ['assurance', 'consulting', 'tax', 'sat']

assurance = ['Other Assurance', 'CCaSS', 'Audit & Governance', 'Forensics', 'Finance', 'FAAS', 'Technology Assurance', 'Audit & Governance']
consulting = ['Cybersecurity', 'Strategy & Transformation', 'Risk', 'Customer & Growth', 'Compliance and Resilience', 'Supply Chain & Operations', 'Technology', 'Sustainability', 'Technology Assurance']
tax = ['BTS', 'Law', 'Indirect', 'International Tax Transaction Services', 'PAS', 'GCR']
sat = ['Transactions & Corporate Finance', 'EY-P', 'Transactions & Corporate Finance']

Direct = ['FS', 'TMT', 'GPS', 'Private']
FS = ['Banking & Capital Markets', 'Insurance', 'Wealth & Asset Management']
TMT = ['Technology', 'Media & Entertainment', 'Telecommunications']
GPS = ['Defense', 'Health', 'Infrastructure']

afrique_countries = ['Gabon', 'Nigeria', 'Togo', 'Cameroun', 'Angola', 'Mali', 'Éthiopie', 'Soudan', 'Kenya', 'Burundi', 'Madagascar', 'Sao Tomé', 'Mauritanie', 'Maroc', 'Côte d’Ivoire', 'Djibouti', 'Algérie', 'Sénégal', 'Égypte', 'Guinée', 'Bénin', 'Lesotho', 'Burkina Faso', 'Sierra Leone', 'Comores', 'Congo Brazzaville', 'République démocratique du Congo']
asie_countries = ['Qatar', 'Liban', 'Pakistan', 'Jordanie', 'Koweït', 'Arabie saoudite', 'Émirats arabes unis']
europe_countries = ['France', 'Suisse', 'Lettonie', 'Grèce', 'Italie', 'Portugal', 'Angleterre', 'Danemark', 'Belgique', 'Luxembourg', 'Espagne', 'Allemagne', 'Russie', 'Pologne', 'Pays-Bas', 'République tchèque']
tunisia = ['Tunisie']

countries = afrique_countries + asie_countries + europe_countries + tunisia

def get_region_and_currency(country):
    if country in afrique_countries:
        return 'Afrique', 'USD'
    elif country in asie_countries:
        return 'Asie', 'USD'
    elif country in europe_countries:
        return 'Europe', 'EUR'
    elif country in tunisia:
        return 'Tunisia', 'TND'

opportunity_id = 0
generated_opportunityorg = set()
data = []

for _ in range(500):
    country = random.choice(countries)
    region, currency = get_region_and_currency(country)
    
    company = fake.company()
    MS = random.choice(Direct)
    
    if MS == 'FS':
        Client_sector = random.choice(FS)
    elif MS == 'TMT':
        Client_sector = random.choice(TMT)
    elif MS == 'GPS':
        Client_sector = random.choice(GPS)
    elif MS == 'Private':
        Client_sector = 'startup'

    sl_choice = random.choice(SL_List)

    if sl_choice == 'assurance':
        ssl_choice = random.choice(assurance)
    elif sl_choice == 'consulting':
        ssl_choice = random.choice(consulting)
    elif sl_choice == 'tax':
        ssl_choice = random.choice(tax)
    elif sl_choice == 'sat':
        ssl_choice = random.choice(sat)

    status = random.choice(stage_list)
    effective_open_date, win_date, effective_close_date = generate_project_dates(2021, 2023)
    
    if status == 'Won':
        proba_of_win = random.choice([20, 100, 5])
        PACEStatus = 'approved'
        close_date = effective_close_date
    elif status == 'Closing':
        proba_of_win = random.choice([75, 100, 5])
        PACEStatus = ''
        close_date = ''
    elif status in ['Lost', 'Declined']:
        proba_of_win = random.choice([20, 100, 5])
        PACEStatus = ''
        close_date = ''
    elif status == 'Pursue':
        proba_of_win = random.choice(range(30, 76, 5))
        PACEStatus = ''
        close_date = ''
    elif status == 'Qualify':
        proba_of_win = random.choice(range(20, 51, 5))
        PACEStatus = ''
        close_date = ''
    else:
        proba_of_win = random.choice(range(10, 21, 5))
        PACEStatus = ''
        close_date = ''

    random_float = random.uniform(50.00, 100.00)

    while True:
        random_number = random.randint(1000000, 9999999)
        opportunityorg = 'E6' + str(random_number)
        if opportunityorg not in generated_opportunityorg:
            generated_opportunityorg.add(opportunityorg)
            break

    name_opp = "{}/{}/{}".format(company, sl_choice, effective_open_date.year)
    ManagedByname = fake.name() + "%"
    identified_by_name = fake.name()
    
    opportunity_id += 1
    Company_client = f"{company}/{fake.name()}"

    data_dict = {
        'OpportunityServiceLine': sl_choice,
        'ClientSector': Client_sector,
        'AccountName': Company_client,
        'ProspectClientName': Company_client,
        'OpportunityName': fake.catch_phrase(),
        'Stage': status,
        'ProbaOfWin': proba_of_win,
        'EffectiveOpenDate': effective_open_date,
        'AnticipatedWinDate': win_date,
        'EffectiveCloseDate': close_date,
        'OpportunityPartnerName': fake.name(),
        'PursuitLeaderName': fake.name(),
        'ManagedByName': ManagedByname,
        'PursuitTeamName': fake.name(),
        'IdentifiedByName': identified_by_name,
        'PACEStatus': PACEStatus,
        'RelatedEngagements': '',
        'Currency': currency,
        'TotalValueOfPotentialSale': random_float,
        'TotalValueTND': random_float,
        'OpportunitySubSL': sl_choice,
        'OriginalOpportunityID': opportunityorg,
        'OpportunityID': f"{opportunityorg}-{opportunity_id}",
        'MS': MS,
        'SSL1': ssl_choice,
        'Country': country,
        'Region': region
    }

    data.append(data_dict)

for opportunity in data[:10]:
    print(opportunity)

for _ in range(10):
    random_index = random.randint(0, len(data) - 1)
    duplicate_data = data[random_index].copy()
    data.append(duplicate_data)

new_data = pd.DataFrame(data)

if not existing_data.empty:
    combined_data = pd.concat([existing_data, new_data], ignore_index=True)
else:
    combined_data = new_data

combined_data.to_csv(LOCAL_FILE_PATH, index=False, encoding='utf-8')

blob_client = container_client.get_blob_client(BLOB_NAME)
with open(LOCAL_FILE_PATH, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print("Data uploaded to Azure Blob Storage successfully")
