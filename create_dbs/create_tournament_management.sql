CREATE DATABASE IF NOT EXISTS tournament_management;
USE tournament_management;

CREATE TABLE IF NOT EXISTS grade_type(
    grade_type_id INT NOT NULL PRIMARY KEY 
    AUTO_INCREMENT,
    grade_type VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS location(
    location_id INT NOT NULL PRIMARY KEY 
    AUTO_INCREMENT,
    location VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS age_category(
    age_category_id INT NOT NULL PRIMARY KEY 
    AUTO_INCREMENT,
    age_category VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS perfomance_type(
    perfomance_type_id INT NOT NULL PRIMARY KEY 
    AUTO_INCREMENT,
    perfomance_type VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS competition_type(
    competition_type_id INT NOT NULL PRIMARY KEY 
    AUTO_INCREMENT,
    competition_type VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS competition(
    competition_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    competition_name VARCHAR(50) NOT NULL,
    competition_date DATE,
    competition_type_id INT NOT NULL,
    location_id INT NOT NULL,
    CONSTRAINT competition_type_comp_id_fk
    FOREIGN KEY (competition_type_id) REFERENCES 
    competition_type(competition_type_id) ON DELETE
    CASCADE ON UPDATE CASCADE,
    CONSTRAINT location_id_fk
    FOREIGN KEY (location_id) REFERENCES location
    (location_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS country(
    country_id INT NOT NULL PRIMARY KEY
    AUTO_INCREMENT,
    country VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS judge_type(
    judge_type_id INT NOT NULL PRIMARY KEY
    AUTO_INCREMENT,
    judge_type VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS grade(
    grade_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    date DATE,
    verification BOOLEAN,
    grade_type_id INT NOT NULL,
    competition_type_id INT NOT NULL,
    CONSTRAINT grade_type_id_fk
    FOREIGN KEY (grade_type_id) REFERENCES 
    grade_type(grade_type_id) ON DELETE CASCADE ON UPDATE
    CASCADE,
    CONSTRAINT competition_type_id_fk
    FOREIGN KEY (competition_type_id) REFERENCES 
    competition_type(competition_type_id) ON DELETE CASCADE
    ON UPDATE 
    CASCADE
);


CREATE TABLE IF NOT EXISTS judge(
    judge_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    judge_name VARCHAR(50) NOT NULL,
    judge_lastname VARCHAR(50) NOT NULL,
    judge_middlename VARCHAR(50),
    judge_score INT,
    judge_type_id INT NOT NULL,
    CONSTRAINT judge_type_id_fk
    FOREIGN KEY (judge_type_id) REFERENCES judge_type
    (judge_type_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS judge_panel(
    judge_panel_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    judge_count INT,
    total_score INT,
    total_allowance INT,
    disculification BOOLEAN NOT NULL,
    judge_id INT NOT NULL,
    CONSTRAINT judge_id_fk
    FOREIGN KEY (judge_id) REFERENCES judge(judge_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS perfomance(
    perfomance_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    perfomance_place INT,
    spotsman_count INT NOT NULL,
    competition_id INT NOT NULL,
    perfomance_type_id INT NOT NULL,
    age_category_id INT NOT NULL,
    judge_panel_id INT NOT NULL,
    CONSTRAINT competition_id_fk
    FOREIGN KEY (competition_id) REFERENCES competition
    (competition_id) ON DELETE CASCADE ON UPDATE
    CASCADE,
    CONSTRAINT perfomance_type_id_fk
    FOREIGN KEY (perfomance_type_id) REFERENCES 
    perfomance_type(perfomance_type_id) ON DELETE CASCADE ON 
    UPDATE CASCADE,
    CONSTRAINT age_category_id_fk
    FOREIGN KEY (age_category_id) REFERENCES
    age_category(age_category_id) ON DELETE CASCADE ON 
    UPDATE CASCADE,
    CONSTRAINT judge_panel_fk
    FOREIGN KEY (judge_panel_id) REFERENCES 
    judge_panel(judge_panel_id) ON DELETE CASCADE ON
    UPDATE CASCADE  
);

CREATE TABLE IF NOT EXISTS region(
    region_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    region_name VARCHAR(50) NOT NULL,
    region_ranking INT,
    sportsman_count INT,
    country_id INT NOT NULL,
    CONSTRAINT country_id_fk
    FOREIGN KEY (country_id) REFERENCES country
    (country_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS club(
    club_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    club_name VARCHAR(50) NOT NULL,
    club_ranking INT,
    birthdate DATE,
    email VARCHAR(50),
    region_id INT NOT NULL,
    CONSTRAINT region_id_fk
    FOREIGN KEY (region_id) REFERENCES region(region_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS sportsman(
    sportsman_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    sportsman_name VARCHAR(50) NOT NULL,
    sportsman_lastname VARCHAR(50) NOT NULL,
    sportsman_middlename VARCHAR(50),
    sportsman_birthdate DATE NOT NULL,
    club_id INT NOT NULL,
    grade_id INT NOT NULL,
    CONSTRAINT club_id_fk
    FOREIGN KEY (club_id) REFERENCES club(club_id) 
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT grade_id_fk
    FOREIGN KEY (grade_id) REFERENCES grade(grade_id) 
    ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS spotsman_perfomance(
    sportsman_perfomance_id INT NOT NULL PRIMARY KEY 
    AUTO_INCREMENT,
    perfomance_id INT NOT NULL,
    sportsman_id INT NOT NULL,
    CONSTRAINT perfomance_id_fk
    FOREIGN KEY (perfomance_id) REFERENCES perfomance
    (perfomance_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT sportsman_id_fk
    FOREIGN KEY (sportsman_id) REFERENCES sportsman
    (sportsman_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS judge_panel_judge(
    judge_panel_judge_id INT NOT NULL PRIMARY KEY
    AUTO_INCREMENT,
    judge_panel_id INT NOT NULL,
    judge_id INT NOT NULL,
    CONSTRAINT judge_panel_id_fk
    FOREIGN KEY (judge_panel_id) REFERENCES 
    judge_panel(judge_panel_id) ON DELETE CASCADE
    ON UPDATE CASCADE,
    CONSTRAINT judge_slov_id_fk
    FOREIGN KEY (judge_id) REFERENCES judge(judge_id) 
    ON DELETE CASCADE ON UPDATE CASCADE
);
