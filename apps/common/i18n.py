import locale

def get_locale(language):
    locale_code = locale.locale_alias.get(language)
    if locale_code:
        locale_code = locale_code.split('.')[0].replace('_', '-')
        if locale_code == "en-US":
            locale_code = "en-GB"
    return locale_code
