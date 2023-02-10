import config

DB_NAME = config.config['db']
TABLE_NAME = config.table_name

create_db = f"""
    CREATE DATABASE IF NOT EXISTS {DB_NAME} 
"""

show_tables = 'SHOW TABLES'

create_table = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
        id INT AUTO_INCREMENT PRIMARY KEY,
        type VARCHAR(1) NOT NULL,
        added DATE NOT NULL,
        genre VARCHAR(30) NOT NULL,
        language VARCHAR(10) NOT NULL,
        author VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        started DATE,
        finished DATE,
        page_nb INT NOT NULL,
        importance INT NOT NULL,
        added_to_db TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""
add_data = f"""
INSERT INTO {TABLE_NAME}(
    type,
    added,
    genre,
    language,
    author,
    name,
    started,
    finished,
    page_nb,
    importance)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

create_genre_weight_table = """
    CREATE TABLE IF NOT EXISTS genre_weight(
        id INT AUTO_INCREMENT PRIMARY KEY,
        genre VARCHAR(30) NOT NULL,
        weight FLOAT NOT NULL
        );
"""
add_data_to_gw_table = """
INSERT INTO genre_weight(
    genre,
    weight)
    VALUES
    (%s, %s);
"""

select_top_books = """
    WITH Weights AS (
        SELECT 
            id,
            name,
            author,
            DATEDIFF(NOW(), added)/
                (SELECT MAX(DATEDIFF(NOW(), added)) AS date_par FROM books WHERE YEAR(finished) <= 1900) AS date_par,
            (SELECT MIN(page_nb) FROM books WHERE YEAR(finished) <= 1900)/page_nb AS page_par,
            importance/3 AS importance_par,
            (SELECT weight FROM genre_weight WHERE genre_weight.genre = books.genre)/3 AS genre_par
        FROM books
        WHERE YEAR(finished) <= 1900)
    
    SELECT id, name, author, ROUND((date_par + page_par + importance_par + genre_par)/4, 4) AS score
    FROM Weights
    ORDER BY score DESC
    LIMIT 5
"""

select_average_data_by_category = """
WITH temp AS 
	(SELECT
		COALESCE(NULLIF(genre, ''), 'TOTAL') AS genre,
		AVG(DATEDIFF(finished, started)+1) AS average_time,
		AVG(page_nb) AS average_page,
		ROUND(AVG(page_nb)/AVG(DATEDIFF(finished, started)+1), 4) AS average_page_by_day
	FROM books
	WHERE
		YEAR(finished) > 1900
	AND
		DATEDIFF(finished, started)+1 < 180
	GROUP BY genre WITH ROLLUP)

SELECT * 
FROM temp
ORDER BY genre='TOTAL' DESC, average_page_by_day DESC
"""

get_read = f"""
    UPDATE {TABLE_NAME}
    SET
        finished = %s,
        added_to_db = CURRENT_TIMESTAMP()
    WHERE
        id = %s
"""

get_started = f"""
    UPDATE {TABLE_NAME}
    SET
        started = %s,
        added_to_db = CURRENT_TIMESTAMP()
    WHERE
        id = %s
"""

add_log_message = f"""
    INSERT INTO users(
        user_id,
        access_level,
        username,
        first_name,
        language_code,
        chat_id,
        chat_type,
        message_id,
        content_type,
        text
    )
    VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

create_buttons_db = f"""
    CREATE TABLE IF NOT EXISTS buttons(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        type VARCHAR(12) NOT NULL,
        handler VARCHAR(30) NOT NULL,
        added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) AUTO_INCREMENT = 10000;
"""

add_button = f"""
    INSERT INTO buttons(
        name,
        type,
        handler
    )
    VALUES (%s, %s, %s)
"""

add_translation = """
        INSERT INTO translations(
        type,
        lang_ru,
        lang_fr,
        lang_en,
        lang_es
    )
    VALUES (%s, %s, %s, %s, %s)
"""

select_books_for_pagination = f"""
    SELECT id, author, name
    FROM books
    WHERE 
        YEAR(started) < 1900
		AND YEAR(finished) < 1900
    LIMIT 10 OFFSET %s
"""

select_books_nb_non_read = """
    SELECT COUNT(*) as count
    FROM books
    WHERE
        YEAR(started) < 1900
		AND 
		YEAR(finished) < 1900
"""

queries = {
    'create_db': create_db,
    'show_tables': show_tables,
    'create_table': create_table,
    'add_data': add_data,
    'create_genre_weight_table': create_genre_weight_table,
    'add_data_to_gw_table': add_data_to_gw_table,
    'select_top_books': select_top_books,
    'get_read': get_read,
    'get_started': get_started,
    'select_average_data_by_category': select_average_data_by_category,
    'add_log_message': add_log_message,
    'create_buttons_db': create_buttons_db,
    'add_button': add_button,
    'add_translation':add_translation,
    'select_books_for_pagination': select_books_for_pagination,
    'select_books_nb_non_read': select_books_nb_non_read,

}
