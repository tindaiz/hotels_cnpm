LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/processed_data.csv'
INTO TABLE hotel_details
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
