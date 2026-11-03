"""iconos: catálogo de iconos de Terracotta para slides HTML (Material Symbols Outlined, peso 300).

Una sola familia (N1). La fuente completa en peso 300 vive en assets/fonts/material-symbols-completo-300.woff2
(descargada del repositorio oficial google/material-design-icons, licencia Apache 2.0) y de ella se genera el
subconjunto que va incrustado en cada HTML (material-symbols-ea.woff2) con los iconos de este catálogo. Así la
página pesa poco y no hace falta internet.

Cómo se usa:
- buscar_icono("vaca") devuelve los nombres del catálogo cuyo tema o palabras clave coinciden.
- Si en el catálogo no hay ninguno apto, buscar_completo("cow farm") busca en los ~3.900 iconos de Material Symbols
  por nombre y por las etiquetas oficiales de Google (en inglés; material-symbols-etiquetas.json). El que encaje se
  añade a TEMAS con sus palabras clave en español y se regenera la fuente. Nunca se mezcla otra familia de iconos.
- icono("agriculture") (en base) falla con un aviso si el nombre no está en el catálogo, en vez de pintar la palabra.
- comprobar_iconos(html) lista los iconos de un HTML que la fuente no tiene.
- Para añadir un icono: buscarlo en fonts.google.com/icons (estilo Outlined), añadirlo aquí con sus palabras clave y
  ejecutar build_galeria_elementos.py, que regenera la fuente y la página «Catálogo de iconos.html».
"""
import pathlib
import re
import unicodedata

AQUI = pathlib.Path(__file__).resolve().parent.parent          # presentaciones/
COMPLETA = AQUI / "assets/fonts/material-symbols-completo-300.woff2"
CODIGOS = AQUI / "assets/fonts/material-symbols.codepoints"
ETIQUETAS = AQUI / "assets/fonts/material-symbols-etiquetas.json"     # metadatos oficiales (fonts.google.com/metadata/icons)
SUBSET = AQUI / "assets/fonts/material-symbols-ea.woff2"

