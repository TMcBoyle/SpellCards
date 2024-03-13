import re
import pandas as pd

def load_card_data(file: str):
    spell_data = pd.read_csv(file)
    spell_data.columns = spell_data.columns.str.replace(" ", "_").str.lower()
    spell_data = spell_data.rename(columns={ "reaction_condition": "reaction", "reviseddescription": "rules" })
    spell_data = spell_data.loc[:, ~spell_data.columns.str.contains('^unnamed')]
    spell_data["reaction"] = spell_data["reaction"].astype(str).str.replace("nan", "")
    spell_data["materials"] = spell_data["materials"].astype(str).str.replace("nan", "")
    spell_data["verbal"] = spell_data.apply(lambda x: 'V' in x.components, axis=1)
    spell_data["somatic"] = spell_data.apply(lambda x: 'S' in x.components, axis=1)
    spell_data["material"] = spell_data.apply(lambda x: 'M' in x.components, axis=1)
    spell_data["level"] = spell_data["level"].str.slice(0, 1)
    spell_data["rules"] = spell_data["rules"].fillna(spell_data["description"])

    # Attempt to remove extra spaces
    spell_data["reaction"] = spell_data["reaction"].apply(lambda x: re.sub(r'(^|\s)([B-HJ-Zb-hj-z]) +(.)', r' \2\3', x))
    spell_data["reaction"] = spell_data["reaction"].apply(lambda x: re.sub(r'(\w) (ed) ', r'\1\2 ', x))
    spell_data["materials"] = spell_data["materials"].apply(lambda x: re.sub(r'(^|\s)([B-HJ-Zb-hj-z]) +(.)', r' \2\3', x))
    spell_data["materials"] = spell_data["materials"].apply(lambda x: re.sub(r'(\w) (ed) ', r'\1\2 ', x))
    spell_data["rules"] = spell_data["rules"].apply(lambda x: re.sub(r'(^|\s)([B-HJ-Zb-hj-z]) +(.)', r' \2\3', x))
    spell_data["rules"] = spell_data["rules"].apply(lambda x: re.sub(r'(\w) (ed) ', r'\1\2 ', x))

    # Change certain descriptions
    spell_data["range"] = spell_data["range"].apply(lambda x: re.sub(r'[Ss] ?elf \((.*)\)', r'\1', x))
    spell_data["rules"] = spell_data["rules"].apply(lambda x: re.sub(r'\n\-', r'\n•', x))
    spell_data["duration"] = spell_data["duration"].str.replace("Instantaneous", "Instant")
    spell_data["duration"] = spell_data["duration"].str.replace("up to ", "")
    spell_data["duration"] = spell_data["duration"].str.replace("Until dispelled", "Unlimited")

    spell_data = spell_data.drop(["simplified_name", "roll_type", "description", "components"], axis=1)
    return spell_data
