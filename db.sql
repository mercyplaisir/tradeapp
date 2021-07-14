create database bot;

use bot;
create TABLE Trades(tradeid INT(15) PRIMARY KEY not null,
                    crypto VARCHAR(20) not null,
                    tradeTime TIMESTAMP not null);


create TABLE Coin(coinName VARCHAR(20) PRIMARY KEY not null,
                fullName varchar(50) not null,
                marketCap INT(30) not null);



INSERT INTO Coin(coinName,fullName,marketCap)
VALUES ('BTC','BITCOIN',0),('ETH','ETHEREUM',0),('BNB','BINANCE COIN',0),('DOGE','DOGECOIN',0);