TEMAS = [
    ("Campo y producción primaria", "Cultivo, ganadería, pesca, clima y recursos naturales", [
        ("agriculture", "tractor campo agricultura cultivo granja ganadería"), ("grass", "hierba pasto pradera"), ("eco", "hoja sostenible ecológico bio"),
        ("compost", "compost residuo orgánico suelo"), ("potted_plant", "planta maceta vivero"), ("forest", "bosque árboles"),
        ("park", "árbol"), ("yard", "jardín huerto"), ("nature", "naturaleza"), ("local_florist", "flor"),
        ("grain", "grano cereal trigo"), ("water_drop", "agua gota riego"), ("water", "agua mar río"), ("waves", "olas mar acuicultura"),
        ("humidity_percentage", "humedad"), ("sunny", "sol clima"), ("rainy", "lluvia clima"), ("ac_unit", "frío congelado nieve"),
        ("device_thermostat", "temperatura termómetro"), ("thermostat", "temperatura control"), ("pest_control", "plaga insecto"),
        ("emoji_nature", "abeja polinización insecto"), ("pets", "animal ganadería ganado vaca cerdo mascota"), ("cruelty_free", "bienestar animal conejo"),
        ("egg", "huevo"), ("egg_alt", "huevo avícola"), ("set_meal", "pescado pesca marisco"), ("phishing", "pesca anzuelo"),
        ("sailing", "barco pesca puerto"), ("landscape", "paisaje territorio"), ("energy_savings_leaf", "ahorro energía sostenible"),
        ("recycling", "reciclaje circular"), ("public", "mundo global planeta"),
        # añadidos el 01-11-2026 con buscar_completo()
        ("wheat", "trigo cereal espiga"),
        ("avocado_bean", "aguacate legumbre vegetal fruta"),
        ("outdoor_garden", "huerto jardín exterior"),
        ("garden_cart", "carretilla huerta"),
        ("nature_people", "naturaleza personas campo"),
        ("air", "aire viento"),
        ("co2", "co2 carbono emisiones huella"),
        ("salinity", "salinidad sal agua"),
        ("partly_cloudy_day", "nubes clima tiempo"),
        ("snowflake", "congelado nieve frío"),
        ("severe_cold", "frío extremo congelación"),
        ("front_loader", "maquinaria pala cargadora"),
        ("drone_2", "dron agricultura de precisión"),
    ]),
    ("Alimentos y bebidas", "Producto, categorías de alimento y consumo", [
        ("nutrition", "nutrición fruta manzana"), ("restaurant", "restaurante horeca comida"), ("local_dining", "comida cubiertos"),
        ("lunch_dining", "hamburguesa comida rápida"), ("bakery_dining", "panadería bollería pan"), ("breakfast_dining", "desayuno tostada"),
        ("local_pizza", "pizza"), ("icecream", "helado"), ("cake", "pastel repostería"), ("cookie", "galleta snack"),
        ("local_cafe", "café"), ("coffee", "café taza"), ("emoji_food_beverage", "té infusión bebida caliente"), ("liquor", "licor alcohol"),
        ("wine_bar", "vino"), ("sports_bar", "cerveza"), ("local_drink", "bebida vaso agua"), ("water_full", "agua envase botella"),
        ("kitchen", "nevera frigorífico"), ("blender", "batidora licuadora"), ("soup_kitchen", "sopa cocina"), ("rice_bowl", "arroz bol"),
        ("ramen_dining", "fideos asiático"), ("kebab_dining", "carne pincho"), ("fastfood", "comida rápida"), ("dinner_dining", "cena plato"),
        ("cooking", "cocinar olla"), ("skillet", "sartén cocina"), ("outdoor_grill", "barbacoa parrilla carne"), ("takeout_dining", "para llevar delivery"),
        ("tapas", "tapas aperitivo"), ("food_bank", "banco de alimentos donación"), ("grocery", "alimentación compra cesta"),
        ("shopping_basket", "cesta compra"), ("flatware", "cubiertos"), ("brunch_dining", "brunch desayuno"), ("allergies", "alergia alérgeno"),
        ("no_food", "sin comida ayuno"), ("spa", "bienestar natural"),
        # añadidos el 01-11-2026 con buscar_completo()
        ("hand_meal", "servir comida plato"),
        ("calendar_meal", "menú planificación de comidas"),
        ("no_meals", "sin comida ayuno"),
        ("water_bottle", "botella agua envase"),
        ("water_bottle_large", "garrafa agua envase grande"),
        ("local_bar", "cóctel bar"),
        ("no_drinks", "sin bebidas sin alcohol"),
    ]),
    ("Ciencia, salud e I+D", "Laboratorio, biotecnología, salud y nutrición funcional", [
        ("science", "ciencia laboratorio matraz química"), ("biotech", "microscopio biotecnología"), ("microbiology", "microbiología bacteria célula"),
        ("labs", "laboratorio tubos ensayo"), ("experiment", "experimento química ensayo"), ("genetics", "genética adn"),
        ("vaccines", "vacuna jeringa inyectable"), ("medication", "medicamento fármaco"), ("pill", "pastilla cápsula suplemento"),
        ("prescriptions", "receta fármaco"), ("health_and_safety", "salud seguridad"), ("monitor_heart", "corazón salud cardiovascular"),
        ("vital_signs", "constantes salud"), ("stethoscope", "médico clínico"), ("clinical_notes", "ensayo clínico historia"),
        ("psychology", "mente cognitivo cerebro"), ("neurology", "neurología cerebro"), ("body_fat", "grasa corporal obesidad"),
        ("monitor_weight", "peso báscula"), ("fitness_center", "deporte ejercicio"), ("self_improvement", "bienestar meditación"),
        ("bloodtype", "sangre análisis"), ("lab_profile", "informe de laboratorio análisis"), ("lab_research", "investigación laboratorio"),
        ("lab_panel", "panel de laboratorio"), ("coronavirus", "virus patógeno"), ("sanitizer", "higiene desinfección"),
        ("immunology", "inmunidad sistema inmune"), ("gastroenterology", "digestivo intestino microbiota"), ("dermatology", "piel dermatología"),
        ("oncology", "oncología célula"), ("pediatrics", "infantil pediatría"), ("elderly", "mayores envejecimiento"),
        # añadidos el 01-11-2026 con buscar_completo()
        ("glucose", "glucosa diabetes azúcar en sangre"),
        ("ecg_heart", "electrocardiograma corazón"),
        ("health_metrics", "métricas de salud"),
        ("heart_check", "salud cardiovascular"),
        ("monitor_weight_loss", "pérdida de peso obesidad adelgazar"),
        ("monitor_weight_gain", "ganancia de peso"),
        ("cognition", "cognición cerebro mente"),
        ("pregnant_woman", "embarazo maternidad"),
        ("breastfeeding", "lactancia materna bebé"),
        ("allergy", "alergia alérgeno"),
        ("sick", "enfermedad enfermo"),
        ("masks", "mascarilla protección"),
        ("medication_liquid", "jarabe fármaco líquido"),
        ("specific_gravity", "densidad viscosidad"),
        ("health_and_beauty", "cosmética belleza cuidado"),
        ("clean_hands", "higiene manos"),
        ("thermometer", "termómetro temperatura"),
    ]),
    ("Industria y proceso", "Fábrica, transformación, energía y operaciones", [
        ("factory", "fábrica planta industria"), ("precision_manufacturing", "fabricación robot línea"), ("conveyor_belt", "cinta transportadora línea"),
        ("settings", "ajustes engranaje"), ("construction", "obra construcción"), ("engineering", "ingeniería técnico"), ("build", "herramienta reparar"),
        ("handyman", "mantenimiento"), ("inventory_2", "caja envase almacén"), ("package_2", "paquete envase"), ("deployed_code", "producto cubo"),
        ("warehouse", "almacén nave"), ("forklift", "carretilla almacén"), ("pallet", "palé"), ("propane_tank", "depósito gas tanque"),
        ("oil_barrel", "barril aceite"), ("water_pump", "bomba agua"), ("heat_pump", "bomba de calor"), ("mode_heat", "calor tratamiento térmico"),
        ("local_fire_department", "fuego combustión"), ("filter_alt", "filtro filtración"), ("compress", "comprimir prensa"), ("content_cut", "cortar tijeras"),
        ("blender", "mezcla homogeneizar"), ("scale", "báscula pesar dosis"), ("timer", "tiempo cronómetro"), ("speed", "velocidad rendimiento"),
        ("autorenew", "ciclo renovar"), ("cycle", "ciclo proceso"), ("sync", "sincronizar ciclo"), ("bolt", "energía rayo"),
        ("electric_bolt", "electricidad"), ("solar_power", "solar fotovoltaica"), ("wind_power", "eólica viento"), ("gas_meter", "contador gas"),
        ("valve", "válvula"), ("plumbing", "fontanería tubería"), ("tune", "ajustar parámetros"), ("science_off", "sin química"),
        # añadidos el 01-11-2026 con buscar_completo()
        ("manufacturing", "fabricación producción industria"),
        ("package", "paquete envase"),
        ("hand_package", "entrega de paquete"),
        ("energy", "energía"),
        ("faucet", "grifo agua"),
        ("heat", "calor"),
        ("production_quantity_limits", "límite de producción capacidad"),
    ]),
    ("Logística y canal", "Transporte, distribución, retail y consumo", [
        ("local_shipping", "camión transporte logística"), ("airport_shuttle", "furgoneta reparto"), ("flight_takeoff", "avión exportación vuelo"),
        ("directions_boat", "barco transporte marítimo"), ("train", "tren ferrocarril"), ("delivery_dining", "reparto moto delivery"),
        ("two_wheeler", "moto"), ("route", "ruta recorrido"), ("alt_route", "ruta alternativa bifurcación"), ("map", "mapa"),
        ("near_me", "ubicación dirección"), ("location_on", "ubicación punto"), ("language", "internacional idiomas"), ("travel_explore", "explorar buscar mundo"),
        ("inventory", "inventario stock"), ("storefront", "tienda escaparate retail"), ("store", "tienda comercio"), ("store_mall_directory", "centro comercial"),
        ("shopping_cart", "carrito compra supermercado"), ("shopping_bag", "bolsa compra"), ("local_mall", "compra"), ("sell", "venta etiqueta precio"),
        ("point_of_sale", "caja venta tpv"), ("barcode", "código de barras"), ("qr_code_2", "código qr"), ("home", "hogar casa consumidor"),
        ("apartment", "edificio oficina ciudad"), ("location_city", "ciudad urbano"), ("cottage", "rural casa de campo"), ("ac_unit", "cadena de frío"),
        # añadidos el 01-11-2026 con buscar_completo()
        ("delivery_truck_speed", "entrega rápida última milla"),
        ("delivery_truck_bolt", "camión eléctrico"),
        ("moped_package", "reparto en moto"),
        ("add_shopping_cart", "añadir a la compra conversión"),
        ("anchor", "puerto ancla"),
        ("boat_railway", "intermodal barco tren"),
    ]),
    ("Negocio y mercado", "Finanzas, mercado, estrategia y propuesta de valor", [
        ("payments", "pago dinero coste"), ("attach_money", "dinero dólar"), ("euro", "euro dinero"), ("savings", "ahorro hucha"),
        ("account_balance", "banco institución"), ("account_balance_wallet", "cartera financiación"), ("trending_up", "crecimiento sube"),
        ("trending_down", "caída baja"), ("trending_flat", "estable plano"), ("bar_chart", "gráfico barras datos"), ("pie_chart", "gráfico tarta cuota"),
        ("donut_large", "anillo reparto"), ("show_chart", "gráfico línea evolución"), ("query_stats", "análisis estadística"), ("analytics", "analítica datos"),
        ("leaderboard", "ranking clasificación"), ("monitoring", "seguimiento monitorización"), ("finance", "finanzas mercado"),
        ("request_quote", "presupuesto cotización"), ("receipt_long", "factura recibo"), ("price_check", "precio comprobar"),
        ("handshake", "acuerdo alianza socio"), ("partner_exchange", "intercambio socios"), ("work", "trabajo maletín"), ("business_center", "empresa negocio"),
        ("domain", "empresa sede"), ("corporate_fare", "corporativo"), ("campaign", "campaña comunicación marketing"), ("ads_click", "marketing digital clic"),
        ("target", "objetivo diana"), ("diamond", "valor diferencial premium"), ("workspace_premium", "premio calidad excelencia"),
        ("rocket_launch", "lanzamiento startup escalar"), ("lightbulb", "idea innovación"), ("insights", "hallazgo insight"), ("timeline", "trayectoria cronología"),
        ("stacked_line_chart", "series apiladas"), ("currency_exchange", "divisas cambio"), ("contract", "contrato"), ("store_mall_directory", "canal retail"),
        ("monetization_on", "monetizar ingresos"), ("price_change", "cambio de precio"), ("shopping_cart_checkout", "conversión venta"),
        ("hub", "ecosistema red nodo"), ("diversity_2", "comunidad red"),
        # añadidos el 01-11-2026 con buscar_completo()
        ("paid", "pagado dinero"),
        ("money_bag", "inversión financiación capital"),
        ("money", "dinero billetes"),
        ("redeem", "regalo promoción"),
        ("stacked_bar_chart", "barras apiladas gráfico"),
        ("bubble_chart", "gráfico de burbujas"),
        ("data_exploration", "exploración de datos"),
        ("insert_chart", "gráfico informe"),
        ("rocket", "cohete lanzamiento"),
        ("stars", "destacado estrellas"),
    ]),
    ("Regulación y calidad", "Normativa, certificación, propiedad intelectual y riesgo", [
        ("gavel", "regulación ley norma mazo"), ("policy", "política cumplimiento patente"), ("verified", "verificado certificado"),
        ("verified_user", "seguridad verificada"), ("rule", "norma requisito"), ("fact_check", "verificación comprobado"), ("checklist", "lista de control requisitos"),
        ("task_alt", "tarea hecha"), ("assignment", "expediente documento"), ("description", "documento ficha"), ("article", "artículo publicación"),
        ("draft", "borrador"), ("approval", "aprobación sello"), ("license", "licencia"), ("shield", "protección escudo"), ("security", "seguridad"),
        ("lock", "candado confidencial"), ("lock_open", "abierto libre"), ("admin_panel_settings", "administración control"), ("report", "aviso informe"),
        ("gpp_good", "protección buena práctica"), ("rate_review", "revisión evaluación"), ("plagiarism", "búsqueda documental"), ("copyright", "derechos propiedad intelectual"),
        ("balance", "equilibrio justicia"), ("flag", "bandera alerta hito"), ("history_edu", "historial certificado"), ("labs", "ensayo de calidad"),
        ("eco", "sello ecológico"), ("health_and_safety", "seguridad alimentaria"),
        # añadidos el 01-11-2026 con buscar_completo()
        ("high_quality", "alta calidad"),
        ("verified_off", "no verificado"),
        ("crisis_alert", "crisis alerta"),
        ("threat_intelligence", "amenaza riesgo inteligencia"),
        ("lock_person", "acceso restringido"),
        ("card_membership", "membresía certificado tarjeta"),
        ("menu_book", "manual guía libro"),
    ]),
    ("Personas y organización", "Equipos, clientes, consumidores y comunicación", [
        ("groups", "grupo equipo personas"), ("group", "personas usuarios"), ("person", "persona usuario"), ("person_search", "búsqueda de talento candidato"),
        ("diversity_3", "comunidad diversidad"), ("supervisor_account", "responsable dirección"), ("badge", "credencial empleado"), ("school", "universidad formación"),
        ("record_voice_over", "entrevista portavoz"), ("forum", "conversación foro"), ("chat", "chat mensaje"), ("mail", "correo"), ("call", "llamada teléfono"),
        ("support_agent", "atención soporte"), ("family_restroom", "familia hogar"), ("child_care", "infancia bebé"), ("emoji_people", "persona consumidor"),
        ("accessibility_new", "accesibilidad persona"), ("sentiment_satisfied", "satisfecho contento"), ("sentiment_dissatisfied", "insatisfecho"),
        ("thumb_up", "me gusta aprobación"), ("thumb_down", "rechazo"), ("favorite", "corazón preferencia"), ("star", "estrella valoración"),
        ("interpreter_mode", "entrevista experto"), ("co_present", "presentación reunión"), ("account_circle", "perfil"), ("waving_hand", "saludo bienvenida"),
        # añadidos el 01-11-2026 con buscar_completo()
        ("person_add", "alta persona añadir"),
        ("group_add", "unir al equipo"),
        ("manage_accounts", "gestión de cuentas"),
        ("elderly_woman", "mujer mayor envejecimiento"),
        ("psychology_alt", "mente comportamiento"),
        ("contacts", "contactos agenda"),
    ]),
    ("Estado y señales", "Estados, avisos, tiempo y direcciones", [
        ("check_circle", "correcto hecho"), ("check_circle_outline", "correcto contorno"), ("check_circle_filled", "correcto relleno"),
        ("cancel", "cancelado no"), ("do_disturb", "prohibido"), ("block", "bloqueado"), ("do_not_disturb_alt", "no permitido"),
        ("not_interested", "descartado"), ("warning", "aviso alerta"), ("warning_amber", "aviso"), ("report_problem", "problema riesgo"),
        ("error", "error"), ("info", "información"), ("help", "ayuda pregunta duda"), ("schedule", "reloj tiempo plazo"), ("access_time", "hora tiempo"),
        ("access_time_filled", "hora relleno"), ("query_builder", "reloj"), ("watch_later", "más tarde pendiente"), ("hourglass_empty", "espera reloj de arena"),
        ("pending", "pendiente"), ("priority_high", "prioridad urgente"), ("bookmark", "marcador"), ("push_pin", "fijado"), ("visibility", "visible ver"),
        ("remove_red_eye", "ojo vigilancia"), ("new_releases", "novedad nuevo"), ("label", "etiqueta"), ("label_outline", "etiqueta contorno"),
        ("done", "hecho"), ("close", "cerrar"), ("add", "añadir más"), ("remove", "quitar menos"), ("arrow_forward", "flecha siguiente"),
        ("arrow_upward", "subir"), ("arrow_downward", "bajar"), ("north_east", "sube diagonal"), ("south_east", "baja diagonal"),
        ("play_circle", "iniciar reproducir"), ("pause_circle", "pausa"), ("stop_circle", "parar"), ("radio_button_checked", "seleccionado"),
    ]),
    ("Datos, digital e ideas", "Información, tecnología, planificación y estructura", [
        ("search", "buscar lupa"), ("database", "base de datos"), ("storage", "almacenamiento datos"), ("cloud", "nube"), ("lan", "red conexión"),
        ("memory", "chip procesador"), ("smart_toy", "inteligencia artificial robot"), ("auto_awesome", "ia mágico automático"), ("tips_and_updates", "consejo idea"),
        ("code", "código software"), ("terminal", "terminal programación"), ("devices", "dispositivos"), ("smartphone", "móvil app"),
        ("computer", "ordenador"), ("link", "enlace"), ("share", "compartir"), ("download", "descargar"), ("upload", "subir archivo"),
        ("dashboard", "panel cuadro de mando"), ("grid_view", "rejilla vista"), ("view_timeline", "cronograma"), ("calendar_month", "calendario mes"),
        ("event", "evento fecha"), ("date_range", "rango de fechas"), ("alarm", "alarma aviso"), ("layers", "capas"), ("category", "categoría tipo"),
        ("extension", "pieza encaje módulo"), ("stacks", "pila capas"), ("account_tree", "árbol jerarquía estructura"), ("schema", "esquema flujo"),
        ("filter_list", "filtrar lista"), ("sort", "ordenar"), ("format_list_numbered", "lista numerada"), ("table_chart", "tabla"),
        ("sensors", "sensor señal"), ("satellite_alt", "satélite teledetección"), ("qr_code_scanner", "escanear trazabilidad"), ("token", "token blockchain"),
        # añadidos el 01-11-2026 con buscar_completo()
        ("robot", "robot automatización"),
        ("robot_2", "robot ia"),
        ("network_intelligence", "inteligencia artificial red"),
        ("model_training", "entrenamiento de modelo ia"),
        ("simulation", "simulación modelo"),
        ("data_table", "tabla de datos"),
        ("summarize", "resumen síntesis"),
        ("map_search", "buscar en mapa"),
        ("my_location", "mi ubicación"),
        ("history", "historial pasado"),
    ]),
]

