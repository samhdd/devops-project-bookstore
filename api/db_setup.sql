-- db_setup.sql
-- Database schema for the bookstore application

-- Categories table
CREATE TABLE categories (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Products (Books) table
CREATE TABLE products (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    author VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category_id VARCHAR(50) REFERENCES categories(id),
    category VARCHAR(100),
    description TEXT,
    image_url VARCHAR(255),
    pages INTEGER,
    published INTEGER
);

-- Cart table (optional, could be managed in memory or with sessions)
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) REFERENCES products(id),
    user_id VARCHAR(100), -- Could be a session ID or user ID
    name VARCHAR(255) NOT NULL,
    author VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    image_url VARCHAR(255)
);

-- Insert initial category data
INSERT INTO categories (id, name, description) VALUES
    ('classics', 'Classics', 'Timeless masterpieces from renowned authors.'),
    ('modern', 'Modern Literature', 'Contemporary works from modern authors.'),
    ('poetry', 'Poetry', 'Beautiful poetry from literary giants.'),
    ('fiction', 'Fiction', 'Fictional works with universal appeal.'),
    ('fantasy', 'Fantasy', 'Magical and fantastical stories.'),
    ('science', 'Science', 'Scientific exploration and discovery.');

-- Insert sample books
-- Classics
INSERT INTO products (id, name, author, price, category_id, category, description, image_url, pages, published) VALUES
    ('1', 'War and Peace', 'Leo Tolstoy', 24.99, 'classics', 'Classics', 'War and Peace is a novel by Leo Tolstoy, published in 1869. It is regarded as one of Tolstoy''s finest literary achievements and remains an internationally praised classic of world literature.', '/images/books/war-and-peace-leo-tolstoy.jpg', 1225, 1869),
    ('2', 'Anna Karenina', 'Leo Tolstoy', 19.99, 'classics', 'Classics', 'Anna Karenina is a novel by Leo Tolstoy, first published in book form in 1878. Widely considered a pinnacle in realist fiction, Tolstoy himself called it his first true novel.', '/images/books/anna-karenina-leo-tolstoy.jpg', 864, 1878),
    ('3', 'Crime and Punishment', 'Fyodor Dostoevsky', 18.99, 'classics', 'Classics', 'Crime and Punishment focuses on the mental anguish and moral dilemmas of Rodion Raskolnikov, an impoverished ex-student in Saint Petersburg who formulates a plan to kill an unscrupulous pawnbroker for her money.', '/images/books/crime-and-punishment-fyodor-dostoevsky.jpg', 671, 1866);

-- Add more sample books from your mock data
INSERT INTO products (id, name, author, price, category_id, category, description, image_url, pages, published) VALUES
    ('4', 'The Idiot', 'Fyodor Dostoevsky', 17.99, 'classics', 'Classics', 'The Idiot is a novel by Fyodor Dostoevsky. It was first published serially in the journal The Russian Messenger in 1868–69. The title is an ironic reference to the central character of the novel, Prince Lev Nikolayevich Myshkin.', '/images/books/the-idiot-fyodor-dostoevsky.jpg', 652, 1869),
    ('5', 'Eugene Onegin', 'Alexander Pushkin', 15.99, 'poetry', 'Poetry', 'Eugene Onegin is a novel in verse written by Alexander Pushkin. Onegin is considered a classic of literature, and its eponymous protagonist has served as the model for a number of literary heroes.', '/images/books/eugene-onegin-alexander-pushkin.jpg', 224, 1833),
    ('6', 'Fathers and Sons', 'Ivan Turgenev', 16.99, 'classics', 'Classics', 'Fathers and Sons, also translated more literally as Fathers and Children, is an 1862 novel by Ivan Turgenev, published in Moscow by Grachev & Co. It is one of the most acclaimed novels of the 19th century.', '/images/books/fathers-and-sons-ivan-turgenev.jpg', 226, 1862),
    ('7', 'The Master and Margarita', 'Mikhail Bulgakov', 21.99, 'modern', 'Modern Literature', 'The Master and Margarita is a novel by Mikhail Bulgakov, written between 1928 and 1940 during Stalin''s regime. A censored version was published in Moscow magazine in 1966–1967, after the writer''s death.', '/images/books/master-and-margarita-mikhail-bulgakov.jpg', 384, 1967),
    ('8', 'The Lower Depths', 'Maxim Gorky', 14.99, 'classics', 'Classics', 'The Lower Depths is a play by Maxim Gorky, written in 1902. It was a sensation at the Moscow Art Theatre, and it established Gorky''s reputation as one of the leading writers.', '/images/books/the-lower-depths-maxim-gorky.jpg', 115, 1902),
    ('9', 'What Dreams May Come', 'Richard Matheson', 16.99, 'modern', 'Modern', 'What Dreams May Come is a 1978 novel by Richard Matheson. The plot centers on Chris, a man who dies and goes to Heaven, but descends into Hell to rescue his wife. It was adapted into the 1998 film of the same name.', '/images/books/what-dreams-may-come-richard-matheson.jpg', 288, 1978),
    ('10', 'Dracula', 'Bram Stoker', 14.99, 'classics', 'Classics', 'Dracula is an 1897 Gothic horror novel by Irish author Bram Stoker. It introduced the character of Count Dracula and established many conventions of subsequent vampire fantasy.', '/images/books/bram-stoker-dracula.jpg', 418, 1897);
