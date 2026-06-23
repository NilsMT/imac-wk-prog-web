PRAGMA foreign_keys = ON;

CREATE TABLE USER (
  id_user  TEXT PRIMARY KEY,
  name      TEXT NOT NULL,
  firstname   TEXT NOT NULL,
  email    TEXT UNIQUE NOT NULL,
  pseudo   TEXT UNIQUE NOT NULL,
  promo    INTEGER,
  password TEXT NOT NULL,
  admin    INTEGER,
  active   INTEGER
);

CREATE TABLE EVENT (
  id_event    INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT NOT NULL,
  start_date  TEXT NOT NULL,
  end_date    TEXT NOT NULL,
  location    TEXT NOT NULL,
  image       TEXT,
  description TEXT,
  id_user     TEXT NOT NULL,
  FOREIGN KEY (id_user) REFERENCES USER (id_user)
);

CREATE TABLE PARTICIPATION (
  id_user  TEXT NOT NULL,
  id_event INTEGER NOT NULL,
  PRIMARY KEY (id_user, id_event),
  FOREIGN KEY (id_event) REFERENCES EVENT (id_event),
  FOREIGN KEY (id_user) REFERENCES USER (id_user)
);

CREATE TABLE COMMENT (
  id_user  TEXT NOT NULL,
  id_event INTEGER NOT NULL,
  message  TEXT NOT NULL,
  datetime TEXT,
  PRIMARY KEY (id_user, id_event, datetime),
  FOREIGN KEY (id_event) REFERENCES EVENT (id_event),
  FOREIGN KEY (id_user) REFERENCES USER (id_user)
);

CREATE TABLE ENTITY (
  id_entity INTEGER PRIMARY KEY AUTOINCREMENT,
  type       TEXT,
  id_event   INTEGER NOT NULL,
  FOREIGN KEY (id_event) REFERENCES EVENT (id_event)
);

CREATE TABLE ATTRIBUTE (
  id_attribute INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT,
  description TEXT,
  type        TEXT
);

CREATE TABLE VALUE (
  id_attribut INTEGER NOT NULL,
  id_entity  INTEGER NOT NULL,
  value   TEXT,
  PRIMARY KEY (id_attribut, id_entity),
  FOREIGN KEY (id_entity) REFERENCES ENTITY (id_entity),
  FOREIGN KEY (id_attribut) REFERENCES ATTRIBUTE (id_attribut)
);