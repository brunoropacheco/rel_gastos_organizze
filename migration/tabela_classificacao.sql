-- Criacao do Banco --
CREATE DATABASE rel_gastos_organizze;
USE rel_gastos_organizze;
-- Criacao da tabela
CREATE TABLE classificacao (
    termo VARCHAR(255) NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    PRIMARY KEY (termo)
);

-- Inserção dos termos para a categoria 'viagem'
INSERT INTO classificacao (termo, categoria) VALUES ('movida', 'viagem');
INSERT INTO classificacao (termo, categoria) VALUES ('rentcars', 'viagem');
INSERT INTO classificacao (termo, categoria) VALUES ('melia', 'viagem');
INSERT INTO classificacao (termo, categoria) VALUES ('latam', 'viagem');
INSERT INTO classificacao (termo, categoria) VALUES ('iberia', 'viagem');
INSERT INTO classificacao (termo, categoria) VALUES ('unidas', 'viagem');
INSERT INTO classificacao (termo, categoria) VALUES ('airbnb', 'viagem');
INSERT INTO classificacao (termo, categoria) VALUES ('azul', 'viagem');
INSERT INTO classificacao (termo, categoria) VALUES ('smiles', 'viagem');
INSERT INTO classificacao (termo, categoria) VALUES ('gol', 'viagem');
INSERT INTO classificacao (termo, categoria) VALUES ('city_hall', 'viagem');
INSERT INTO classificacao (termo, categoria) VALUES ('foco_aluguel', 'viagem');
INSERT INTO classificacao (termo, categoria) VALUES ('tam_lin', 'viagem');

