--
-- Table structure for table 'DOIManager'
--

CREATE TABLE IF NOT EXISTS DOIManager (
  doi_sequence int(8) NOT NULL COMMENT 'A unique sequence number used for seeding the DOI and serves as a primary key',
  doi char(25) NOT NULL COMMENT 'The generate DOI',
  salt varchar(35) NOT NULL COMMENT 'The salt added to the doi_sequence.',
  created_by varchar(10) NOT NULL COMMENT 'Identifier for the person creating the DOI',
  date_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp for when the DOI was created',
  PRIMARY KEY (doi_sequence),
  UNIQUE KEY doi (doi)
)