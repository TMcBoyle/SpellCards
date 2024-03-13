import card_builder
import re
import pandas as pd

spell_data = pd.read_csv("output.csv")
spell_data.columns = spell_data.columns.str.replace(" ", "_").str.lower()
spell_data = spell_data.rename(columns={"reaction_condition": "reaction", "description": "rules"})
spell_data["reaction"] = spell_data["reaction"].astype(str).str.replace("nan", "")
spell_data["materials"] = spell_data["materials"].astype(str).str.replace("nan", "")
spell_data["verbal"] = spell_data.apply(lambda x: 'V' in x.components, axis=1)
spell_data["somatic"] = spell_data.apply(lambda x: 'S' in x.components, axis=1)
spell_data["material"] = spell_data.apply(lambda x: 'M' in x.components, axis=1)
spell_data["level"] = spell_data["level"].str.slice(0, 1)

# Attempt to remove extra spaces
spell_data["reaction"] = spell_data["reaction"].apply(lambda x: re.sub(r' ([B-HJ-Zb-hj-z]) +(.)', r' \1\2', x))
spell_data["reaction"] = spell_data["reaction"].apply(lambda x: re.sub(r'(\w) (ed) ', r'\1\2 ', x))
spell_data["materials"] = spell_data["materials"].apply(lambda x: re.sub(r' ([B-HJ-Zb-hj-z]) +(.)', r' \1\2', x))
spell_data["materials"] = spell_data["materials"].apply(lambda x: re.sub(r'(\w) (ed) ', r'\1\2 ', x))
spell_data["rules"] = spell_data["rules"].apply(lambda x: re.sub(r' ([B-HJ-Zb-hj-z]) +(.)', r' \1\2', x))
spell_data["rules"] = spell_data["rules"].apply(lambda x: re.sub(r'(\w) (ed) ', r'\1\2 ', x))

spell_data = spell_data.drop(["simplified_name", "roll_type", "casters", "components"], axis=1)
spell_data

spell_dicts = spell_data.to_dict(orient="records")
for idx, s in enumerate(spell_dicts[:5]):
    spell = card_builder.Spell(**s)
    card = card_builder.Card(spell)
    card.to_svg().save_svg(f"{spell.name}.svg")
