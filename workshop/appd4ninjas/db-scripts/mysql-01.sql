SET GLOBAL query_cache_size = 0;

SET GLOBAL query_cache_type = 0;

DROP DATABASE IF EXISTS supercars;

CREATE DATABASE supercars;

USE supercars;

CREATE TABLE MANUFACTURER (
    MANUFACTURER_ID MEDIUMINT NOT NULL,
    NAME VARCHAR(80),
    WEB VARCHAR(180),
    EMAIL VARCHAR(240),
    SMLLOGO VARCHAR(80),
    LRGLOGO VARCHAR(80)
);

CREATE TABLE CARS (
     CAR_ID MEDIUMINT NOT NULL AUTO_INCREMENT,
     NAME VARCHAR(120),
     MODEL VARCHAR(120),
     DESCRIPTION VARCHAR(3000),
     MANUFACTURER_ID MEDIUMINT NOT NULL,
     COLOUR VARCHAR(120),
     YEAR MEDIUMINT,
     PRICE FLOAT,
     SUMMARY VARCHAR(3000),
     PHOTO VARCHAR(80),
     PRIMARY KEY (CAR_ID)
);

CREATE TABLE ENQUIRIES (
    ENQUIRY_ID MEDIUMINT NOT NULL AUTO_INCREMENT,
    NAME VARCHAR(150),
    EMAIL VARCHAR(240),
    COMMENT VARCHAR(240),
    CAR_ID MEDIUMINT,
    DUMMY MEDIUMINT,
    PRIMARY KEY (ENQUIRY_ID)
);

INSERT INTO MANUFACTURER (MANUFACTURER_ID, NAME, WEB, EMAIL, SMLLOGO, LRGLOGO) VALUES
    (1, 'Porsche', 'http://www.porsche.com', 'web@porsche.com', 'Porsche.gif', 'Porsche.png'),
    (2, 'Ferrari', 'http://www.ferrari.com/en_us/', 'web@ferrari.com','Ferrari.gif','Ferrari.png'),
    (3, 'Aston Martin','http://www.astonmartin.com','web@astonmartin.com','AstonMartin.gif','AstonMartin.png'),
    (4, 'BMW', 'http://www.bmw.com/com/en/', 'web@bmw.com', 'Bmw.gif', 'Bmw.png'),
    (5, 'Mercedes', 'https://www.mbusa.com/en/home', 'web@mbusa.com', 'Mercedes.gif', 'Mercedes.png'),
    (6, 'Jaguar', 'http://www.jaguarusa.com/index.html', 'web@jaguarusa.com', 'Jaguar.gif', 'Jaguar.png'),
    (7, 'Lamborghini', 'http://www.lamborghini.com/en/home/', 'web@lamborghini.com', 'Lamborghini.gif', 'Lamborghini.png'),
    (8, 'Lotus', 'http://www.lotuscars.com', 'web@lotuscars.com', 'Lotus.gif', 'Lotus.png'),
    (9, 'McLaren', 'https://www.mclaren.com/', 'web@mclaren.com', 'McLaren.gif', 'McLaren.png');

