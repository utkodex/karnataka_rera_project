from config.config_loader import load_config

config=load_config()

sheet_link = config["sheet_info"]["sheet_link"]
subsheet_name = config["sheet_info"]["subsheet_name"]

print(sheet_link)
print(subsheet_name)