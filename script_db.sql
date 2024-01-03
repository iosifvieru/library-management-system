CREATE TABLE "book_quantities" (
    "id"    INTEGER NOT NULL UNIQUE,
    "quantity"    INTEGER,
    PRIMARY KEY("id"),
    FOREIGN KEY("id") REFERENCES "books"("id")
);

CREATE TABLE "books" (
    "id"    INTEGER NOT NULL UNIQUE,
    "author"    TEXT NOT NULL,
    "title"    TEXT,
    "status"    NUMERIC,
    "publishDate"    TEXT,
    "borrowedBy"    TEXT,
    "noPages"    INTEGER,
    FOREIGN KEY("borrowedBy") REFERENCES "libraries"("libraryID"),
    FOREIGN KEY("id") REFERENCES "borrowedBooks"("book_id"),
    PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "borrowedBooks" (
    "user_id"    INTEGER NOT NULL,
    "book_id"    INTEGER NOT NULL
);

CREATE TABLE "libraries" (
    "libraryID"    INTEGER NOT NULL UNIQUE,
    "name"    TEXT NOT NULL,
    PRIMARY KEY("libraryID" AUTOINCREMENT)
);

CREATE TABLE "pass_salt" (
    "id"    INTEGER NOT NULL UNIQUE,
    "salt"    TEXT NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE "session" (
    "id"    INTEGER NOT NULL,
    "session_id"    INTEGER NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE "users" (
    "id"    INTEGER NOT NULL UNIQUE,
    "username"    TEXT NOT NULL UNIQUE,
    "password"    TEXT NOT NULL,
    "firstName"    TEXT,
    "lastName"    TEXT,
    "city"    TEXT,
    "phoneNo"    TEXT,
    "email"    TEXT NOT NULL,
    "birthDate"    TEXT,
    "university"    TEXT,
    "specialization"    TEXT,
    "year"    INTEGER,
    "adminLevel"    INTEGER,
    PRIMARY KEY("id" AUTOINCREMENT),
    FOREIGN KEY("id") REFERENCES "pass_salt"("id"),
    FOREIGN KEY("id") REFERENCES "session"("id")
);

