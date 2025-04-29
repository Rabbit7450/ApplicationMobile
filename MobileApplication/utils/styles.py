from kivy.utils import get_color_from_hex

# Paleta de colores
COLORS = {
    'primary': get_color_from_hex('#2196F3'),  # Azul principal
    'primary_dark': get_color_from_hex('#1976D2'),  # Azul oscuro
    'accent': get_color_from_hex('#FF4081'),  # Rosa acento
    'background': get_color_from_hex('#F5F5F5'),  # Fondo gris claro
    'text_primary': get_color_from_hex('#212121'),  # Texto principal
    'text_secondary': get_color_from_hex('#757575'),  # Texto secundario
    'white': get_color_from_hex('#FFFFFF'),  # Blanco
    'success': get_color_from_hex('#4CAF50'),  # Verde éxito
    'warning': get_color_from_hex('#FFC107'),  # Amarillo advertencia
    'error': get_color_from_hex('#F44336'),  # Rojo error
}

# Estilos de texto
TEXT_STYLES = {
    'title': {
        'font_size': '24sp',
        'color': COLORS['text_primary'],
        'bold': True
    },
    'subtitle': {
        'font_size': '18sp',
        'color': COLORS['text_secondary']
    },
    'button': {
        'font_size': '16sp',
        'color': COLORS['white']
    }
}

# Estilos de botones
BUTTON_STYLES = {
    'primary': {
        'background_color': COLORS['primary'],
        'background_normal': '',
        'size_hint_y': None,
        'height': '50dp'
    },
    'accent': {
        'background_color': COLORS['accent'],
        'background_normal': '',
        'size_hint_y': None,
        'height': '50dp'
    }
}

# Estilos de tarjetas
CARD_STYLES = {
    'default': {
        'size_hint_y': None,
        'height': '100dp',
        'padding': [15, 15, 15, 15],
        'spacing': 10
    }
} 