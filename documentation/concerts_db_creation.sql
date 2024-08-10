CREATE TABLE Artists(
   id_artist INT,
   name VARCHAR(120) NOT NULL,
   country VARCHAR(120) NOT NULL,
   PRIMARY KEY(id_artist)
);

CREATE TABLE Festivals(
   id_festival INT,
   name VARCHAR(120) NOT NULL,
   event_year VARCHAR(4) NOT NULL,
   country VARCHAR(60) NOT NULL,
   start_date DATE,
   end_date DATE,
   PRIMARY KEY(id_festival)
);

CREATE TABLE Persons(
   id_person INT,
   firstname VARCHAR(120) NOT NULL,
   lastname VARCHAR(120),
   PRIMARY KEY(id_person)
);

CREATE TABLE Addresses(
   id_address INT,
   city VARCHAR(60) NOT NULL,
   country VARCHAR(60) NOT NULL,
   PRIMARY KEY(id_address)
);

CREATE TABLE Venues(
   id_venue INT,
   name VARCHAR(60) NOT NULL,
   id_address INT NOT NULL,
   PRIMARY KEY(id_venue),
   FOREIGN KEY(id_address) REFERENCES Addresses(id_address)
);

CREATE TABLE Concerts(
   id_concert INT,
   event_date DATE NOT NULL,
   comments VARCHAR(3000),
   id_venue INT NOT NULL,
   id_festival INT,
   PRIMARY KEY(id_concert),
   FOREIGN KEY(id_venue) REFERENCES Venues(id_venue),
   FOREIGN KEY(id_festival) REFERENCES Festivals(id_festival)
);

CREATE TABLE perform(
   id_concert INT,
   id_artist INT,
   PRIMARY KEY(id_concert, id_artist),
   FOREIGN KEY(id_concert) REFERENCES Concerts(id_concert),
   FOREIGN KEY(id_artist) REFERENCES Artists(id_artist)
);

CREATE TABLE attend(
   id_concert INT,
   id_person INT,
   PRIMARY KEY(id_concert, id_person),
   FOREIGN KEY(id_concert) REFERENCES Concerts(id_concert),
   FOREIGN KEY(id_person) REFERENCES Persons(id_person)
);
