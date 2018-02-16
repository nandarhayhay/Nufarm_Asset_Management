-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Jan 28, 2018 at 02:30 PM
-- Server version: 10.2.11-MariaDB
-- PHP Version: 7.0.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `na_ms`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `IDApp` int(11) NOT NULL,
  `NIK` varchar(50) NOT NULL,
  `Employee_Name` varchar(150) DEFAULT NULL,
  `TypeApp` varchar(1) DEFAULT NULL,
  `JobType` varchar(150) DEFAULT NULL,
  `Gender` varchar(10) NOT NULL,
  `Status` varchar(1) DEFAULT NULL,
  `TelpHP` varchar(20) DEFAULT NULL,
  `Territory` varchar(50) DEFAULT NULL,
  `Descriptions` varchar(50) DEFAULT NULL,
  `InActive` varchar(5) NOT NULL,
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` varchar(100) NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Triggers `employee`
--
DELIMITER $$
CREATE TRIGGER `Created_Employee_Log` AFTER INSERT ON `employee` FOR EACH ROW begin
set @toJSON = concat("{""created""",":", "[", """",new.nik,"""",",","""",new.employee_name,"""", ",", """",new.typeapp,"""",",", """",new.jobtype,"""",",","""",new.gender,"""",",","""",new.status,"""",",","""",new.telphp,"""",",","""",new.territory,"""",",","""",new.descriptions,"""",",", """",new.inactive,"""",",", """",new.createdby,"""" "]}");
insert into LogEvent(NameApp, TypeApp, descriptionsapp, CreatedDate, CreatedBy) values("Created Employee", "P", @toJSON, now(), new.createdby);
end
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `Updated_Employee_Log` AFTER UPDATE ON `employee` FOR EACH ROW begin
set @toJSON = concat("{""after""",":", "[", """",new.nik,"""",",","""",new.employee_name,"""", ",", """",new.typeapp,"""",",", """",new.jobtype,"""",",","""",new.gender,"""",",","""",new.status,"""",",","""",new.telphp,"""",",","""",new.territory,"""",",","""",new.descriptions,"""",",", """",new.inactive,"""",",", """",new.createdby,"""" "]",",","""before""",":","[","""",old.nik,"""",",","""",old.employee_name,"""", ",", """",old.typeapp,"""",",", """",old.jobtype,"""",",","""",old.gender,"""",",","""",old.status,"""",",","""",old.telphp,"""",",","""",old.territory,"""",",","""",old.descriptions,"""",",", """",old.inactive,"""",",", """",old.createdby,"""" "]}");
insert into LogEvent(NameApp, TypeApp, descriptionsapp, CreatedDate, CreatedBy) values("Updated Employee", "P", @toJSON, now(), new.modifiedby);
end
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `logevent`
--

CREATE TABLE `logevent` (
  `IDApp` int(11) NOT NULL,
  `NameApp` varchar(30) NOT NULL,
  `TypeApp` varchar(10) NOT NULL,
  `descriptionsapp` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `na_user_user`
--

CREATE TABLE `na_user_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `username` varchar(250) NOT NULL,
  `first_name` varchar(256) NOT NULL,
  `last_name` varchar(256) NOT NULL,
  `email` varchar(254) NOT NULL,
  `picture` varchar(100) DEFAULT NULL,
  `height_field` int(11) DEFAULT NULL,
  `width_field` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `na_user_user_groups`
--

CREATE TABLE `na_user_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `na_user_user_user_permissions`
--

CREATE TABLE `na_user_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `n_a_suplier`
--