INSERT INTO CARS (CAR_ID, NAME, MODEL, DESCRIPTION, MANUFACTURER_ID, COLOUR, YEAR, PRICE, SUMMARY, PHOTO) VALUES
    (1, 'V8', 'Vantage', '2019 Aston Martin Vantage in Jet Black over Pure Black Alcantara/Obsidian Black Leather. This Vantage is a local 1-owner trade-in that was originally sold here. Options include Black Body-Pack, Comfort Collection, Tech Collection, Exterior Black Collection, Embroidered Aston Wings Headrest, Graphite Seat Belts, and Black Cross Brace. This Vantage still shows like new with the remainder of the factory warranty.', 3, 'Jet Black', '2019', '125000', 'Mileage: 1,512 miles
 Transmission: 8-Speed Automatic
 Exterior Color: Jet Black
 Interior Color: Pure Black
 Maximum Seating: 2 seats
 Gas Mileage: 18 MPG City 25 MPG Highway
 Engine: V8
 Drivetrain: Rear-Wheel Drive
 Fuel Type: Gasoline', '1'),
    (2, 'V12', 'DB11', '2017 Aston Martin DB11 Launch Edition Cinnabar Orange RWD 8-Speed Automatic V12 Options: Power Seat Bolsters, Auto Park Assist, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Dark Exterior Finisher Pack, Paint Contemporary, Headrest Embroidery - Aston Martin Wings, Heavy Pile Floor Mats / Leather Binding, Garage Door Opener, Headlining - Match to Seat Inner, Protective Tape, Lther Col - Out of Range/Match to Sample, Gloss Black Roof Panel, Nexus Quilting, S/Wheel - C/Keyed - Dark Chrome Bezel, Internal Shadow Pack, Trim Inlay High Gloss Chopped Carbon, 10spk Directional Gloss Black DT.',3, 'Cinnabar Orange', '2017', '162900', 'Mileage: 5,565 miles
 Transmission: 8-Speed Automatic
 Exterior Color: Cinnabar Orange
 Interior Color: Metallic Black
 Maximum Seating: 4 seats
 Gas Mileage: 15 MPG City 21 MPG Highway
 Engine: V12
 Drivetrain: Rear-Wheel Drive
 Fuel Type: Gasoline', '2'),
    (3, 'V12', 'Vanquish Volante', '2014 Aston Martin Vanquish Volante Convertible White RWD 6-Speed Automatic V12 Options: Power Seat Bolsters, Auto Park Assist, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',3, 'White', '2014', '106900', 'Mileage: 5,808 miles
 Transmission: 6-Speed Automatic
 Exterior Color: White
 Interior Color: Cuoio
 Maximum Seating: 4 seats
 Gas Mileage: 13 MPG City 19 MPG Highway
 Engine: V12
 Drivetrain: Rear-Wheel Drive
 Fuel Type: Gasoline', '3'),
    (4, 'V8', 'Ferrari 488 Pista', '2019 Ferrari 488 Pista RWD Red RWD 6-Speed Automatic V8 Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',2, 'Rosso Corsa', '2019', '439900', 'Mileage: 826 miles
 Transmission: 6-Speed Automatic
 Exterior Color: Rosso Corsa
 Interior Color: Nero
 Maximum Seating: 2 seats
 Gas Mileage: 15 MPG City 20 MPG Highway
 Engine: V8
 Drivetrain: Rear-Wheel Drive
 Fuel Type: Gasoline', '4'),
    (5, 'V8', 'Ferrari 488 Spider', '2017 Ferrari 488 Spider Silver RWD 6-Speed Automatic V8 Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',2, 'Grigio Titanio', '2017', '275900', 'Mileage: 3,462 miles
 Transmission: 6-Speed Automatic
 Exterior Color: Grigio Titanio
 Interior Color: Nero
 Maximum Seating: 2 seats
 Gas Mileage: 15 MPG City 22 MPG Highway
 Engine: V8
 Drivetrain: Rear-Wheel Drive
 Fuel Type: Gasoline', '5'),
    (6, 'V8', 'Ferrari 488 GTB', '2016 Ferrari 488 GTB Coupe Red RWD 6-Speed Automatic V8 Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',2, 'Rosso Corsa', '2016', '244900', 'Mileage: 1,002 miles
 Transmission: 6-Speed Automatic
 Exterior Color: Rosso Corsa
 Interior Color: Nero
 Maximum Seating: 2 seats
 Gas Mileage: 15 MPG City 22 MPG Highway
 Engine: V8
 Drivetrain: Rear-Wheel Drive
 Fuel Type: Gasoline', '6'),
    (7, 'H6', 'Porsche 911 GT3 RS', '2019 Porsche 911 GT3 RS Coupe Green RWD 6-Speed Automatic V8 Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',1, 'Green', '2019', '198900', 'Mileage: 1,126 miles
 Transmission: 6-Speed Automatic
 Exterior Color: Green
 Interior Color: Black
 Maximum Seating: 2 seats
 Gas Mileage: 15 MPG City 19 MPG Highway
 Engine: H6
 Drivetrain: Rear-Wheel Drive
 Fuel Type: Gasoline', '7'),
    (8, 'H6', 'Porsche 911 Carrera', '2018 Porsche 911 Carrera GTS Coupe Black RWD 6-Speed Automatic V8 Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',1, 'Black', '2018', '143900', 'Mileage: 6,793 miles
 Transmission: 6-Speed Automatic
 Exterior Color: Black
 Interior Color: Black
 Maximum Seating: 2 seats
 Gas Mileage: 20 MPG City 26 MPG Highway
 Engine: H6
 Drivetrain: Rear-Wheel Drive
 Fuel Type: Gasoline', '8'),
    (9, 'H6', 'Porsche 911 GT2 RS', '2018 Porsche 911 GT2 RS Coupe Silver RWD 6-Speed Automatic V8 Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',1, 'Gt Silver', '2018', '321000', 'Mileage: 4,881 miles
 Transmission: 6-Speed Automatic
 Exterior Color: Gt Silver Metallic
 Interior Color: Black
 Maximum Seating: 2 seats
 Gas Mileage: 20 MPG City 26 MPG Highway
 Engine: H6
 Drivetrain: Rear-Wheel Drive
 Fuel Type: Gasoline', '9'),
    (10, 'V12', 'BMW Nazca M12', '1991 BMW Nazca M12 Silver RWD 6-Speed Automatic V8 Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',4, 'Silver', '1991', '1825000', 'Mileage: 872 miles
 Transmission: 6-Speed Automatic
 Exterior Color: Silver Metallic
 Interior Color: Black
 Maximum Seating: 2 seats
 Gas Mileage: 15 MPG City 19 MPG Highway
 Engine: V12
 Drivetrain: Rear-Wheel Drive
 Fuel Type: Gasoline', '10'),
    (11, 'Hybrid', 'BMW i8', '2019 BMW i8 Base AWD Copper 6-Speed Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',4, 'Copper Metallic', '2019', '135000', 'Mileage: 6,313 miles
 Transmission: 6-Speed Automatic
 Exterior Color: Copper Metallic
 Interior Color: Copper
 Maximum Seating: 2 seats
 Gas Mileage: 15 MPG City 19 MPG Highway
 Engine: Hybrid
 Drivetrain: AWD
 Fuel Type: Other', '11'),
    (12, 'IL6', 'BMW 328 Hommag', '2017 BMW 328 Hommag Black 6-Speed Automatic IL6 Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',4, 'Black', '2017', '634000', 'Mileage: 2,313 miles
 Transmission: 6-Speed Automatic
 Exterior Color: Black
 Interior Color: Tan
 Maximum Seating: 2 seats
 Gas Mileage: 20 MPG City 22 MPG Highway
 Engine: IL6
 Drivetrain: RWD
 Fuel Type: Gasoline', '12'),
    (13, 'Hybrid', 'Mercedes AMG Project ONE', '2017 Mercedes AMG Project ONE Black 8-Speed Manual Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',5, 'Cobalt Silver', '2017', '1752000', 'Mileage: 765 miles
 Transmission: 8-Speed Manual
 Exterior Color: Cobalt Silver 
 Interior Color: Black
 Maximum Seating: 2 seats
 Gas Mileage: NA
 Engine: Hybrid
 Drivetrain: AWD
 Fuel Type: Gasoline', '13'),
    (14, 'V8', 'Mercedes AMG GT R PRO', '2020 Mercedes-Benz AMG GT R PRO Black 7-Speed Automatic Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',5, 'GT Silver', '2020', '241000', 'Mileage: 51 miles
 Transmission: 7-Speed Automatic
 Exterior Color: GT Silver 
 Interior Color: Black
 Maximum Seating: 2 seats
 Gas Mileage: 18 MPG City 22 MPG Highway
 Engine: V8 Turbo
 Drivetrain: RWD
 Fuel Type: Gasoline', '14'),
    (15, 'V8', 'Mercedes CLS 63 AMG', '2012 Mercedes-Benz CLS 63 AMG White 7-Speed Automatic Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',5, 'White', '2012', '81000', 'Mileage: 12,000 miles
 Transmission: 7-Speed Automatic
 Exterior Color: White 
 Interior Color: Black
 Maximum Seating: 4 seats
 Gas Mileage: 18 MPG City 24 MPG Highway
 Engine: V8 Turbo
 Drivetrain: RWD
 Fuel Type: Gasoline', '15'),
    (16, 'Electric', 'Jaguar Vision GT', '2019 Jaguar Vision GT Silver 7-Speed Automatic Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',6, 'Silver', '2019', '91000', 'Mileage: 972 miles
 Transmission: 7-Speed Automatic
 Exterior Color: Silver 
 Interior Color: Black
 Maximum Seating: 2 seats
 Gas Mileage: NA
 Engine: Electric
 Drivetrain: AWD
 Fuel Type: Electric', '16'),
    (17, 'V6', 'Jaguar XJ220', '1994 Jaguar XJ220 Silver 7-Speed Automatic Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',6, 'Silver', '1994', '83000', 'Mileage: 2,213 miles
 Transmission: 7-Speed Automatic
 Exterior Color: Silver 
 Interior Color: Black
 Maximum Seating: 2 seats
 Gas Mileage: 18 MPG City 22 MPG Highway
 Engine: V6 Turbo
 Drivetrain: RWD
 Fuel Type: Gasoline', '17'),
    (18, 'IL6', 'Jaguar XKE', '1963 Jaguar XKE 3.8 Roadster Series I 4-Speed Manual Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',6, 'Red', '1963', '152000', 'Mileage: 12,021 miles
 Transmission: 4-Speed Manual
 Exterior Color: Red 
 Interior Color: Tan
 Maximum Seating: 2 seats
 Gas Mileage: 15 MPG City 20 MPG Highway
 Engine: Inline 6
 Drivetrain: RWD
 Fuel Type: Gasoline', '18'),
    (19, 'V12', 'Lamborghini Aventador', '2019 Lamborghini Aventador LP 740-4 S Roadster AWD Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',7, 'Nero Aldebaran', '2019', '419900', 'Mileage: 1,107 miles
 Transmission: Automatic
 Exterior Color: Nero Aldebaran 
 Interior Color: Nero Ade
 Maximum Seating: 2 seats
 Gas Mileage: 9 MPG City 15 MPG Highway
 Engine: V12
 Drivetrain: AWD
 Fuel Type: Gasoline', '19'),
    (20, 'V10', 'Lamborghini Huracan LP', '2017 Lamborghini Huracan LP 580-2 Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',7, 'Rosso Mars', '2017', '178880', 'Mileage: 9,495 miles
 Transmission: Automatic
 Exterior Color: Rosso Mars 
 Interior Color: Nero Ade
 Maximum Seating: 2 seats
 Gas Mileage: 14 MPG City 21 MPG Highway
 Engine: V10
 Drivetrain: RWD
 Fuel Type: Gasoline', '20'),
    (21, 'V10', 'Lamborghini Gallardo LP', '2013 Lamborghini Gallardo LP 550-2 Spyder RWD Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',7, 'Grigio Lynx Metallic', '2013', '129999', 'Mileage: 4,285 miles
 Transmission: Automatic
 Exterior Color: Grigio Lynx Metallic 
 Interior Color: Black-Tan
 Maximum Seating: 2 seats
 Gas Mileage: 13 MPG City 20 MPG Highway
 Engine: V10
 Drivetrain: RWD
 Fuel Type: Gasoline', '21'),
    (22, 'V6', 'Lotus Evora Coupe', '2011 Lotus Evora Coupe 2+2 Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',8, 'Graphite Grey', '2011', '85627', 'Mileage: 23,114 miles
 Transmission: 6 Speed Manual
 Exterior Color: Graphite Grey 
 Interior Color: Red
 Maximum Seating: 4 seats
 Gas Mileage: 18 MPG City 27 MPG Highway
 Engine: V6
 Drivetrain: RWD
 Fuel Type: Gasoline', '22'),
    (23, 'Electric', 'Lotus Evija', '2020 Lotus Evija 2000hp Electric Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',8, 'Graphite Grey', '2020', '2234000', 'Mileage: 12 miles
 Transmission: 6 Speed Automatic
 Exterior Color: Ghost Grey 
 Interior Color: Black
 Maximum Seating: 2 seats
 Gas Mileage: NA
 Engine: Electric
 Drivetrain: AWD
 Fuel Type: Electric', '23'),
    (24, 'V8', 'Lotus Esprit Turbo', '2002 Lotus Esprit Turbo Coupe Options: Power Seat Bolsters, Brogue Detailing, Brake Calipers Black, Ventilated Front Seats, Heavy Pile Floor Mats / Leather Binding, ',8, 'Solar Yellow Metallic', '2002', '71950', 'Mileage: 2142 miles
 Transmission: 5 Speed Manual
 Exterior Color: Solar Yellow Metallic 
 Interior Color: Black
 Maximum Seating: 2 seats
 Gas Mileage: 14 MPG City 21 MPG Highway
 Engine: V8
 Drivetrain: RWD
 Fuel Type: Electric', '24');