_SINONIMOS = {}


def _norm(t):
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def catalogo():
    """{nombre: (tema, palabras clave)}; un icono que sale en dos temas conserva el primero y suma las palabras."""
    out = {}
    for tema, _, items in TEMAS:
        for n, kw in items:
            if n in out:
                out[n] = (out[n][0], out[n][1] + " " + kw)
            else:
                out[n] = (tema, kw)
    return out


NOMBRES = set(catalogo())


def buscar_icono(texto):
    """Nombres de icono cuyo nombre, tema o palabras clave contienen todas las palabras de `texto` (sin tildes)."""
    pal = _norm(texto).split()
    res = []
    for n, (tema, kw) in catalogo().items():
        h = _norm(f"{n.replace('_', ' ')} {tema} {kw}")
        if all(p in h for p in pal):
            res.append(n)
    return res


def buscar_completo(texto, n=20):
    """Busca en toda la familia Material Symbols Outlined (no solo en el catálogo) por nombre y etiquetas oficiales, en
    inglés. Devuelve [(nombre, en_catalogo, categorías, etiquetas que coinciden)], primero lo más relevante y popular.
    Paso siguiente si uno encaja: añadirlo a TEMAS con sus palabras clave en español y ejecutar build_galeria_elementos.py."""
    import json
    meta = json.loads(ETIQUETAS.read_text())
    pal = _norm(texto).split()
    res = []
    for nom, m in meta.items():
        nombre = nom.replace("_", " ")
        tags = [_norm(t) for t in m["t"]]
        puntos, casan = 0, []
        for p in pal:
            if p in nombre.split():
                puntos += 6
            elif p in nombre:
                puntos += 4
            exactas = [t for t in tags if t == p]
            parciales = [t for t in tags if p in t and t != p]
            if exactas:
                puntos += 3
                casan += exactas[:1]
            elif parciales:
                puntos += 1
                casan += parciales[:1]
            elif p not in nombre:
                puntos = -1
                break
        if puntos > 0:
            res.append((puntos, m["p"], nom, nom in NOMBRES, m["c"], casan))
    res.sort(key=lambda r: (-r[0], -r[1]))
    return [(nom, cat, c, t) for _, _, nom, cat, c, t in res[:n]]


