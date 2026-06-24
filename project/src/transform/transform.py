import pandas as pd
import logging
import re
import os
import datetime

def rename_columns_snake_case(df: pd.DataFrame) -> pd.DataFrame:
    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Entrada deve ser um DataFrame")

        df.columns = [re.sub(r'(?<!^)(?=[A-Z])', '_', col).lower() for col in df.columns]
        return df

    except Exception as e:
        logging.error(f"Falha ao renomear colunas para snake_case: {e}")
        return df

def rename_columns_ptbr(dict_df: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    try:
        col_map = {
            "id": "id_animal",
            "intakedate": "data_entrada",
            "intakereason": "motivo_entrada",
            "istransfer": "transferencia",
            "sheltercode": "codigo_abrigo",
            "identichipnumber": "numero_microchip",
            "animalname": "nome_animal",
            "breedname": "raca",
            "basecolour": "cor_base",
            "speciesname": "especie",
            "animalage": "idade_animal",
            "sexname": "sexo",
            "location": "localizacao",
            "movementdate": "data_movimentacao",
            "movementtype": "tipo_movimentacao",
            "istrial": "adocao_teste",
            "returndate": "data_retorno",
            "returnedreason": "motivo_retorno",
            "deceaseddate": "data_obito",
            "deceasedreason": "motivo_obito",
            "diedoffshelter": "morreu_fora_do_abrigo",
            "puttosleep": "eutanasiado",
            "isdoa": "morto_ao_chegar"
        }

        for key, df in dict_df.items():
            dict_df[key] = df.rename(columns=col_map)
            logging.info(f"Colunas renomeadas no DataFrame '{key}'.")

    except Exception as e:
        logging.error(f"Erro ao renomear colunas nos DataFrames: {e}")

    return dict_df

def translate_categorical_columns(df) -> pd.DataFrame:
    try:
        translations = {
            "intakereason": {
                "Abandoned": "Abandonado",
                "Abuse/ neglect": "Abuso / Negligencia",
                "Allergies": "Alergias",
                "Behavioral Issues": "Problemas Comportamentais",
                "Biting": "Mordedura",
                "Born in Shelter": "Nascido no Abrigo",
                "DOA": "Morto ao Chegar",
                "Incompatible with other pets": "Incompativel com Outros Animais",
                "Incompatible with owner lifestyle": "Incompativel com Estilo de Vida do Tutor",
                "Injured Wildlife": "Animal Silvestre Ferido",
                "Landlord issues": "Problemas com Proprietario do Imovel",
                "Litter relinquishment": "Entrega de Ninhada",
                "Marriage/Relationship split": "Separacao / Divorcio",
                "Moving": "Mudança",
                "Owner Deceased": "Tutor Falecido",
                "Owner Died": "Tutor Faleceu",
                "Owner requested Euthanasia": "Eutanasia Solicitada pelo Tutor",
                "Police Assist": "Apoio Policial",
                "Rabies Monitoring": "Monitoramento de Raiva",
                "Sick/Injured": "Doente / Ferido",
                "Stray": "Animal Errante",
                "TNR - Trap/Neuter/Release": "Captura / Castracao / Soltura (TNR)",
                "Transfer from Other Shelter": "Transferencia de Outro Abrigo",
                "Unable to Afford": "Incapacidade Financeira",
                "Unsuitable Accommodation": "Moradia Inadequada"
            },

            "basecolour": {
                "Apricot": "Damasco",
                "Black": "Preto",
                "Black Tortie": "Preto Tartaruga",
                "Black and Brindle": "Preto e Tigrado",
                "Black and Brown": "Preto e Marrom",
                "Black and Tan": "Preto e Castanho",
                "Black and White": "Preto e Branco",
                "Black and grey": "Preto e Cinza",
                "Black merle": "Preto Merle",
                "Black, Brown and White": "Preto, Marrom e Branco",
                "Blue": "Azul",
                "Blue Point": "Azul Point",
                "Blue merle": "Azul Merle",
                "Brindle": "Tigrado",
                "Brindle and Black": "Tigrado e Preto",
                "Brindle and White": "Tigrado e Branco",
                "Brown": "Marrom",
                "Brown and Black": "Marrom e Preto",
                "Brown and White": "Marrom e Branco",
                "Brown, Black and White": "Marrom, Preto e Branco",
                "Buff": "Bege",
                "Buff and white": "Bege e Branco",
                "Calico": "Cálico",
                "Chocolate": "Chocolate",
                "Chocolate Point": "Chocolate Point",
                "Cinnamon": "Canela",
                "Cream": "Creme",
                "Dilute calico": "Calico Diluido",
                "Dilute tortoiseshell": "Tartaruga Diluida",
                "Fawn": "Fulvo",
                "Flame Point": "Flame Point",
                "Golden": "Dourado",
                "Green": "Verde",
                "Grey": "Cinza",
                "Grey Black and White": "Cinza, Preto e Branco",
                "Grey and White": "Cinza e Branco",
                "Grey and black": "Cinza e Preto",
                "Lilac": "Lilas",
                "Lilac Point": "Lilas Point",
                "Liver": "Marrom Figado",
                "Liver and White": "Figado e Branco",
                "Lynx point": "Lynx Point",
                "Orange": "Laranja",
                "Orange and White": "Laranja e Branco",
                "Red": "Vermelho",
                "Red and Black": "Vermelho e Preto",
                "Red and White": "Vermelho e Branco",
                "Red merle": "Vermelho Merle",
                "Ruddy": "Ruddy",
                "Seal": "Seal",
                "Seal Point": "Seal Point",
                "Silver": "Prata",
                "Siver and Black": "Prata e Preto",
                "Siver and Tan": "Prata e Castanho",
                "Smoke": "Fume",
                "Tabbico": "Tabbico",
                "Tabby": "Rajado",
                "Tabby and White": "Rajado e Branco",
                "Tan": "Castanho",
                "Tan and Black": "Castanho e Preto",
                "Tan and Brown": "Castanho e Marrom",
                "Tan and White": "Castanho e Branco",
                "Torbie": "Torbie",
                "Tortie": "Tartaruga",
                "Tortie Point": "Tartaruga Point",
                "Tortie and White": "Tartaruga e Branco",
                "Tricolour": "Tricolor",
                "Various": "Variado",
                "White": "Branco",
                "White and Black": "Branco e Preto",
                "White and Brindle": "Branco e Tigrado",
                "White and Brown": "Branco e Marrom",
                "White and Grey": "Branco e Cinza",
                "White and Liver": "Branco e Fígado",
                "White and Orange": "Branco e Laranja",
                "White and Tabby": "Branco e Rajado",
                "White and Tan": "Branco e Castanho",
                "Yellow": "Amarelo"
            },

            "speciesname": {
                "Bird": "Ave",
                "Cat": "Gato",
                "Chicken": "Galinha",
                "Chinchilla": "Chinchila",
                "Dog": "Cachorro",
                "Ferret": "Furao",
                "Fish": "Peixe",
                "Gerbil": "Gerbil",
                "Goat": "Cabra",
                "Guinea Pig": "Porquinho-da-India",
                "Hamster": "Hamster",
                "Hedgehog": "Ourico",
                "House Rabbit": "Coelho Domestico",
                "Livestock": "Animal de Fazenda",
                "Lizard": "Lagarto",
                "Mouse": "Camundongo",
                "Opossum": "Gamba",
                "Pig": "Porco",
                "Raccoon": "Guaxinim",
                "Rat": "Rato",
                "Snake": "Cobra",
                "Squirrel": "Esquilo",
                "Sugar Glider": "Petauro-do-acucar",
                "Tarantula": "Tarantula",
                "Tortoise": "Tartaruga Terrestre",
                "Turtle": "Tartaruga",
                "Wildlife": "Animal Silvestre"
            },

            "sexname": {
                "Male": "Macho",
                "Female": "Femea",
                "Unknown": "Desconhecido",
            },

            "location": {
                "Adoptable Cat Big Colony": "Gatos Adotaveis, Colonia Grande",
                "Adoptable Cat Glass Colony": "Gatos Adotaveis, Colonia de Vidro",
                "Adoptable Cat Kennels": "Gatos Adotaveis, Canis",
                "Adoptable Cat Middle Colony": "Gatos Adotaveis, Colonia Média",
                "Adoptable Cat Small Colony": "Gatos Adotaveis, Colonia Pequena",
                "Adoptable Dogs": "Cães Adotaveis",
                "Adoptable window colony": "Colonia Adotavel, Janela",
                "Canine intake room": "Sala de Entrada, Caes",
                "Cat Iso": "Isolamento, Gatos",
                "Cat obs": "Observacao, Gatos",
                "Cat room A": "Sala de Gatos A",
                "Cat room B": "Sala de Gatos B",
                "Cat room C": "Sala de Gatos C",
                "Check-in": "Check-in",
                "Clinic room": "Sala da Clinica",
                "Dog room A": "Sala de Caes A",
                "Dog room B": "Sala de Caes B",
                "Dog room C": "Sala de Caes C",
                "Dog room D": "Sala de Caes D",
                "Dog room Isolation": "Isolamento, Caes",
                "Feline Nursery": "Bercario, Felinos",
                "Feline intake room": "Sala de Entrada, Felinos",
                "Food prep room": "Sala de Preparacao de Alimentos",
                "Foster": "Lar Temporario",
                "Incinerator": "Incinerador",
                "Lobby": "Recepcao",
                "MCHA-offices shelter cat": "MCHA, Escritorios, Gatos do Abrigo",
                "Office": "Escritorio",
                "Petsmart": "PetSmart",
                "Shelter": "Abrigo",
                "Small Animal room": "Sala de Pequenos Animais",
                "Special Care Cats": "Cuidados Especiais, Gatos",
                "Special Care Dogs": "Cuidados Especiais, Caes",
                "Stray Cats": "Gatos Errantes",
                "Stray Dogs Alpha": "Caes Errantes, Alfa",
                "Stray Dogs Beta": "Caes Errantes, Beta",
                "Stray Dogs Theta": "Caes Errantes, Theta",
                "Stray side Men`s restroom-Use for small animal holding-non-adoptable": "Banheiro Masculino, Area de Contencao de Pequenos Animais, Nao Adotaveis",
                "Veterinary office": "Consultorio Veterinario"
            },

            "movementtype": {
                "Adoption": "Adocao",
                "Escaped": "Fuga",
                "Foster": "Lar Temporario",
                "Reclaimed": "Recuperado pelo Tutor",
                "Released To Wild": "Solto na Natureza",
                "Stolen": "Furto",
                "Transfer": "Transferencia"
            },

            "returnedreason": {
                "Abandoned": "Abandonado",
                "Abuse/ neglect": "Abuso / Negligencia",
                "Allergies": "Alergias",
                "Behavioral Issues": "Problemas Comportamentais",
                "Biting": "Mordida",
                "DOA": "Morto ao Chegar",
                "Incompatible with other pets": "Incompativel com Outros Animais",
                "Incompatible with owner lifestyle": "Incompativel com Estilo de Vida do Tutor",
                "Landlord issues": "Problemas com Proprietario",
                "Marriage/Relationship split": "Separacao / Divorcio",
                "Moving": "Mudança",
                "Owner Deceased": "Tutor Falecido",
                "Owner requested Euthanasia": "Eutanasia Solicitada pelo Tutor",
                "Police Assist": "Apoio Policial",
                "Rabies Monitoring": "Monitoramento de Raiva",
                "Return Adopt - Animal Health": "Retorno Pos-Adocao - Saude",
                "Return Adopt - Behavior": "Retorno Pos-Adocao - Comportamento",
                "Return Adopt - Other": "Retorno Pos-Adocao - Outros",
                "Return adopt - lifestyle issue": "Retorno Pos-Adocao - Estilo de Vida",
                "Sick/Injured": "Doente / Ferido",
                "Stray": "Animal Errante",
                "Transfer from Other Shelter": "Transferencia de Outro Abrigo",
                "Unable to Afford": "Incapacidade Financeira",
                "Unsuitable Accommodation": "Moradia Inadequada"
            },

            "deceasedreason": {
                "Biting": "Mordida",
                "Court Order/ Legal": "Ordem Judicial / Determinacao Legal",
                "Dead On Arrival": "Morto ao Chegar",
                "Died in care": "Falecimento sob Cuidados",
                "Died in community": "Falecimento na Comunidade",
                "Healthy": "Saudavel",
                "Medical": "Motivo Medico",
                "Owner Requested": "Solicitacao do Tutor",
                "Sick/Injured": "Doente / Ferido",
                "TM - Treatable Manageable": "Tratavel e Gerenciavel",
                "Temperament/Behavior": "Temperamento / Comportamento",
                "UU - untreatable, unmanageable": "Intratavel / Ingerenciavel",
                "Vet advised euthanasia": "Eutanasia Recomendada pelo Veterinario"
            },


        }

        for col, mapping in translations.items():
            if col in df.columns:
                df[col] = df[col].map(mapping).fillna(df[col])
                logging.info(f"Coluna '{col}' traduzida com sucesso.")
            else:
                logging.warning(f"Coluna '{col}' não encontrada no DataFrame.")

    except Exception as e:
        logging.error(f"Erro ao traduzir colunas categóricas: {e}")

    return df

def transform_animal_age(df: pd.DataFrame) -> pd.DataFrame:

    def age_to_months(age_str):
        if pd.isna(age_str):
            return None
        age_str = str(age_str).lower()

        years = re.search(r'(\d+)\s+year', age_str)
        months = re.search(r'(\d+)\s+month', age_str)

        years = int(years.group(1)) if years else 0
        months = int(months.group(1)) if months else 0

        return years * 12 + months

    df["animalage"] = df["animalage"].apply(age_to_months)

    return df

def extract_domain_dataframes(df: pd.DataFrame) -> dict[str, pd.DataFrame]:

    try:
        animal_base = [
            "id",
            "identichipnumber",
            "animalname",
            "speciesname",
            "breedname",
            "basecolour",
            "sexname",
            "animalage"
        ]

        fluxo = [
            "id",
            "intakedate",
            "intakereason",
            "istransfer",
            "sheltercode",
            "location",
            "movementdate",
            "movementtype",
            "istrial",
            "returndate",
            "returnedreason"
        ]

        desfecho = [
            "id",
            "deceaseddate",
            "deceasedreason",
            "diedoffshelter",
            "puttosleep",
            "isdoa"
        ]

        base_df = df[[c for c in animal_base if c in df.columns]].copy()
        fluxo_df = df[[c for c in fluxo if c in df.columns]].copy()
        desfecho_df = df[[c for c in desfecho if c in df.columns]].copy()

        logging.info("Animal domain DataFrames extracted successfully.")

        return {
            "animal_base": base_df,
            "fluxo": fluxo_df,
            "desfecho": desfecho_df
        }

    except Exception as e:
        logging.error(f"Erro inesperado durante extração do DF: {e}")
        return {}

def transform_data(key: str) -> dict[str, pd.DataFrame]:

    try:
        logging.info("Iniciando transformações nos dados...")

        df = pd.read_csv(key)  # ou "data/raw/animal-data-1.csv"
        df = rename_columns_snake_case(df)
        df = transform_animal_age(df)
        df = translate_categorical_columns(df)
        dict_df_domains = extract_domain_dataframes(df)
        dict_df_domains = rename_columns_ptbr(dict_df_domains)

        for name, df_domain in dict_df_domains.items():
            transform_dir = os.path.join("data", "transform")
            os.makedirs(transform_dir, exist_ok=True)

            file_path = os.path.join(transform_dir, f"{name}.parquet")
            df_domain.to_parquet(file_path, index=False)

        logging.info("Transformações concluídas com sucesso.")
        return dict_df_domains

    except Exception as e:
        logging.error(f"Erro durante transformações: {e}")
        raise e