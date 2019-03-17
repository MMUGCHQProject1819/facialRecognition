CREATE DATABASE project;
USE project;
CREATE TABLE `person` (
  `pid` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `nationality` varchar(255) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `hair_colour` varchar(255) DEFAULT NULL,
  `hair_style` varchar(255) DEFAULT NULL,
  `skin_colour` varchar(255) DEFAULT NULL,
  `facial_hair` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pid`)
);
CREATE TABLE `photos` (
  `pid` int(11) NOT NULL,
  `image` mediumblob,
  `encoding` text,
  `encoded` int(1) DEFAULT NULL
);