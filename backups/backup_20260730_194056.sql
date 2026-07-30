--
-- PostgreSQL database dump
--

\restrict Rk122LrZRyZ6f4B6TtytTxCVhQOdQ8zEHCiiPhev6lH3tezSoDbctRmUwAlDUO3

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admins (
    id integer NOT NULL,
    full_name character varying,
    login character varying,
    password_hash character varying
);


ALTER TABLE public.admins OWNER TO postgres;

--
-- Name: COLUMN admins.full_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.admins.full_name IS 'ФИО администратора';


--
-- Name: COLUMN admins.login; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.admins.login IS 'Логин для входа';


--
-- Name: COLUMN admins.password_hash; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.admins.password_hash IS 'Хеш пароля';


--
-- Name: admins_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.admins_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.admins_id_seq OWNER TO postgres;

--
-- Name: admins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.admins_id_seq OWNED BY public.admins.id;


--
-- Name: bays; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bays (
    id integer NOT NULL,
    number character varying,
    capacity integer
);


ALTER TABLE public.bays OWNER TO postgres;

--
-- Name: COLUMN bays.number; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.bays.number IS 'Номер бокса';


--
-- Name: COLUMN bays.capacity; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.bays.capacity IS 'Лимит вместимости (ФТ4)';


--
-- Name: bays_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bays_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bays_id_seq OWNER TO postgres;

--
-- Name: bays_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bays_id_seq OWNED BY public.bays.id;


--
-- Name: callback_requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.callback_requests (
    id integer NOT NULL,
    client_name character varying,
    phone character varying,
    status character varying,
    created_at timestamp without time zone
);


ALTER TABLE public.callback_requests OWNER TO postgres;

--
-- Name: COLUMN callback_requests.client_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.callback_requests.client_name IS 'Имя клиента';


--
-- Name: COLUMN callback_requests.phone; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.callback_requests.phone IS 'Телефон для связи';


--
-- Name: COLUMN callback_requests.status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.callback_requests.status IS 'Ожидает обработки / Обработана';


--
-- Name: COLUMN callback_requests.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.callback_requests.created_at IS 'Дата создания';


--
-- Name: callback_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.callback_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.callback_requests_id_seq OWNER TO postgres;

--
-- Name: callback_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.callback_requests_id_seq OWNED BY public.callback_requests.id;


--
-- Name: cars; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cars (
    id integer NOT NULL,
    client_id integer,
    brand_model character varying,
    license_plate character varying,
    vin character varying
);


ALTER TABLE public.cars OWNER TO postgres;

--
-- Name: COLUMN cars.client_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cars.client_id IS 'Связь с клиентом (ФТ1)';


--
-- Name: COLUMN cars.brand_model; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cars.brand_model IS 'Марка и модель';


--
-- Name: COLUMN cars.license_plate; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cars.license_plate IS 'Гос. номер';


--
-- Name: COLUMN cars.vin; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cars.vin IS 'VIN-код';


--
-- Name: cars_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cars_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cars_id_seq OWNER TO postgres;

--
-- Name: cars_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cars_id_seq OWNED BY public.cars.id;


--
-- Name: clients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clients (
    id integer NOT NULL,
    full_name character varying,
    phone character varying,
    email character varying,
    password_hash character varying,
    visit_count integer,
    current_discount numeric
);


ALTER TABLE public.clients OWNER TO postgres;

--
-- Name: COLUMN clients.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.clients.id IS 'Уникальный ID клиента';


--
-- Name: COLUMN clients.full_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.clients.full_name IS 'ФИО';


--
-- Name: COLUMN clients.phone; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.clients.phone IS 'Используется для входа';


--
-- Name: COLUMN clients.email; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.clients.email IS 'Используется для входа';


--
-- Name: COLUMN clients.password_hash; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.clients.password_hash IS 'Хеш пароля (НФТ2)';


--
-- Name: COLUMN clients.visit_count; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.clients.visit_count IS 'Счетчик посещений для ФТ3';


--
-- Name: COLUMN clients.current_discount; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.clients.current_discount IS 'Текущий % скидки';