CREATE TABLE `n_a_suplier` (
  `SuplierCode` varchar(30) NOT NULL,
  `SuplierName` varchar(100) DEFAULT NULL,
  `Address` varchar(150) DEFAULT NULL,
  `Telp` varchar(20) DEFAULT NULL,
  `HP` varchar(20) DEFAULT NULL,
  `ContactPerson` varchar(100) DEFAULT NULL,
  `InActive` varchar(3) NOT NULL,
  `CreatedDate` datetime DEFAULT NULL,
  `CreatedBy` varchar(100) DEFAULT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Triggers `n_a_suplier`
--
DELIMITER $$
CREATE TRIGGER `Create_Suplier_Log` AFTER INSERT ON `n_a_suplier` FOR EACH ROW begin
set @toJSON = concat("{""created""",":", "[", """",new.supliercode,"""",",","""",new.supliername,"""", ",", """",new.address,"""",",", """",new.telp,"""",",","""",new.hp,"""",",","""",new.contactperson,"""",",","""",new.inactive,"""",",","""",new.createddate,"""",",", """",new.createdby,"""" "]}");
insert into LogEvent(NameApp, TypeApp, descriptionsapp, CreatedDate, CreatedBy) values("Created Suplier", "P", @toJSON, now(), new.createdby);
end
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `Update_Suplier_Log` AFTER UPDATE ON `n_a_suplier` FOR EACH ROW begin
set @toJSON = concat("{""after""",":", "[", """",new.supliercode,"""",",","""",new.supliername,"""",",","""",new.address,"""", ",", """",new.telp,"""",",", """",new.hp,"""",",","""",new.contactperson,"""",",", """",new.inactive,"""",",","""",new.createddate,"""",",", """",new.createdby,"""",",","""",new.modifieddate,"""",",","""",new.modifiedby,"""" "]",",","""before""",":","[","""",old.supliercode,"""",",","""",old.supliername,"""",",","""",old.address,"""",",","""",old.telp,"""",",","""",old.hp,"""",",","""",old.contactperson,"""",",","""",old.inactive,"""",",","""",old.createddate,"""",",","""",old.createdby,"""","]}");
insert into LogEvent(NameApp, TypeApp, descriptionsapp, CreatedDate, CreatedBy) values("Updated Suplier", "P", @toJSON, now(), new.modifiedby);
end
$$
DELIMITER ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_NA_User_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`IDApp`);

--
-- Indexes for table `logevent`
--
ALTER TABLE `logevent`
  ADD PRIMARY KEY (`IDApp`);

--
-- Indexes for table `na_user_user`
--
ALTER TABLE `na_user_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `na_user_user_groups`
--
ALTER TABLE `na_user_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `NA_User_user_groups_user_id_group_id_eafe9f63_uniq` (`user_id`,`group_id`),
  ADD KEY `NA_User_user_groups_group_id_6a664286_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `na_user_user_user_permissions`
--
ALTER TABLE `na_user_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `NA_User_user_user_permis_user_id_permission_id_6fb77bae_uniq` (`user_id`,`permission_id`),
  ADD KEY `NA_User_user_user_pe_permission_id_6cbe9ddb_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `n_a_suplier`
--
ALTER TABLE `n_a_suplier`
  ADD PRIMARY KEY (`SuplierCode`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;
--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=80;
--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `IDApp` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=166;
--
-- AUTO_INCREMENT for table `logevent`
--
ALTER TABLE `logevent`
  MODIFY `IDApp` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=336;
--
-- AUTO_INCREMENT for table `na_user_user`
--
ALTER TABLE `na_user_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `na_user_user_groups`
--
ALTER TABLE `na_user_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `na_user_user_user_permissions`
--
ALTER TABLE `na_user_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_NA_User_user_id` FOREIGN KEY (`user_id`) REFERENCES `na_user_user` (`id`);

--
-- Constraints for table `na_user_user_groups`
--
ALTER TABLE `na_user_user_groups`
  ADD CONSTRAINT `NA_User_user_groups_group_id_6a664286_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `NA_User_user_groups_user_id_a3a5e655_fk_NA_User_user_id` FOREIGN KEY (`user_id`) REFERENCES `na_user_user` (`id`);

--
-- Constraints for table `na_user_user_user_permissions`
--
ALTER TABLE `na_user_user_user_permissions`
  ADD CONSTRAINT `NA_User_user_user_pe_permission_id_6cbe9ddb_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `NA_User_user_user_pe_user_id_1bb88007_fk_NA_User_u` FOREIGN KEY (`user_id`) REFERENCES `na_user_user` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
