DROP TABLE IF EXISTS Customer CASCADE;

CREATE TABLE IF NOT EXISTS Customer (
    customerId SERIAL PRIMARY KEY NOT NULL,
    firstName VARCHAR (50) NULL,
    patronymic VARCHAR (50) NULL,
    lastName VARCHAR (50) NULL,
    birthDate DATE NULL,
    email VARCHAR (50) UNIQUE NOT NULL,
    phoneNumber VARCHAR (11) UNIQUE NOT NULL,
    password VARCHAR (50) NOT NULL
);

DROP TABLE IF EXISTS Weighing CASCADE;

CREATE TABLE IF NOT EXISTS Weighing (
    weighingId SERIAL PRIMARY KEY NOT NULL,
    weight FLOAT4 NOT NULL,
    musclePercentage INT CHECK (1 <= musclePercentage AND musclePercentage <= 100) NOT NULL,
    fatPercentage INT CHECK (1 <= musclePercentage AND musclePercentage <= 100) NOT NULL,
    dateTimeOfWeighing TIMESTAMP NOT NULL,
    customerId INT NOT NULL REFERENCES Customer (customerId)
);

DROP TABLE IF EXISTS Training CASCADE;

CREATE TABLE IF NOT EXISTS Training (
    trainingId SERIAL PRIMARY KEY NOT NULL,
    dateTimeOfStart TIMESTAMP NOT NULL,
    dateTimeOfFinish TIMESTAMP NULL,
    customerId INT NOT NULL REFERENCES Customer (customerId)
);

DROP TABLE IF EXISTS Trainer_Type CASCADE;

CREATE TABLE IF NOT EXISTS Trainer_Type (
    trainerTypeId SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR (100) NOT NULL
);


DROP TABLE IF EXISTS Trainer CASCADE;

CREATE TABLE IF NOT EXISTS Trainer (
    trainerId SERIAL PRIMARY KEY NOT NULL,
    dateOfStartExploitation DATE NOT NULL,
    trainerTypeId INT NOT NULL REFERENCES Trainer_Type (trainerTypeId)
);

DROP TABLE IF EXISTS Strength_Exercise_Type CASCADE;

CREATE TABLE IF NOT EXISTS Strength_Exercise_Type (
    strengthExerciseTypeId SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR (100) NOT NULL
);

INSERT INTO Strength_Exercise_Type (name) VALUES
('Тяга верхнего блока');

DROP TABLE IF EXISTS Strength_Exercise CASCADE;

CREATE TABLE IF NOT EXISTS Strength_Exercise (
    strengthExerciseId SERIAL PRIMARY KEY NOT NULL,
    dateTimeOfStart TIMESTAMP NOT NULL,
    dateTimeOfFinish TIMESTAMP NULL,
    trainingId INT NOT NULL REFERENCES Training (trainingId),
    strengthExerciseTypeId INT NOT NULL REFERENCES Strength_Exercise_Type (strengthExerciseTypeId),
    trainerId INT NOT NULL REFERENCES Trainer (trainerId)
);

DROP TABLE IF EXISTS Approach CASCADE;

CREATE TABLE IF NOT EXISTS Approach (
    approachId SERIAL PRIMARY KEY NOT NULL,
    dateTimeOfStart TIMESTAMP NOT NULL,
    dateTimeOfFinish TIMESTAMP NULL,
    weight FLOAT (1)  NOT NULL,
    repetition INT NOT NULL,
    strengthExerciseId INT NOT NULL REFERENCES Strength_Exercise (strengthExerciseId)
);

DROP TABLE IF EXISTS Running_Exercise_Type CASCADE;

CREATE TABLE IF NOT EXISTS Running_Exercise_Type (
    runningExerciseTypeId SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR (100) NOT NULL
);

INSERT INTO Running_Exercise_Type (name) VALUES
('Беговая дорожка');

DROP TABLE IF EXISTS Running_Exercise CASCADE;

CREATE TABLE IF NOT EXISTS Running_Exercise (
    runningExerciseId SERIAL PRIMARY KEY NOT NULL,
    dateTimeOfStart TIMESTAMP NOT NULL,
    dateTimeOfFinish TIMESTAMP NOT NULL,
    distance FLOAT (1) NOT NULL,
    time FLOAT (1) NOT NULL,
    averageSpeed FLOAT (1) NOT NULL,
    averagePulse INT CHECK (0 <= averagePulse AND averagePulse <= 300) NULL,
    minPulse INT CHECK (0 <= minPulse AND minPulse <= 300) NULL,
    maxPulse INT CHECK (0 <= maxPulse AND maxPulse <= 300) NULL,
    runningExerciseTypeId INT NOT NULL REFERENCES Running_Exercise_Type (runningExerciseTypeId),
    trainingId INT NOT NULL REFERENCES Training (trainingId),
    trainerId INT NOT NULL REFERENCES Trainer (trainerId)
)