--
-- Name: clients_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clients_id_seq OWNER TO postgres;

--
-- Name: clients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clients_id_seq OWNED BY public.clients.id;


--
-- Name: discount_rules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.discount_rules (
    id integer NOT NULL,
    min_visits integer,
    max_visits integer,
    discount_percent numeric
);


ALTER TABLE public.discount_rules OWNER TO postgres;

--
-- Name: COLUMN discount_rules.min_visits; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.discount_rules.min_visits IS 'Минимальное количество посещений';


--
-- Name: COLUMN discount_rules.max_visits; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.discount_rules.max_visits IS 'Максимальное количество посещений';


--
-- Name: COLUMN discount_rules.discount_percent; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.discount_rules.discount_percent IS 'Правила начисления скидок (ФТ3)';


--
-- Name: discount_rules_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.discount_rules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.discount_rules_id_seq OWNER TO postgres;

--
-- Name: discount_rules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.discount_rules_id_seq OWNED BY public.discount_rules.id;


--
-- Name: mechanics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mechanics (
    id integer NOT NULL,
    full_name character varying,
    specialization character varying,
    login character varying,
    password_hash character varying
);


ALTER TABLE public.mechanics OWNER TO postgres;

--
-- Name: COLUMN mechanics.full_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanics.full_name IS 'ФИО мастера';


--
-- Name: COLUMN mechanics.specialization; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanics.specialization IS 'Профиль мастера (ФТ2)';


--
-- Name: COLUMN mechanics.login; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanics.login IS 'Логин для входа';


--
-- Name: COLUMN mechanics.password_hash; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mechanics.password_hash IS 'Хеш пароля';


--
-- Name: mechanics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mechanics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mechanics_id_seq OWNER TO postgres;

--
-- Name: mechanics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mechanics_id_seq OWNED BY public.mechanics.id;


--
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    id integer NOT NULL,
    order_id integer,
    service_id integer,
    quantity integer,
    fact_price numeric
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- Name: COLUMN order_items.order_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.order_items.order_id IS 'Связь с заказ-нарядом';


--
-- Name: COLUMN order_items.service_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.order_items.service_id IS 'Связь с услугой';


--
-- Name: COLUMN order_items.quantity; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.order_items.quantity IS 'Количество';


--
-- Name: COLUMN order_items.fact_price; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.order_items.fact_price IS 'Фактическая цена';


--
-- Name: order_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_items_id_seq OWNER TO postgres;

--
-- Name: order_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_items_id_seq OWNED BY public.order_items.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    client_id integer,
    car_id integer,
    mechanic_id integer,
    bay_id integer,
    status character varying,
    planned_start timestamp without time zone,
    planned_end timestamp without time zone,
    total_cost numeric,
    discount_amount numeric,
    final_cost numeric,
    payment_method character varying,
    created_at timestamp without time zone
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: COLUMN orders.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.id IS 'Заказ-наряд (ФТ2)';


--
-- Name: COLUMN orders.mechanic_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.mechanic_id IS 'Назначенный мастер';


--
-- Name: COLUMN orders.bay_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.bay_id IS 'Назначенный бокс';


--
-- Name: COLUMN orders.status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.status IS 'Ожидает / В работе / Выполнено / Завершена';


--
-- Name: COLUMN orders.planned_start; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.planned_start IS 'Планируемое начало';


--
-- Name: COLUMN orders.planned_end; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.planned_end IS 'Планируемое окончание';


--
-- Name: COLUMN orders.total_cost; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.total_cost IS 'Общая стоимость до скидки';


--
-- Name: COLUMN orders.discount_amount; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.discount_amount IS 'Сумма скидки';


--
-- Name: COLUMN orders.final_cost; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.final_cost IS 'Итоговая стоимость';


--
-- Name: COLUMN orders.payment_method; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.payment_method IS 'Способ оплаты';


--
-- Name: COLUMN orders.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.orders.created_at IS 'Дата создания';


--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_id_seq OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: services; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.services (
    id integer NOT NULL,
    name character varying,
    price numeric,
    req_specialization character varying,
    duration_hours integer DEFAULT 1
);


