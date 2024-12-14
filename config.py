from typing import Dict, List

# TMDb API Configuration
TMDB_API_KEY = "92b63b1f936bace16f88cc01cd4541a7"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Content Types with translations
CONTENT_TYPES = {
    "en": {
        "🎬 Movies": "movie",
        "📺 TV Shows": "tv"
    },
    "ar": {
        "🎬 الأفلام": "movie",
        "📺 المسلسلات": "tv"
    },
    "es": {
        "🎬 Películas": "movie",
        "📺 Series": "tv"
    }
}

# Available Interface Languages
INTERFACE_LANGUAGES = {
    "🇺🇸 English": "en",
    "🇸🇦 العربية": "ar",
    "🇪🇸 Español": "es"
}

# Movie Languages with translations
MOVIE_LANGUAGES: Dict[str, Dict[str, str]] = {
    "en": {
        "🇺🇸 English": "en",
        "🇸🇦 Arabic": "ar",
        "🇪🇸 Spanish": "es",
        "🇫🇷 French": "fr",
        "🇩🇪 German": "de",
        "🇮🇹 Italian": "it",
        "🇯🇵 Japanese": "ja",
        "🇰🇷 Korean": "ko",
        "🇨🇳 Chinese": "zh",
        "🇮🇳 Hindi": "hi"
    },
    "ar": {
        "🇺🇸 الإنجليزية": "en",
        "🇸🇦 العربية": "ar",
        "🇪🇸 الإسبانية": "es",
        "🇫🇷 الفرنسية": "fr",
        "🇩🇪 الألمانية": "de",
        "🇮🇹 الإيطالية": "it",
        "🇯🇵 اليابانية": "ja",
        "🇰🇷 الكورية": "ko",
        "🇨🇳 الصينية": "zh",
        "🇮🇳 الهندية": "hi"
    },
    "es": {
        "🇺🇸 Inglés": "en",
        "🇸🇦 Árabe": "ar",
        "🇪🇸 Español": "es",
        "🇫🇷 Francés": "fr",
        "🇩🇪 Alemán": "de",
        "🇮🇹 Italiano": "it",
        "🇯🇵 Japonés": "ja",
        "🇰🇷 Coreano": "ko",
        "🇨🇳 Chino": "zh",
        "🇮🇳 Hindi": "hi"
    }
}

# Movie Genres with translations
GENRES: Dict[str, Dict[str, int]] = {
    "en": {
        "Action": 28,
        "Adventure": 12,
        "Animation": 16,
        "Comedy": 35,
        "Crime": 80,
        "Documentary": 99,
        "Drama": 18,
        "Family": 10751,
        "Fantasy": 14,
        "Horror": 27,
        "Romance": 10749,
        "Science Fiction": 878,
        "Thriller": 53,
        "War": 10752
    },
    "ar": {
        "أكشن": 28,
        "مغامرة": 12,
        "رسوم متحركة": 16,
        "كوميديا": 35,
        "جريمة": 80,
        "وثائقي": 99,
        "دراما": 18,
        "عائلي": 10751,
        "خيال": 14,
        "رعب": 27,
        "رومانسي": 10749,
        "خيال علمي": 878,
        "إثارة": 53,
        "حرب": 10752
    },
    "es": {
        "Acción": 28,
        "Aventura": 12,
        "Animación": 16,
        "Comedia": 35,
        "Crimen": 80,
        "Documental": 99,
        "Drama": 18,
        "Familia": 10751,
        "Fantasía": 14,
        "Terror": 27,
        "Romance": 10749,
        "Ciencia ficción": 878,
        "Suspense": 53,
        "Guerra": 10752
    }
}

# TV Show Genres with translations
TV_GENRES: Dict[str, Dict[str, int]] = {
    "en": {
        "Action & Adventure": 10759,
        "Animation": 16,
        "Comedy": 35,
        "Crime": 80,
        "Documentary": 99,
        "Drama": 18,
        "Family": 10751,
        "Kids": 10762,
        "Mystery": 9648,
        "Reality": 10764,
        "Sci-Fi & Fantasy": 10765,
        "Soap": 10766,
        "Talk": 10767,
        "War & Politics": 10768
    },
    "ar": {
        "أكشن ومغامرة": 10759,
        "رسوم متحركة": 16,
        "كوميديا": 35,
        "جريمة": 80,
        "وثائقي": 99,
        "دراما": 18,
        "عائلي": 10751,
        "أطفال": 10762,
        "غموض": 9648,
        "واقعي": 10764,
        "خيال علمي وخيال": 10765,
        "مسلسل يومي": 10766,
        "حواري": 10767,
        "حرب وسياسة": 10768
    },
    "es": {
        "Acción y Aventura": 10759,
        "Animación": 16,
        "Comedia": 35,
        "Crimen": 80,
        "Documental": 99,
        "Drama": 18,
        "Familia": 10751,
        "Niños": 10762,
        "Misterio": 9648,
        "Reality": 10764,
        "Ciencia Ficción y Fantasía": 10765,
        "Telenovela": 10766,
        "Talk Show": 10767,
        "Guerra y Política": 10768
    }
}

