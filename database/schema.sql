CREATE DATABASE IF NOT EXISTS `NVC` CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `NVC`;
CREATE TABLE IF NOT EXISTS `Collection` (
    `Id` INT NOT NULL AUTO_INCREMENT,
    `StartDate` DATE NOT NULL,
    `EndDate` DATE NOT NULL,
    `Ipfs` nvarchar(256) NOT NULL,
    `TotalSupply` INT NOT NULL,
    `Address` varchar(128) NOT NULL,
    `NetworkId` INT NOT NULL,
    PRIMARY KEY (`Id`)
);

CREATE TABLE IF NOT EXISTS `CollectionUpdate` (
    `Id` INT NOT NULL AUTO_INCREMENT,
    `CollectionId` INT NOT NULL,
    
    `Principal` int NOT NULL,
    `Interest` float NOT NULL,
    
    `FromDate` DATE NOT NULL,
    
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
    `HoldDays` INT NOT NULL,
    `InterestEarned` DECIMAL NOT NULL,
    `SnapshotDate` DATE NOT NULL,
    `UpdateAppliedId` INT NOT NULL,
    
    PRIMARY KEY (`Id`),
    FOREIGN KEY (TokenId,CollectionId) REFERENCES Nft(TokenId,CollectionId),
    FOREIGN KEY (Holder) REFERENCES Wallet(Address),
    FOREIGN KEY (UpdateAppliedId) REFERENCES CollectionUpdate(Id)
);

CREATE TABLE IF NOT EXISTS HolderByMonth(
    `Id` INT NOT NULL AUTO_INCREMENT,
    `Holder` varchar(128) NOT NULL,
    `CollectionId` INT NOT NULL,
    `ResetDate` DATETIME NOT NULL,
    `TotalNFTs` INT NOT NULL,
    `InterestEarned` DECIMAL NOT NULL,
    `UpdateAppliedId` INT NOT NULL,
    
    PRIMARY KEY (`Id`),
    FOREIGN KEY (CollectionId) REFERENCES Collection(Id),
    FOREIGN KEY (Holder) REFERENCES Wallet(Address),
    FOREIGN KEY (UpdateAppliedId) REFERENCES CollectionUpdate(Id)

)