ALTER TABLE public.services OWNER TO postgres;

--
-- Name: COLUMN services.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.services.name IS 'Название услуги (ФТ6)';


--
-- Name: COLUMN services.price; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.services.price IS 'Фиксированная цена';


--
-- Name: COLUMN services.req_specialization; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.services.req_specialization IS 'Требуемый профиль мастера';


--
-- Name: services_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.services_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.services_id_seq OWNER TO postgres;

--
-- Name: services_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.services_id_seq OWNED BY public.services.id;


--
-- Name: admins id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins ALTER COLUMN id SET DEFAULT nextval('public.admins_id_seq'::regclass);


--
-- Name: bays id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bays ALTER COLUMN id SET DEFAULT nextval('public.bays_id_seq'::regclass);


--
-- Name: callback_requests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.callback_requests ALTER COLUMN id SET DEFAULT nextval('public.callback_requests_id_seq'::regclass);


--
-- Name: cars id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars ALTER COLUMN id SET DEFAULT nextval('public.cars_id_seq'::regclass);


--
-- Name: clients id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients ALTER COLUMN id SET DEFAULT nextval('public.clients_id_seq'::regclass);


--
-- Name: discount_rules id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discount_rules ALTER COLUMN id SET DEFAULT nextval('public.discount_rules_id_seq'::regclass);


--
-- Name: mechanics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mechanics ALTER COLUMN id SET DEFAULT nextval('public.mechanics_id_seq'::regclass);


