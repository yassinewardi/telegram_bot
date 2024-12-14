import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
import requests
from config import (
    TMDB_API_KEY,
    TMDB_BASE_URL,
    INTERFACE_LANGUAGES,
    MOVIE_LANGUAGES,
    GENRES,
    TV_GENRES,
    CONTENT_TYPES,
    BUTTON_TEXTS,
    MESSAGES,
    States
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# User data storage (In production, use a proper database)
user_preferences = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Send welcome message and language selection."""
    keyboard = []
    for text, code in INTERFACE_LANGUAGES.items():
        keyboard.append([InlineKeyboardButton(text, callback_data=f"lang_{code}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(MESSAGES["en"]["welcome"], reply_markup=reply_markup)
    return States.SELECTING_LANGUAGE

async def select_interface_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Handle interface language selection."""
    query = update.callback_query
    await query.answer()
    
    selected_lang = query.data.split('_')[1]
    context.user_data['interface_language'] = selected_lang
    
    # Show content type selection keyboard
    keyboard = []
    for text, content_type in CONTENT_TYPES[selected_lang].items():
        keyboard.append([InlineKeyboardButton(text, callback_data=f"content_{content_type}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=MESSAGES[selected_lang]["select_content"],
        reply_markup=reply_markup
    )
    return States.SELECTING_CONTENT_TYPE

async def select_content_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Handle content type selection."""
    query = update.callback_query
    await query.answer()
    
    content_type = query.data.split('_')[1]
    context.user_data['content_type'] = content_type
    
    # Show movie language selection keyboard
    selected_lang = context.user_data['interface_language']
    keyboard = []
    for text, lang_code in MOVIE_LANGUAGES[selected_lang].items():
        keyboard.append([InlineKeyboardButton(text, callback_data=f"movielang_{lang_code}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=MESSAGES[selected_lang]["select_language"],
        reply_markup=reply_markup
    )
    return States.SELECTING_MOVIE_LANGUAGE

async def select_movie_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Handle movie language selection."""
    query = update.callback_query
    await query.answer()
    
    selected_lang = query.data.split('_')[1]
    context.user_data['movie_language'] = selected_lang
    
    # Show genre selection keyboard
    interface_lang = context.user_data['interface_language']
    content_type = context.user_data['content_type']
    genres = TV_GENRES[interface_lang] if content_type == 'tv' else GENRES[interface_lang]
    
    keyboard = []
    for genre, genre_id in genres.items():
        keyboard.append([InlineKeyboardButton(genre, callback_data=f"genre_{genre_id}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=MESSAGES[interface_lang]["select_genre"],
        reply_markup=reply_markup
    )
    return States.SELECTING_GENRE

async def select_genre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Handle genre selection and prompt for year range."""
    query = update.callback_query
    await query.answer()
    
    genre_id = query.data.split('_')[1]
    context.user_data['genre'] = genre_id
    
    interface_lang = context.user_data['interface_language']
    await query.edit_message_text(
        text=MESSAGES[interface_lang]["enter_year"]
    )
    return States.SELECTING_YEAR_RANGE

async def get_movie_recommendation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Get movie or TV show recommendation based on user preferences."""
    try:
        year_range = update.message.text.split('-')
        start_year, end_year = map(int, year_range)
        
        # Save user preferences
        user_id = update.effective_user.id
        user_preferences[user_id] = {
            'content_type': context.user_data['content_type'],
            'language': context.user_data['movie_language'],
            'genre': context.user_data['genre'],
            'year_range': (start_year, end_year)
        }
        
        # Get recommendation from TMDb
        content_type = context.user_data['content_type']
        params = {
            'api_key': TMDB_API_KEY,
            'language': context.user_data['movie_language'],
            'with_genres': context.user_data['genre'],
            'first_air_date.gte' if content_type == 'tv' else 'primary_release_date.gte': f"{start_year}-01-01",
            'first_air_date.lte' if content_type == 'tv' else 'primary_release_date.lte': f"{end_year}-12-31",
            'sort_by': 'popularity.desc'
        }
        
        response = requests.get(f"{TMDB_BASE_URL}/discover/{content_type}", params=params)
        results = response.json()['results']
        
        interface_lang = context.user_data['interface_language']
        if not results:
            await update.message.reply_text(
                MESSAGES[interface_lang]["no_content"]
            )
            return ConversationHandler.END
        
        item = results[0]
        title = item.get('title') if content_type == 'movie' else item.get('name')
        release_date = item.get('release_date') if content_type == 'movie' else item.get('first_air_date')
        poster_path = item.get('poster_path')
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
        
        recommendation_text = f"""
🎬 {title}
📅 {release_date[:4] if release_date else 'N/A'}
⭐ {item['vote_average']}/10

📝 {item['overview']}
"""
        
        if poster_url:
            await update.message.reply_photo(
                photo=poster_url,
                caption=recommendation_text
            )
        else:
            await update.message.reply_text(recommendation_text)
        
        # Add buttons for next actions
        keyboard = [
            [InlineKeyboardButton(BUTTON_TEXTS[interface_lang]["get_another"], callback_data="another_similar")],
            [InlineKeyboardButton(BUTTON_TEXTS[interface_lang]["start_over"], callback_data="start_over")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            MESSAGES[interface_lang]["what_next"],
            reply_markup=reply_markup
        )
        
        return States.AWAITING_RECOMMENDATION
        
    except (ValueError, IndexError):
        interface_lang = context.user_data['interface_language']
        await update.message.reply_text(
            MESSAGES[interface_lang]["invalid_year"]
        )
        return States.SELECTING_YEAR_RANGE

async def another_similar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Get another similar recommendation using the same preferences."""
    query = update.callback_query
    await query.answer()
    
    # Use existing preferences to get another recommendation
    user_id = update.effective_user.id
    prefs = user_preferences.get(user_id)
    interface_lang = context.user_data['interface_language']
    
    if not prefs:
        return await start(update, context)
    
    content_type = prefs['content_type']
    params = {
        'api_key': TMDB_API_KEY,
        'language': prefs['language'],
        'with_genres': prefs['genre'],
        'first_air_date.gte' if content_type == 'tv' else 'primary_release_date.gte': f"{prefs['year_range'][0]}-01-01",
        'first_air_date.lte' if content_type == 'tv' else 'primary_release_date.lte': f"{prefs['year_range'][1]}-12-31",
        'sort_by': 'popularity.desc',
        'page': context.user_data.get('current_page', 1) + 1
    }
    
    context.user_data['current_page'] = params['page']
    
    response = requests.get(f"{TMDB_BASE_URL}/discover/{content_type}", params=params)
    results = response.json()['results']
    
    if not results:
        keyboard = [[InlineKeyboardButton(BUTTON_TEXTS[interface_lang]["start_over"], callback_data="start_over")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=MESSAGES[interface_lang]["no_more"],
            reply_markup=reply_markup
        )
        return States.AWAITING_RECOMMENDATION
    
    item = results[0]
    title = item.get('title') if content_type == 'movie' else item.get('name')
    release_date = item.get('release_date') if content_type == 'movie' else item.get('first_air_date')
    poster_path = item.get('poster_path')
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    
    recommendation_text = f"""
🎬 {title}
📅 {release_date[:4] if release_date else 'N/A'}
⭐ {item['vote_average']}/10

📝 {item['overview']}
"""
    
    if poster_url:
        await query.message.reply_photo(
            photo=poster_url,
            caption=recommendation_text
        )
    else:
        await query.message.reply_text(recommendation_text)
    
    # Add buttons for next actions
    keyboard = [
        [InlineKeyboardButton(BUTTON_TEXTS[interface_lang]["get_another"], callback_data="another_similar")],
        [InlineKeyboardButton(BUTTON_TEXTS[interface_lang]["start_over"], callback_data="start_over")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        MESSAGES[interface_lang]["what_next"],
        reply_markup=reply_markup
    )
    
    return States.AWAITING_RECOMMENDATION

async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Start the conversation over."""
    query = update.callback_query
    await query.answer()
    
    # Clear user data
    context.user_data.clear()
    
    # Start over
    return await start(update, context)

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token("7731761670:AAEKbP9hYbqJ_5t7TZ-lCDo1Uv4RL10QnyE").build()

    # Setup conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            States.SELECTING_LANGUAGE: [
                CallbackQueryHandler(select_interface_language, pattern=r"^lang_")
            ],
            States.SELECTING_CONTENT_TYPE: [
                CallbackQueryHandler(select_content_type, pattern=r"^content_")
            ],
            States.SELECTING_MOVIE_LANGUAGE: [
                CallbackQueryHandler(select_movie_language, pattern=r"^movielang_")
            ],
            States.SELECTING_GENRE: [
                CallbackQueryHandler(select_genre, pattern=r"^genre_")
            ],
            States.SELECTING_YEAR_RANGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_movie_recommendation)
            ],
            States.AWAITING_RECOMMENDATION: [
                CallbackQueryHandler(another_similar, pattern=r"^another_similar$"),
                CallbackQueryHandler(start_over, pattern=r"^start_over$")
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
