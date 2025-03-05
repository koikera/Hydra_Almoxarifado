CREATE DATABASE almoxarifado;

USE almoxarifado;

CREATE TABLE usuario (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(250),
    senha VARCHAR(250),
    email VARCHAR(250),
    telefone VARCHAR(50),
    permissao VARCHAR(250),
    PRIMARY KEY (id)
);