--
-- Name: order_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items ALTER COLUMN id SET DEFAULT nextval('public.order_items_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: services id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.services ALTER COLUMN id SET DEFAULT nextval('public.services_id_seq'::regclass);


--
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admins (id, full_name, login, password_hash) FROM stdin;
1	Админ Иван	admin_root	$2b$12$hIg83lH.7gg/uIAs61HNs.M0cEJSMPntcBvp9r.KEc3I1jE6V2Zym
\.


--
-- Data for Name: bays; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bays (id, number, capacity) FROM stdin;
1	1	1
2	1	1
3	2	1
4	2	1
\.


--
-- Data for Name: callback_requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.callback_requests (id, client_name, phone, status, created_at) FROM stdin;
2	Никита	+79835828441	Обработана	2026-07-27 14:58:51.457143
1	Никита	+79885888844	Обработана	2026-07-23 13:06:35.473173
3	Ашов Никита Анатольевич	+79835828441	Обработана	2026-07-30 11:17:34.530192
4	Ашов Никита Анатольевич	+79835828441	Ожидает обработки	2026-07-30 11:46:26.235023
\.


--
-- Data for Name: cars; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cars (id, client_id, brand_model, license_plate, vin) FROM stdin;
2	1	BMW X5	А136ВС70	1FTFW1EF6JEA00000
3	6	BMW X5	А111АА 70	
\.


--
-- Data for Name: clients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clients (id, full_name, phone, email, password_hash, visit_count, current_discount) FROM stdin;
3	Иванов Иван Иванович	+79001999234567	ivan2@example.com	$2b$12$c9fxmRXXE5y1KM.Ffwieju8i0Yc.W1zOoTf0/c5506AKMbUH3OHcu	0	0.0
4	Петров Петр Петрович	+79007654321	petr@example.com	$2b$12$IdcPceTxrytMzaNFKplFTuLOR/khUp.UkN83bhe5aIAp3ea3SAwFS	0	0.0
1	Иванов Иван Иванович	+79001234567	ivan@example.com	$2b$12$JR.Tb0WmWGKor07QsNyqP.lU96atsbPga7rx6ZoCLFd5ilZ8e.5dS	1	0.0
6	Ашов Никита Анатольевич	+79835828441	delovoy.nikita.ashov@gmail.com	$2b$12$OhuruROu6hnltGXk9I6W5.kHOocrMNYZa7SPU59tFx9ImbtX/rdVi	13	10.0
\.


--
-- Data for Name: discount_rules; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.discount_rules (id, min_visits, max_visits, discount_percent) FROM stdin;
1	0	2	0.0
2	3	5	5.0
3	6	100	10.0
\.


--
-- Data for Name: mechanics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mechanics (id, full_name, specialization, login, password_hash) FROM stdin;
2	Иванов Иван	Электрик	ivan_mech	hash123
3	Петров Петр	Электрик	petr_mech	hash123
4	Сидоров Сидор	Ходовик	sidor_mech	hash123
5	Мастер Саша	Электрик	sasha_mech	$2b$12$hIg83lH.7gg/uIAs61HNs.M0cEJSMPntcBvp9r.KEc3I1jE6V2Zym
1	Иванов Иван Иванович	Ходовик	12345	\N
\.


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_items (id, order_id, service_id, quantity, fact_price) FROM stdin;
1	1	1	1	1000
2	1	2	2	500
9	1	1	1	1000
10	1	1	1	500
11	8	1	1	1000
12	9	2	1	500
13	10	3	1	2500
14	11	3	1	2500
15	12	3	1	2500
16	13	3	1	2500
17	14	3	1	2500
18	15	1	1	1000
19	16	1	1	1000
20	17	1	1	1000
21	18	3	1	2500
22	19	3	1	2500
23	20	3	1	2500
24	21	3	1	2500
25	22	3	1	2500
26	23	3	1	2500
27	24	3	1	2500
28	25	3	1	2500
29	26	3	1	2500
30	27	3	1	2500
31	28	3	1	2500
32	29	3	1	2500
33	30	3	1	2500
34	31	3	1	2500
35	32	3	1	2500
36	33	3	1	2500
37	34	3	1	2500
38	35	3	1	2500
39	36	3	1	2500
40	37	1	1	1000
41	38	1	1	1000
42	39	1	1	1000
43	40	1	1	1000
44	41	1	1	1000
45	42	3	1	2500
46	42	2	1	500
47	43	3	1	2500
48	43	2	1	500
49	44	3	1	2500
50	44	2	1	500
51	45	3	1	2500
52	45	2	1	500
53	46	3	1	2500
54	46	2	1	500
55	47	3	1	2500
56	47	2	1	500
57	48	3	1	2500
58	48	2	1	500
59	49	3	1	2500
60	49	2	1	500
61	50	3	1	2500
62	50	2	1	500
63	51	3	1	2500
64	51	2	1	500
65	52	3	1	2500
66	52	2	1	500
67	53	3	1	2500
68	53	1	1	1000
69	54	3	1	2500
70	54	1	1	1000
71	55	3	1	2500
72	55	1	1	1000
73	56	3	1	2500
74	56	1	1	1000
75	57	3	1	2500
76	57	1	1	1000
77	58	3	1	2500
78	58	1	1	1000
79	59	3	1	2500
80	59	1	1	1000
81	60	3	1	2500
82	61	1	1	1000
83	62	1	1	1000
84	62	3	1	2500
85	62	3	1	2500
86	63	1	1	1000
87	63	1	1	1000
88	63	3	1	2500
89	64	1	1	1000
90	64	1	1	1000
91	64	3	1	2500
92	65	1	1	1000
93	65	1	1	1000
94	65	3	1	2500
95	66	1	1	1000
96	66	1	1	1000
97	66	3	1	2500
98	67	1	1	1000
99	67	1	1	1000
100	67	3	1	2500
101	68	1	1	1000
102	68	1	1	1000
103	68	3	1	2500
104	69	1	1	1000
105	69	1	1	1000
106	69	3	1	2500
107	70	1	1	1000
108	70	1	1	1000
109	70	3	1	2500
110	71	1	1	1000
111	71	1	1	1000
112	71	3	1	2500
113	72	1	1	1000
114	72	1	1	1000
115	73	3	1	2500
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, client_id, car_id, mechanic_id, bay_id, status, planned_start, planned_end, total_cost, discount_amount, final_cost, payment_method, created_at) FROM stdin;
34	6	3	\N	\N	Ожидает	2026-07-31 18:01:00	2026-07-31 20:01:00	2500.0	250.0	2250.0	\N	2026-07-28 11:01:49.401645
35	6	3	\N	\N	Ожидает	2026-07-31 18:01:00	2026-07-31 20:01:00	2500.0	250.0	2250.0	\N	2026-07-28 11:01:49.563698
36	6	3	\N	\N	Ожидает	2026-07-31 18:01:00	2026-07-31 20:01:00	2500.0	250.0	2250.0	\N	2026-07-28 11:01:49.7313
37	6	3	\N	\N	Ожидает	2026-08-13 18:01:00	2026-08-13 20:01:00	1000.0	100.0	900.0	\N	2026-07-28 11:01:57.426665
38	6	3	\N	\N	Ожидает	2026-08-13 18:01:00	2026-08-13 20:01:00	1000.0	100.0	900.0	\N	2026-07-28 11:01:57.586274
39	6	3	\N	\N	Ожидает	2026-08-13 18:01:00	2026-08-13 20:01:00	1000.0	100.0	900.0	\N	2026-07-28 11:01:57.752422
40	6	3	\N	\N	Ожидает	2026-08-13 18:01:00	2026-08-13 20:01:00	1000.0	100.0	900.0	\N	2026-07-28 11:01:57.92268
41	6	3	3	1	В работе	2026-08-13 18:01:00	2026-08-13 20:01:00	1000.0	100.0	900.0	\N	2026-07-28 11:01:58.059786
42	6	3	\N	\N	Ожидает	2026-08-13 20:57:00	2026-08-13 22:57:00	3000.0	300.0	2700.0	\N	2026-07-29 13:57:32.321652
1	1	2	1	1	Завершена	2026-07-19 10:00:00	2026-07-19 12:00:00	2000.0	0.0	2000	Карта	2023-10-15 10:00:00
7	1	2	1	1	Завершена	2023-10-20 10:00:00	2023-10-20 12:00:00	1500	0	1500	\N	2023-10-20 10:00:00
43	6	3	\N	\N	Ожидает	2026-08-13 20:57:00	2026-08-13 22:57:00	3000.0	300.0	2700.0	\N	2026-07-29 13:57:32.738227
44	6	3	\N	\N	Ожидает	2026-08-13 20:57:00	2026-08-13 22:57:00	3000.0	300.0	2700.0	\N	2026-07-29 13:57:33.170857
8	6	3	5	1	Завершена	2026-07-22 17:17:25.159	2026-07-22 17:17:25.159	1000.0	100.0	900.0	string	2026-07-22 10:18:53.008147
9	6	3	2	1	В работе	2026-07-24 10:00:00	2026-07-24 12:00:00	500.0	50.0	450.0	\N	2026-07-23 14:12:35.937943
10	6	3	2	1	В работе	2026-07-24 10:18:00	2026-07-24 12:18:00	2500.0	250.0	2250.0	\N	2026-07-23 14:18:25.572198
11	6	3	2	4	В работе	2026-07-10 22:11:00	2026-07-11 00:11:00	2500.0	250.0	2250.0	\N	2026-07-24 15:11:58.475801
12	6	3	2	3	В работе	2026-07-24 22:16:00	2026-07-25 00:16:00	2500.0	250.0	2250.0	\N	2026-07-24 15:16:10.79367
13	6	3	3	2	В работе	2026-07-24 22:17:00	2026-07-25 00:17:00	2500.0	250.0	2250.0	\N	2026-07-24 15:17:57.907947
45	6	3	\N	\N	Ожидает	2026-08-13 20:57:00	2026-08-13 22:57:00	3000.0	300.0	2700.0	\N	2026-07-29 13:57:33.478429
46	6	3	\N	\N	Ожидает	2026-08-13 20:57:00	2026-08-13 22:57:00	3000.0	300.0	2700.0	\N	2026-07-29 13:57:33.743897
14	6	3	5	4	Завершена	2026-07-24 22:20:00	2026-07-25 00:20:00	2500.0	250.0	2250.0	Карта	2026-07-24 15:20:36.213843
15	6	3	\N	1	В работе	2026-06-23 21:11:00	2026-06-23 23:11:00	1000.0	100.0	900.0	\N	2026-07-27 14:11:21.279946
17	6	3	\N	4	В работе	2026-07-29 00:12:00	2026-07-29 02:12:00	1000.0	100.0	900.0	\N	2026-07-28 10:13:05.767382
16	6	3	\N	3	В работе	2026-07-28 17:07:00	2026-07-28 19:07:00	1000.0	100.0	900.0	\N	2026-07-28 10:08:31.322531
47	6	3	\N	\N	Ожидает	2026-08-13 20:57:00	2026-08-13 22:57:00	3000.0	300.0	2700.0	\N	2026-07-29 13:57:33.982675
48	6	3	\N	\N	Ожидает	2026-08-13 20:57:00	2026-08-13 22:57:00	3000.0	300.0	2700.0	\N	2026-07-29 13:57:34.181944
18	6	3	5	1	Завершена	2026-07-29 17:15:00	2026-07-29 19:15:00	2500.0	250.0	2250.0	Безналичный расчет	2026-07-28 10:15:59.693271
19	6	3	\N	\N	Ожидает	2026-07-28 20:39:00	2026-07-28 22:39:00	2500.0	250.0	2250.0	\N	2026-07-28 10:39:26.793175
20	6	3	\N	\N	Ожидает	2026-07-28 20:39:00	2026-07-28 22:39:00	2500.0	250.0	2250.0	\N	2026-07-28 10:39:28.487936
21	6	3	\N	\N	Ожидает	2026-07-28 20:39:00	2026-07-28 22:39:00	2500.0	250.0	2250.0	\N	2026-07-28 10:39:38.671688
22	6	3	\N	\N	Ожидает	2026-07-28 20:39:00	2026-07-28 22:39:00	2500.0	250.0	2250.0	\N	2026-07-28 10:39:38.884981
23	6	3	\N	\N	Ожидает	2026-07-28 20:39:00	2026-07-28 22:39:00	2500.0	250.0	2250.0	\N	2026-07-28 10:39:39.083604
24	6	3	\N	\N	Ожидает	2026-07-28 20:39:00	2026-07-28 22:39:00	2500.0	250.0	2250.0	\N	2026-07-28 10:39:39.283306
25	6	3	\N	\N	Ожидает	2026-07-28 20:39:00	2026-07-28 22:39:00	2500.0	250.0	2250.0	\N	2026-07-28 10:39:39.501495
29	6	3	5	1	В работе	2026-07-28 20:39:00	2026-07-28 22:39:00	2500.0	250.0	2250.0	\N	2026-07-28 10:39:40.361913
28	6	3	5	3	В работе	2026-07-28 20:39:00	2026-07-28 22:39:00	2500.0	250.0	2250.0	\N	2026-07-28 10:39:40.161736
27	6	3	2	2	В работе	2026-07-28 20:39:00	2026-07-28 22:39:00	2500.0	250.0	2250.0	\N	2026-07-28 10:39:39.9357
26	6	3	4	4	В работе	2026-07-28 20:39:00	2026-07-28 22:39:00	2500.0	250.0	2250.0	\N	2026-07-28 10:39:39.723972
30	6	3	\N	\N	Ожидает	2026-07-31 18:01:00	2026-07-31 20:01:00	2500.0	250.0	2250.0	\N	2026-07-28 11:01:48.564262
31	6	3	\N	\N	Ожидает	2026-07-31 18:01:00	2026-07-31 20:01:00	2500.0	250.0	2250.0	\N	2026-07-28 11:01:48.657621
32	6	3	\N	\N	Ожидает	2026-07-31 18:01:00	2026-07-31 20:01:00	2500.0	250.0	2250.0	\N	2026-07-28 11:01:49.043161
33	6	3	\N	\N	Ожидает	2026-07-31 18:01:00	2026-07-31 20:01:00	2500.0	250.0	2250.0	\N	2026-07-28 11:01:49.222967
49	6	3	\N	\N	Ожидает	2026-08-13 20:57:00	2026-08-13 22:57:00	3000.0	300.0	2700.0	\N	2026-07-29 13:57:34.38733
50	6	3	\N	\N	Ожидает	2026-08-13 20:57:00	2026-08-13 22:57:00	3000.0	300.0	2700.0	\N	2026-07-29 13:57:34.771562
51	6	3	\N	\N	Ожидает	2026-08-13 20:57:00	2026-08-13 22:57:00	3000.0	300.0	2700.0	\N	2026-07-29 13:57:36.786589
52	6	3	5	3	В работе	2026-08-13 20:57:00	2026-08-13 22:57:00	3000.0	300.0	2700.0	\N	2026-07-29 13:57:36.954558
53	6	3	\N	\N	Ожидает	2026-08-20 21:40:00	2026-08-20 23:40:00	3500.0	350.0	3150.0	\N	2026-07-29 14:40:29.272362
54	6	3	\N	\N	Ожидает	2026-08-20 21:40:00	2026-08-20 23:40:00	3500.0	350.0	3150.0	\N	2026-07-29 14:40:33.044914
55	6	3	\N	\N	Ожидает	2026-08-20 21:40:00	2026-08-20 23:40:00	3500.0	350.0	3150.0	\N	2026-07-29 14:40:33.227178
56	6	3	\N	\N	Ожидает	2026-08-20 21:40:00	2026-08-20 23:40:00	3500.0	350.0	3150.0	\N	2026-07-29 14:40:33.46315
57	6	3	\N	\N	Ожидает	2026-08-20 21:40:00	2026-08-20 23:40:00	3500.0	350.0	3150.0	\N	2026-07-29 14:40:33.67309
58	6	3	\N	\N	Ожидает	2026-08-20 21:40:00	2026-08-20 23:40:00	3500.0	350.0	3150.0	\N	2026-07-29 14:40:33.884695
59	6	3	\N	\N	Разделен	2026-08-20 21:40:00	2026-08-20 23:40:00	3500.0	350.0	3150.0	\N	2026-07-29 14:40:34.085068
60	6	3	5	1	В работе	2026-08-20 21:40:00	2026-08-20 23:40:00	2500	\N	2500	\N	2026-07-29 22:02:13.881469
61	6	3	2	2	В работе	2026-08-20 21:40:00	2026-08-20 23:40:00	1000	\N	1000	\N	2026-07-29 22:02:13.894468
62	6	3	\N	\N	Ожидает	2026-07-31 22:13:00	2026-08-01 05:13:00	6000.0	600.0	5400.0	\N	2026-07-29 15:13:17.971183
63	6	3	\N	\N	Ожидает	2026-08-11 22:48:00	2026-08-12 03:48:00	4500.0	450.0	4050.0	\N	2026-07-29 15:48:47.852921
64	6	3	\N	\N	Ожидает	2026-08-11 22:48:00	2026-08-12 03:48:00	4500.0	450.0	4050.0	\N	2026-07-29 15:48:48.382917
65	6	3	\N	\N	Ожидает	2026-08-11 22:48:00	2026-08-12 03:48:00	4500.0	450.0	4050.0	\N	2026-07-29 15:48:48.887951
66	6	3	\N	\N	Ожидает	2026-08-11 22:48:00	2026-08-12 03:48:00	4500.0	450.0	4050.0	\N	2026-07-29 15:48:49.379649
67	6	3	\N	\N	Ожидает	2026-08-11 22:48:00	2026-08-12 03:48:00	4500.0	450.0	4050.0	\N	2026-07-29 15:48:49.88424
68	6	3	\N	\N	Ожидает	2026-08-11 22:48:00	2026-08-12 03:48:00	4500.0	450.0	4050.0	\N	2026-07-29 15:48:50.479021
69	6	3	\N	\N	Ожидает	2026-08-11 22:48:00	2026-08-12 03:48:00	4500.0	450.0	4050.0	\N	2026-07-29 15:48:50.66906
70	6	3	\N	\N	Ожидает	2026-08-11 22:48:00	2026-08-12 03:48:00	4500.0	450.0	4050.0	\N	2026-07-29 15:48:50.846774
71	6	3	\N	\N	Разделен	2026-08-11 22:48:00	2026-08-12 03:48:00	4500.0	450.0	4050.0	\N	2026-07-29 15:48:51.024919
72	6	3	\N	\N	Ожидает	2026-08-11 22:48:00	2026-08-12 03:48:00	2000	\N	2000	\N	2026-07-29 22:49:16.256663
73	6	3	\N	\N	Ожидает	2026-08-11 22:48:00	2026-08-12 03:48:00	2500	\N	2500	\N	2026-07-29 22:49:16.263647
\.