def parecidos(nombre, n=5):
    import difflib
    return difflib.get_close_matches(nombre, sorted(NOMBRES), n=n, cutoff=.5)


def comprobar_iconos(html):
    """Iconos de un HTML (<span class="ms">nombre</span>) que no están en el catálogo y saldrían como texto."""
    usados = set(re.findall(r'class="ms"[^>]*>([a-z0-9_]+)<', html))
    return sorted(usados - NOMBRES)


def generar_fuente():
    """Regenera material-symbols-ea.woff2 a partir de la fuente completa con los iconos del catálogo. Devuelve
    (iconos, KB) y falla si algún nombre del catálogo no existe en Material Symbols."""
    from fontTools import subset
    from fontTools.ttLib import TTFont
    cp = dict(l.split() for l in CODIGOS.read_text().splitlines() if l.strip())
    faltan = sorted(NOMBRES - set(cp))
    if faltan:
        raise ValueError(f"No existen en Material Symbols: {', '.join(faltan)}")
    f = TTFont(str(COMPLETA))
    o = subset.Options()
    o.layout_closure = False           # solo las ligaduras de los iconos pedidos, no todas las que forman sus letras
    o.layout_features = ["liga", "rlig", "calt", "ccmp"]
    o.flavor = "woff2"
    o.notdef_outline = True
    s = subset.Subsetter(o)
    s.populate(unicodes=[ord(c) for c in "abcdefghijklmnopqrstuvwxyz0123456789_"] + [int(cp[n], 16) for n in NOMBRES])
    s.subset(f)
    f.save(str(SUBSET))
    return len(NOMBRES), SUBSET.stat().st_size // 1024
