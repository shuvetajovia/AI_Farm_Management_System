import os

settings_path = r'd:\EY_4.0_AVCOE\Farm_Managemnet (2)\Farm_Managemnet\farm_management\settings.py'

with open(settings_path, 'r') as f:
    content = f.read()

if "'custom_admin'" not in content and '"custom_admin"' not in content:
    # Find the end of INSTALLED_APPS list
    marker = 'dashboard\','
    if marker in content:
        new_content = content.replace(marker, marker + "\n    'custom_admin',")
    else:
        marker = 'dashboard"'
        if marker in content:
             new_content = content.replace(marker, marker + ",\n    'custom_admin'")
        else:
             # Try a more generic approach if markers fail
             if 'INSTALLED_APPS = [' in content:
                 parts = content.split('INSTALLED_APPS = [')
                 list_part = parts[1].split(']')[0]
                 new_list_part = list_part.rstrip()
                 if not new_list_part.endswith(','):
                     new_list_part += ','
                 new_list_part += "\n    'custom_admin',\n"
                 new_content = parts[0] + 'INSTALLED_APPS = [' + new_list_part + ']' + parts[1].split(']', 1)[1]

    with open(settings_path, 'w') as f:
        f.write(new_content)
    print("Successfully added custom_admin to INSTALLED_APPS")
else:
    print("custom_admin already in INSTALLED_APPS")
