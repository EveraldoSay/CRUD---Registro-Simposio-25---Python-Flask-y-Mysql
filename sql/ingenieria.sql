-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 12-02-2025 a las 17:30:57
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ingenieria`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registros`
--

CREATE TABLE `registros` (
  `Id_Registro` int(11) NOT NULL,
  `Carnet_Carrera` varchar(10) NOT NULL,
  `Carnet_Anio` varchar(2) NOT NULL,
  `Carnet_Correlativo` varchar(10) NOT NULL,
  `Primer_Nombre` varchar(120) NOT NULL,
  `Segundo_Nombre` varchar(20) NOT NULL,
  `Primer_Apellido` varchar(20) NOT NULL,
  `Segundo_Apellido` varchar(20) NOT NULL,
  `Telefono` int(8) NOT NULL,
  `Correo` varchar(100) NOT NULL,
  `Pagado` tinyint(1) NOT NULL DEFAULT 0,
  `Fecha_Nacimiento` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `registros`
--

INSERT INTO `registros` (`Id_Registro`, `Carnet_Carrera`, `Carnet_Anio`, `Carnet_Correlativo`, `Primer_Nombre`, `Segundo_Nombre`, `Primer_Apellido`, `Segundo_Apellido`, `Telefono`, `Correo`, `Pagado`, `Fecha_Nacimiento`) VALUES
(3, '1490', '21', '64490', 'Edvin', 'Everaldo', 'De Leon', 'Say', 88665511, 'deleonedvin94@gmail.com', 0, '2000-07-09'),
(4, '1490', '23', '7616', 'Jeniferr', 'Andrea', 'Morales', 'Morales', 12345678, 'jrponcio65@gmail.com', 1, '2003-09-08');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `registros`
--
ALTER TABLE `registros`
  ADD PRIMARY KEY (`Id_Registro`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `registros`
--
ALTER TABLE `registros`
  MODIFY `Id_Registro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
