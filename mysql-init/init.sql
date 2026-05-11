CREATE USER IF NOT EXISTS 'travelapp'@'%' IDENTIFIED BY 'travelapp';
GRANT ALL PRIVILEGES ON travelcrm.* TO 'travelapp'@'%';
FLUSH PRIVILEGES;