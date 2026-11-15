DROP TABLE IF EXISTS innlegg_tagger;
DROP TABLE IF EXISTS kommentarer;
DROP TABLE IF EXISTS tagger;
DROP TABLE IF EXISTS innlegg;

CREATE TABLE innlegg (
    id INTEGER PRIMARY KEY,
    tittel TEXT NOT NULL,
    dato TEXT NOT NULL,
    tekst TEXT NOT NULL
);

CREATE TABLE kommentarer (
    id INTEGER PRIMARY KEY,
    innlegg_id INTEGER NOT NULL,
    tittel TEXT NOT NULL,
    dato TEXT NOT NULL,
    tekst TEXT NOT NULL,
    FOREIGN KEY (innlegg_id) REFERENCES innlegg(id)
);

CREATE TABLE tagger (
    id INTEGER PRIMARY KEY,
    navn TEXT NOT NULL UNIQUE
);

CREATE TABLE innlegg_tagger (
    innlegg_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (innlegg_id, tag_id),
    FOREIGN KEY (innlegg_id) REFERENCES innlegg(id),
    FOREIGN KEY (tag_id) REFERENCES tagger(id)
);