# Button texts
BUTTON_TEXTS = {
    "en": {
        "get_another": "Get Another Similar",
        "start_over": "Start Over",
        "watch_now": "🎬 Watch Now"
    },
    "ar": {
        "get_another": "احصل على توصية مشابهة",
        "start_over": "ابدأ من جديد",
        "watch_now": "🎬 شاهد الآن"
    },
    "es": {
        "get_another": "Obtener Otro Similar",
        "start_over": "Empezar de Nuevo",
        "watch_now": "🎬 Ver Ahora"
    }
}

# URLs
WATCH_URL = "https://vidsrc.to/embed/movie/{tmdb_id}"

# Messages
MESSAGES = {
    "en": {
        "welcome": "Welcome to Entertainment Recommendation Bot!\nPlease select your preferred language:",
        "select_content": "What would you like to watch?",
        "select_language": "Please select the content language:",
        "select_genre": "Please select your preferred genre:",
        "enter_year": "Please enter the year range (e.g., 1990-2023):",
        "invalid_year": "Invalid year range format. Please use format: YYYY-YYYY (e.g., 1990-2023)",
        "no_content": "No content found matching your criteria. Please try different preferences.",
        "what_next": "What would you like to do next?",
        "no_more": "No more recommendations found. Would you like to start over?"
    },
    "ar": {
        "welcome": "مرحباً بك في روبوت توصية المحتوى الترفيهي!\nالرجاء اختيار لغتك المفضلة:",
        "select_content": "ماذا تريد أن تشاهد؟",
        "select_language": "الرجاء اختيار لغة المحتوى:",
        "select_genre": "الرجاء اختيار النوع المفضل:",
        "enter_year": "الرجاء إدخال نطاق السنوات (مثال: 1990-2023):",
        "invalid_year": "تنسيق نطاق السنوات غير صالح. يرجى استخدام التنسيق: YYYY-YYYY (مثال: 1990-2023)",
        "no_content": "لم يتم العثور على محتوى يطابق معاييرك. يرجى تجربة تفضيلات مختلفة.",
        "what_next": "ماذا تريد أن تفعل بعد ذلك؟",
        "no_more": "لم يتم العثور على المزيد من التوصيات. هل تريد البدء من جديد؟"
    },
    "es": {
        "welcome": "¡Bienvenido al Bot de Recomendación de Entretenimiento!\nPor favor, seleccione su idioma preferido:",
        "select_content": "¿Qué te gustaría ver?",
        "select_language": "Por favor, seleccione el idioma del contenido:",
        "select_genre": "Por favor, seleccione su género preferido:",
        "enter_year": "Por favor, ingrese el rango de años (ejemplo: 1990-2023):",
        "invalid_year": "Formato de rango de años no válido. Utilice el formato: YYYY-YYYY (ejemplo: 1990-2023)",
        "no_content": "No se encontró contenido que coincida con sus criterios. Intente con diferentes preferencias.",
        "what_next": "¿Qué le gustaría hacer a continuación?",
        "no_more": "No se encontraron más recomendaciones. ¿Desea comenzar de nuevo?"
    }
}

# Conversation States
class States:
    SELECTING_LANGUAGE = "SELECTING_LANGUAGE"
    SELECTING_CONTENT_TYPE = "SELECTING_CONTENT_TYPE"
    SELECTING_MOVIE_LANGUAGE = "SELECTING_MOVIE_LANGUAGE"
    SELECTING_GENRE = "SELECTING_GENRE"
    SELECTING_YEAR_RANGE = "SELECTING_YEAR_RANGE"
    AWAITING_RECOMMENDATION = "AWAITING_RECOMMENDATION"
