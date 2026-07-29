import re

# -----------------------------
# Entity Dictionary
# -----------------------------

ENTITY_PATTERNS = {

    "course": {
        "b.sc ai": "B.Sc AI",
        "bsc ai": "B.Sc AI",
        "artificial intelligence": "B.Sc AI",
        "ai": "B.Sc AI",

        "bca": "BCA",
        "mca": "MCA",

        "data science": "Data Science"
    },

    "admission": {
        "apply": "application",
        "application": "application",
        "admission": "general",

        "deadline": "deadline",
        "last date": "deadline",

        "international": "international",

        "status": "status",
        "open": "status"
    },

    "eligibility": {

        "eligibility": "general",
        "eligible": "general",
        "who can apply": "general",
        "qualification": "general",
        "criteria": "general"

    },

    "fees": {

        "fee": "general",
        "fees": "general",
        "payment": "payment",
        "hostel fee": "hostel"

    },

    "hostel": {

        "boys": "boys",
        "girls": "girls",
        "hostel": "facilities",

        "mess": "facilities",
        "laundry": "facilities",
        "wifi": "facilities"

    },

    "scholarship": {

        "merit": "merit",
        "government": "government",
        "sports": "sports",
        "girls": "girls"

    },

    "placement": {

        "placement": "statistics",
        "placement rate": "statistics",

        "recruiters": "recruiters",
        "companies": "recruiters",

        "highest": "highest",
        "average": "average",

        "internship": "internship"

    },

    "documents": {

        "documents": "admission",
        "document": "admission",

        "aadhaar": "identity",
        "identity": "identity",
        "id": "identity"

    },

    "contact": {

        "office": "office",
        "website": "website",
        "contact": "admission",
        "helpline": "admission"

    },

    "facilities": {

        "library": "library",
        "lab": "lab",
        "transport": "transport",
        "bus": "transport",

        "medical": "medical",

        "sports": "sports",

        "wifi": "wifi",

        "cafeteria": "cafeteria",

        "club": "clubs",
        "clubs": "clubs"

    }

}


# -----------------------------
# Entity Extraction
# -----------------------------

def extract_entity(query):

    query = query.lower()

    for category in ENTITY_PATTERNS:

        for keyword, entity in ENTITY_PATTERNS[category].items():

            if re.search(r"\b" + re.escape(keyword) + r"\b", query):

                return entity

    return "general"

if __name__ == "__main__":

    while True:

        q = input("\nQuery: ")

        if q.lower() == "exit":
            break

        print("Entity:", extract_entity(q))