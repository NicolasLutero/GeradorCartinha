CREATE TABLE pedido (
    id INTEGER PRIMARY KEY,
    cliente VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    valor NUMERIC(10,2) NOT NULL,
    deletado BOOLEAN DEFAULT FALSE
);
