create database bot;

use bot;
create TABLE Trades(coinName VARCHAR(10) PRIMARY KEY,
                    crypto VARCHAR(20) not null,
                    orderType VARCHAR(20),
                    quantity FLOAT(20) NOT NULL,
                    tradeTime DATETIME);


create TABLE Coin(coinName VARCHAR(20) PRIMARY KEY not null,
                fullName varchar(50) not null,
                marketCap INT(30) not null);



INSERT INTO Coin(coinName,fullName,marketCap)
VALUES ('BTC','BITCOIN',0),('ETH','ETHEREUM',0),('BNB','BINANCE COIN',0),('DOGE','DOGECOIN',0);

