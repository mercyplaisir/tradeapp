CREATE Database `tradeapp`;
use `tradeapp` ;
create TABLE `Coin`(`shortname` VARCHAR(20) ,
                 `fullname` varchar(50) not null,
                 PRIMARY KEY(`shortname`)
                );
create TABLE `Trades`(`shortname` VARCHAR(10) ,
                    `basecoin` VARCHAR(20)
                    `orderType` VARCHAR(20),
                    `quantity` DOUBLE NOT NULL,
                    `tradeTime` DATETIME,
                    FOREIGN KEY (`shortname`) REFERENCES `Coin`(`shortname`),
                    FOREIGN KEY (`basecoin`) REFERENCES `Coin`(`shortname`);
                    );

--ALTER TABLE `Trades` ADD FOREIGN KEY `shortname` REFERENCES `Coin`(`shortname`);

create TABLE `Balance`(`shortname` VARCHAR(20) ,
                    `quantity` INT(30) ,
                    FOREIGN KEY (`shortname`) REFERENCES `Coin`(`shortname`));

--ALTER TABLE `Balance` ADD FOREIGN KEY `shortname` REFERENCES `Coin`(`shortname`);


INSERT INTO `Coin`(`shortname`,`fullName`)
VALUES ('BTC','BITCOIN'),('ETH','ETHEREUM'),('BNB','BINANCE COIN'),('DOGE','DOGECOIN');


