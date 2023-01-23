import os

club_list = [
    "ajaccio",
    "angers",
    "auxerre",
    "brest",
    "clermont",
    "lens",
    "lille",
    "lorient",
    "lyon",
    "marseille",
    "nantes",
    "nice",
    "PSG",
    "reims",
    "rennes",
    "strasbourg",
    "toulouse",
    "troyes",
]

logos_dir = (
    r"C:\Users\andreas\Documents\Projects\football_data_api\post_data\logos_to_upload"
)


def partial(lst, query):
    return [s for s in lst if query in s]


list_logos = os.listdir(logos_dir)
print(list_logos)

for index, club in enumerate(club_list):
    if partial(list_logos, club):
        logo = partial(list_logos, club)[0]
        logo_new_name = logo.split(".")
        logo_new_name[0] = str(index + 61)
        logo_new_name = ".".join(logo_new_name)
        print(logo)
        print(logo_new_name)
        os.rename(os.path.join(logos_dir, logo), os.path.join(logos_dir, logo_new_name))
