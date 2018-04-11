/* --Alter table (rename table) na_goods_receive
use na_m_s;
--Rubah/Alter table n_a_goods, price perunitjadi decimal 30.4
--BrandName varchar(100)
--goodsName varchar(150)
ALTER TABLE n_a_goods MODIFY idapp INT AUTO_INCREMENT PRIMARY KEY;
ALTER TABLE n_a_goods MODIFY depreciationmethod VARCHAR(3);
ALTER TABLE n_a_goods MODIFY BrandName varchar(100) ;
ALTER TABLE n_a_goods MODIFY goodsName varchar(150);
ALTER TABLE n_a_goods MODIFY price decimal(30.4);

RENAME TABLE 'n_a_goods_recieve' TO 'n_a_goods_receive';

--Gantisemua columns fk_goodsdarivarchar(30) keint
--Rename column FK_RecievedByjadiFK_ReceivedBy
ALTER TABLE n_a_goods_receive CHANGE FK_RecievedBy FK_ReceivedBy VARCHAR(50);
ALTER TABLE n_a_goods_receive CHANGE DateRecievedDate ReceivedDateTime; 
ALTER TABLEn_a_goods_receive ADD FK_goods INT;

ALTER TABLE n_a_goods_receive ADD DescBySystem VARCHAR(250) DEFAULT 'N/A';


--rubah table employee
DROP TABLE IF EXISTS Employee;

CREATE TABLE Employee ( IDApp SMALLINT NOT NULL AUTO_INCREMENT PRIMARY KEY, NIK VARCHAR(50) NOT NULL, Employee_Name VARCHAR(150), TypeApp VARCHAR(32) DEFAULT 'N/A', JobType VARCHAR(150) DEFAULT 'N/A', Gender CHAR(1) DEFAULT 'F' NOT NULL, Status CHAR(1) DEFAULT 'S', TelpHP VARCHAR(20), Territory VARCHAR(50) DEFAULT 'jakarta', Descriptions VARCHAR(50), InActivetinyint(1) DEFAULT 0 NOT NULL, CreatedDate DATE NOT NULL, CreatedBy VARCHAR(100) NOT NULL, ModifiedDate DATE, ModifiedBy VARCHAR(100));
ALTER TABLE n_a_stock CHANGE FK_Goods_Recieved FK_Goods_Received int(11);
-- Dumping data for table employee
INSERT INTO employee (IDApp, NIK, Employee_Name, TypeApp, JobType, Gender, Status, TelpHP, Territory, Descriptions, InActive, CreatedDate, CreatedBy, ModifiedDate, ModifiedBy) VALUES
(141, '00122453457', 'Rimba', 'C', 'Student', 'M', 'S', '0895322085649', 'Cimahi', 'Descriptions', '1', '2018-01-25 15:54:51', 'rimba47prayoga', '2018-01-28 13:47:40', 'rimba47prayoga'),
(143, '11223445', 'Rimba P', 'K', 'Life', 'M', 'S', '08953320215121', 'Cisurupan', 'There''s No Descriptions', '1', '2018-01-25 18:04:20', 'rimba47prayoga', '2018-01-28 13:56:45', 'rimba47prayoga'),
(144, '1122131544', 'RimbaPrayoga', 'K', 'Life', 'M', 'S', '08532201245457', 'Citeureup', 'Descriptions', '0', '2018-01-25 18:05:06', 'rimba47prayoga', '2018-01-28 13:58:29', 'rimba47prayoga'),
(145, '00122445577889', 'Rimba Pray', 'P', 'Schools', 'M', 'S', '089322054678684', 'Jawabarat', 'Desc', '1', '2018-01-25 18:06:55', 'rimba47prayoga', '2018-01-27 13:13:12', 'rimba47prayoga'),
(147, '1123454878', 'RimbaPrayog', 'P', 'Schools', 'M', 'S', '089532201154', 'Cimahi', 'Descriptions', '0', '2018-01-25 18:29:59', 'rimba47prayoga', '2018-01-27 13:12:44', 'rimba47prayoga'),
(148, '001234', 'RimbaPrayoga', 'P', 'School', 'M', 'S', '08953220121488', 'Cimahi', 'Desc', '1', '2018-01-27 13:11:14', 'rimba47prayoga', '2018-01-27 13:12:59', 'rimba47prayoga'),
(149, '00111234887898', 'Rimba', 'C', 'Student', 'M', 'S', '08984512313574', 'Cimahi', 'Employee', '1', '2018-01-27 13:14:15', 'rimba47prayoga', '2018-01-28 13:50:36', 'rimba47prayoga'),
(150, '01144747789', 'Rimba', 'P', 'Student', 'M', 'S', '089522144855487', 'JawaBarat,Cimahi,Cisurupan', 'There''s No Descriptions', 'False', '2018-01-27 13:18:24', 'rimba47prayoga', '2018-01-27 13:18:24', NULL),
(151, '00123454', 'Rimba', 'P', 'Student', 'M', 'S', '089532201245', 'Cimahi', 'Descriptions :D', 'False', '2018-01-27 13:22:42', 'rimba47prayoga', '2018-01-27 13:22:42', NULL),
(152, '001245789', 'Rimba', 'P', 'Student', 'M', 'S', '08532214485789', 'Citeureup', 'Descriptions', 'False', '2018-01-27 13:24:35', 'rimba47prayoga', '2018-01-27 13:24:35', NULL),
(153, '011115278899', 'Rimba', 'P', 'Schools', 'M', 'S', '089523154871156', 'Dunia', 'Description', 'False', '2018-01-27 13:25:46', 'rimba47prayoga', '2018-01-27 13:25:46', NULL),
(154, '00111144777', 'Rimba P', 'P', 'Job', 'M', 'S', '0895552312444', 'Cimahi', 'Desc', '1', '2018-01-27 13:27:36', 'rimba47prayoga', '2018-01-29 17:50:20', 'rimba47prayoga'),
(162, '1121545454544', 'RimbaPrayoga', 'P', 'Student', 'M', 'S', '08953321248541', 'Cimahi', 'There''s no descriptions', '1', '2018-01-28 13:30:12', 'rimba47prayoga', '2018-01-28 13:31:06', 'rimba47prayoga'),
(163, '1121246345', 'Rimba P', 'P', 'Schools', 'M', 'S', '0895322085649', 'Citeureup', 'There''s No Descriptions', 'False', '2018-01-28 13:44:30', 'rimba47prayoga', '2018-01-28 13:44:30', NULL),
(164, '11223448788', 'Rimba', 'K', 'Schools', 'M', 'S', '0895332085649', 'Cimahi', 'Descriptions', 'False', '2018-01-28 13:47:10', 'rimba47prayoga', '2018-01-28 13:47:10', NULL),
(165, '0112145678901123', 'RimbaPrayoga', 'C', 'Student', 'M', 'S', '08122165422312', 'Cisurupan', 'No Descriptions that is expensive', '0', '2018-01-28 13:50:08', 'rimba47prayoga', '2018-01-28 20:48:09', 'rimba47prayoga'),
(166, '011247487875411', 'Rimba', 'C', 'Life', 'M', 'S', '0895322085649', 'Cimahi', 'Descriptions', '0', '2018-01-29 17:06:02', 'rimba47prayoga', NULL, NULL),
(167, '1123245789784', 'Rimbaprayoga', 'K', 'Life', 'M', 'S', '089532208547477', 'Cisurupan', 'Employee', '0', '2018-01-29 17:07:28', 'rimba47prayoga', NULL, NULL),
(168, '00123487878', 'Rimba', 'P', 'Life', 'M', 'S', '0895322085649', 'Cimahi', 'No', '0', '2017-12-17 00:00:00', 'rimba47prayoga', NULL, NULL),
(169, '02214567897512', 'Rimbaprayoga', 'C', 'Life', 'M', 'S', '089532208544', 'Dunia', 'No Descriptions', '0', '2018-01-29 17:26:15', 'rimba47prayoga', NULL, NULL);

DROP TABLE IF EXISTS n_a_stock;

CREATE TABLE n_a_stock (
IDApp int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
FK_Goods int(11) NOT NULL,
TotalQty int(11) NOT NULL,
TIsUsed int(11) NOT NULL,
TIsNew int(11) NOT NULL,
TIsRenew int(11) NOT NULL,
TGoods_Return smallint(6) DEFAULT NULL,
TGoods_Received int(11) DEFAULT NULL,
TMaintenance smallint(6) DEFAULT NULL,
CreatedDate datetime DEFAULT NULL,
CreatedBy varchar(100) DEFAULT NULL,
ModifiedDate datetime DEFAULT NULL,
ModifiedBy varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE n_a_goods_lending (
IDApp int(11) NOT NULL,
FK_Goods varchar(30) NOT NULL,
IsNewtiny int(1) NOT NULL DEFAULT 0,

FK_Employee varchar(50) NOT NULL,
DateLending date DEFAULT NULL,
  Qty int(11) NOT NULL,
FK_Stock varchar(50) NOT NULL,
FK_Responsible_Person varchar(50) DEFAULT NULL,
BenefitOf varchar(150) DEFAULT NULL,
FK_Sender varchar(50) DEFAULT NULL,
  Status varchar(10) DEFAULT NULL,
CreatedDate datetime DEFAULT NULL,
CreatedBy varchar(50) DEFAULT NULL,
ModifiedDate datetime DEFAULT NULL,
ModifiedBy varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table n_a_goods_outwards
--

CREATE TABLE n_a_goods_outwards (
IDApp int(11) NOT NULL,
FK_Goods varchar(30) NOT NULL,
IsNew tinyint(1) NOT NULL DEFAULT 0,
Qty int(11) DEFAULT NULL,
DateRequest datetime NOT NULL,
DateReleased datetime NOT NULL,
FK_Employee varchar(50) DEFAULT NULL,
FK_UsedEmployee varchar(50) DEFAULT NULL,
FK_FromMaintenance int(11) DEFAULT NULL,
FK_ResponsiblePerson varchar(50) DEFAULT NULL,
FK_Sender varchar(50) DEFAULT NULL,
FK_Stockint(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE n_a_stock CHANGE FK_Goods FK_Goods INT(11) NULL;
ALTER TABLE n_a_stock DROP COLUMN TotalQty;

ALTER TABLE n_a_stock ADD T_Goods_Lending INT;

DROP TABLE IF EXISTS n_a_goods_receive_detail;

CREATE TABLE n_a_goods_receive_detail (
IDApp int(32) NOT NULL,
FK_App int(32) UNSIGNED NOT NULL,
BrandName varchar(150) NOT NULL,
PricePerUnit decimal(18,2) UNSIGNED NOT NULL,
TypeApp VARCHAR(32),
SerialNumber varchar(50) DEFAULT NULL,
warranty TINYINT(2) NOT NULL DEFAULT 0,
EndOfWarranty datetime,
CreatedBy varchar(100) DEFAULT NULL,
CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
ModifiedBy varchar(100) DEFAULT NULL,
ModifiedDate datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table n_a_goods_receive_detail
--
ALTER TABLE n_a_goods_receive_detail
  ADD PRIMARY KEY (IDApp),
  ADD UNIQUE KEY IDApp (IDApp);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table n_a_goods_receive_detail
--*/
--=================perbaikan n_a_goods_return==================
DROP TABLE IF EXISTS n_a_goods_return;

