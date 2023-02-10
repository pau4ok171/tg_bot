from command import CommandManager

cm = CommandManager()

def add_button_to_db():
    buttons = [
        ['calender_cancel', 'MENU', 'other'],
        ['calender_home', 'MENU', 'other'],
        ['/home', 'MENU', 'other'],
        ['common_stats', 'MENU', 'other'],
        ['stats_by_category', 'MENU', 'client'],
        ['stats_by_language', 'MENU', 'client'],
        ['stats_by_category_and_lang', 'MENU', 'client'],
        ['to_read', 'MENU', 'client'],
        ['panel', 'MENU', 'admin'],
        ['mark_read', 'MENU', 'admin'],
        ['books_nb', 'INFO', 'client'],
        ['read_books_nb', 'INFO', 'client'],
        ['books_by_category', 'INFO', 'client'],
        ['read_by_category', 'INFO', 'client'],
        ['average_data_by_category', 'INFO', 'client'],
        ['books_by_language', 'INFO', 'client'],
        ['read_by_language', 'INFO', 'client'],
        ['books_by_category_and_lang', 'INFO', 'client'],
        ['top_books', 'INFO', 'client'],
        ['unique_users', 'INFO', 'admin'],
        ['confirm_get_finished_book', 'ACTION', 'other'],
        ['decline_get_finished_book', 'MENU', 'other'],

    ]

    translations = [
        ['button', 'К книгам', 'Aux livres', 'To books', 'A los libros'],
        ['button', 'Домой', 'Accueil', 'Home', 'Portada'],
        ['button', 'Вернуться назад', 'Retour', 'Back', 'Volver'],
        ['button', 'Общая статистика', 'Stats générales', 'General stats', 'Estadísticas Generales'],
        ['button', 'По категориям', 'Par catégories', 'By categories', 'Por categorias'],
        ['button', 'По языкам', 'Par langues', 'By languages', 'Por idiomas'],
        ['button', 'По категориям и языкам', 'Par catégories et langues', 'By categories and languages',
         'Por categorías e idiomas'],
        ['button', 'Что почитать', 'Que lire', 'What to read', 'Qué leer'],
        ['button', 'Панель Админа', 'Panneau d\'admin', 'Admin Panel', 'Panel de admin'],
        ['button', 'Отметить прочитанной', 'Marquer comme lu', 'Mark as read', 'Marcar como leído'],
        ['button', 'Всего книг', 'Nombre total de livres', 'Total books', 'Total de libros'],
        ['button', 'Прочитано книг', 'Livres lus', 'Books read', 'Libros leidos'],
        ['button', 'Всего', 'En total', 'Total', 'Total'],
        ['button', 'Прочитанных', 'Lus', 'Read', 'Leidos'],
        ['button', 'В среднем', 'En moyenne', 'On average', 'Promedio'],
        ['button', 'ТОП-5 книг', 'TOP-5 livres', 'TOP-5 books', 'TOP-5 libros'],
        ['button', 'Уникальные пользователи', 'Utilisateurs uniques', 'Unique users', 'Usuarios únicos'],
        ['button', 'Да', 'Oui', 'Yes', 'Sí'],
        ['button', 'Нет', 'Non', 'No', 'No'],

    ]

    new_trans = [
        # type, ru, fr, en, es
        ['text', 'Выберете дату окончания чтения', 'Sélectionne la date de fin de lecture', 'Select the end date of reading', 'Seleccione la fecha de finalización de la lectura'],
        ['text', 'Какую книгу нужно отметить?', 'Quel livre tu veux marquer comme lu?', 'Which book should be noted?', '¿Qué libro se debe marquarse?'],
        ['text', 'Панель администратора', 'Panneau d\'administration', 'Admin panel', 'Panel de administración'],
        ['text', 'Привет', 'Bonjour', 'Hello', 'Hola'],
        ['text', 'Добро пожаловать', 'Bienvenue', 'Welcome', 'Bienvenido.a'],
        ['text', 'Выбери нужную вкладку', 'Sélectionne l\'onglet souhaité', 'Select the desired tab', 'Seleccione la pestaña deseada'],
        ['text', 'Пожалуйста, пропишите /start чтобы начать', 'Veuillez taper /start pour commencer', 'Please type /start to start', 'Escriba /start to start'],
        ['text', 'Общая статистика', 'Statistiques générales', 'General statistics', 'Estadísticas generales'],
        ['text', 'Всего книг', 'Total de livres', 'Total books', 'Total de libros'],
        ['text', 'Всего прочитано книг', 'Total de livres lus', 'otal books read', 'Total de libros leídos'],
        ['text', 'Статистика по категориям', 'Statistiques par catégorie', 'Statistics by category', 'Estadísticas por categoría'],
        ['text', 'Всего книг по категориям', 'Total de livres par catégorie', 'Total books by category', 'Total de libros por categoría'],
        ['text', 'Прочитано по категориям', 'Lu par catégorie', 'Read by category', 'Leídos por categoría'],
        ['text', 'Средние значения по категориям', 'Moyennes par catégorie', 'Averages by category', 'Promedios por categoría'],
        ['text', 'Статистика по языкам', 'Statistiques linguistiques', 'Statistics by language', 'Estadísticas por idioma'],
        ['text', 'Всего книг по языка', 'Total de livres par langue', 'Total books by language', 'Total de libros por idioma'],
        ['text', 'Прочитано книг по языкам', 'Livres lus par langue', 'Books read by language', 'Libros leídos por idiomas'],
        ['text', 'Статистика по категориям и языкам', 'Statistiques par catégorie et langue', 'Statistics by category and language', 'Estadísticas por categoría e idioma'],
        ['text', 'Всего книг по категориям и языкам', 'Total de livres par catégorie et langue', 'Total books by category and language', 'Total de libros por categoría e idioma'],
        ['text', 'Вот список', 'Voici la liste', 'Here is the list', 'Aquí está la lista'],
        ['text', 'Выберите вкладку', 'Sélectionne l\'onglet', 'Select the tab', 'Selecciona la pestaña'],
        ['text', 'Выберете', 'Sélectionne', 'Select', 'Selecciona'],
        ['text', 'Книга, которую вы хотите отметить', 'Livre que vous souhaitez marquer', 'Book you want to mark', 'Libro que quieres marca'],
        ['text', 'Дата прочтения', 'Date de lecture', 'Date of read', 'Fecha de lectura'],
        ['text', 'Подтвердить?', 'Confirmer ?', 'Confirm?', '¿Confirmar?'],
        ['text', 'Данные успешно обновлены', 'Données sont mises à jour avec succès', 'Data updated successfully', 'Datos actualizados con éxito'],

    ]

    for translation in new_trans:
        # ПРОВЕРИТЬ ПРАВИЛЬНОСТЬ QUERY!!!
        cm.get_execute_query(tuple(translation))

add_button_to_db()