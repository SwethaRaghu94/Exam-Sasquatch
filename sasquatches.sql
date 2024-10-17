
        
CREATE TABLE sightings
(
  id                    INT          NOT NULL AUTO_INCREMENT,
  location              VARCHAR(255) NULL    ,
  date_of_sighting      DATE         NOT NULL,
  number_of_sasquatches INT          NULL    ,
  what_happened         LONGTEXT     NULL    ,
  created_at            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  user_id               INT          NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE users
(
  id         INT          NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(255) NULL    ,
  last_name  VARCHAR(255) NULL    ,
  email      VARCHAR(255) NULL    ,
  password   VARCHAR(255) NULL    ,
  created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

ALTER TABLE sightings
  ADD CONSTRAINT FK_users_TO_sightings
    FOREIGN KEY (user_id)
    REFERENCES users (id);

        
      