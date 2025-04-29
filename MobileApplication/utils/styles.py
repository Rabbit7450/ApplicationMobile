from kivy.utils import get_color_from_hex

# Nueva paleta de colores basada en la imagen
COLORS = {
    'primary': get_color_from_hex('#D8E3D1'),   # Verde muy claro
    'accent': get_color_from_hex('#F3F2D8'),    # Crema claro
    'secondary': get_color_from_hex('#B8AD97'), # Marrón claro
    'highlight': get_color_from_hex('#E07A3F'), # Naranja
    'background': get_color_from_hex('#F3F2D8'), # Fondo igual al crema claro
    'text_primary': get_color_from_hex('#212121'),
    'text_secondary': get_color_from_hex('#757575'),
    'white': get_color_from_hex('#FFFFFF'),
    'shadow': get_color_from_hex('#000000'),
}

# Estilos de texto
TEXT_STYLES = {
    'title': {
        'font_size': '28sp',
        'color': COLORS['text_primary'],
        'bold': True
    },
    'subtitle': {
        'font_size': '20sp',
        'color': COLORS['text_secondary']
    },
    'button': {
        'font_size': '18sp',
        'color': COLORS['white'],
        'bold': True
    }
}

# Estilos de botones usando la nueva paleta
BUTTON_STYLES = {
    'primary': {
        'background_color': COLORS['primary'],
        'background_normal': '',
        'size_hint_y': None,
        'height': '60dp',
        'font_size': '18sp',
        'bold': True
    },
    'accent': {
        'background_color': COLORS['accent'],
        'background_normal': '',
        'size_hint_y': None,
        'height': '60dp',
        'font_size': '18sp',
        'bold': True
    },
    'secondary': {
        'background_color': COLORS['secondary'],
        'background_normal': '',
        'size_hint_y': None,
        'height': '60dp',
        'font_size': '18sp',
        'bold': True
    },
    'highlight': {
        'background_color': COLORS['highlight'],
        'background_normal': '',
        'size_hint_y': None,
        'height': '60dp',
        'font_size': '18sp',
        'bold': True
    }
}

# Estilos de tarjetas
CARD_STYLES = {
    'default': {
        'size_hint_y': None,
        'height': '120dp',
        'padding': [20, 20, 20, 20],
        'spacing': 15
    }
} 