-- Inserção dos termos para a categoria 'alimentacao_casa'
INSERT INTO classificacao (termo, categoria) VALUES ('hfruti_dcm', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('dom_atacadista', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('rede_economia', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('sam_s_club', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('buffet', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('hortifruti', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('mercado_', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('pao_de_açucar', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('mercear', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('hermon', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('tempero', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('alimento', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('padar', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('depos', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('sams', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('assai', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('pao_de', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('lulu', 'alimentacao_casa');
INSERT INTO classificacao (termo, categoria) VALUES ('frutas', 'alimentacao_casa');

-- Inserção do termo para a categoria 'seguro_carro'
INSERT INTO classificacao (termo, categoria) VALUES ('hdi', 'seguro_carro');

-- Inserção dos termos para a categoria 'transp(ub+gas+vel+ccr)'
INSERT INTO classificacao (termo, categoria) VALUES ('centro_automotivo_pend', 'transp(ub+gas+vel+ccr)');
INSERT INTO classificacao (termo, categoria) VALUES ('uber', 'transp(ub+gas+vel+ccr)');
INSERT INTO classificacao (termo, categoria) VALUES ('pop_', 'transp(ub+gas+vel+ccr)');
INSERT INTO classificacao (termo, categoria) VALUES ('99_tecnologia', 'transp(ub+gas+vel+ccr)');
INSERT INTO classificacao (termo, categoria) VALUES ('99app', 'transp(ub+gas+vel+ccr)');
INSERT INTO classificacao (termo, categoria) VALUES ('estaciona', 'transp(ub+gas+vel+ccr)');
INSERT INTO classificacao (termo, categoria) VALUES ('posto', 'transp(ub+gas+vel+ccr)');
INSERT INTO classificacao (termo, categoria) VALUES ('conectcar', 'transp(ub+gas+vel+ccr)');
INSERT INTO classificacao (termo, categoria) VALUES ('tembici', 'transp(ub+gas+vel+ccr)');
INSERT INTO classificacao (termo, categoria) VALUES ('park', 'transp(ub+gas+vel+ccr)');
INSERT INTO classificacao (termo, categoria) VALUES ('barcas', 'transp(ub+gas+vel+ccr)');
INSERT INTO classificacao (termo, categoria) VALUES ('digipare', 'transp(ub+gas+vel+ccr)');
INSERT INTO classificacao (termo, categoria) VALUES ('auto_pos', 'transp(ub+gas+vel+ccr)');

-- Inserção dos termos para a categoria 'compras'
INSERT INTO classificacao (termo, categoria) VALUES ('pantys', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('borelli_niteroi', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('relusa', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('lojas_g', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('roupas', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('panna', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('assb_comerci', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('toy_boy', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('kop', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('happy', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('presente', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('daiso', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('picadilly', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('elister_joias', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('nestle_brasil_ltda', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('arte_dos_vinhos', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('riachuelo', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('americanas', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('cell', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('mundo_baby', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('centauro', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('cea', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('renner', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('pag*lojasrennersa', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('iphone', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('casa_e_vi', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('marketplace', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('mr_cat', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('cresci_e_perdi', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('tonys_baby', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('cirandinha_baby', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('loungerie', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('amazon', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('shein', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('calcad', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('mercadolivre', 'compras');
INSERT INTO classificacao (termo, categoria) VALUES ('compras', 'compras');

-- Inserção dos termos para a categoria 'assinaturas'
INSERT INTO classificacao (termo, categoria) VALUES ('produtos_globo', 'assinaturas');
INSERT INTO classificacao (termo, categoria) VALUES ('ilha_mix', 'assinaturas');
INSERT INTO classificacao (termo, categoria) VALUES ('melimais', 'assinaturas');
INSERT INTO classificacao (termo, categoria) VALUES ('netflix', 'assinaturas');
INSERT INTO classificacao (termo, categoria) VALUES ('spotify', 'assinaturas');
INSERT INTO classificacao (termo, categoria) VALUES ('apple.com/bill', 'assinaturas');
INSERT INTO classificacao (termo, categoria) VALUES ('apple_com/bill', 'assinaturas');
INSERT INTO classificacao (termo, categoria) VALUES ('primebr', 'assinaturas');
INSERT INTO classificacao (termo, categoria) VALUES ('doist', 'assinaturas');

-- Inserção dos termos para a categoria 'saude'
INSERT INTO classificacao (termo, categoria) VALUES ('dermage', 'saude');
INSERT INTO classificacao (termo, categoria) VALUES ('drog', 'saude');
INSERT INTO classificacao (termo, categoria) VALUES ('labora', 'saude');

-- Inserção dos termos para a categoria 'casa'
INSERT INTO classificacao (termo, categoria) VALUES ('midea', 'casa');
INSERT INTO classificacao (termo, categoria) VALUES ('calhas', 'casa');
INSERT INTO classificacao (termo, categoria) VALUES ('first_class', 'casa');
INSERT INTO classificacao (termo, categoria) VALUES ('chaveiro', 'casa');
INSERT INTO classificacao (termo, categoria) VALUES ('leroy', 'casa');
INSERT INTO classificacao (termo, categoria) VALUES ('angela', 'casa');
INSERT INTO classificacao (termo, categoria) VALUES ('camica', 'casa');
INSERT INTO classificacao (termo, categoria) VALUES ('tok', 'casa');
INSERT INTO classificacao (termo, categoria) VALUES ('darkstore', 'casa');
INSERT INTO classificacao (termo, categoria) VALUES ('obras_casa', 'casa');
INSERT INTO classificacao (termo, categoria) VALUES ('eletrodomestico', 'casa');

-- Inserção dos termos para a categoria 'educacao'
INSERT INTO classificacao (termo, categoria) VALUES ('infne', 'educacao');
INSERT INTO classificacao (termo, categoria) VALUES ('cisco', 'educacao');
INSERT INTO classificacao (termo, categoria) VALUES ('rdmedicine', 'educacao');
INSERT INTO classificacao (termo, categoria) VALUES ('papelaria', 'educacao');
INSERT INTO classificacao (termo, categoria) VALUES ('livraria', 'educacao');
INSERT INTO classificacao (termo, categoria) VALUES ('colegio', 'educacao');
INSERT INTO classificacao (termo, categoria) VALUES ('saraiva', 'educacao');
INSERT INTO classificacao (termo, categoria) VALUES ('cursos', 'educacao');
INSERT INTO classificacao (termo, categoria) VALUES ('curso', 'educacao');
INSERT INTO classificacao (termo, categoria) VALUES ('escola', 'educacao');
INSERT INTO classificacao (termo, categoria) VALUES ('faculdade', 'educacao');
INSERT INTO classificacao (termo, categoria) VALUES ('universidade', 'educacao');

-- Inserção do termo para a categoria 'esporte'
INSERT INTO classificacao (termo, categoria) VALUES ('funcional', 'esporte');

-- Inserção dos termos para a categoria 'diversao-lazer-comida'
INSERT INTO classificacao (termo, categoria) VALUES ('cheirin_bao', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('belarmino', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('mcdonald', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('burger', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('subway', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('kfc', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('bobs', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('outback', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('pizza', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('boulevard_go', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('starbuc', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('cookie', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('cafe', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('ex_touro', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('beco_do_espa', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('rockribs', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('lanch', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('suco', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('megamatte', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('chocolate', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('rei_do_mate', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('sunomono', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('drink', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('convenie', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('hot_dog', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('rest', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('food', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('emporio', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('bacio_di', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('verdanna', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('ifd', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('comida_fora', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('rio_arena', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('beto_carrero', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('ticket', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('rio_Arena', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('coffee', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('casal_20', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('panito', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('sush', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('sabor', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('cheiro', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('delicate', 'diversao-lazer-comida');
INSERT INTO classificacao (termo, categoria) VALUES ('art_cafe_lapa', 'diversao-lazer-comida');

-- Inserção dos termos para a categoria 'beleza'
INSERT INTO classificacao (termo, categoria) VALUES ('natura___propria', 'beleza');
INSERT INTO classificacao (termo, categoria) VALUES ('maboltt', 'beleza');
INSERT INTO classificacao (termo, categoria) VALUES ('chic', 'beleza');
INSERT INTO classificacao (termo, categoria) VALUES ('cabel', 'beleza');
INSERT INTO classificacao (termo, categoria) VALUES ('sephora', 'beleza');
INSERT INTO classificacao (termo, categoria) VALUES ('skin', 'beleza');
INSERT INTO classificacao (termo, categoria) VALUES ('boticario', 'beleza');
INSERT INTO classificacao (termo, categoria) VALUES ('_beleza', 'beleza');

-- Inserção do termo para a categoria 'anuidade'
INSERT INTO classificacao (termo, categoria) VALUES ('anuid', 'anuidade');

-- Observação: Caso nenhum termo seja reconhecido, a lógica da função pode definir a categoria 'outros'.
