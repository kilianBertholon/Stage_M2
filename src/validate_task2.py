# ---
# jupyter:
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

""" Ce script permet de valider que la tache a bien été réalisée (ici pour 2 taches)"""

# %% 
upstream = None

# %% tags=["parameters"]
file1 = None
file2 = None



# %%
def validate_import(file1, file2):
    """ Valider que les fichiers ont bien été importés"""
    try:
        # Si les fichiers existent, considérez la validation réussie
        with open(file1, 'r'), open(file2, 'r'):
            pass
        validation_result = "Both model and tracker files are successfully imported."
        is_valid = True
    except Exception as e:
        validation_result = f"Validation failed: {str(e)}"
        is_valid = False

    return validation_result, is_valid

validation_result, is_valid = validate_import(file1,file2)
