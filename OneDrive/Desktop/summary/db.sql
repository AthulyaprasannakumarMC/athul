/*
SQLyog Community v13.0.1 (64 bit)
MySQL - 5.7.9 : Database - summary_generator
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`summary_generator` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `summary_generator`;

/*Table structure for table `complaints` */

DROP TABLE IF EXISTS `complaints`;

CREATE TABLE `complaints` (
  `complaints_id` int(11) NOT NULL AUTO_INCREMENT,
  `sender_id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL,
  `reply` varchar(100) NOT NULL,
  `date` varchar(100) NOT NULL,
  PRIMARY KEY (`complaints_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `complaints` */

insert  into `complaints`(`complaints_id`,`sender_id`,`title`,`description`,`reply`,`date`) values 
(1,1,'Slow','Slow generation','will check soon','21-02-2024'),
(2,1,'Slow','Slow generation','will check soon','2024-03-20');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `sender_id` int(11) NOT NULL,
  `description` varchar(100) NOT NULL,
  `date` varchar(100) NOT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`feedback_id`,`sender_id`,`description`,`date`) values 
(2,1,'good app','2024-03-21');

/*Table structure for table `files` */

DROP TABLE IF EXISTS `files`;

CREATE TABLE `files` (
  `file_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `file` varchar(100) NOT NULL,
  `date` varchar(100) NOT NULL,
  PRIMARY KEY (`file_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `files` */

/*Table structure for table `general_summary` */

DROP TABLE IF EXISTS `general_summary`;

CREATE TABLE `general_summary` (
  `general_su_idmmary` int(11) NOT NULL AUTO_INCREMENT,
  `file_id` int(11) NOT NULL,
  `general_result_summary` varchar(100) NOT NULL,
  PRIMARY KEY (`general_su_idmmary`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `general_summary` */

/*Table structure for table `gpt_summary` */

DROP TABLE IF EXISTS `gpt_summary`;

CREATE TABLE `gpt_summary` (
  `gpt_summary_id` int(11) NOT NULL AUTO_INCREMENT,
  `file_id` int(11) NOT NULL,
  `gpt_result_summary` varchar(100) NOT NULL,
  PRIMARY KEY (`gpt_summary_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `gpt_summary` */

/*Table structure for table `high_rank_summary` */

DROP TABLE IF EXISTS `high_rank_summary`;

CREATE TABLE `high_rank_summary` (
  `high_rank_summary_id` int(11) NOT NULL AUTO_INCREMENT,
  `file_id` int(11) NOT NULL,
  `high_rank_result_summary` varchar(100) NOT NULL,
  PRIMARY KEY (`high_rank_summary_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `high_rank_summary` */

/*Table structure for table `keywords_summary` */

DROP TABLE IF EXISTS `keywords_summary`;

CREATE TABLE `keywords_summary` (
  `keywords_summary_id` int(11) NOT NULL AUTO_INCREMENT,
  `file_id` int(11) NOT NULL,
  `keywords_result_summary` varchar(100) NOT NULL,
  PRIMARY KEY (`keywords_summary_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `keywords_summary` */

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `usertype` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values 
(1,'admin','admin','admin'),
(2,'athu','athu','user'),
(3,'aishu','aishu','user'),
(4,'miha','miha','user');

/*Table structure for table `review` */

DROP TABLE IF EXISTS `review`;

CREATE TABLE `review` (
  `review_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `review_rating` varchar(100) NOT NULL,
  `date` varchar(100) NOT NULL,
  PRIMARY KEY (`review_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `review` */

insert  into `review`(`review_id`,`user_id`,`review_rating`,`date`) values 
(1,1,'5','2024-03-21');

/*Table structure for table `sentiment_analysis_summary` */

DROP TABLE IF EXISTS `sentiment_analysis_summary`;

CREATE TABLE `sentiment_analysis_summary` (
  `sentiment_analysis_summary_id` int(11) NOT NULL AUTO_INCREMENT,
  `file_id` int(11) NOT NULL,
  `sentiment_analysis_result_summary` varchar(100) NOT NULL,
  PRIMARY KEY (`sentiment_analysis_summary_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `sentiment_analysis_summary` */

/*Table structure for table `simple_words_summary` */

DROP TABLE IF EXISTS `simple_words_summary`;

CREATE TABLE `simple_words_summary` (
  `simple_words_summary_id` int(11) NOT NULL AUTO_INCREMENT,
  `file_id` int(11) NOT NULL,
  `simple_words_results_summary` varchar(100) NOT NULL,
  PRIMARY KEY (`simple_words_summary_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `simple_words_summary` */

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) NOT NULL,
  `fname` varchar(100) NOT NULL,
  `lname` varchar(100) NOT NULL,
  `place` varchar(100) NOT NULL,
  `phone` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_id`,`login_id`,`fname`,`lname`,`place`,`phone`,`email`) values 
(1,2,'Athulya','MC','Mundemadathil Chirangara valappil(ho) Mezhathur (po), Thrithala','2345678901','SSSSSSSS'),
(2,4,'Aish','PM','ssd','3456','fg'),
(3,5,'Pavi','CR','aaaa','3456','hg');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
