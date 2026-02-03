CREATE TABLE IF NOT EXISTS usuario (
    nome TEXT PRIMARY KEY,
    senha TEXT NOT NULL,

    data_reforjar DATE,
    data_cartas_diarias DATE,
    data_fundir DATE
);
