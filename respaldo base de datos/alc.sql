-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 01-10-2025 a las 15:58:43
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `alc`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ayudas`
--

CREATE TABLE `ayudas` (
  `id` int(11) NOT NULL,
  `idP` int(11) NOT NULL,
  `idUs` int(11) NOT NULL,
  `motivo_caso` enum('Ayudas Sociales','Ayudas Económicas','Ayudas Técnicas (Médicas)','Solicitud de Medicinas','Quejas, Sugerencias y/o Denuncias') NOT NULL DEFAULT 'Ayudas Sociales',
  `especificacion_caso` varchar(200) NOT NULL DEFAULT '',
  `valor_inversion_social` decimal(10,2) DEFAULT 0.00,
  `tpayuda` varchar(60) NOT NULL,
  `valayuda` int(11) NOT NULL,
  `FechaSolicitud` date NOT NULL,
  `FechaEntrega` date DEFAULT NULL,
  `descayuda` varchar(300) NOT NULL,
  `estado` varchar(40) NOT NULL,
  `remitido` enum('No','Sí') NOT NULL DEFAULT 'No',
  `entidad_remision` varchar(200) DEFAULT NULL,
  `fecha_remision` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ayudas`
--

INSERT INTO `ayudas` (`id`, `idP`, `idUs`, `motivo_caso`, `especificacion_caso`, `valor_inversion_social`, `tpayuda`, `valayuda`, `FechaSolicitud`, `FechaEntrega`, `descayuda`, `estado`, `remitido`, `entidad_remision`, `fecha_remision`) VALUES
(6, 1, 1, 'Ayudas Sociales', 'Tanques', 30.00, 'Tanques', 30, '2025-03-24', '2025-03-24', 'un tanque de agua', 'Entregado', 'No', NULL, NULL),
(7, 1, 1, 'Ayudas Económicas', 'Economica', 100.00, 'Economica', 100, '2025-03-24', '2025-03-24', '100 dolitas', 'Entregado', 'No', NULL, NULL),
(8, 4, 1, 'Ayudas Económicas', 'Economica', 100.00, 'Economica', 100, '2025-04-04', '2025-04-04', 'dinero\r\n', 'Entregado', 'Sí', 'Secretaría de Educación', '2025-10-01'),
(9, 11, 1, 'Ayudas Sociales', 'Tanques de agua', 70.00, '', 0, '2025-10-01', NULL, 'solicitud de tanque de agua', 'Aprobado', 'No', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `persona`
--

CREATE TABLE `persona` (
  `id` int(11) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `cedula` varchar(30) NOT NULL,
  `direccion` text NOT NULL,
  `telefono` varchar(30) NOT NULL,
  `comuna` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `persona`
--

INSERT INTO `persona` (`id`, `nombre`, `cedula`, `direccion`, `telefono`, `comuna`) VALUES
(1, 'macyulis gonzalez', '27878085', 'los pilotines', '04245848948', 'volcadero'),
(4, 'Medsi Jove', '52841000', 'asdasd', '04245848948', 'Barrio Colombia'),
(8, 'macyulis gonzalez', '11420917', 'qfqdf', '04245848948', 'Victoria Perfecta'),
(11, 'Monica Larez', '14477826', 'Guanta', '04121783971', 'Francisco de Miranda');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `usuario` varchar(40) NOT NULL,
  `clave` varchar(60) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `cedula` varchar(30) NOT NULL,
  `rol` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `usuario`, `clave`, `nombre`, `cedula`, `rol`) VALUES
(1, 'Adrianmbt', 'adrianmbt1', 'Adrian M. Bello', '19674244', 'Administrador');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `ayudas`
--
ALTER TABLE `ayudas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `persona` (`idP`);

--
-- Indices de la tabla `persona`
--
ALTER TABLE `persona`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `ayudas`
--
ALTER TABLE `ayudas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `persona`
--
ALTER TABLE `persona`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
