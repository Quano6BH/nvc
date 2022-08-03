CREATE DATABASE IF NOT EXISTS `NextVisionCapital` CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `NextVisionCapital`;
CREATE TABLE IF NOT EXISTS `Collection` (
    `Id` INT NOT NULL AUTO_INCREMENT,
    `StartDate` DATE NOT NULL,
    `Name` nvarchar(256),
    `EndDate` DATE NOT NULL,
    `Ipfs` nvarchar(256) NOT NULL,
    `Price` FLOAT NOT NULL,
    `TotalSupply` INT NOT NULL,
    `Address` varchar(128) NOT NULL,
    `NetworkId` INT NOT NULL,
    PRIMARY KEY (`Id`)
);

CREATE TABLE IF NOT EXISTS `CollectionUpdate` (
    `Id` INT NOT NULL AUTO_INCREMENT,
    `CollectionId` INT NOT NULL,
    
    `Principal` int NULL,
    `Interest` float NULL,
    
    `FromDate` DATE NOT NULL,
    `Type` varchar(32) NOT NULL,
    `Message` nvarchar(256) NULL,
    `BuyBack` BIT NOT NULL DEFAULT 0,
    
    PRIMARY KEY (`Id`),
    FOREIGN KEY (CollectionId) REFERENCES Collection(Id)
);

CREATE TABLE IF NOT EXISTS `Nft` (
    `TokenId` INT NOT NULL ,
    
    `CollectionId` INT NOT NULL,
    
    PRIMARY KEY (`TokenId`,`CollectionId`),
    FOREIGN KEY (CollectionId) REFERENCES Collection(Id)
);

CREATE TABLE IF NOT EXISTS `Wallet` (
    `Address` varchar(128) NOT NULL,
    `Kyc` BIT NOT NULL DEFAULT 0,
    
    PRIMARY KEY (`Address`)
);

CREATE TABLE IF NOT EXISTS `NftHolder` (
    `Id` INT NOT NULL AUTO_INCREMENT,
    
    `TokenId` INT NOT NULL,
    `CollectionId` INT NOT NULL,
    `Holder` varchar(128) NOT NULL,

    `Principal` INT NOT NULL,
    `Interest` FLOAT NOT NULL,
    
    `SnapshotDate` DATE NOT NULL,

    PRIMARY KEY (`Id`),
    FOREIGN KEY (TokenId,CollectionId) REFERENCES Nft(TokenId,CollectionId),
    FOREIGN KEY (Holder) REFERENCES Wallet(Address)
);

CREATE TABLE IF NOT EXISTS HolderByDate(
    `Id` INT NOT NULL AUTO_INCREMENT,
    `Holder` varchar(128) NOT NULL,
    `TokenId` INT NOT NULL,
    `CollectionId` INT NOT NULL,
    `SnapshotDate` DATE NOT NULL,
    `HoldDays` INT NOT NULL,
    `HoldDaysInMonth` INT NOT NULL,
    `InterestEarned` FLOAT NOT NULL,
    `InterestEarnedInMonth` FLOAT NOT NULL,
    `UpdateAppliedId` INT NOT NULL,
    `Holding` BIT NOT NULL DEFAULT 0,
    `Paid` BIT NOT NULL DEFAULT 0,
    
    PRIMARY KEY (`Id`),
    UNIQUE KEY `HolderByDate_Unique_Keys` (`Holder`,`TokenId`,`CollectionId`,`SnapshotDate`),
    FOREIGN KEY (TokenId,CollectionId) REFERENCES Nft(TokenId,CollectionId),
    FOREIGN KEY (Holder) REFERENCES Wallet(Address),
    FOREIGN KEY (UpdateAppliedId) REFERENCES CollectionUpdate(Id)
);

CREATE TABLE IF NOT EXISTS HolderByMonth(
    `Id` INT NOT NULL AUTO_INCREMENT,
    `Holder` varchar(128) NOT NULL,
    `CollectionId` INT NOT NULL,
    `ResetDate` DATE NOT NULL,
    `TotalNFTs` INT NOT NULL,
    `InterestEarned` FLOAT NOT NULL,
    `UpdateAppliedId` INT NOT NULL,
    `Paid` BIT NOT NULL DEFAULT 0,
    
    PRIMARY KEY (`Id`),
    UNIQUE KEY `HolderByMonth_Unique_Keys` (`Holder`,`CollectionId`,`ResetDate`),
    FOREIGN KEY (CollectionId) REFERENCES Collection(Id),
    FOREIGN KEY (Holder) REFERENCES Wallet(Address),
    FOREIGN KEY (UpdateAppliedId) REFERENCES CollectionUpdate(Id)
)