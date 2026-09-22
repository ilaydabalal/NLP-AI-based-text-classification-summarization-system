
# İLAYDA BALAL - 05.12.2025

def parse_header(line):
    """
    HTTPX kütüphanesinin ihtiyaç duyduğu,
    Python 3.13'te kaldırılan `cgi.parse_header` fonksiyonunu taklit eder.
    """
    parts = line.split(';')
    if not parts:
        return '', {}
        
    main_type = parts[0].strip().lower()
    params = {}
    
    for param in parts[1:]:
        if '=' in param:
            key, value = param.split('=', 1)
            key = key.strip().lower()
            value = value.strip().strip('"')
            params[key] = value
            
    return main_type, params