--
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services (id, name, price, req_specialization, duration_hours) FROM stdin;
1	Замена масла	1000		1
2	Диагностика	500		2
3	Электромонтажные работы	2500	Электрик	3
\.


--
-- Name: admins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.admins_id_seq', 1, true);


--
-- Name: bays_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bays_id_seq', 1, false);


--
-- Name: callback_requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.callback_requests_id_seq', 4, true);


--
-- Name: cars_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cars_id_seq', 3, true);


--
-- Name: clients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clients_id_seq', 6, true);


--
-- Name: discount_rules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.discount_rules_id_seq', 3, true);


--
-- Name: mechanics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mechanics_id_seq', 2, true);


--
-- Name: order_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_items_id_seq', 115, true);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 73, true);


--
-- Name: services_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_id_seq', 3, true);


--
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (id);


--
-- Name: bays bays_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bays
    ADD CONSTRAINT bays_pkey PRIMARY KEY (id);


--
-- Name: callback_requests callback_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.callback_requests
    ADD CONSTRAINT callback_requests_pkey PRIMARY KEY (id);


--
-- Name: cars cars_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_pkey PRIMARY KEY (id);


--
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (id);


--
-- Name: discount_rules discount_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discount_rules
    ADD CONSTRAINT discount_rules_pkey PRIMARY KEY (id);


