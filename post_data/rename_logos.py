import os

club_list = [
    "Atalanta",
    "Bologna",
    "Cremonese",
    "Empoli",
    "Spezia",
    "Fiorentina",
    "Verona",
    "Inter",
    "Juventus",
    "Lazio",
    "Lecce",
    "Milan",
    "Monza",
    "Napoli",
    "Roma",
    "Salernitana",
    "Sampdoria",
    "Sassuolo",
    "Torino",
    "Udinese",
]

logos_dir = (
    r"C:\Users\andreas\Documents\Projects\football_data_api\post_data\logos_to_upload"
)


def partial(lst, query):
    return [s for s in lst if query in s]


list_logos = os.listdir(logos_dir)

for index, club in enumerate(club_list):
    if partial(list_logos, club.lower()):
        logo = partial(list_logos, club.lower())[0]
        logo_new_name = logo.split(".")
        logo_new_name[0] = str(index + 21)
        logo_new_name = ".".join(logo_new_name)
        print(logo)
        print(logo_new_name)
        os.rename(os.path.join(logos_dir, logo), os.path.join(logos_dir, logo_new_name))
