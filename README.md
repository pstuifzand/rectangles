# Rechthoek Voorbeelden

Deze repository bevat verschillende Python-voorbeelden die laten zien hoe je rechthoeken kunt tekenen en animeren met pygame. De voorbeelden zijn gerangschikt van eenvoudig naar complex.

## Vereisten

```bash
pip install pygame
```

## Voorbeelden (van eenvoudig naar complex)

### 1. Basis Rechthoeken (`rectangle_example.py`)
**Complexiteit:** ⭐ (Eenvoudig)

Een eenvoudige demonstratie van hoe je rechthoeken tekent met verschillende posities, kleuren en rotaties.

**Wat je leert:**
- Basis rechthoek tekenen
- Kleuren en posities instellen
- Eenvoudige rotatie

**Uitvoeren:**
```bash
python rectangle_example.py
```

### 2. Bewegende Rechthoeken (`moving_rectangle_example.py`)
**Complexiteit:** ⭐⭐ (Gemiddeld)

Rechthoeken die bewegen in verschillende patronen met behulp van trigonometrische functies.

**Wat je leert:**
- Animatie met tijd-gebaseerde beweging
- Trigonometrische functies (sin, cos)
- Verschillende bewegingspatronen (horizontaal, circulair, diagonaal)

**Uitvoeren:**
```bash
python moving_rectangle_example.py
```

### 3. Deeltjes Systeem (`particle_system_example.py`)
**Complexiteit:** ⭐⭐⭐ (Gemiddeld-Complex)

Een systeem met 100 rechthoekige deeltjes die rondbewegen en van de randen van het scherm afketsen.

**Wat je leert:**
- Object-georiënteerd programmeren met klassen
- Deeltjes systemen
- Botsingsdetectie met schermranden
- Willekeurige waarden voor variatie

**Uitvoeren:**
```bash
python particle_system_example.py
```

### 4. Emitter Deeltjes Systeem (`emitter_particle_system.py`)
**Complexiteit:** ⭐⭐⭐⭐ (Complex)

Geavanceerd deeltjes systeem met drie verschillende emitters die verschillende soorten deeltjes maken (fontein, explosie, rook).

**Wat je leert:**
- Geavanceerde deeltjes systemen
- Verschillende emitter types
- Deeltjes levensduur (TTL)
- Alpha blending voor vervaging
- Emitter beheer en begrenzing

**Uitvoeren:**
```bash
python emitter_particle_system.py
```

### 5. Muis-Gestuurd Emitter Systeem (`mouse_emitter_system.py`)
**Complexiteit:** ⭐⭐⭐⭐⭐ (Zeer Complex)

Interactief systeem waar je emitters plaatst met muisklikken. Bevat verschillende emitter types inclusief regen en wolken die interacteren met de grond.

**Wat je leert:**
- Muis input handling
- Dynamische emitter creatie
- Grond botsingsdetectie
- Nat/droog terrein effecten
- Toetsenbord input voor type switching
- Complexe deeltjes interacties

**Besturing:**
- Klik: Plaats emitter
- Spatiebalk: Wissel emitter type

**Uitvoeren:**
```bash
python mouse_emitter_system.py
```

### 6. Cursor Wolk Systeem (`cursor_cloud_system.py`)
**Complexiteit:** ⭐⭐⭐⭐⭐⭐ (Zeer Complex)

Het meest geavanceerde voorbeeld: een wolk die je cursor volgt en regen/mist kan maken. Bevat een brandbestrijdingsspel waar je vuren moet blussen.

**Wat je leert:**
- Geavanceerde cursor tracking
- Dynamische wolk groottes
- Regen vs mist afhankelijk van positie
- Complexe gameplay mechanica
- Vuur systemen en uitdoving
- Rond-gebaseerd gameplay
- Geavanceerde UI elementen

**Besturing:**
- Beweeg muis: Beweeg wolk
- Houd muisknop ingedrukt: Maak regen/mist
- +/-: Vergroot/verklein wolk

**Uitvoeren:**
```bash
python cursor_cloud_system.py
```

## Leerpad

Voor de beste leerervaring raden we aan om de voorbeelden in volgorde door te nemen:

1. **Begin** met `rectangle_example.py` om de basis te leren
2. **Ga door** naar `moving_rectangle_example.py` voor animatie concepten
3. **Leer** object-georiënteerd programmeren met `particle_system_example.py`
4. **Verdiep je** in geavanceerde systemen met `emitter_particle_system.py`
5. **Ontdek** interactiviteit met `mouse_emitter_system.py`
6. **Meester** complexe systemen met `cursor_cloud_system.py`

## Belangrijke Concepten

- **rechthoek() functie**: Kernfunctie voor het tekenen van rechthoeken met rotatie
- **Particle klasse**: Basis deeltjes met positie, snelheid en levensduur
- **Emitter klasse**: Systemen die deeltjes genereren
- **Alpha blending**: Transparantie effecten
- **Botsingsdetectie**: Interactie tussen objecten
- **Input handling**: Muis en toetsenbord besturing

Veel plezier met experimenteren!