CREATE TABLE n_a_goods_return (
  IDApp int(11) NOT NULL,
  FK_Goods varchar(30) NOT NULL,
  DateReturn datetime(6) NOT NULL,
  Conditions varchar(1) NOT NULL,--layak,kurang layak,tidak layak(rusak total)(w=worth,M-minus/kurang layak,B=broken/rusak)
  FK_FromEmployee varchar(50) DEFAULT NULL,
  FK_Goods_Outwards int(11) DEFAULT NULL, --apakah dari fk_goods_outwords (pengeluaran barang inventaris), jika iya isi foreign key nya
  FK_UsedEmployee varchar(50) DEFAULT NULL,--bekas siapa sebelumnya
  FK_Goods_Lend int(11) DEFAULT NULL,--PERBAIKAN DI SINI apakah dari peminjaman jika iya isi foreign key nya
  IsCompleted tinyint(1) NOT NULL,--PERBAIKAN DI SINI
  MinusDesc varchar(150) DEFAULT NULL,--PERBAIKAN DI SINI 
  Descriptions varchar(200) DEFAULT NULL,
  CreatedDate datetime NOT NULL,
  CreatedBy varchar(100) NOT NULL,
  ModifiedDate datetime DEFAULT NULL,
  ModifiedBy varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE n_a_goods_return CHANGE FK_Goods FK_Goods INT(11) UNSIGNED NOT NULL;
ALTER TABLE n_a_goods_return add SerialNumber VARCHAR(50) NOT NULL DEFAULT 'N/A';
ALTER TABLE n_a_goods_return add TypeApp VARCHAR(32) NOT NULL; 
ALTER TABLE n_a_goods_return ADD PRIMARY KEY (IDApp);
ALTER TABLE n_a_goods_return
  MODIFY IDApp int(11) NOT NULL AUTO_INCREMENT;
  
----=====================Perbaiki n_a_disposal =========================
DROP TABLE IF EXISTS n_a_disposal;
CREATE TABLE n_a_disposal (
  IDApp int(11) NOT NULL,
  FK_Goods int(11) DEFAULT NULL,
  DateDisposal date NOT NULL,
  IsHasValue tinyint(1) DEFAULT NULL,
  IsSold tinyint(1) DEFAULT NULL,
  SellingPrice decimal(30,4) DEFAULT NULL,
  FK_Responsible_Person int(11) DEFAULT NULL,--PERBAIKAN DI SINI 
  FK_Acc_FA int(11) DEFAULT NULL,--PERBAIKAN DI SINI
  FK_Stock int(11) DEFAULT NULL,
  BookValue decimal(10,4) NOT NULL,
  Descriptions varchar(200) DEFAULT NULL,
  CreatedDate datetime DEFAULT NULL,
  CreatedBy varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE n_a_disposal CHANGE FK_Goods FK_Goods INT(11) UNSIGNED NOT NULL;
ALTER TABLE n_a_disposal add SerialNumber VARCHAR(50) NOT NULL DEFAULT 'N/A';
ALTER TABLE n_a_disposal add TypeApp VARCHAR(32) NOT NULL; 
ALTER TABLE n_a_disposal add FK_Maintenance INT(11) UNSIGNED NULL;
ALTER TABLE n_a_disposal
  ADD PRIMARY KEY (IDApp);
ALTER TABLE n_a_disposal
  MODIFY IDApp int(11) NOT NULL AUTO_INCREMENT;
  
  --================Perbaikan n_a_maintenance================================
  CREATE TABLE IF NOT EXISTS n_a_maintenance (
  IDApp int(11) NOT NULL,
  RequestDate date DEFAULT NULL,
  StartDate date NOT NULL,
  IsStillGuarantee tinyint(1) NOT NULL,
  Expense decimal(30,4) NOT NULL,--PERBAIKAN DI SINI 
  MaintenanceBy varchar(100) NOT NULL,
  PersonalName varchar(100) DEFAULT NULL,
  EndDate date DEFAULT NULL,
  FK_Goods int(11) NOT NULL,
  IsSucced int(11) DEFAULT NULL,
  Descriptions varchar(200) DEFAULT NULL,
  CreatedDate datetime NOT NULL,
  CreatedBy varchar(100) NOT NULL,
  ModifiedDate datetime DEFAULT NULL,
  ModifiedBy varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE n_a_maintenance CHANGE FK_Goods FK_Goods INT(11) UNSIGNED NOT NULL;
ALTER TABLE n_a_maintenance add SerialNumber VARCHAR(50) NOT NULL DEFAULT 'N/A';
ALTER TABLE n_a_maintenance add TypeApp VARCHAR(32) NOT NULL; 
ALTER TABLE n_a_maintenance add IsFinished tinyint(1) NOT NULL DEFAULT 0; 
ALTER TABLE n_a_maintenance MODIFY Expense MODIFY Expense DECIMAL(30,4) NULL,
ALTER TABLE n_a_maintenance
  ADD PRIMARY KEY (IDApp);
ALTER TABLE n_a_maintenance
  MODIFY IDApp int(11) NOT NULL AUTO_INCREMENT;
  
--============perbaikan n_a_goods_Lending==============================
CREATE TABLE n_a_goods_lending (
  IDApp int(11) NOT NULL,
  FK_Goods varchar(30) NOT NULL,
  FK_Employee varchar(50) NOT NULL,
  DateLending date DEFAULT NULL,
  Qty int(11) NOT NULL,
  FK_Stock varchar(50) NOT NULL,
  FK_Responsible_Person varchar(50) DEFAULT NULL,
  BenefitOf varchar(150) DEFAULT NULL,
  FK_Sender varchar(50) DEFAULT NULL,
  Status varchar(10) DEFAULT NULL,
  CreatedDate datetime DEFAULT NULL,
  CreatedBy varchar(50) DEFAULT NULL,
  ModifiedDate datetime DEFAULT NULL,
  ModifiedBy varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE n_a_goods_Lending add SerialNumber VARCHAR(50) NOT NULL DEFAULT 'N/A';
ALTER TABLE n_a_goods_Lending add TypeApp VARCHAR(32) NOT NULL;  
ALTER TABLE n_a_goods_Lending add FK_Maintenance INT(11) UNSIGNED NULL;
ALTER TABLE n_a_goods_lending CHANGE FK_Goods FK_Goods INT(11) UNSIGNED NOT NULL;

--============perbaikan stock==================
ALTER TABLE n_a_stock CHANGE TotalQty T_Goods_Spare tinyint(5) UNSIGNED NOT NULL;--PERBAIKAN DI SINI 
ALTER TABLE n_a_stock DROP COLUMN IF EXISTS T_Goods_Lending;--PERBAIKAN DI SINI
ALTER TABLE n_a_goods_lending
  ADD PRIMARY KEY (IDApp);
ALTER TABLE n_a_goods_lending
  MODIFY IDApp int(11) NOT NULL AUTO_INCREMENT;
  
  
ALTER TABLE n_a_goods_receive ADD REFNO VARCHAR(50) DEFAULT 'N/A';

ALTER TABLE n_a_goods_receive_detail
MODIFY IDApp int(32) NOT NULL AUTO_INCREMENT;
ALTER TABLE n_a_goods_receive_detail CHANGE warranty warranty DECIMAL(6,2) NOT NULL DEFAULT '0';


ALTER TABLE n_a_goods_outwards CHANGE FK_Goods FK_Goods INT(11) UNSIGNED NOT NULL;
ALTER TABLE n_a_goods_outwards add SerialNumber VARCHAR(50) NOT NULL DEFAULT 'N/A';
ALTER TABLE n_a_goods_outwards add TypeApp VARCHAR(32) NOT NULL; 
ALTER TABLE n_a_goods_outwards add FK_Lending INT(11) UNSIGNED NULL;--PERBAIKAN DI SINI 
ALTER TABLE n_a_goods_outwards DROP column IF EXISTS 'NEW';--PERBAIKAN DI SINI 
ALTER TABLE n_a_goods_outwards ADD IsNew TINYINT(1) NOT NULL DEFAULT 0;--PERBAIKAN DI SINI 


ALTER TABLE n_a_acc_fa CHANGE FK_Goods FK_Goods INT(11) UNSIGNED NOT NULL;
ALTER TABLE n_a_acc_fa add SerialNumber VARCHAR(50) NOT NULL DEFAULT 'N/A';
ALTER TABLE n_a_acc_fa add TypeApp VARCHAR(32) NOT NULL; 