--
-- Name: mechanics mechanics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mechanics
    ADD CONSTRAINT mechanics_pkey PRIMARY KEY (id);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: services services_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_pkey PRIMARY KEY (id);


--
-- Name: ix_admins_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_admins_id ON public.admins USING btree (id);


--
-- Name: ix_admins_login; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_admins_login ON public.admins USING btree (login);


--
-- Name: ix_bays_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_bays_id ON public.bays USING btree (id);


--
-- Name: ix_callback_requests_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_callback_requests_id ON public.callback_requests USING btree (id);


--
-- Name: ix_cars_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_cars_id ON public.cars USING btree (id);


--
-- Name: ix_clients_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_clients_email ON public.clients USING btree (email);


--
-- Name: ix_clients_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_clients_id ON public.clients USING btree (id);


--
-- Name: ix_clients_phone; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_clients_phone ON public.clients USING btree (phone);


--
-- Name: ix_discount_rules_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_discount_rules_id ON public.discount_rules USING btree (id);


--
-- Name: ix_mechanics_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_mechanics_id ON public.mechanics USING btree (id);


--
-- Name: ix_mechanics_login; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_mechanics_login ON public.mechanics USING btree (login);


--
-- Name: ix_order_items_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_items_id ON public.order_items USING btree (id);


--
-- Name: ix_orders_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_id ON public.orders USING btree (id);


--
-- Name: ix_services_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_services_id ON public.services USING btree (id);


--
-- Name: cars cars_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id);


--
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- Name: order_items order_items_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.services(id);


--
-- Name: orders orders_bay_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_bay_id_fkey FOREIGN KEY (bay_id) REFERENCES public.bays(id);


--
-- Name: orders orders_car_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_car_id_fkey FOREIGN KEY (car_id) REFERENCES public.cars(id);


--
-- Name: orders orders_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id);


--
-- Name: orders orders_mechanic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_mechanic_id_fkey FOREIGN KEY (mechanic_id) REFERENCES public.mechanics(id);


--
-- PostgreSQL database dump complete
--

\unrestrict Rk122LrZRyZ6f4B6TtytTxCVhQOdQ8zEHCiiPhev6lH3tezSoDbctRmUwAlDUO3

